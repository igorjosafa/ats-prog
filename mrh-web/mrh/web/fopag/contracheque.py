# -*- coding: utf-8 -*-

import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from .. import Mrh
from ..exceptions import MrhException
from . import MrhFopag


class MrhContracheque(MrhFopag, Mrh):
    def gerar_contracheque_servidor(self, condicao, matriculas=[],
        cabecalho="{default}", fname="contracheques.pdf"):
        
        self.go_contracheque_servidor()

        if condicao:
            self.executa_condicao(condicao)

        self.executar_ordenacao(bool(condicao), matriculas)

        if cabecalho != '{default}':
            cabecalho = cabecalho.format(default=self.get_especificacao_cabecalho())
            self.fill('especificacaoCabecalho', cabecalho)
        
        self.driver.find_element(By.LINK_TEXT, "Imprimir").click()
        self.raise_if_alert()
        self.save_file(fname, timeout=60*10)
