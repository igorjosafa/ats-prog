from os import getenv
import unittest

from mrh.web.ferramentas import MrhFerramentas


class TestFerramentas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        usuario = getenv("MRH_USUARIO")
        senha = getenv("MRH_SENHA")
        cls.mrh = mrh = MrhFerramentas()
        mrh.login(usuario, senha)

    @classmethod
    def tearDownClass(cls):
        cls.mrh.close()

    def setUp(self):
        self.mrh.go_home()

    def test_executar_sql_existente(self):
        raise NotImplementedError

    def test_executar_sql_inexistente(self):
        raise NotImplementedError
    
    def test_exportar_relatorio(self):
        raise NotImplementedError