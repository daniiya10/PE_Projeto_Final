"""Interface de linha de comando (CLI) do Analisador de Código-Fonte Python.

Suporta dois modos de operação:
1. Modo interativo (padrão, sem argumentos): apresenta um menu guiado no terminal.
2. Modo direto por argumentos: permite informar o arquivo de entrada, o limite
   de caracteres e o arquivo de saída diretamente na linha de comando.
"""

import argparse
import os
import sys

# Garante que o diretório raiz do projeto esteja no sys.path,
# permitindo executar tanto `python3 src/main.py` quanto `python3 -m src.main`.
DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if DIRETORIO_RAIZ not in sys.path:
    sys.path.insert(0, DIRETORIO_RAIZ)

from src.analisador import LIMITE_CARACTERES_PADRAO, analisar_codigo
from src.leitor_escritor import (
    ArquivoVazioError,
    gerar_nome_relatorio_padrao,
    ler_arquivo_fonte,
    salvar_relatorio,
    validar_extensao_python,
)
from src.relatorio import formatar_relatorio_json, formatar_relatorio_texto


def exibir_cabecalho() -> None:
    """Exibe o título inicial do programa."""
    print("=" * 64)
    print("       PROJETO 6 - ANALISADOR DE CÓDIGO-FONTE PYTHON")
    print("=" * 64)


def exibir_menu(limite_atual: int) -> None:
    """Mostra as opções disponíveis no menu principal."""
    print("\nMenu Principal:")
    print("  [1] Analisar arquivo de código-fonte")
    print(f"  [2] Alterar limite de caracteres por linha (atual: {limite_atual})")
    print("  [3] Ajuda / Sobre o programa")
    print("  [4] Sair")


def exibir_ajuda() -> None:
    """Exibe orientações rápidas sobre o funcionamento do analisador."""
    print("\n" + "-" * 64)
    print("SOBRE O ANALISADOR DE CÓDIGO-FONTE")
    print("-" * 64)
    print("Esta ferramenta analisa arquivos Python (.py) e calcula:")
    print("  - Total de linhas, linhas de código, vazias e de comentários;")
    print("  - Ocorrências de estruturas condicionais (if e elif);")
    print("  - Ocorrências de estruturas de repetição (for e while);")
    print("  - Definições de funções (def / async def) com nome e linha;")
    print("  - Linhas que ultrapassam o limite de caracteres configurado.")
    print("\nRecursos do desafio adicional:")
    print("  - Uso de expressões regulares (módulo 're') para detecção;")
    print("  - Remoção prévia de strings (simples, duplas e multilinha)")
    print("    e comentários para evitar falsos positivos.")
    print("\nDica: você também pode executar diretamente pela linha de comando:")
    print("  python3 src/main.py exemplos/exemplo_basico.py -o relatorios/saida.txt")
    print("-" * 64)


def perguntar_confirmacao(mensagem: str) -> bool:
    """Solicita uma resposta de confirmação (s/n) ao usuário."""
    while True:
        resposta = input(f"{mensagem} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite 's' para sim ou 'n' para não.")


def solicitar_limite_caracteres(limite_atual: int) -> int:
    """Permite ao usuário configurar um novo limite positivo de caracteres por linha."""
    print(f"\nLimite atual de caracteres por linha: {limite_atual} (padrão PEP 8: 79)")
    entrada = input(
        "Informe o novo limite (ou pressione Enter para manter o atual): "
    ).strip()

    if not entrada:
        print(f"Limite mantido em {limite_atual} caracteres.")
        return limite_atual

    try:
        novo_limite = int(entrada)
        if novo_limite <= 0:
            print("Erro: o limite deve ser um número inteiro maior que zero.")
            return limite_atual
        print(f"Limite atualizado com sucesso para {novo_limite} caracteres.")
        return novo_limite
    except ValueError:
        print("Erro: valor inválido. Digite apenas números inteiros positivos.")
        return limite_atual


def executar_analise_arquivo(
    caminho_entrada: str,
    limite_caracteres: int,
) -> dict[str, object] | None:
    """Lê e analisa um arquivo de código-fonte tratando exceções de I/O.

    Returns:
        Dicionário de resultados em caso de sucesso, ou None em caso de erro.
    """
    try:
        linhas = ler_arquivo_fonte(caminho_entrada)
    except ValueError as erro:
        print(f"\n[Erro de entrada] {erro}")
        return None
    except FileNotFoundError as erro:
        print(f"\n[Arquivo não encontrado] {erro}")
        return None
    except IsADirectoryError as erro:
        print(f"\n[Caminho inválido] {erro}")
        return None
    except PermissionError as erro:
        print(f"\n[Sem permissão] Não foi possível ler '{caminho_entrada}': {erro}")
        return None
    except UnicodeDecodeError:
        print(
            f"\n[Erro de codificação] O arquivo '{caminho_entrada}' não parece ser "
            "um arquivo de texto UTF-8 válido (pode ser um arquivo binário)."
        )
        return None
    except ArquivoVazioError as erro:
        print(f"\n[Aviso - Arquivo vazio] {erro}")
        return None
    except OSError as erro:
        print(f"\n[Erro de leitura] Falha ao ler '{caminho_entrada}': {erro}")
        return None

    return analisar_codigo(
        linhas=linhas,
        nome_arquivo=caminho_entrada,
        limite_caracteres=limite_caracteres,
    )


