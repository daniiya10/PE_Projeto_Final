# Exemplo mais completo contendo laços aninhados, condicionais, comentários inline
# e linhas que ultrapassam propositalmente o limite de 79 caracteres da PEP 8.

LIMITE_TENTATIVAS = 3  # Número máximo de tentativas permitidas


def buscar_elemento(matriz, alvo):
    """Procura um elemento em uma matriz e retorna sua posição (linha, coluna)."""
    for indice_linha, linha in enumerate(matriz):
        for indice_coluna, valor in enumerate(linha):
            if valor == alvo:  # Encontrou o elemento desejado
                return (indice_linha, indice_coluna)
    return None


def processar_fila(fila):
    processados = []
    tentativas = 0

    while fila and tentativas < LIMITE_TENTATIVAS:
        item = fila.pop(0)
        if item < 0:
            tentativas += 1
            continue
        elif item == 0:
            break
        processados.append(item * 2)

    return processados


async def sincronizar_dados_remotos(endereco_servidor_principal, porta_conexao, tempo_limite_segundos):
    mensagem_status = "Iniciando sincronização de dados com o servidor configurado pelo usuário no sistema."
    if tempo_limite_segundos <= 0:
        return False
    return bool(endereco_servidor_principal and porta_conexao and mensagem_status)


def executar_demonstracao():
    matriz_exemplo = [
        [10, 20, 30],
        [40, 50, 60],
    ]
    posicao = buscar_elemento(matriz_exemplo, 50)
    resultado_fila = processar_fila([5, -1, 10, 0, 20])
    print("Posição encontrada:", posicao, "| Itens processados na fila de entrada:", resultado_fila)
