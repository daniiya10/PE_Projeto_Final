# Programa principal do Projeto 6 - Analisador de Código-Fonte Python.
# Interface de linha de comando simples para interação com o usuário.

import os
import funcoes


def mostrar_menu(limite):
    """Exibe as opções do menu principal no terminal."""
    print("\n" + "=" * 55)
    print("      ANALISADOR DE CÓDIGO-FONTE PYTHON (PROJETO 6)")
    print("=" * 55)
    print("1 - Analisar um arquivo de código-fonte")
    print(f"2 - Alterar limite de caracteres por linha (atual: {limite})")
    print("3 - Ajuda")
    print("4 - Sair")
    print("=" * 55)


def mostrar_ajuda():
    """Mostra uma explicação rápida de como usar o programa."""
    print("\n--- AJUDA ---")
    print("Este programa lê um arquivo Python (.py) e analisa:")
    print("- Quantidade total de linhas, linhas vazias e comentários;")
    print("- Quantidade de estruturas condicionais (if e elif);")
    print("- Quantidade de laços de repetição (for e while);")
    print("- Definições de funções (def);")
    print("- Linhas que passam do limite de caracteres escolhido.")
    print("Obs.: palavras dentro de comentários ou entre aspas são ignoradas.")


def alterar_limite(limite_atual):
    """Pede um novo limite inteiro positivo de caracteres ao usuário."""
    entrada = input(
        f"Digite o novo limite de caracteres (atual: {limite_atual}): "
    ).strip()

    try:
        novo_limite = int(entrada)
        if novo_limite <= 0:
            print("Erro: o limite precisa ser maior que zero.")
            return limite_atual
        print(f"Limite alterado para {novo_limite} caracteres.")
        return novo_limite
    except ValueError:
        print("Erro: digite apenas um número inteiro válido.")
        return limite_atual


def analisar_arquivo(limite):
    """Conduz a análise de um arquivo informado pelo usuário."""
    print("\nExemplo de caminho: exemplos/exemplo_basico.py")
    caminho = input("Digite o caminho do arquivo de código-fonte: ").strip()

    # Avisa caso o arquivo não termine com .py, mas deixa o usuário decidir
    if caminho != "" and not caminho.lower().endswith(".py"):
        print("Aviso: o arquivo informado não termina com '.py'.")
        continuar = input("Deseja analisar mesmo assim? (s/n): ").strip().lower()
        if continuar != "s":
            print("Análise cancelada.")
            return

    linhas = funcoes.ler_arquivo(caminho)
    if linhas is None:
        return

    # Realiza todas as contagens usando as funções do módulo funcoes.py
    total_linhas = len(linhas)
    vazias = funcoes.contar_linhas_vazias(linhas)
    linhas_limpas, comentarios = funcoes.remover_textos_e_comentarios(linhas)
    qtd_if, qtd_elif = funcoes.contar_condicionais(linhas_limpas)
    qtd_for, qtd_while = funcoes.contar_repeticoes(linhas_limpas)
    lista_funcoes = funcoes.encontrar_funcoes(linhas_limpas)
    linhas_longas = funcoes.encontrar_linhas_longas(linhas, limite)

    relatorio = funcoes.montar_relatorio(
        caminho,
        total_linhas,
        vazias,
        comentarios,
        qtd_if,
        qtd_elif,
        qtd_for,
        qtd_while,
        lista_funcoes,
        linhas_longas,
        limite,
    )

    print("\n" + relatorio)

    salvar = input("Deseja salvar o relatório em um arquivo? (s/n): ").strip().lower()
    if salvar == "s":
        # Sugere um nome padrão na pasta relatorios/
        nome_arquivo = os.path.basename(caminho)
        nome_sem_ext = os.path.splitext(nome_arquivo)[0]
        sugestao = f"relatorios/relatorio_{nome_sem_ext}.txt"

        caminho_saida = input(
            f"Digite o caminho do arquivo de saída (Enter para '{sugestao}'): "
        ).strip()

        if caminho_saida == "":
            caminho_saida = sugestao

        salvou = funcoes.salvar_relatorio(caminho_saida, relatorio)
        if salvou:
            print(f"Relatório salvo com sucesso em: {caminho_saida}")


def main():
    """Fluxo principal do programa com menu interativo."""
    limite = 79  # Padrão recomendado pela PEP 8

    while True:
        mostrar_menu(limite)
        opcao = input("Escolha uma opção (1 a 4): ").strip()

        if opcao == "1":
            analisar_arquivo(limite)
        elif opcao == "2":
            limite = alterar_limite(limite)
        elif opcao == "3":
            mostrar_ajuda()
        elif opcao == "4":
            print("Programa encerrado. Até mais!")
            break
        else:
            print("Opção inválida! Escolha um número entre 1 e 4.")


# Executa o menu quando o arquivo main.py é rodado diretamente
if __name__ == "__main__":
    main()
