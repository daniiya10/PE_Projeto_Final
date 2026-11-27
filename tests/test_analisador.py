"""Suíte de testes automatizados para o Analisador de Código-Fonte Python.

Executa testes unitários e de integração cobrindo análise léxica/regex,
remoção de strings e comentários, manipulação de arquivos, tratamento de
exceções, formatação de relatórios e execução via linha de comando.
"""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from src.analisador import (
    analisar_codigo,
    contar_condicionais,
    contar_linhas_vazias,
    contar_repeticoes,
    identificar_funcoes,
    identificar_linhas_longas,
    limpar_strings_e_comentarios,
)
from src.leitor_escritor import (
    ArquivoVazioError,
    gerar_nome_relatorio_padrao,
    ler_arquivo_fonte,
    salvar_relatorio,
    validar_extensao_python,
)
from src.main import main
from src.relatorio import formatar_relatorio_json, formatar_relatorio_texto

DIRETORIO_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_EXEMPLOS = os.path.join(DIRETORIO_PROJETO, "exemplos")


class TestAnalisador(unittest.TestCase):
    """Testes das funções de análise de código em src/analisador.py."""

    def test_contar_linhas_vazias(self):
        linhas = ["x = 1\n", "\n", "   \n", "\t\t\r\n", "# comentario\n"]
        self.assertEqual(contar_linhas_vazias(linhas), 3)

    def test_limpar_strings_e_comentarios_casos_complexos(self):
        linhas = [
            "# if for while def\n",
            'msg = "if x > 0: # nao e comentario"\n',
            "outra = 'while True: for i in x:'  # comentario inline if\n",
            'escapada = "aspas \\"if for while\\" fim"\n',
            '"""\n',
            "if dentro_de_docstring:\n",
            "# tambem nao e comentario\n",
            '"""\n',
            "if valor > 0:\n",
        ]
        limpas, stats = limpar_strings_e_comentarios(linhas)

        self.assertEqual(len(limpas), len(linhas))
        self.assertEqual(stats["linhas_comentarios"], 1)
        self.assertEqual(stats["comentarios_inline"], 1)
        self.assertEqual(contar_condicionais(limpas)["if"], 1)
        self.assertEqual(contar_repeticoes(limpas)["total"], 0)
        self.assertEqual(identificar_funcoes(limpas), [])

    def test_nao_confundir_palavras_reservadas_com_identificadores(self):
        linhas = [
            "verificar_if = 10\n",
            "formato = 'abc'\n",
            "while_ativo = True\n",
            "definicao = 42\n",
            "if verificar_if and while_ativo:\n",
            "    for item in formato:\n",
            "        while definicao > 0:\n",
            "            definicao -= 1\n",
        ]
        limpas, _ = limpar_strings_e_comentarios(linhas)
        self.assertEqual(contar_condicionais(limpas), {"if": 1, "elif": 0})
        self.assertEqual(
            contar_repeticoes(limpas), {"for": 1, "while": 1, "total": 2}
        )
        self.assertEqual(identificar_funcoes(limpas), [])

    def test_identificar_funcoes_sincronas_e_assincronas(self):
        linhas = [
            "def primeira(a, b):\n",
            "    return a + b\n",
            "\n",
            "class Exemplo:\n",
            "    def metodo(self):\n",
            "        pass\n",
            "\n",
            "async def tarefa_assincrona():\n",
            "    pass\n",
        ]
        limpas, _ = limpar_strings_e_comentarios(linhas)
        funcoes = identificar_funcoes(limpas)
        self.assertEqual(
            funcoes,
            [
                {"nome": "primeira", "linha": 1},
                {"nome": "metodo", "linha": 5},
                {"nome": "tarefa_assincrona", "linha": 8},
            ],
        )

    def test_identificar_linhas_longas_fronteira(self):
        linhas = [
            "a" * 79 + "\n",  # Exatamente no limite: NÃO ultrapassa
            "b" * 80 + "\n",  # Ultrapassa por 1 caractere
            "c" * 10 + "\n",
        ]
        longas = identificar_linhas_longas(linhas, limite_caracteres=79)
        self.assertEqual(len(longas), 1)
        self.assertEqual(longas[0]["linha"], 2)
        self.assertEqual(longas[0]["tamanho"], 80)

    def test_limite_invalido_lanca_value_error(self):
        with self.assertRaises(ValueError):
            identificar_linhas_longas(["x = 1\n"], limite_caracteres=0)
        with self.assertRaises(ValueError):
            analisar_codigo(["x = 1\n"], limite_caracteres=-5)

    def test_analise_exemplo_basico(self):
        caminho = os.path.join(PASTA_EXEMPLOS, "exemplo_basico.py")
        linhas = ler_arquivo_fonte(caminho)
        res = analisar_codigo(linhas, nome_arquivo=caminho, limite_caracteres=79)

        self.assertEqual(res["total_linhas"], 29)
        self.assertEqual(res["linhas_vazias"], 8)
        self.assertEqual(res["linhas_comentarios"], 3)
        self.assertEqual(res["linhas_codigo"], 18)
        self.assertEqual(res["condicionais"], {"if": 2, "elif": 1})
        self.assertEqual(res["repeticoes"], {"for": 1, "while": 0, "total": 1})
        self.assertEqual(res["total_funcoes"], 2)
        self.assertEqual(res["total_linhas_longas"], 0)

    def test_analise_exemplo_desafio_regex(self):
        caminho = os.path.join(PASTA_EXEMPLOS, "exemplo_desafio_regex.py")
        linhas = ler_arquivo_fonte(caminho)
        res = analisar_codigo(linhas, nome_arquivo=caminho, limite_caracteres=79)

        self.assertEqual(res["linhas_comentarios"], 4)
        self.assertEqual(res["comentarios_inline"], 1)
        self.assertEqual(res["condicionais"]["if"], 1)
        self.assertEqual(res["repeticoes"]["for"], 1)
        self.assertEqual(res["repeticoes"]["while"], 1)
        self.assertEqual(res["total_funcoes"], 1)
        self.assertEqual(res["funcoes"][0]["nome"], "funcao_real")


