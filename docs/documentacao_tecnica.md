# Documentação Técnica – Organização do Código, Funções e Algoritmos

Este documento explica, de forma clara e direta, como o programa está organizado, para que serve cada função e como funcionam os algoritmos usados na análise.

---

## 1. Organização do Código

Para manter o projeto organizado e fácil de entender (sem misturar tudo em um único bloco), dividimos o código em dois arquivos principais e um script de testes:

- **`main.py`**: cuida da conversa com o usuário (menu principal, leitura das opções com `input()`, exibição do relatório com `print()` e chamada das funções).
- **`funcoes.py`**: reúne todas as funções de trabalho (ler arquivo, salvar relatório, limpar textos/comentários, fazer as contagens e montar o texto do relatório).
- **`testar.py`**: executa testes automáticos usando os arquivos da pasta `exemplos/` para conferir se as contagens e os avisos de erro estão funcionando corretamente.

### Fluxo de Execução

1. O programa começa em `main.py` chamando a função `main()`.
2. Dentro de um laço `while True`, o menu é mostrado e o usuário escolhe uma opção.
3. Quando o usuário escolhe a opção `1` (`analisar_arquivo`):
   - `funcoes.ler_arquivo(caminho)` abre o arquivo com `with open(...)` e devolve a lista de linhas (ou `None` se houver erro/arquivo vazio).
   - `funcoes.contar_linhas_vazias(linhas)` conta as linhas em branco.
   - `funcoes.remover_textos_e_comentarios(linhas)` gera uma cópia das linhas sem textos entre aspas e sem comentários `#`, além de contar as linhas de comentário.
   - Sobre as linhas limpas, chamamos `contar_condicionais`, `contar_repeticoes` e `encontrar_funcoes`.
   - Sobre as linhas originais, chamamos `encontrar_linhas_longas(linhas, limite)`.
   - `funcoes.montar_relatorio(...)` junta tudo em um texto organizado.
   - O relatório é exibido na tela e, se o usuário quiser, salvo com `funcoes.salvar_relatorio(...)`.

---

## 2. Explicação das Funções (`funcoes.py`)

### Manipulação de Arquivos e Tratamento de Erros
- **`ler_arquivo(caminho)`:**
  - Usa `with open(caminho, "r", encoding="utf-8") as arquivo:` e `arquivo.readlines()` para ler todas as linhas em uma **lista**. O comando `with` garante que o arquivo seja fechado automaticamente ao terminar.
  - Usa blocos `try` / `except` para tratar `FileNotFoundError` (arquivo não existe), `IsADirectoryError` (caminho é uma pasta), `PermissionError`, `UnicodeDecodeError` e `OSError`.
  - Também verifica `if len(linhas) == 0:` para avisar caso o arquivo esteja vazio.
- **`salvar_relatorio(caminho_saida, texto_relatorio)`:**
  - Cria a pasta de destino com `os.makedirs(..., exist_ok=True)` caso ela ainda não exista.
  - Abre o arquivo no modo `"w"` (escrita) com `with open(..., "w", encoding="utf-8")` e grava o conteúdo com `arquivo.write(...)`, tratando possíveis erros com `try` / `except`.

### Contagens e Análise do Código
- **`contar_linhas_vazias(linhas)`:**
  - Percorre cada linha com `for linha in linhas:`.
  - Usa `linha.strip() == ""` (método de string visto em aula que remove espaços e quebras de linha das pontas). Se sobrar string vazia, soma `1`.
- **`remover_textos_e_comentarios(linhas)`:**
  - Implementa o **desafio adicional** (explicado em detalhes na seção 3).
  - Retorna dois valores como uma **tupla**: `(linhas_limpas, qtd_comentarios)`.
- **`contar_condicionais(linhas_limpas)`:**
  - Usa `re.findall(r"\bif\b", linha)` e `re.findall(r"\belif\b", linha)` em cada linha já limpa.
  - Retorna a tupla `(qtd_if, qtd_elif)`.
- **`contar_repeticoes(linhas_limpas)`:**
  - Usa `re.findall(r"\bfor\b", linha)` e `re.findall(r"\bwhile\b", linha)` em cada linha limpa.
  - Retorna a tupla `(qtd_for, qtd_while)`.
- **`encontrar_funcoes(linhas_limpas)`:**
  - Usa `for numero_linha, linha in enumerate(linhas_limpas, start=1):` (para já ter o número da linha começando em 1).
  - Usa `re.findall(r"^\s*def\s+([a-zA-Z_]\w*)\s*\(", linha)` para capturar o nome da função e guarda `(numero_linha, nome)` em uma lista.
