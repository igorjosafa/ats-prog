from os import getenv
import os.path
import unittest
import tempfile
import shutil
import datetime

from mrh.web.fopag.documentos import MrhDocumentos


class TestFopagDocs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        usuario = getenv("MRH_USUARIO")
        senha = getenv("MRH_SENHA")
        cls.tempdir = tempfile.mkdtemp()
        cls.mrh = mrh = MrhDocumentos(download_dir=cls.tempdir)
        mrh.login(usuario, senha)
        mrh.selecionar_folha(12, 2021, 1) # id 2709

    @classmethod
    def tearDownClass(cls):
        cls.mrh.close()
        shutil.rmtree(cls.tempdir)

    def setUp(self):
        self.mrh.go_home()

    def test_gerar_resumo_bases(self):
        self.mrh.gerar_resumo_bases(condicao=187, base1=33, fname='base33.pdf')
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, 'base33.pdf')))

    def test_gerar_resumo_geral(self):
        fname = "resumogeral.pdf"
        self.mrh.gerar_resumo_geral(condicao=187, fname=fname)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, fname)))

    def test_gerar_relacao_consignatarias(self):
        fname = "rconsig.pdf"
        self.mrh.gerar_relacao_consignatarias(condicao=187, fname=fname)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, fname)))

    def test_gerar_elemento_despesa(self):
        fname = "eldesp.pdf"
        self.mrh.gerar_elemento_despesa(condicao=187, fname=fname)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, fname)))

    def test_gerar_liquido_banco_agencia(self):
        fname = "lba.pdf"
        self.mrh.gerar_liquido_banco_agencia(condicao=187, fname=fname)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, fname)))

    def test_gerar_liquidos_totalizadores(self):
        fname = "ltot.pdf"
        self.mrh.gerar_liquidos_totalizadores(condicao=187, fname=fname)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, fname)))

    def test_gerar_rubricas_calculadas(self):
        fname = "rcalc.pdf"
        self.mrh.gerar_rubricas_calculadas(condicao=187, fname=fname)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, fname)))

    def test_gerar_arquivo_bancario(self):
        fname = "abanc.txt"
        self.mrh.gerar_arquivo_bancario(
            condicao=187, data=datetime.date(2020, 12, 20),
            banco="6", parametro="2", fname=fname)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, fname)))


