# Script simples para testar todas as funções do analisador.
# Execute com: python3 testar.py

import funcoes


def testar_exemplo_basico():
    linhas = funcoes.ler_arquivo("exemplos/exemplo_basico.py")
    assert linhas is not None

    linhas_limpas, comentarios = funcoes.remover_textos_e_comentarios(linhas)
    vazias = funcoes.contar_linhas_vazias(linhas)
    qtd_if, qtd_elif = funcoes.contar_condicionais(linhas_limpas)
    qtd_for, qtd_while = funcoes.contar_repeticoes(linhas_limpas)
    lista_funcoes = funcoes.encontrar_funcoes(linhas_limpas)
    longas = funcoes.encontrar_linhas_longas(linhas, 79)

    assert len(linhas) == 29
    assert vazias == 8
    assert comentarios == 3
    assert qtd_if == 2
    assert qtd_elif == 1
    assert qtd_for == 1
    assert qtd_while == 0
    assert len(lista_funcoes) == 2
    assert len(longas) == 0
    print("[OK] testar_exemplo_basico")


def testar_exemplo_complexo():
    linhas = funcoes.ler_arquivo("exemplos/exemplo_complexo.py")
    assert linhas is not None

    linhas_limpas, comentarios = funcoes.remover_textos_e_comentarios(linhas)
    qtd_if, qtd_elif = funcoes.contar_condicionais(linhas_limpas)
    qtd_for, qtd_while = funcoes.contar_repeticoes(linhas_limpas)
    lista_funcoes = funcoes.encontrar_funcoes(linhas_limpas)
    longas = funcoes.encontrar_linhas_longas(linhas, 79)

    assert comentarios == 2
    assert qtd_if == 3
    assert qtd_elif == 1
    assert qtd_for == 2
    assert qtd_while == 1
    assert len(lista_funcoes) == 4
    assert len(longas) > 0
    print("[OK] testar_exemplo_complexo")


def testar_desafio_regex():
    # Garante que palavras reservadas em comentários e strings NÃO sejam contadas
    linhas = funcoes.ler_arquivo("exemplos/exemplo_desafio_regex.py")
    assert linhas is not None

    linhas_limpas, comentarios = funcoes.remover_textos_e_comentarios(linhas)
    qtd_if, qtd_elif = funcoes.contar_condicionais(linhas_limpas)
    qtd_for, qtd_while = funcoes.contar_repeticoes(linhas_limpas)
    lista_funcoes = funcoes.encontrar_funcoes(linhas_limpas)

    assert comentarios == 4
    assert qtd_if == 1
    assert qtd_elif == 0
    assert qtd_for == 1
    assert qtd_while == 1
    assert lista_funcoes == [(6, "funcao_real")]
    print("[OK] testar_desafio_regex")


def testar_erros_de_arquivo():
    print("\n--- Testando mensagens de erro esperadas ---")
    assert funcoes.ler_arquivo("exemplos/exemplo_vazio.py") is None
    assert funcoes.ler_arquivo("exemplos/arquivo_que_nao_existe.py") is None
    assert funcoes.ler_arquivo("exemplos") is None
    assert funcoes.ler_arquivo("") is None
    assert funcoes.salvar_relatorio("", "texto") is False
    print("[OK] testar_erros_de_arquivo")


def main():
    testar_exemplo_basico()
    testar_exemplo_complexo()
    testar_desafio_regex()
    testar_erros_de_arquivo()
    print("\nTodos os testes passaram com sucesso!")


if __name__ == "__main__":
    main()
