# Projeto 6 – Analisador de Código-Fonte Python

Projeto final da disciplina de **Programação Estruturada** (Profa. Ariadne Arrais – IFSP), desenvolvido em **Python 3** de forma simples e organizada em funções, utilizando os conteúdos estudados em aula (condicionais, laços `while` e `for`, `enumerate`, listas, tuplas, strings, funções, manipulação de arquivos e expressões regulares).

---

## O que o programa faz

- Lê um arquivo de código-fonte Python (`.py`) informado pelo usuário.
- Trata erros comuns (arquivo não encontrado, arquivo vazio, pasta informada no lugar de arquivo, erro de leitura/gravação e limite inválido).
- Contabiliza:
  - Total de linhas, linhas de código, linhas vazias e linhas de comentários (`#`);
  - Estruturas condicionais (`if` e `elif`);
  - Estruturas de repetição (`for` e `while`);
  - Definições de funções (`def`), indicando o nome e o número da linha;
  - Linhas que ultrapassam um limite configurável de caracteres (padrão: 79).
- **Desafio adicional:** usa expressões regulares (`re`) e remove comentários e textos entre aspas antes das contagens para evitar falsos positivos.
- Exibe o relatório no terminal e permite salvá-lo em um arquivo `.txt`.

---

## Estrutura do Repositório

```text
PE_Projeto_Final/
├── main.py                                   # Menu principal e interação com o usuário
├── funcoes.py                                # Funções de leitura, análise e relatório
├── testar.py                                 # Script simples de testes automáticos
├── exemplos/                                 # Arquivos de entrada usados nos testes
│   ├── exemplo_basico.py
│   ├── exemplo_complexo.py
│   ├── exemplo_desafio_regex.py
│   └── exemplo_vazio.py
├── relatorios/                               # Relatórios gerados pelo programa
│   ├── relatorio_exemplo_basico.txt
│   ├── relatorio_exemplo_complexo.txt
│   └── relatorio_exemplo_desafio_regex.txt
└── docs/                                     # Documentação do projeto (Etapas 1 e 2)
    ├── etapa1_planejamento_e_pesquisa.md
    ├── manual_de_utilizacao.md
    ├── documentacao_tecnica.md
    └── registro_uso_ia.md
```

---

## Como Executar

1. Para abrir o programa (menu no terminal):
```bash
python3 main.py
```

2. Para rodar os testes prontos:
```bash
python3 testar.py
```

---

## Documentação

- [Etapa 1 – Planejamento e Pesquisa](docs/etapa1_planejamento_e_pesquisa.md) *(completar as matrículas pendentes dos integrantes)*
- [Manual de Utilização](docs/manual_de_utilizacao.md)
- [Documentação Técnica (Organização, Funções e Algoritmos)](docs/documentacao_tecnica.md)
- [Registro de Uso de Inteligência Artificial](docs/registro_uso_ia.md)
