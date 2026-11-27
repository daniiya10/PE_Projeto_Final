# Manual de Utilização – Analisador de Código-Fonte Python

Este manual explica de forma simples como executar e usar o programa.

---

## 1. Requisitos

- Ter o **Python 3** instalado no computador.
- Não é preciso instalar nenhuma biblioteca extra: o programa usa apenas módulos que já vêm com o Python (`os` e `re`).

---

## 2. Como Executar o Programa

Abra o terminal na pasta do projeto (`PE_Projeto_Final`) e digite:

```bash
python3 main.py
```

O menu principal será exibido:

```text
=======================================================
      ANALISADOR DE CÓDIGO-FONTE PYTHON (PROJETO 6)
=======================================================
1 - Analisar um arquivo de código-fonte
2 - Alterar limite de caracteres por linha (atual: 79)
3 - Ajuda
4 - Sair
=======================================================
Escolha uma opção (1 a 4):
```

---

## 3. Como Usar Cada Opção

### Opção 1 – Analisar um arquivo de código-fonte
1. Digite `1` e aperte **Enter**.
2. Digite o caminho do arquivo Python que deseja analisar, por exemplo:
   `exemplos/exemplo_basico.py`
   - Se o arquivo não terminar com `.py`, o programa avisa e pergunta se você quer continuar mesmo assim (`s/n`).
3. O relatório aparecerá na tela.
4. Depois, o programa pergunta: `Deseja salvar o relatório em um arquivo? (s/n):`
   - Se digitar `s`, basta apertar **Enter** para salvar no caminho sugerido (por exemplo, `relatorios/relatorio_exemplo_basico.txt`) ou digitar outro caminho de sua preferência.

### Opção 2 – Alterar limite de caracteres por linha
1. Digite `2` e aperte **Enter**.
2. Informe um número inteiro maior que zero (por exemplo, `80` ou `100`).
3. As próximas análises passarão a usar esse novo limite.

### Opção 3 – Ajuda
Mostra um resumo rápido das funcionalidades do analisador.

### Opção 4 – Sair
Encerra o programa com segurança.

---

## 4. Mensagens de Erro Tratadas

Se acontecer algum problema, o programa avisa de forma clara e volta ao menu sem travar:

- **Arquivo inexistente:** `Erro: o arquivo '...' não foi encontrado.`
- **Arquivo vazio:** `Aviso: o arquivo '...' está vazio.`
- **Pasta no lugar de arquivo:** `Erro: '...' é uma pasta, e não um arquivo.`
- **Limite inválido (texto ou número <= 0):** `Erro: digite apenas um número inteiro válido.` ou `Erro: o limite precisa ser maior que zero.`
- **Opção inválida no menu:** `Opção inválida! Escolha um número entre 1 e 4.`

---

## 5. Como Rodar os Testes

Para executar o script que testa automaticamente os arquivos da pasta `exemplos/` e os casos de erro, digite:

```bash
python3 testar.py
```
