"""Módulo responsável pela formatação dos relatórios de análise.

Permite gerar relatórios textuais bem estruturados para leitura humana (.txt)
ou em formato estruturado (.json) para integração com outras ferramentas.
"""

from datetime import datetime
import json


def _calcular_percentual(parte: int, total: int) -> float:
    """Calcula a porcentagem evitando divisão por zero."""
    if total == 0:
        return 0.0
    return (parte / total) * 100.0


def formatar_relatorio_texto(
    resultado: dict[str, object],
    data_hora: str | None = None,
) -> str:
    """Formata o dicionário de resultados em um relatório textual legível.

    Args:
        resultado: Dicionário retornado por `analisar_codigo`.
        data_hora: Data/hora opcional já formatada (útil para testes).

    Returns:
        String contendo o relatório completo pronto para exibição ou gravação.
    """
    if data_hora is None:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    total_linhas = int(resultado["total_linhas"])
    linhas_vazias = int(resultado["linhas_vazias"])
    linhas_comentarios = int(resultado["linhas_comentarios"])
    comentarios_inline = int(resultado["comentarios_inline"])
    linhas_codigo = int(resultado["linhas_codigo"])
    limite_caracteres = int(resultado["limite_caracteres"])

    condicionais = resultado["condicionais"]
    repeticoes = resultado["repeticoes"]
    funcoes = resultado["funcoes"]
    linhas_longas = resultado["linhas_longas"]

    pct_vazias = _calcular_percentual(linhas_vazias, total_linhas)
    pct_comentarios = _calcular_percentual(linhas_comentarios, total_linhas)
    pct_codigo = _calcular_percentual(linhas_codigo, total_linhas)

    separador = "=" * 70
    subseparador = "-" * 70

    linhas_saida = [
        separador,
        "           RELATÓRIO DE ANÁLISE DE CÓDIGO-FONTE (PYTHON)",
        separador,
        f"Arquivo analisado : {resultado['arquivo']}",
        f"Data da análise   : {data_hora}",
        f"Limite por linha  : {limite_caracteres} caracteres",
        subseparador,
        "1. ESTATÍSTICAS DE LINHAS",
        f"   - Total de linhas               : {total_linhas}",
        f"   - Linhas de código              : {linhas_codigo} ({pct_codigo:.1f}%)",
        f"   - Linhas vazias                 : {linhas_vazias} ({pct_vazias:.1f}%)",
        f"   - Linhas de comentários (#)     : {linhas_comentarios} ({pct_comentarios:.1f}%)",
        f"   - Comentários inline (# no fim) : {comentarios_inline}",
        subseparador,
        "2. ESTRUTURAS DE CONTROLE (ignorando strings e comentários)",
        f"   - Condicionais (if)             : {condicionais['if']}",
        f"   - Ramificações adicionais (elif): {condicionais['elif']}",
        f"   - Repetições (total)            : {repeticoes['total']}",
        f"       * Laços 'for'               : {repeticoes['for']}",
        f"       * Laços 'while'             : {repeticoes['while']}",
        subseparador,
        f"3. DEFINIÇÕES DE FUNÇÕES (total: {resultado['total_funcoes']})",
    ]

    if funcoes:
        for funcao in funcoes:
            linhas_saida.append(
                f"   - Linha {funcao['linha']:>4}: def {funcao['nome']}()"
            )
    else:
        linhas_saida.append("   - Nenhuma definição de função encontrada.")

    linhas_saida.append(subseparador)
    linhas_saida.append(
        f"4. LINHAS ACIMA DE {limite_caracteres} CARACTERES "
        f"(total: {resultado['total_linhas_longas']})"
    )

    if linhas_longas:
        for item in linhas_longas:
            linhas_saida.append(
                f"   - Linha {item['linha']:>4} ({item['tamanho']} chars): {item['trecho']}"
            )
    else:
        linhas_saida.append(
            f"   - Nenhuma linha ultrapassou o limite de {limite_caracteres} caracteres."
        )

    linhas_saida.append(separador)
    return "\n".join(linhas_saida) + "\n"


def formatar_relatorio_json(
    resultado: dict[str, object],
    data_hora: str | None = None,
) -> str:
    """Formata o dicionário de resultados em JSON indentado com suporte a UTF-8."""
    if data_hora is None:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    carga = {
        "data_analise": data_hora,
        **resultado,
    }
    return json.dumps(carga, ensure_ascii=False, indent=2) + "\n"
