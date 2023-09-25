# -*- coding: utf-8 -*-

import datetime
import time
import os

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from ..ferramentas import MrhFerramentas
from ..exceptions import MrhException
from . import MrhFopag


class MrhDocumentos(MrhFopag, MrhFerramentas):

    def _imprimir(self, handle_alert=True) -> str|None:
        el = self.driver.find_element(By.LINK_TEXT, "Imprimir")
        if el.get_attribute('href').startswith('javascript:'):
            self.driver.execute_script(el.get_attribute('href'))
        else:
            self.driver.execute_script("arguments[0].click();", el)
        if handle_alert:
            self.raise_if_alert()

        el = self.driver.find_element(By.NAME, "impressaoId")
        timeout = 40
        while not el.get_attribute("value"):
            time.sleep(0.1)
            timeout -= 1
            if timeout <= 0: break

        return el.get_attribute("value")

    def gerar_ats(self, condicao, data_limite):
        nome_arquivo = f'ats gerados - {data_limite[-6:-4]}-{data_limite[-4:]}.pdf'

        self.go_calculo_efetivacao_ats()
        
        if condicao:
            self.executar_condicao(condicao)

        #informa a data limite no campo 'Data limite para cálculo'
        self.driver.find_element(By.NAME, "dataLimite").send_keys(data_limite)

        #seleciona a opção 'Concessões que ocorrerem no mês selecionado'
        self.driver.find_element(By.XPATH, "//input[@name='tipoProcessamento'][@value='1']").click()

        #seleciona a opção 'Concessões que ocorrerem no mês selecionado'
        self.driver.find_element(By.XPATH, "//input[@name='tipoAdicional'][@value='1']").click()

        #informa 1 no campo 'Quantidade de anos'
        self.driver.find_element(By.NAME, "quantidadeAnos").send_keys(1)

        #informa 1 no campo 'Percentual do adicional'
        self.driver.find_element(By.NAME, "percentualAdicional").send_keys(1)

        #informa 99 no campo 'Limite máximo do adicional'
        self.driver.find_element(By.NAME, "maximoAdicional").send_keys(99)

        self.driver.find_element(By.XPATH, "//a[@href='javascript:executar();']").click()
        self.handle_alert()
        
        impressao_id = self._imprimir()

        numero_do_arquivo = 1
        while os.path.exists(os.path.join(self.download_dir, nome_arquivo)):
            nome_arquivo = nome_arquivo[:-4] + f' {numero_do_arquivo}' + nome_arquivo[-4:]
            numero_do_arquivo += 1

        self.save_file(nome_arquivo)

        return nome_arquivo[:-4], impressao_id
    
    def efetivar_ats(self):
        self.go_calculo_efetivacao_ats()

        self.driver.find_element(By.XPATH, "//a[contains(text(),'Efetivação')]").click()

        select = Select(self.driver.find_element(By.NAME, 'tipoCalculo'))
        select.select_by_value('4')
        self.driver.find_element(By.XPATH, "//a[@href='javascript:efetivar();']").click()

    def gerar_progressao(self, condicao, data_limite):
        nome_arquivo = f'progressoes geradas - {data_limite[-6:-4]}-{data_limite[-4:]}.pdf'

        self.go_nivel_letra()
        
        if condicao:
            self.executar_condicao(condicao)
            self.executar_ordenacao_progressao(condicao)

        self.driver.find_element(By.NAME, "dataLimite").send_keys(data_limite)

        self.driver.find_element(By.XPATH, "//input[@name='opcaoImprimir'][@value='1']").click()

        self.driver.find_element(By.XPATH, "//a[@href='javascript:executar();']").click()
        self.handle_alert()

        impressao_id = self._imprimir()

        numero_do_arquivo = 1
        while os.path.exists(os.path.join(self.download_dir, nome_arquivo)):
            nome_arquivo = nome_arquivo[:-4] + f' {numero_do_arquivo}' + nome_arquivo[-4:]
            numero_do_arquivo += 1

        self.save_file(nome_arquivo)

        return nome_arquivo[:-4], impressao_id
    
    def efetivar_progressao(self):
        self.go_nivel_letra()

        self.driver.find_element(By.XPATH, "//input[@name='opcaoImprimir'][@value='1']").click()

        self.driver.find_element(By.XPATH, "//a[contains(text(),'Efetivação')]").click()

        select = Select(self.driver.find_element(By.NAME, 'tipoProvimento'))
        select.select_by_value('5')
        self.driver.find_element(By.XPATH, "//a[@href='javascript:efetivar();']").click()
    