class TestLeitorEscritor(unittest.TestCase):
    """Testes das operações de I/O e tratamento de exceções."""

    def test_ler_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            ler_arquivo_fonte("caminho/que/nao/existe.py")

    def test_ler_caminho_vazio(self):
        with self.assertRaises(ValueError):
            ler_arquivo_fonte("   ")

    def test_ler_diretorio_lanca_erro(self):
        with self.assertRaises(IsADirectoryError):
            ler_arquivo_fonte(PASTA_EXEMPLOS)

    def test_ler_arquivo_vazio_lanca_arquivo_vazio_error(self):
        caminho_vazio = os.path.join(PASTA_EXEMPLOS, "exemplo_vazio.py")
        with self.assertRaises(ArquivoVazioError):
            ler_arquivo_fonte(caminho_vazio)

    def test_ler_arquivo_binario_lanca_unicode_decode_error(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"\xff\xfe\x00\x80\x81")
            caminho_tmp = tmp.name
        try:
            with self.assertRaises(UnicodeDecodeError):
                ler_arquivo_fonte(caminho_tmp)
        finally:
            os.remove(caminho_tmp)

    def test_salvar_relatorio_cria_diretorios_e_grava(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            caminho_saida = os.path.join(tmpdir, "subpasta", "relatorio.txt")
            salvo = salvar_relatorio(caminho_saida, "conteudo de teste")
            self.assertTrue(os.path.isfile(salvo))
            with open(salvo, "r", encoding="utf-8") as arq:
                self.assertEqual(arq.read(), "conteudo de teste")

    def test_salvar_relatorio_em_diretorio_lanca_erro(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(IsADirectoryError):
                salvar_relatorio(tmpdir, "conteudo")

    def test_validar_extensao_e_nome_padrao(self):
        self.assertTrue(validar_extensao_python("script.py"))
        self.assertTrue(validar_extensao_python("SCRIPT.PY"))
        self.assertFalse(validar_extensao_python("texto.txt"))
        self.assertEqual(
            gerar_nome_relatorio_padrao("exemplos/teste.py", formato="txt"),
            os.path.join("relatorios", "relatorio_teste.txt"),
        )
        self.assertEqual(
            gerar_nome_relatorio_padrao("exemplos/teste.py", formato="json"),
            os.path.join("relatorios", "relatorio_teste.json"),
        )


class TestRelatorioECLI(unittest.TestCase):
    """Testes da geração de relatórios e da interface CLI."""

    def test_formatar_relatorio_texto_e_json(self):
        resultado = analisar_codigo(
            ["# cabecalho\n", "def f():\n", "    if True:\n", "        pass\n"],
            nome_arquivo="teste.py",
            limite_caracteres=79,
        )
        texto = formatar_relatorio_texto(resultado, data_hora="01/12/2026 10:00:00")
        self.assertIn("RELATÓRIO DE ANÁLISE DE CÓDIGO-FONTE", texto)
        self.assertIn("def f()", texto)
        self.assertIn("01/12/2026 10:00:00", texto)

        texto_json = formatar_relatorio_json(
            resultado, data_hora="01/12/2026 10:00:00"
        )
        dados = json.loads(texto_json)
        self.assertEqual(dados["total_funcoes"], 1)
        self.assertEqual(dados["condicionais"]["if"], 1)

    def test_cli_execucao_direta_e_gravacao(self):
        caminho_entrada = os.path.join(PASTA_EXEMPLOS, "exemplo_complexo.py")
        with tempfile.TemporaryDirectory() as tmpdir:
            caminho_saida = os.path.join(tmpdir, "saida.txt")
            saida_stdout = io.StringIO()
            with redirect_stdout(saida_stdout):
                codigo = main([caminho_entrada, "-o", caminho_saida, "-l", "79"])

            self.assertEqual(codigo, 0)
            self.assertTrue(os.path.isfile(caminho_saida))
            with open(caminho_saida, "r", encoding="utf-8") as arq:
                conteudo = arq.read()
            self.assertIn("buscar_elemento", conteudo)
            self.assertIn("sincronizar_dados_remotos", conteudo)

    def test_cli_erros_retornam_codigo_1(self):
        buf_out = io.StringIO()
        buf_err = io.StringIO()
        with redirect_stdout(buf_out), redirect_stderr(buf_err):
            self.assertEqual(
                main([os.path.join(PASTA_EXEMPLOS, "exemplo_vazio.py")]), 1
            )
            self.assertEqual(main(["arquivo_inexistente.py"]), 1)
            self.assertEqual(
                main(
                    [os.path.join(PASTA_EXEMPLOS, "exemplo_basico.py"), "-l", "0"]
                ),
                1,
            )


if __name__ == "__main__":
    unittest.main()
