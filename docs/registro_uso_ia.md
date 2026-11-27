# Registro de Utilização de Ferramentas de Inteligência Artificial

Em conformidade com a **Etapa 2** e a **Seção 5 (Utilização de Inteligência Artificial)** do enunciado do projeto, este documento registra as ferramentas de IA utilizadas ao longo do planejamento, desenvolvimento, testes e documentação do **Projeto 6 – Analisador de Código-Fonte**.

---

## 1. Ferramentas Utilizadas

| Ferramenta | Etapa(s) de Uso | Finalidade Principal |
| :--- | :--- | :--- |
| **Antigravity (Google DeepMind / Gemini)** | Etapas 1 e 2 | Apoio à estruturação modular, revisão de algoritmos de análise textual, escrita de expressões regulares, geração de casos de teste e documentação técnica. |

---

## 2. Descrição Detalhada do Uso

1. **Pesquisa e Planejamento (Etapa 1):**
   - Discussão de referências de análise estática de código (`cloc`, `pycodestyle`/PEP 8, `radon`) e organização modular adequada à disciplina de Programação Estruturada.
   - Definição da separação entre módulos (`leitor_escritor.py`, `analisador.py`, `relatorio.py`, `main.py`).

2. **Algoritmos e Expressões Regulares (Etapa 2):**
   - Apoio na concepção da máquina de estados na função `limpar_strings_e_comentarios` para lidar corretamente com strings simples, duplas, multilinha (`"""` e `'''`), caracteres de escape (`\"`, `\'`, `\\`) e comentários `#` sem gerar falsos positivos.
   - Validação das expressões regulares com fronteiras de palavra (`\b`) e grupo de captura para definições `def` / `async def`.

3. **Tratamento de Exceções e Interface CLI:**
   - Revisão dos cenários de exceção previstos nos requisitos (arquivo inexistente, arquivo vazio com `ArquivoVazioError`, diretório, erro de permissão e erro de codificação UTF-8).
   - Estruturação do menu interativo e do suporte opcional a argumentos via `argparse`.

4. **Testes e Documentação:**
   - Elaboração dos arquivos de exemplo em `exemplos/` (incluindo `exemplo_desafio_regex.py` e `exemplo_vazio.py`) e da suíte automatizada em `tests/test_analisador.py` utilizando `unittest`.
   - Apoio na redação e revisão do manual de utilização e da documentação técnica.

---

## 3. Responsabilidade da Equipe

Todo o código-fonte, os testes e a documentação gerados com auxílio da ferramenta de IA foram revisados, executados e validados para garantir aderência integral aos requisitos da disciplina. Conforme as regras da **Etapa 3** e da **Etapa 4**, a equipe assume total responsabilidade pela compreensão da lógica implementada, sendo capaz de explicar cada função, o fluxo de execução, o uso das expressões regulares, a manipulação de arquivos e realizar modificações no código durante a apresentação e a arguição individual.
