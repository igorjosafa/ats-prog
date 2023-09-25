# -*- coding: utf-8 -*-
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from .. import Mrh


MESES_FOLHA = [
    'JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO',
    'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
]


class MrhFopag(Mrh):

    def executar_ordenacao(self, condicao=True, matriculas=[]):
        frm = self.driver.execute_script("return self.name")

        wcount = len(self.driver.window_handles)
        parent_window = self.driver.current_window_handle

        self.driver.find_element(By.LINK_TEXT, "Ordenação").click()

        # pula pra janela recem aberta
        while len(self.driver.window_handles) == wcount:
            time.sleep(0.1)
        self.driver.switch_to.window(self.driver.window_handles[wcount])

        el = self.driver.find_element(By.NAME, 'matriculas')
        el.clear()
        if matriculas:
            self.fill('matriculas', ";".join(map(str, matriculas)))
        
        self.check('condicao', condicao)

        self.driver.execute_script("Salvar()")
        self.handle_alert(timeout=60*5)

        self.driver.execute_script("Executar()")
        self.handle_alert()

        # Apos executar, a janela fecha automaticamente
        self.driver.switch_to.window(parent_window)
        if frm:
            self.driver.switch_to.frame(frm)

    def get_especificacao_cabecalho(self, elname='especificacaoCabecalho'):
        el = self.driver.find_element(By.NAME, elname)
        return el.get_attribute('value')

    def selecionar_folha(self, mes, ano, seq):
        self.go_selecao_folha()
        select = Select(self.driver.find_element(By.NAME, 'Ano'))
        select.select_by_value(str(ano))

        nome_mes = MESES_FOLHA[mes-1]
        sel = "//tr[td='{}']/td/following-sibling::td[text()='{}']/parent::tr/td[1]".format(nome_mes, seq)
        
        while 1:
            try:
                el = self.driver.find_element(By.XPATH, sel)
            except NoSuchElementException:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, '#tb_Folha_next:not(.disabled)')
                    el.click()
                except NoSuchElementException:
                    return None
            else:
                break

        self.double_click(el)
        return int(el.text)
