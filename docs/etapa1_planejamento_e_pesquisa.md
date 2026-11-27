# Etapa 1 – Planejamento e Pesquisa

## 1. Identificação dos Integrantes

| Nome Completo | Matrícula / RA |
| :--- | :--- |
| Dani Prada Porto | JC3046541 |
| Jonatas Alves de Andrades | _[Preencher matrícula]_ |
| Maisa de Souza Amaral | _[Preencher matrícula]_ |

- **Disciplina:** Programação Estruturada
- **Data limite para apresentação:** 16/12/2026

---

## 2. Tema Escolhido

**Projeto 6 – Analisador de código-fonte** (focado em arquivos escritos na linguagem **Python**, incluindo o **desafio adicional** com expressões regulares e exclusão de palavras reservadas em comentários e strings).

---

## 3. Descrição do Problema

Durante o desenvolvimento de software, é comum que projetos cresçam rapidamente e se tornem difíceis de ler, revisar e manter. Verificar manualmente métricas estruturais de um arquivo de código-fonte — como proporção de comentários, quantidade de funções, uso de condicionais e laços de repetição, ou conformidade com limites de largura de linha — é uma tarefa repetitiva e sujeita a erros humanos.

O programa proposto resolve esse problema automatizando a **análise estática textual** de arquivos Python (`.py`). A partir de um arquivo informado pelo usuário, a ferramenta extrai estatísticas estruturais confiáveis e gera um relatório claro (exibido no terminal e opcionalmente gravado em disco), evitando falsos positivos causados por palavras reservadas escritas dentro de comentários ou textos entre aspas.

---

## 4. Pesquisa sobre Ferramentas, Algoritmos e Soluções de Referência

Para planejar a solução, foram pesquisadas ferramentas consolidadas de análise estática e métricas de código no ecossistema de software:

1. **`cloc` (Count Lines of Code):** ferramenta amplamente usada para contabilizar linhas totais, linhas em branco, linhas de comentários e linhas de código-fonte em diversas linguagens. Serviu de inspiração para a separação clara e mutuamente exclusiva entre linhas vazias, linhas de comentário e linhas de código.
2. **`pycodestyle` / `flake8` (PEP 8):** ferramentas de verificação de estilo para Python que adotam o limite clássico de **79 caracteres por linha** (definido na PEP 8 – *Style Guide for Python Code*). Essa referência orientou a escolha do limite padrão configurável do analisador.
3. **`radon`:** biblioteca Python voltada a métricas de código (como número de linhas lógicas, comentários, funções e complexidade estrutural baseada em desvios `if`, `for`, `while`). Inspirou a apresentação detalhada das estruturas de controle e das definições de função.
4. **Conceitos de Análise Léxica (Autômatos / Máquina de Estados) e Expressões Regulares:** uma análise puramente baseada em busca simples de substrings (`"if" in linha`) gera muitos falsos positivos — por exemplo, detectando `if` na variável `verificar_if`, em comentários (`# if x > 0`) ou em textos (`"if desejado"`). Por isso, a solução combina:
   - Uma **máquina de estados simples** (varredura caractere a caractere) para remover com precisão comentários (`#`) e literais de string (`'...'`, `"..."`, `'''...'''`, `"""..."""`), respeitando caracteres de escape (`\"`, `\'`, `\\`);
   - **Expressões regulares (`re`)** com fronteiras de palavra (`\b`) para identificar padrões exatos sobre o código sanitizado.

---

## 5. Descrição das Funcionalidades a Serem Implementadas

### 5.1. Funcionalidades Obrigatórias
- Leitura de um arquivo de código-fonte informado pelo usuário.
- Contabilização da quantidade total de linhas do arquivo.
- Identificação e contabilização de linhas vazias (incluindo linhas contendo apenas espaços ou tabulações).
- Identificação e contabilização de linhas de comentários (`#`).
- Contabilização de ocorrências de estruturas condicionais (`if`, além de exibir `elif` como detalhe complementar).
- Contabilização de estruturas de repetição (`for` e `while`, com total consolidado e detalhamento por tipo).
- Identificação e contabilização das definições de funções (`def` e `async def`), listando o nome e o número da linha de cada função.
- Identificação de linhas que ultrapassem um limite configurável de caracteres (padrão: 79 caracteres), exibindo número da linha, tamanho e trecho resumido.
- Geração de relatório estruturado com exibição em tela e gravação opcional em arquivo.

