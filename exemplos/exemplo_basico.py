# Exemplo básico de código Python para teste do analisador.
# Calcula a média de uma lista de notas e classifica a situação do aluno.


def calcular_media(notas):
    soma = 0
    for nota in notas:
        soma += nota

    if len(notas) == 0:
        return 0.0

    return soma / len(notas)


def classificar_aluno(media):
    if media >= 7.0:
        return "Aprovado"
    elif media >= 5.0:
        return "Recuperação"
    else:
        return "Reprovado"


# Execução principal de demonstração
notas_turma = [8.5, 6.0, 9.0, 7.5]
media_final = calcular_media(notas_turma)
situacao = classificar_aluno(media_final)
print(f"Média: {media_final:.2f} - Situação: {situacao}")
