# Módulo com as funções do Analisador de Código-Fonte Python.
# Desenvolvido com conceitos básicos de Programação Estruturada:
# variáveis, if/elif/else, while, for, listas, tuplas, strings,
# funções, manipulação de arquivos e expressões regulares (re).

import os
import re


def ler_arquivo(caminho):
    """Lê o arquivo informado e devolve uma lista com suas linhas.

    Caso aconteça algum erro (arquivo não existe, vazio, etc.),
    exibe uma mensagem clara e devolve None.
    """
    if caminho.strip() == "":
        print("Erro: você não informou o caminho do arquivo.")
        return None

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print(f"Erro: o arquivo '{caminho}' não foi encontrado.")
        return None
    except IsADirectoryError:
        print(f"Erro: '{caminho}' é uma pasta, e não um arquivo.")
        return None
    except PermissionError:
        print(f"Erro: sem permissão para ler o arquivo '{caminho}'.")
        return None
    except UnicodeDecodeError:
        print(f"Erro: não foi possível ler '{caminho}' como arquivo de texto.")
        return None
    except OSError as erro:
        print(f"Erro ao abrir o arquivo '{caminho}': {erro}")
        return None

    if len(linhas) == 0:
        print(f"Aviso: o arquivo '{caminho}' está vazio.")
        return None

    return linhas


def salvar_relatorio(caminho_saida, texto_relatorio):
    """Grava o relatório em um arquivo de texto. Devolve True se deu certo."""
    if caminho_saida.strip() == "":
        print("Erro: o nome do arquivo de saída não pode ficar vazio.")
        return False

    try:
        pasta = os.path.dirname(caminho_saida)
        if pasta != "":
            os.makedirs(pasta, exist_ok=True)

        with open(caminho_saida, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto_relatorio)
        return True
    except IsADirectoryError:
        print(f"Erro: '{caminho_saida}' é uma pasta. Informe o nome do arquivo.")
        return False
    except PermissionError:
        print(f"Erro: sem permissão para gravar em '{caminho_saida}'.")
        return False
    except OSError as erro:
        print(f"Erro ao gravar o arquivo '{caminho_saida}': {erro}")
        return False


def remover_textos_e_comentarios(linhas):
    """Remove textos entre aspas e comentários para evitar contagens erradas.

    Mantém a mesma quantidade de linhas do arquivo original e também conta
    quantas linhas são comentários (linhas que começam com '#').
    Devolve uma tupla: (linhas_limpas, qtd_comentarios).
    """
    linhas_limpas = []
    qtd_comentarios = 0
    bloco_aspas = ""  # Guarda '"""' ou "'''" se estivermos em texto de várias linhas

    for linha in linhas:
        texto = linha.rstrip("\r\n")

        # Linha inteira de comentário (somente fora de aspas triplas)
        if bloco_aspas == "" and texto.strip().startswith("#"):
            qtd_comentarios += 1
            linhas_limpas.append("")
            continue

        nova_linha = ""
        aspas_simples = ""  # Guarda '"' ou "'" se estivermos em texto na mesma linha
        i = 0

        while i < len(texto):
            # Caso 1: dentro de aspas triplas (""" ou ''')
            if bloco_aspas != "":
                if texto[i] == "\\" and i + 1 < len(texto):
                    i += 2
                elif texto[i : i + 3] == bloco_aspas:
                    bloco_aspas = ""
                    nova_linha += " "
                    i += 3
                else:
                    i += 1

            # Caso 2: dentro de aspas simples ou duplas (' ou ")
            elif aspas_simples != "":
                if texto[i] == "\\" and i + 1 < len(texto):
                    i += 2
                elif texto[i] == aspas_simples:
                    aspas_simples = ""
                    nova_linha += " "
                    i += 1
                else:
                    i += 1

            # Caso 3: código normal (fora de qualquer texto entre aspas)
            else:
                if texto[i] == "#":
                    # Tudo após '#' até o fim da linha é comentário
                    break
                elif texto[i : i + 3] == '"""' or texto[i : i + 3] == "'''":
                    bloco_aspas = texto[i : i + 3]
                    nova_linha += " "
                    i += 3
                elif texto[i] == '"' or texto[i] == "'":
                    aspas_simples = texto[i]
                    nova_linha += " "
                    i += 1
                else:
                    nova_linha += texto[i]
                    i += 1

        linhas_limpas.append(nova_linha)

    return linhas_limpas, qtd_comentarios