- **`encontrar_linhas_longas(linhas, limite)`:**
  - Percorre as linhas **originais** com `enumerate(linhas, start=1)`, remove a quebra de linha (`\n`) com `.rstrip("\r\n")` e compara `if len(texto) > limite:`.
  - Guarda `(numero_linha, tamanho)` na lista `linhas_longas`.
- **`montar_relatorio(...)`:**
  - Calcula `linhas_codigo = total_linhas - vazias - comentarios` e `total_repeticoes = qtd_for + qtd_while`, monta todas as linhas do relatório em uma lista `partes` e junta tudo com `"\n".join(partes)`.

---

## 3. Como Funciona o Algoritmo do Desafio Adicional

### 3.1. Remoção de Textos entre Aspas e Comentários

Se procurássemos `"if"` diretamente nas linhas originais, o programa contaria errado em situações como:
- `# if x > 0:` (é apenas um comentário);
- `mensagem = "if o aluno passar"` (é um texto entre aspas);
- Docstrings de várias linhas (`""" ... if ... for ... """`).

Para resolver isso usando apenas laços `for`/`while`, `if`/`elif`/`else` e fatiamento de strings (`texto[i : i + 3]`):

1. Mantemos a variável `bloco_aspas` (vazia `""`, ou `'"""'`, ou `"'''"`) para saber se estamos dentro de um texto de várias linhas.
2. Se não estamos em `bloco_aspas` e a linha começa com `#` (`texto.strip().startswith("#")`), contamos como **linha de comentário** e colocamos `""` em `linhas_limpas`.
3. Caso contrário, percorremos os caracteres da linha com `while i < len(texto):` usando também `aspas_simples` (`""`, `'"'` ou `"'"`):
   - **Dentro de `bloco_aspas`:** ignoramos tudo (pulando `\"` ou `\\` com `i += 2`) até encontrar o fechamento `"""` ou `'''`.
   - **Dentro de `aspas_simples`:** ignoramos tudo (pulando `\"` ou `\'` com `i += 2`) até encontrar a aspa correspondente.
   - **Fora de aspas (código normal):**
     - Se achar `#`, damos `break` porque o resto da linha é comentário;
     - Se achar `"""` ou `'''`, entramos em `bloco_aspas`;
     - Se achar `"` ou `'`, entramos em `aspas_simples`;
     - Senão, copiamos o caractere para `nova_linha`.

Ao substituir cada texto entre aspas por um espaço `" "`, evitamos que palavras vizinhas grudem uma na outra.

### 3.2. Expressões Regulares (`import re`)

Depois que `linhas_limpas` contém somente código real, usamos `re.findall()` com padrões curtos e fáceis de explicar:

| Padrão | O que significa | Exemplo |
| :--- | :--- | :--- |
| `r"\bif\b"` | Palavra exata `if` (`\b` marca início e fim de palavra). | Conta `if x > 0:`, mas **não** conta `verificar_if` nem `elif`. |
| `r"\belif\b"` | Palavra exata `elif`. | Conta `elif media >= 5:`. |
| `r"\bfor\b"` | Palavra exata `for`. | Conta `for i in range(5):`, mas **não** conta `formato`. |
| `r"\bwhile\b"` | Palavra exata `while`. | Conta `while x > 0:`, mas **não** conta `while_ativo`. |
| `r"^\s*def\s+([a-zA-Z_]\w*)\s*\("` | Início da linha (`^`), espaços opcionais (`\s*`), palavra `def`, espaços (`\s+`), nome válido de função `([a-zA-Z_]\w*)` seguido de `(`. | Em `def calcular_media(notas):`, captura `"calcular_media"`. |

---

## 4. Estruturas de Dados Utilizadas

- **Listas (`list`):** usadas para guardar as linhas lidas do arquivo, as linhas limpas, a lista de funções encontradas, a lista de linhas longas e as linhas do relatório.
- **Tuplas (`tuple`):** usadas para devolver múltiplos valores em funções (`return qtd_for, qtd_while`) e para agrupar pares fixos de informações, como `(numero_linha, nome_funcao)` e `(numero_linha, tamanho)`.
- **Strings (`str`):** manipuladas com `.strip()`, `.rstrip()`, `.startswith()`, `.lower()`, `len()`, fatiamento `texto[i:i+3]` e `"\n".join(...)`.

---

## 5. Limitações Conhecidas

- O programa foi feito especificamente para a sintaxe da linguagem **Python** (`#` para comentários e `def` para funções).
- Como tudo o que está entre aspas é ignorado, expressões `if` ou `for` escritas dentro de chaves de uma *f-string* (ex.: `f"{a if b else c}"`) não são contadas.
- Compreensões de lista (ex.: `[x for x in lista]`) e `if` ternário também são contados como ocorrências de `for` e `if`, pois a análise é textual e baseada nas palavras reservadas.
