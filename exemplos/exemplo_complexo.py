# Exemplo mais completo com laços aninhados, condicionais, comentários
# e linhas que ultrapassam propositalmente o limite de 79 caracteres.

LIMITE_TENTATIVAS = 3  # Quantidade máxima de tentativas


def buscar_elemento(matriz, alvo):
    """Procura um elemento em uma matriz e devolve a posição (linha, coluna)."""
    for indice_linha, linha in enumerate(matriz):
        for indice_coluna, valor in enumerate(linha):
            if valor == alvo:  # Encontrou o valor procurado
                return (indice_linha, indice_coluna)
    return None


def processar_fila(fila):
    processados = []
    tentativas = 0

    while len(fila) > 0 and tentativas < LIMITE_TENTATIVAS:
        item = fila.pop(0)
        if item < 0:
            tentativas += 1
            continue
        elif item == 0:
            break
        processados.append(item * 2)

    return processados


def verificar_configuracao(endereco_servidor_principal, porta_conexao, tempo_limite_segundos):
    mensagem = "Iniciando verificação de conexão com o servidor configurado pelo usuário no sistema."
    if tempo_limite_segundos <= 0:
        return False
    print(mensagem)
    return endereco_servidor_principal != "" and porta_conexao > 0


def executar_demonstracao():
    matriz_exemplo = [
        [10, 20, 30],
        [40, 50, 60],
    ]
    posicao = buscar_elemento(matriz_exemplo, 50)
    resultado = processar_fila([5, -1, 10, 0, 20])
    print("Posição encontrada:", posicao, "| Itens processados na fila de entrada:", resultado)
