"""Módulo principal de análise estática textual de código-fonte Python.

Utiliza uma máquina de estados simples para remover conteúdos de strings
(simples, duplas e multilinha) e comentários antes da aplicação de expressões
regulares, garantindo que palavras reservadas presentes em textos ou comentários
não sejam contabilizadas erroneamente.
"""

import re

LIMITE_CARACTERES_PADRAO = 79

# Expressões regulares pré-compiladas para identificação de padrões no código
PADRAO_LINHA_VAZIA = re.compile(r"^\s*$")
PADRAO_COMENTARIO_LINHA = re.compile(r"^\s*#")
PADRAO_IF = re.compile(r"\bif\b")
PADRAO_ELIF = re.compile(r"\belif\b")
PADRAO_FOR = re.compile(r"\bfor\b")
PADRAO_WHILE = re.compile(r"\bwhile\b")
PADRAO_DEF = re.compile(r"^\s*(?:async\s+)?def\s+([A-Za-z_]\w*)\s*\(")


def limpar_strings_e_comentarios(
    linhas: list[str],
) -> tuple[list[str], dict[str, int]]:
    """Remove literais de string e comentários mantendo a correspondência de linhas.

    Percorre o código caractere a caractere mantendo o estado de strings
    multilinha (aspas triplas \"\"\" ou '''). Literais de string são substituídos
    por um espaço para evitar a junção indevida de tokens adjacentes, e qualquer
    texto após '#' fora de strings é descartado.

    Args:
        linhas: Lista de linhas originais do arquivo de código-fonte.

    Returns:
        Uma tupla (linhas_limpas, estatisticas_comentarios), onde:
        - linhas_limpas: lista com o mesmo número de linhas contendo apenas código.
        - estatisticas_comentarios: dicionário com contagem de
          'linhas_comentarios' (comentários de linha inteira) e
          'comentarios_inline' (comentários ao final de linhas de código).
    """
    linhas_limpas: list[str] = []
    linhas_comentarios = 0
    comentarios_inline = 0

    # Guarda o delimitador ('"""' ou "'''") caso estejamos dentro de string multilinha
    delimitador_multilinha: str | None = None

    for linha_bruta in linhas:
        linha = linha_bruta.rstrip("\r\n")

        # Verifica comentário de linha inteira apenas quando fora de string multilinha
        if delimitador_multilinha is None and PADRAO_COMENTARIO_LINHA.match(linha):
            linhas_comentarios += 1
            linhas_limpas.append("")
            continue

        resultado_chars: list[str] = []
        i = 0
        tamanho = len(linha)
        delimitador_simples: str | None = None
        tem_comentario_inline = False

        while i < tamanho:
            # Caso 1: dentro de uma string multilinha (""" ou ''')
            if delimitador_multilinha is not None:
                if linha[i] == "\\" and i + 1 < tamanho:
                    i += 2
                    continue
                if linha[i : i + 3] == delimitador_multilinha:
                    delimitador_multilinha = None
                    resultado_chars.append(" ")
                    i += 3
                else:
                    i += 1
                continue

            # Caso 2: dentro de uma string de linha única (" ou ')
            if delimitador_simples is not None:
                if linha[i] == "\\" and i + 1 < tamanho:
                    i += 2
                    continue
                if linha[i] == delimitador_simples:
                    delimitador_simples = None
                    resultado_chars.append(" ")
                i += 1
                continue

            # Caso 3: fora de qualquer string — código normal
            caractere = linha[i]

            if caractere == "#":
                # Todo o restante da linha é comentário inline
                tem_comentario_inline = True
                break

            if linha[i : i + 3] in ('"""', "'''"):
                delimitador_multilinha = linha[i : i + 3]
                resultado_chars.append(" ")
                i += 3
                continue

            if caractere in ('"', "'"):
                delimitador_simples = caractere
                resultado_chars.append(" ")
                i += 1
                continue

            resultado_chars.append(caractere)
            i += 1

        linha_limpa = "".join(resultado_chars)
        if tem_comentario_inline:
            comentarios_inline += 1

        linhas_limpas.append(linha_limpa)

    estatisticas_comentarios = {
        "linhas_comentarios": linhas_comentarios,
        "comentarios_inline": comentarios_inline,
    }
    return linhas_limpas, estatisticas_comentarios


def contar_linhas_vazias(linhas: list[str]) -> int:
    """Conta quantas linhas estão vazias ou contêm apenas espaços em branco."""
    total_vazias = 0
    for linha in linhas:
        if PADRAO_LINHA_VAZIA.match(linha.rstrip("\r\n")):
            total_vazias += 1
    return total_vazias


