# Arquivo projetado para testar o desafio adicional (expressões regulares e
# exclusão de palavras reservadas em comentários e literais de string).
# Falso positivo em comentário: if x > 0: for i in range(5): while True: def falsa():


def funcao_real(valores):
    """
    Docstring multilinha com palavras reservadas que NÃO devem ser contadas:
    if condicao:
        for item in lista:
            while ativo:
                pass
    def funcao_falsa_na_docstring():
        return None
    # Isto está dentro da docstring, portanto não é um comentário real.
    """
    texto_duplas = "if x == 1: for a in b: while False: def ignorar():"
    texto_simples = 'if True: for k in v: while 1: # sustenido dentro de string'
    texto_escapado = "texto com aspas \"if for while def\" escapadas"
    bloco_simples = '''
    if outro_falso:
        while ainda_falso:
            for mais_um_falso in range(3):
                pass
    '''

    # Identificadores que apenas contêm palavras reservadas como subtexto
    verificar_if = 1
    formato = "padrao"
    while_ativo = True
    definicao = "teste"

    contador = 0  # Comentário inline com: if for while def
    for numero in valores:
        if numero > 0:
            contador += numero

    while contador > 10 and while_ativo:
        contador -= 1

    return (
        contador,
        texto_duplas,
        texto_simples,
        texto_escapado,
        bloco_simples,
        verificar_if,
        formato,
        definicao,
    )