def fluxo_salvar_relatorio(
    resultado: dict[str, object],
    caminho_entrada: str,
) -> None:
    """Conduz a interação para gravação do relatório em disco."""
    if not perguntar_confirmacao("\nDeseja salvar este relatório em um arquivo?"):
        return

    print("Escolha o formato do relatório:")
    print("  [1] Texto formatado (.txt)")
    print("  [2] Estruturado em JSON (.json)")
    escolha_formato = input("Formato [1]: ").strip()
    formato = "json" if escolha_formato == "2" else "txt"

    caminho_padrao = gerar_nome_relatorio_padrao(caminho_entrada, formato=formato)
    caminho_saida = input(
        f"Informe o caminho do arquivo de saída [{caminho_padrao}]: "
    ).strip()

    if not caminho_saida:
        caminho_saida = caminho_padrao

    if formato == "json":
        conteudo = formatar_relatorio_json(resultado)
    else:
        conteudo = formatar_relatorio_texto(resultado)

    try:
        caminho_absoluto = salvar_relatorio(caminho_saida, conteudo)
        print(f"\nRelatório salvo com sucesso em:\n  {caminho_absoluto}")
    except (ValueError, IsADirectoryError, PermissionError, OSError) as erro:
        print(f"\n[Erro ao salvar relatório] {erro}")


def fluxo_analise_interativa(limite_caracteres: int) -> None:
    """Solicita o arquivo de entrada, executa a análise e exibe o relatório."""
    print("\nExemplo de caminho: exemplos/exemplo_basico.py")
    caminho_entrada = input("Informe o caminho do arquivo de código-fonte: ").strip()

    if not caminho_entrada:
        print("Operação cancelada: nenhum arquivo foi informado.")
        return

    if os.path.isfile(caminho_entrada) and not validar_extensao_python(caminho_entrada):
        print(
            f"\n[Aviso] O arquivo '{caminho_entrada}' não possui extensão '.py'. "
            "Este analisador foi projetado para código-fonte Python."
        )
        if not perguntar_confirmacao("Deseja continuar a análise mesmo assim?"):
            print("Análise cancelada pelo usuário.")
            return

    resultado = executar_analise_arquivo(caminho_entrada, limite_caracteres)
    if resultado is None:
        return

    relatorio_texto = formatar_relatorio_texto(resultado)
    print("\n" + relatorio_texto)
    fluxo_salvar_relatorio(resultado, caminho_entrada)


def executar_modo_interativo() -> int:
    """Executa o loop principal do menu interativo no terminal."""
    exibir_cabecalho()
    limite_caracteres = LIMITE_CARACTERES_PADRAO

    while True:
        exibir_menu(limite_caracteres)
        opcao = input("\nEscolha uma opção (1-4): ").strip()

        if opcao == "1":
            fluxo_analise_interativa(limite_caracteres)
        elif opcao == "2":
            limite_caracteres = solicitar_limite_caracteres(limite_caracteres)
        elif opcao == "3":
            exibir_ajuda()
        elif opcao == "4":
            print("\nEncerrando o Analisador de Código-Fonte. Até logo!")
            return 0
        else:
            print("Opção inválida. Escolha um número entre 1 e 4.")


def criar_parser_argumentos() -> argparse.ArgumentParser:
    """Configura os argumentos aceitos na execução direta por linha de comando."""
    parser = argparse.ArgumentParser(
        prog="analisador-codigo",
        description=(
            "Analisador estático de código-fonte Python. "
            "Execute sem argumentos para abrir o menu interativo."
        ),
    )
    parser.add_argument(
        "arquivo",
        nargs="?",
        help="Caminho do arquivo de código-fonte (.py) a ser analisado.",
    )
    parser.add_argument(
        "-o",
        "--saida",
        dest="saida",
        help="Caminho do arquivo onde o relatório será salvo.",
    )
    parser.add_argument(
        "-l",
        "--limite",
        dest="limite",
        type=int,
        default=LIMITE_CARACTERES_PADRAO,
        help=(
            "Limite máximo de caracteres por linha "
            f"(padrão: {LIMITE_CARACTERES_PADRAO})."
        ),
    )
    parser.add_argument(
        "-f",
        "--formato",
        dest="formato",
        choices=("txt", "json"),
        default="txt",
        help="Formato do relatório gerado: 'txt' (padrão) ou 'json'.",
    )
    return parser


def executar_modo_argumentos(args: argparse.Namespace) -> int:
    """Executa a análise diretamente a partir dos argumentos da linha de comando."""
    if args.limite <= 0:
        print(
            "[Erro] O limite de caracteres (-l/--limite) deve ser maior que zero.",
            file=sys.stderr,
        )
        return 1

    if os.path.isfile(args.arquivo) and not validar_extensao_python(args.arquivo):
        print(
            f"[Aviso] O arquivo '{args.arquivo}' não possui extensão '.py'. "
            "Prosseguindo com a análise textual para Python.",
            file=sys.stderr,
        )

    resultado = executar_analise_arquivo(args.arquivo, args.limite)
    if resultado is None:
        return 1

    if args.formato == "json":
        conteudo = formatar_relatorio_json(resultado)
    else:
        conteudo = formatar_relatorio_texto(resultado)

    print(conteudo, end="")

    if args.saida:
        try:
            caminho_absoluto = salvar_relatorio(args.saida, conteudo)
            print(f"\nRelatório salvo em: {caminho_absoluto}")
        except (ValueError, IsADirectoryError, PermissionError, OSError) as erro:
            print(f"[Erro ao salvar relatório] {erro}", file=sys.stderr)
            return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada principal da aplicação."""
    parser = criar_parser_argumentos()
    args = parser.parse_args(argv)

    try:
        if args.arquivo is None:
            return executar_modo_interativo()
        return executar_modo_argumentos(args)
    except KeyboardInterrupt:
        print("\n\nExecução interrompida pelo usuário.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