### 5.2. Desafio Adicional e Recursos Complementares
- Uso de **expressões regulares** (`re`) para detecção precisa de padrões estruturais.
- **Pré-processamento léxico** para ignorar palavras reservadas presentes em comentários (de linha inteira ou inline) e literais de string (aspas simples, duplas e strings/docstrings multilinha).
- Contabilização complementar de comentários *inline* (`#` ao final de linhas de código).
- Suporte à exportação do relatório em **texto formatado (`.txt`)** ou **JSON (`.json`)**.
- Interface de linha de comando com **menu interativo** e **modo direto por argumentos**, além de tratamento robusto de exceções (arquivo inexistente, vazio, diretório, erro de permissão ou codificação).

---

## 6. Arquivos de Entrada e Resultados Esperados

### 6.1. Arquivos de Entrada Planejados (`exemplos/`)
| Arquivo | Finalidade do Teste |
| :--- | :--- |
| `exemplos/exemplo_basico.py` | Código curto e limpo para validação manual direta de todas as métricas. |
| `exemplos/exemplo_complexo.py` | Código com laços aninhados (`for` e `while`), `async def`, comentários inline e linhas acima de 79 caracteres. |
| `exemplos/exemplo_desafio_regex.py` | Casos críticos do desafio adicional: palavras reservadas em comentários, docstrings multilinha, strings com aspas escapadas, `#` dentro de strings e identificadores parecidos (`verificar_if`, `formato`). |
| `exemplos/exemplo_vazio.py` | Arquivo com 0 bytes para validar o tratamento de erro para arquivos vazios. |

### 6.2. Resultados Esperados (`relatorios/`)
Para cada arquivo válido analisado, o programa gera um relatório contendo:
1. Metadados da análise (caminho do arquivo, data/hora, limite de caracteres utilizado);
2. Estatísticas de linhas (total, código, vazias, comentários e comentários inline, com percentuais);
3. Contagem de estruturas de controle (`if`, `elif`, `for`, `while` e total de repetições);
4. Lista de funções encontradas com seus respectivos números de linha;
5. Lista de linhas que excedem o limite de caracteres definido.

---

## 7. Planejamento das Principais Funções

O sistema será organizado de forma modular em quatro arquivos dentro da pasta `src/`, aplicando os princípios da Programação Estruturada:

| Módulo | Função Principal | Responsabilidade |
| :--- | :--- | :--- |
| `src/leitor_escritor.py` | `ler_arquivo_fonte(caminho)` | Valida o caminho, abre e lê as linhas do arquivo em UTF-8, tratando exceções (inclusive arquivo vazio). |
| `src/leitor_escritor.py` | `salvar_relatorio(caminho, conteudo)` | Cria diretórios necessários e grava o relatório em disco com tratamento de erros de escrita. |
| `src/leitor_escritor.py` | `validar_extensao_python(caminho)` | Verifica se o arquivo informado possui extensão `.py`. |
| `src/analisador.py` | `limpar_strings_e_comentarios(linhas)` | Remove strings (simples, duplas e multilinha) e comentários `#`, preservando os números das linhas. |
| `src/analisador.py` | `contar_linhas_vazias(linhas)` | Conta linhas sem caracteres visíveis usando regex. |
| `src/analisador.py` | `contar_condicionais(linhas_limpas)` | Contabiliza ocorrências de `if` e `elif` via regex com `\b`. |
| `src/analisador.py` | `contar_repeticoes(linhas_limpas)` | Contabiliza ocorrências de `for` e `while` via regex com `\b`. |
| `src/analisador.py` | `identificar_funcoes(linhas_limpas)` | Extrai nomes e números de linha de definições `def` / `async def`. |
| `src/analisador.py` | `identificar_linhas_longas(linhas, limite)` | Localiza linhas que excedam o limite de caracteres configurado. |
| `src/analisador.py` | `analisar_codigo(linhas, nome, limite)` | Coordena todas as análises e consolida o dicionário de métricas. |
| `src/relatorio.py` | `formatar_relatorio_texto(resultado)` | Monta o relatório legível em texto (`.txt`). |
| `src/relatorio.py` | `formatar_relatorio_json(resultado)` | Serializa as métricas em formato `.json`. |
| `src/main.py` | `executar_modo_interativo()` | Controla o menu de opções no terminal e interage com o usuário. |
| `src/main.py` | `executar_modo_argumentos(args)` | Executa a análise diretamente por argumentos de linha de comando. |
