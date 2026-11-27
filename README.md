# Projeto 6 – Analisador de Código-Fonte (Programação Estruturada)

Ferramenta de linha de comando desenvolvida em **Python 3** (utilizando apenas a biblioteca padrão) para realizar análise estática textual de arquivos de código-fonte Python (`.py`), extrair métricas estruturais e gerar relatórios em `.txt` ou `.json`.

---

## Funcionalidades Implementadas

- Leitura de arquivos de código-fonte com tratamento de exceções (arquivo inexistente, vazio, diretório, erro de permissão e codificação inválida).
- Contagem de **total de linhas**, **linhas de código**, **linhas vazias**, **linhas de comentários (`#`)** e **comentários inline**.
- Contabilização de **estruturas condicionais (`if` e `elif`)**.
- Contabilização de **estruturas de repetição (`for` e `while`)**.
- Identificação de **definições de funções (`def` e `async def`)** com nome e número de linha.
- Identificação de **linhas que ultrapassam um limite configurável de caracteres** (padrão PEP 8: 79 caracteres).
- **Desafio adicional concluído:** uso de expressões regulares (`re`) combinado com pré-processamento por máquina de estados para **ignorar palavras reservadas dentro de comentários e textos entre aspas** (simples, duplas, escapadas e multilinha `"""`/`'''`).
- Geração de relatórios estruturados em **`.txt`** e **`.json`**, com exibição em tela e gravação em disco.
- Interface CLI com **menu interativo** e **execução direta por argumentos**.

---

## Estrutura do Repositório

```text
PE_Projeto_Final/
├── README.md
├── src/
│   ├── __init__.py
│   ├── leitor_escritor.py                    # Leitura/gravação de arquivos e exceções
│   ├── analisador.py                         # Sanitização léxica + regex + métricas
│   ├── relatorio.py                          # Formatação de relatórios TXT e JSON
│   └── main.py                               # Interface CLI (menu + argumentos)
├── exemplos/                                 # Arquivos de entrada usados nos testes
│   ├── exemplo_basico.py
│   ├── exemplo_complexo.py
│   ├── exemplo_desafio_regex.py
│   └── exemplo_vazio.py
├── relatorios/                               # Relatórios gerados pelo programa
│   ├── relatorio_exemplo_basico.txt
│   ├── relatorio_exemplo_complexo.txt
│   ├── relatorio_exemplo_desafio_regex.txt
│   └── relatorio_exemplo_desafio_regex.json
├── tests/
│   └── test_analisador.py                    # 19 testes automatizados (unittest)
└── docs/
    ├── etapa1_planejamento_e_pesquisa.md     # Entrega da Etapa 1
    ├── manual_de_utilizacao.md               # Manual de uso (Etapa 2)
    ├── documentacao_tecnica.md               # Arquitetura, funções e algoritmos (Etapa 2)
    └── registro_uso_ia.md                    # Registro de uso de IA (Etapa 2)
```

---

## Como Executar

### 1. Modo Interativo (Menu)
```bash
python3 src/main.py
```

### 2. Modo Direto por Linha de Comando
```bash
# Exibir relatório no terminal
python3 src/main.py exemplos/exemplo_basico.py

# Salvar relatório em arquivo TXT com limite de 79 caracteres
python3 src/main.py exemplos/exemplo_complexo.py -l 79 -o relatorios/relatorio_exemplo_complexo.txt

# Salvar relatório em JSON
python3 src/main.py exemplos/exemplo_desafio_regex.py -f json -o relatorios/relatorio_exemplo_desafio_regex.json
```

### 3. Executar os Testes Automatizados
```bash
python3 -m unittest discover -s tests -v
```

---

## Documentação Completa

- [Etapa 1 – Planejamento e Pesquisa](docs/etapa1_planejamento_e_pesquisa.md) *(completar as matrículas pendentes dos integrantes)*
- [Manual de Utilização](docs/manual_de_utilizacao.md)
- [Documentação Técnica (Organização, Funções e Algoritmos)](docs/documentacao_tecnica.md)
- [Registro de Uso de Ferramentas de IA](docs/registro_uso_ia.md)