def contar_linhas_vazias(linhas):
    """Conta quantas linhas estão vazias (ou têm apenas espaços)."""
    vazias = 0
    for linha in linhas:
        if linha.strip() == "":
            vazias += 1
    return vazias


def contar_condicionais(linhas_limpas):
    """Conta quantas vezes aparecem 'if' e 'elif' usando expressões regulares."""
    qtd_if = 0
    qtd_elif = 0

    for linha in linhas_limpas:
        # \b garante que seja a palavra inteira (não conta 'verificar_if')
        qtd_if += len(re.findall(r"\bif\b", linha))
        qtd_elif += len(re.findall(r"\belif\b", linha))

    return qtd_if, qtd_elif


def contar_repeticoes(linhas_limpas):
    """Conta quantas vezes aparecem 'for' e 'while' usando expressões regulares."""
    qtd_for = 0
    qtd_while = 0

    for linha in linhas_limpas:
        qtd_for += len(re.findall(r"\bfor\b", linha))
        qtd_while += len(re.findall(r"\bwhile\b", linha))

    return qtd_for, qtd_while


def encontrar_funcoes(linhas_limpas):
    """Encontra as definições de funções (def) e devolve uma lista de tuplas.

    Cada item da lista é uma tupla (numero_linha, nome_funcao).
    """
    funcoes = []

    for numero_linha, linha in enumerate(linhas_limpas, start=1):
        nomes = re.findall(r"^\s*def\s+([a-zA-Z_]\w*)\s*\(", linha)
        for nome in nomes:
            funcoes.append((numero_linha, nome))

    return funcoes


def encontrar_linhas_longas(linhas, limite):
    """Encontra linhas que passam do limite de caracteres definido.

    Devolve uma lista de tuplas (numero_linha, quantidade_caracteres).
    """
    linhas_longas = []

    for numero_linha, linha in enumerate(linhas, start=1):
        texto = linha.rstrip("\r\n")
        tamanho = len(texto)
        if tamanho > limite:
            linhas_longas.append((numero_linha, tamanho))

    return linhas_longas


def montar_relatorio(
    caminho,
    total_linhas,
    vazias,
    comentarios,
    qtd_if,
    qtd_elif,
    qtd_for,
    qtd_while,
    funcoes,
    linhas_longas,
    limite,
):
    """Monta o texto formatado do relatório final com todos os resultados."""
    linhas_codigo = total_linhas - vazias - comentarios
    total_repeticoes = qtd_for + qtd_while

    partes = []
    partes.append("=" * 60)
    partes.append("         RELATÓRIO DE ANÁLISE DE CÓDIGO-FONTE")
    partes.append("=" * 60)
    partes.append(f"Arquivo analisado : {caminho}")
    partes.append(f"Limite por linha  : {limite} caracteres")
    partes.append("-" * 60)
    partes.append("1. ESTATÍSTICAS DE LINHAS")
    partes.append(f"   Total de linhas       : {total_linhas}")
    partes.append(f"   Linhas de código      : {linhas_codigo}")
    partes.append(f"   Linhas vazias         : {vazias}")
    partes.append(f"   Linhas de comentários : {comentarios}")
    partes.append("-" * 60)
    partes.append("2. ESTRUTURAS DE CONTROLE (sem contar textos e comentários)")
    partes.append(f"   Condicionais (if)     : {qtd_if}")
    partes.append(f"   Condicionais (elif)   : {qtd_elif}")
    partes.append(f"   Repetições (total)    : {total_repeticoes}")
    partes.append(f"     - Laços for         : {qtd_for}")
    partes.append(f"     - Laços while       : {qtd_while}")
    partes.append("-" * 60)
    partes.append(f"3. DEFINIÇÕES DE FUNÇÕES (total: {len(funcoes)})")

    if len(funcoes) == 0:
        partes.append("   Nenhuma função encontrada.")
    else:
        for numero_linha, nome in funcoes:
            partes.append(f"   Linha {numero_linha}: def {nome}()")

    partes.append("-" * 60)
    partes.append(
        f"4. LINHAS ACIMA DE {limite} CARACTERES (total: {len(linhas_longas)})"
    )

    if len(linhas_longas) == 0:
        partes.append(f"   Nenhuma linha passou de {limite} caracteres.")
    else:
        for numero_linha, tamanho in linhas_longas:
            partes.append(f"   Linha {numero_linha}: {tamanho} caracteres")

    partes.append("=" * 60)

    return "\n".join(partes) + "\n"
