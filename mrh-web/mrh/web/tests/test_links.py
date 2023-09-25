from os import getenv
import unittest

from mrh.web import Mrh


class TestLinks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        usuario = getenv("MRH_USUARIO")
        senha = getenv("MRH_SENHA")
        cls.mrh = mrh = Mrh()
        mrh.login(usuario, senha)

    @classmethod
    def tearDownClass(cls):
        cls.mrh.close()

    def setUp(self):
        self.mrh.go_home()

    def test_folha_pagamento(self):
        self.mrh.go_folha_pagamento()
        self.assertTrue(self.mrh.is_at_folha_pagamento())

    def test_selecao_folha(self):
        self.mrh.go_selecao_folha()
        self.assertTrue(self.mrh.is_at_selecao_folha())

    def test_relatorios_fechamento(self):
        self.mrh.go_relatorios_fechamento()
        self.assertTrue(self.mrh.is_at_relatorios_fechamento())

    def test_entidades_externas(self):
        self.mrh.go_entidades_externas()
        self.assertTrue(self.mrh.is_at_entidades_externas())

    def test_contracheque_servidor(self):
        self.mrh.go_contracheque_servidor()
        self.assertTrue(self.mrh.is_at_contracheque_servidor())
    
    def test_previa_servidor(self):
        self.mrh.go_previa_servidor()
        self.assertTrue(self.mrh.is_at_previa_servidor())

    def test_contracheque_pa(self):
        self.mrh.go_contracheque_pa()
        self.assertTrue(self.mrh.is_at_contracheque_pa())
    
    def test_email_contracheque(self):
        self.mrh.go_email_contracheque()
        self.assertTrue(self.mrh.is_at_email_contracheque())
    
    def test_elemento_despesa(self):
        self.mrh.go_elemento_despesa()
        self.assertTrue(self.mrh.is_at_elemento_despesa())
    
    def test_entidades_externas(self):
        self.mrh.go_entidades_externas()
        self.assertTrue(self.mrh.is_at_entidades_externas())
    
    def test_gera_arquivo_bancario(self):
        self.mrh.go_gera_arquivo_bancario()
        self.assertTrue(self.mrh.is_at_gera_arquivo_bancario())
    
    def test_liquido_banco_agencia(self):
        self.mrh.go_liquido_banco_agencia()
        self.assertTrue(self.mrh.is_at_liquido_banco_agencia())

    def test_liquidos_totalizadores(self):
        self.mrh.go_liquidos_totalizadores()
        self.assertTrue(self.mrh.is_at_liquidos_totalizadores())
    
    def test_relacao_consignatarias(self):
        self.mrh.go_relacao_consignatarias()
        self.assertTrue(self.mrh.is_at_relacao_consignatarias())
    
    def test_resumo_geral(self):
        self.mrh.go_resumo_geral()
        self.assertTrue(self.mrh.is_at_resumo_geral())
    
    def test_go_rubricas_calculadas(self):
        self.mrh.go_rubricas_calculadas()
        self.assertTrue(self.mrh.is_at_rubricas_calculadas())
    
    def test_relatorios_sql(self):
        self.mrh.go_relatorios_sql()
        self.assertTrue(self.mrh.is_at_relatorios_sql())
    
    def test_exporta_relatorios(self):
        self.mrh.go_exporta_relatorios()
        self.assertTrue(self.mrh.is_at_exporta_relatorios())
    
    def test_portal_usuarios(self):
        self.mrh.go_portal_usuarios()
        self.assertTrue(self.mrh.is_at_portal_usuarios())


if __name__ == '__main__':
    unittest.main()