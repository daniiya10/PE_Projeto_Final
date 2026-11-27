# Manual de Utilização – Analisador de Código-Fonte Python

Este manual apresenta as instruções passo a passo para instalar, executar e utilizar todas as funcionalidades do **Analisador de Código-Fonte Python**.

---

## 1. Pré-requisitos

- **Python 3.10 ou superior** instalado no sistema (verifique executando `python3 --version`).
- **Nenhuma biblioteca externa é necessária**: o projeto utiliza exclusivamente módulos nativos da biblioteca padrão do Python (`re`, `os`, `sys`, `json`, `argparse`, `datetime`, `unittest`).

---

## 2. Como Executar o Programa

Abra um terminal na pasta raiz do projeto (`PE_Projeto_Final`). O programa pode ser executado de duas formas: **Modo Interativo** (menu guiado) ou **Modo Direto** (argumentos na linha de comando).

### 2.1. Modo Interativo (Menu)

Execute:

```bash
python3 src/main.py
```

O menu principal será exibido:

```text
================================================================
       PROJETO 6 - ANALISADOR DE CÓDIGO-FONTE PYTHON
================================================================

Menu Principal:
  [1] Analisar arquivo de código-fonte
  [2] Alterar limite de caracteres por linha (atual: 79)
  [3] Ajuda / Sobre o programa
  [4] Sair
```

**Passo a passo para analisar um arquivo no modo interativo:**

1. Digite `1` e pressione **Enter**.
2. Informe o caminho do arquivo de entrada (por exemplo: `exemplos/exemplo_basico.py`).
   - Caso o arquivo não tenha extensão `.py`, o programa exibe um aviso e pergunta se você deseja prosseguir mesmo assim.
3. O relatório completo será exibido diretamente no terminal.
4. Em seguida, o programa perguntará: `Deseja salvar este relatório em um arquivo? (s/n)`.
5. Se responder `s`:
   - Escolha o formato desejado: `[1]` Texto formatado (`.txt`) ou `[2]` JSON (`.json`).
   - Informe o caminho do arquivo de saída ou pressione **Enter** para aceitar o caminho sugerido automaticamente (ex.: `relatorios/relatorio_exemplo_basico.txt`).

**Para alterar o limite máximo de caracteres por linha:**

1. No menu principal, escolha a opção `2`.
2. Digite um número inteiro positivo (por exemplo, `100`) e pressione **Enter**.
3. Todas as análises subsequentes utilizarão o novo limite configurado.

---

### 2.2. Modo Direto por Linha de Comando

Para análises rápidas ou automação, informe o arquivo diretamente como argumento:

```bash
python3 src/main.py <arquivo_entrada> [opções]
```

**Opções disponíveis:**

| Argumento | Descrição | Padrão |
| :--- | :--- | :--- |
| `arquivo` | Caminho do arquivo Python (`.py`) a ser analisado | *(abre modo interativo se omitido)* |
| `-o`, `--saida` | Caminho do arquivo para salvar o relatório | *(apenas exibe na tela)* |
| `-l`, `--limite` | Limite máximo de caracteres por linha | `79` |
| `-f`, `--formato` | Formato do relatório: `txt` ou `json` | `txt` |
| `-h`, `--help` | Exibe a mensagem de ajuda da CLI | — |

**Exemplos práticos:**

```bash
# Analisar e exibir somente no terminal
python3 src/main.py exemplos/exemplo_basico.py

# Analisar e salvar relatório em arquivo .txt
python3 src/main.py exemplos/exemplo_complexo.py -o relatorios/relatorio_exemplo_complexo.txt

# Analisar com limite personalizado de 100 caracteres
python3 src/main.py exemplos/exemplo_complexo.py -l 100

# Exportar relatório em formato JSON
python3 src/main.py exemplos/exemplo_desafio_regex.py -f json -o relatorios/relatorio_desafio.json
```

---

## 3. Como Interpretar o Relatório Gerado

O relatório é dividido em quatro seções:

1. **Estatísticas de Linhas:**
   - **Total de linhas:** soma total de linhas no arquivo.
   - **Linhas de código:** linhas não vazias que não são comentários de linha inteira.
   - **Linhas vazias:** linhas sem conteúdo ou apenas com espaços/tabulações.
   - **Linhas de comentários (`#`):** linhas cujo único conteúdo é um comentário iniciado por `#`.
   - **Comentários inline:** contagem complementar de linhas de código que contêm um `#` ao final (não duplicada na soma de linhas).
2. **Estruturas de Controle:**
   - Contabiliza ocorrências reais de `if`, `elif`, `for` e `while`, **desconsiderando** ocorrências dentro de comentários e textos entre aspas.
3. **Definições de Funções:**
   - Exibe o total e a lista com número da linha e nome de cada função (`def` / `async def`).
4. **Linhas Acima do Limite de Caracteres:**
   - Lista o número da linha, o comprimento exato e um trecho inicial de cada linha que ultrapassou o limite configurado.

---

## 4. Tratamento de Situações Excepcionais

O programa exibe mensagens claras quando encontra problemas de entrada ou saída, sem encerrar abruptamente com rastreamentos técnicos (*tracebacks*):

- **Arquivo inexistente:** `[Arquivo não encontrado] O arquivo '...' não foi encontrado.`
- **Arquivo vazio (0 bytes):** `[Aviso - Arquivo vazio] O arquivo '...' está vazio e não possui linhas para análise.`
- **Caminho é um diretório:** `[Caminho inválido] O caminho '...' é um diretório, não um arquivo.`
- **Arquivo binário / codificação inválida:** `[Erro de codificação] O arquivo '...' não parece ser um arquivo de texto UTF-8 válido...`
- **Sem permissão ou erro de escrita:** `[Erro ao salvar relatório] ...`
- **Limite de caracteres inválido (`<= 0` ou texto):** exibe aviso e solicita/mantém um valor válido.

---

## 5. Executando a Suíte de Testes Automatizados

Para verificar o funcionamento de todas as funções e cenários de teste, execute na raiz do projeto:

```bash
python3 -m unittest discover -s tests -v
```