def contar_condicionais(linhas_limpas: list[str]) -> dict[str, int]:
    """Contabiliza ocorrências de estruturas condicionais ('if' e 'elif').

    Opera sobre as linhas já sanitizadas para ignorar palavras dentro de
    strings ou comentários.
    """
    ocorrencias_if = 0
    ocorrencias_elif = 0

    for linha in linhas_limpas:
        ocorrencias_if += len(PADRAO_IF.findall(linha))
        ocorrencias_elif += len(PADRAO_ELIF.findall(linha))

    return {
        "if": ocorrencias_if,
        "elif": ocorrencias_elif,
    }


def contar_repeticoes(linhas_limpas: list[str]) -> dict[str, int]:
    """Contabiliza ocorrências de estruturas de repetição ('for' e 'while').

    Opera sobre as linhas já sanitizadas para ignorar palavras dentro de
    strings ou comentários.
    """
    ocorrencias_for = 0
    ocorrencias_while = 0

    for linha in linhas_limpas:
        ocorrencias_for += len(PADRAO_FOR.findall(linha))
        ocorrencias_while += len(PADRAO_WHILE.findall(linha))

    return {
        "for": ocorrencias_for,
        "while": ocorrencias_while,
        "total": ocorrencias_for + ocorrencias_while,
    }


def identificar_funcoes(linhas_limpas: list[str]) -> list[dict[str, object]]:
    """Identifica definições de funções ('def' e 'async def') com nome e linha."""
    funcoes: list[dict[str, object]] = []

    for numero_linha, linha in enumerate(linhas_limpas, start=1):
        correspondencia = PADRAO_DEF.match(linha)
        if correspondencia:
            funcoes.append(
                {
                    "nome": correspondencia.group(1),
                    "linha": numero_linha,
                }
            )

    return funcoes


def identificar_linhas_longas(
    linhas: list[str],
    limite_caracteres: int = LIMITE_CARACTERES_PADRAO,
) -> list[dict[str, object]]:
    """Identifica linhas cujo comprimento ultrapassa o limite definido.

    O cálculo é feito sobre o conteúdo original da linha (sem a quebra de linha),
    seguindo a convenção de guias de estilo como a PEP 8.
    """
    if limite_caracteres <= 0:
        raise ValueError("O limite de caracteres deve ser um número inteiro positivo.")

    linhas_longas: list[dict[str, object]] = []

    for numero_linha, linha_bruta in enumerate(linhas, start=1):
        conteudo = linha_bruta.rstrip("\r\n")
        tamanho = len(conteudo)
        if tamanho > limite_caracteres:
            trecho = conteudo.strip()
            if len(trecho) > 60:
                trecho = trecho[:57] + "..."
            linhas_longas.append(
                {
                    "linha": numero_linha,
                    "tamanho": tamanho,
                    "trecho": trecho,
                }
            )

    return linhas_longas


def analisar_codigo(
    linhas: list[str],
    nome_arquivo: str = "<entrada>",
    limite_caracteres: int = LIMITE_CARACTERES_PADRAO,
) -> dict[str, object]:
    """Executa a análise completa de um arquivo de código-fonte Python.

    Args:
        linhas: Lista de linhas lidas do arquivo.
        nome_arquivo: Nome ou caminho do arquivo analisado (para o relatório).
        limite_caracteres: Limite máximo permitido de caracteres por linha.

    Returns:
        Dicionário estruturado contendo todas as métricas coletadas.
    """
    if limite_caracteres <= 0:
        raise ValueError("O limite de caracteres deve ser um número inteiro positivo.")

    total_linhas = len(linhas)
    linhas_vazias = contar_linhas_vazias(linhas)
    linhas_limpas, estatisticas_comentarios = limpar_strings_e_comentarios(linhas)

    linhas_comentarios = estatisticas_comentarios["linhas_comentarios"]
    comentarios_inline = estatisticas_comentarios["comentarios_inline"]
    linhas_codigo = total_linhas - linhas_vazias - linhas_comentarios

    condicionais = contar_condicionais(linhas_limpas)
    repeticoes = contar_repeticoes(linhas_limpas)
    funcoes = identificar_funcoes(linhas_limpas)
    linhas_longas = identificar_linhas_longas(linhas, limite_caracteres)

    return {
        "arquivo": nome_arquivo,
        "limite_caracteres": limite_caracteres,
        "total_linhas": total_linhas,
        "linhas_vazias": linhas_vazias,
        "linhas_comentarios": linhas_comentarios,
        "comentarios_inline": comentarios_inline,
        "linhas_codigo": linhas_codigo,
        "condicionais": condicionais,
        "repeticoes": repeticoes,
        "total_funcoes": len(funcoes),
        "funcoes": funcoes,
        "total_linhas_longas": len(linhas_longas),
        "linhas_longas": linhas_longas,
    }
