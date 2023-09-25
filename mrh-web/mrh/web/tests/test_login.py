from os import getenv
import unittest

from mrh.web import Mrh
from mrh.web.exceptions import MrhException


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mrh = Mrh()

    @classmethod
    def tearDownClass(cls):
        cls.mrh.close()

    def setUp(self):
        pass

    def test_login_successful(self):
        usuario = getenv("MRH_USUARIO")
        senha = getenv("MRH_SENHA")
        self.mrh.login(usuario, senha)
        self.assertTrue(self.mrh.is_logged_in())

    def test_logged_in_user(self):
        usuario = getenv("MRH_USUARIO")
        senha = getenv("MRH_SENHA")
        nome = getenv("MRH_USUARIO_NOME")
        self.mrh.login(usuario, senha)
        self.assertTrue(self.mrh.is_logged_in(nome))

    def test_login_failed(self):
        with self.assertRaises(MrhException):
            self.mrh.login('ninguem', 'senhaerrada')
