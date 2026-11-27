"""Módulo responsável pela leitura de arquivos de código-fonte e gravação de relatórios.

Centraliza as operações de entrada e saída (I/O) e o tratamento de situações
excepcionais, como arquivos inexistentes, diretórios inválidos, arquivos vazios,
problemas de codificação e falhas de permissão.
"""

import os


class ArquivoVazioError(Exception):
    """Exceção lançada quando o arquivo de entrada não possui conteúdo."""


def validar_extensao_python(caminho_arquivo: str) -> bool:
    """Verifica se o caminho informado possui extensão '.py'.

    Args:
        caminho_arquivo: Caminho para o arquivo de entrada.

    Returns:
        True se a extensão for '.py' (ignorando maiúsculas/minúsculas),
        False caso contrário.
    """
    _, extensao = os.path.splitext(caminho_arquivo)
    return extensao.lower() == ".py"


def ler_arquivo_fonte(caminho_arquivo: str) -> list[str]:
    """Lê um arquivo de código-fonte e retorna suas linhas.

    Realiza verificações e trata exceções comuns de leitura de arquivos.

    Args:
        caminho_arquivo: Caminho relativo ou absoluto do arquivo a ser lido.

    Returns:
        Lista de strings contendo as linhas do arquivo (preservando a ordem).

    Raises:
        ValueError: Se o caminho informado estiver vazio.
        FileNotFoundError: Se o arquivo não existir.
        IsADirectoryError: Se o caminho apontar para um diretório.
        PermissionError: Se não houver permissão de leitura.
        UnicodeDecodeError: Se o arquivo não puder ser decodificado como UTF-8.
        ArquivoVazioError: Se o arquivo estiver vazio (0 caracteres).
        OSError: Para outros erros de sistema operacional na leitura.
    """
    if not caminho_arquivo or not caminho_arquivo.strip():
        raise ValueError("O caminho do arquivo de entrada não pode estar vazio.")

    caminho_normalizado = caminho_arquivo.strip()

    if not os.path.exists(caminho_normalizado):
        raise FileNotFoundError(
            f"O arquivo '{caminho_normalizado}' não foi encontrado."
        )

    if os.path.isdir(caminho_normalizado):
        raise IsADirectoryError(
            f"O caminho '{caminho_normalizado}' é um diretório, não um arquivo."
        )

    with open(caminho_normalizado, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    if len(linhas) == 0:
        raise ArquivoVazioError(
            f"O arquivo '{caminho_normalizado}' está vazio e não possui linhas para análise."
        )

    return linhas


def salvar_relatorio(caminho_saida: str, conteudo: str) -> str:
    """Grava o texto do relatório em um arquivo no caminho especificado.

    Cria automaticamente diretórios intermediários caso ainda não existam.

    Args:
        caminho_saida: Caminho do arquivo onde o relatório será salvo.
        conteudo: Conteúdo textual (TXT ou JSON) a ser gravado.

    Returns:
        Caminho absoluto do arquivo salvo.

    Raises:
        ValueError: Se o caminho de saída estiver vazio.
        IsADirectoryError: Se o caminho de saída apontar para um diretório existente.
        PermissionError: Se não houver permissão de gravação.
        OSError: Para outros erros de escrita em disco.
    """
    if not caminho_saida or not caminho_saida.strip():
        raise ValueError("O caminho do arquivo de saída não pode estar vazio.")

    caminho_normalizado = caminho_saida.strip()

    if os.path.isdir(caminho_normalizado):
        raise IsADirectoryError(
            f"O caminho de saída '{caminho_normalizado}' é um diretório. "
            "Informe também o nome do arquivo."
        )

    diretorio_pai = os.path.dirname(caminho_normalizado)
    if diretorio_pai:
        os.makedirs(diretorio_pai, exist_ok=True)

    with open(caminho_normalizado, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

    return os.path.abspath(caminho_normalizado)


def gerar_nome_relatorio_padrao(
    caminho_entrada: str,
    diretorio_saida: str = "relatorios",
    formato: str = "txt",
) -> str:
    """Sugere um caminho padrão de saída baseado no nome do arquivo analisado.

    Args:
        caminho_entrada: Caminho do arquivo analisado.
        diretorio_saida: Pasta onde o relatório será salvo por padrão.
        formato: Extensão desejada ('txt' ou 'json').

    Returns:
        Caminho sugerido, por exemplo: 'relatorios/relatorio_exemplo.txt'.
    """
    nome_base = os.path.basename(caminho_entrada)
    nome_sem_ext, _ = os.path.splitext(nome_base)
    ext = "json" if formato.lower() == "json" else "txt"
    return os.path.join(diretorio_saida, f"relatorio_{nome_sem_ext}.{ext}")
