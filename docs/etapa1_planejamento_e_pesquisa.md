# Etapa 1 – Planejamento e Pesquisa

## 1. Identificação dos Integrantes

| Nome Completo | Matrícula / RA |
| :--- | :--- |
| Dani Prada Porto | JC3046541 |
| Jonatas Alves de Andrades | _[Preencher matrícula]_ |
| Maisa de Souza Amaral | _[Preencher matrícula]_ |

- **Disciplina:** Programação Estruturada (Profa. Ariadne Arrais – IFSP)
- **Prazo para apresentação:** 16/12/2026

---

## 2. Tema Escolhido

**Projeto 6 – Analisador de código-fonte** (focado em arquivos Python `.py`, incluindo o **desafio adicional** com expressões regulares e exclusão de palavras reservadas em comentários e textos entre aspas).

---

## 3. Descrição do Problema

Quando um programa cresce, fica difícil contar manualmente quantas linhas de código, comentários, funções, condicionais (`if`) ou laços de repetição (`for` e `while`) ele possui, ou conferir se alguma linha ficou comprida demais para facilitar a leitura.

O objetivo do nosso programa é automatizar essa análise: o usuário informa um arquivo Python (`.py`) e o programa lê o conteúdo, calcula estatísticas sobre a estrutura do código e gera um relatório claro na tela e, se o usuário quiser, salvo em um arquivo de texto (`.txt`).

---

## 4. Pesquisa sobre Ferramentas, Algoritmos e Referências

Durante a pesquisa inicial, estudamos ferramentas conhecidas de análise de código e revisamos o material da disciplina:

1. **`cloc` (Count Lines of Code):** ferramenta usada para contar linhas totais, linhas em branco, linhas de comentário e linhas de código. Serviu de inspiração para organizar a primeira parte do relatório.
2. **PEP 8 e `flake8`:** a PEP 8 é o guia oficial de estilo da linguagem Python e recomenda linhas com no máximo **79 caracteres**. Por isso, adotamos `79` como limite padrão (podendo ser alterado pelo usuário no menu).
3. **Expressões Regulares (`re`) e pré-processamento de texto:** uma busca simples como `"if" in linha` gera erros porque conta `if` dentro de nomes de variáveis (como `verificar_if`), dentro de comentários (`# if x > 0`) e dentro de strings (`"if teste"`). Para resolver isso de maneira simples:
   - Primeiro, percorremos cada linha caractere por caractere com um laço `while` para remover comentários (`#`) e textos entre aspas (`'...'`, `"..."`, `'''...'''`, `"""..."""`);
   - Depois, usamos `re.findall()` com `\b` (limite de palavra) para encontrar exatamente `if`, `elif`, `for`, `while` e `def`.
4. **Materiais da disciplina (Programação Estruturada):**
   - Slides da Profa. Ariadne Arrais sobre Variáveis e I/O, Condicionais (`if`/`elif`/`else`), Repetição (`while` e `for`/`enumerate`), Listas, Tuplas, Strings e Funções;
   - PERKOVIC, L. *Introdução à computação usando Python: um foco no desenvolvimento de aplicações*. LTC, 2016;
   - BARRY, P. *Use a cabeça! Python*. Alta Books, 2012;
   - Documentação oficial do Python (`https://www.python.org/`).

---

## 5. Funcionalidades que Serão Implementadas

### Funcionalidades Obrigatórias
- Ler um arquivo de código-fonte informado pelo usuário.
- Contar o total de linhas do arquivo.
- Identificar e contar linhas vazias.
- Identificar e contar linhas de comentários (`#`).
- Contar ocorrências de estruturas condicionais (`if` e `elif`).
- Contar ocorrências de estruturas de repetição (`for` e `while`).
- Identificar e contar definições de funções (`def`), listando nome e linha.
- Identificar linhas que ultrapassem um limite configurável de caracteres.
- Gerar relatório na tela e gravar em arquivo `.txt` quando solicitado.
- Tratar erros de entrada/saída (arquivo inexistente, vazio, pasta, erro de leitura/gravação e opções inválidas).

### Desafio Adicional
- Utilizar expressões regulares (`import re`) para detectar padrões exatos.
- Ignorar palavras reservadas que apareçam dentro de comentários ou textos entre aspas (simples, duplas e aspas triplas de várias linhas).

---

## 6. Arquivos de Entrada e Resultados Esperados

### Arquivos de Entrada (`exemplos/`)
- `exemplos/exemplo_basico.py`: programa curto para conferir todas as contagens facilmente à mão.
- `exemplos/exemplo_complexo.py`: código com laços `for` aninhados, `while`, `if`/`elif`, várias funções e linhas maiores que 79 caracteres.
- `exemplos/exemplo_desafio_regex.py`: arquivo criado especialmente para testar o desafio adicional, contendo `if`, `for`, `while` e `def` dentro de comentários, strings e docstrings.
- `exemplos/exemplo_vazio.py`: arquivo vazio (0 bytes) para testar o aviso de arquivo vazio.

### Resultados Esperados (`relatorios/`)
Um relatório de texto organizado em 4 blocos:
1. Estatísticas de linhas (total, código, vazias e comentários);
2. Estruturas de controle (`if`, `elif`, `for`, `while` e total de repetições);
3. Lista de funções encontradas (linha e nome);
4. Lista de linhas que passaram do limite de caracteres.

---

## 7. Planejamento das Principais Funções

O código será dividido em dois arquivos principais na raiz do projeto, mantendo tudo simples e fácil de entender:

| Arquivo | Função | O que faz |
| :--- | :--- | :--- |
| `funcoes.py` | `ler_arquivo(caminho)` | Abre e lê as linhas do arquivo tratando erros e verificando se está vazio. |
| `funcoes.py` | `salvar_relatorio(caminho_saida, texto)` | Grava o relatório em um arquivo `.txt` tratando erros de escrita. |
| `funcoes.py` | `remover_textos_e_comentarios(linhas)` | Remove strings e comentários `#` e conta as linhas de comentário. |
| `funcoes.py` | `contar_linhas_vazias(linhas)` | Conta linhas vazias usando `.strip() == ""`. |
| `funcoes.py` | `contar_condicionais(linhas_limpas)` | Conta `if` e `elif` com `re.findall`. |
| `funcoes.py` | `contar_repeticoes(linhas_limpas)` | Conta `for` e `while` com `re.findall`. |
| `funcoes.py` | `encontrar_funcoes(linhas_limpas)` | Encontra definições `def` com linha e nome usando `enumerate` e `re.findall`. |
| `funcoes.py` | `encontrar_linhas_longas(linhas, limite)` | Verifica quais linhas passam do limite de caracteres. |
| `funcoes.py` | `montar_relatorio(...)` | Junta todas as informações no texto formatado do relatório. |
| `main.py` | `mostrar_menu(limite)` | Exibe o menu principal no terminal. |
| `main.py` | `alterar_limite(limite_atual)` | Permite ao usuário mudar o limite de caracteres. |
| `main.py` | `analisar_arquivo(limite)` | Pede o arquivo, chama as funções de análise, exibe e salva o relatório. |
| `main.py` | `main()` | Laço `while True` principal do programa. |
