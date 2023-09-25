# -*- coding: utf-8 -*-

import os
import os.path
import time
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from . import config
from .exceptions import MrhException
from .links import Links
from .webdriver import Browser


class Mrh(Links, Browser):

    def executar_condicao(self, condicao:int) -> None:
        """Executa a condição de processamento indicada.

        O método deve ser chamado quando em uma página onde a opção Condição
        estiver disponível, e.g.: Resumo Geral, Elemento de Despesa.

        Página CSP: condicaoProcessamentoExecutar.csp
        
        Parameters
        -----------

        condicao: int
            O id da condição desejada.
        """
        
        frm = self.driver.execute_script("return self.name")
        self.driver.find_element(By.LINK_TEXT, "Condição").click()

        self.driver.switch_to.window("popup")
       
        elem = self.driver.find_element(By.NAME, 'id')
        self.driver.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', elem, str(condicao))
        self.driver.find_element(By.LINK_TEXT, "Executar").click()

        time.sleep(0.1)

        self.driver.switch_to.window("MENTORH")
        el = self.driver.find_element(By.NAME, "titulo")
        while el.get_attribute('value') != "Processamento finalizado.":
            time.sleep(0.1)
        
        time.sleep(0.1)
        el = self.driver.find_element(By.LINK_TEXT, "Sair")
        el.click()
        
        self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.switch_to.default_content()
        if frm:
            self.driver.switch_to.frame(frm)

    # TODO: incluir demais campos de ordenação e opções correspondentes
    def executar_ordenacao_com_condicao(self, condicao: int, campo1="Matricula",
                                        matriculas=[]) -> None:
        """Executa a ordenação na tela em que a ordenação e a seleção de
        condição de processamento estão juntas.

        O método deve ser chamado quando em uma página onde a opção de
        Ordenação estiver disponível e apresentar formulário de
        execução de condição de processamento no mesmo formulário; e.g.:
        Relação de Líquidos / Totalizadores, Resumo das Bases.

        Página CSP: ordenacaoRelatorioII.csp

        Parameters
        -----------

        condicao: int
            O id da condição desejada

        campo1: str
            O valor para o Primeiro campo de ordenação. Deve ser usado o texto da <option>.

        matriculas: list
            Uma lista de matrículas para usar como restrição. [opcional]
        """

        frm = self.driver.execute_script("return self.name")
        self.driver.find_element(By.LINK_TEXT, "Ordenação").click()
        time.sleep(1)
        iframe = self.driver.find_elements(By.TAG_NAME, 'iframe')[0]
        self.driver.switch_to.frame(iframe)

        el = self.driver.find_element(By.NAME, 'matriculas')
        el.clear()

        if condicao:
            elem = self.driver.find_element(By.NAME, 'grid1ID')
            self.driver.execute_script('''
                var elem = arguments[0];
                var value = arguments[1];
                elem.value = value;
            ''', elem, str(condicao))
            self.driver.find_element(By.NAME, "GeraCondicao").click()
            self.handle_progress_bar(close=False)
       
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame('frame1')
        iframe = self.driver.find_elements(By.TAG_NAME, 'iframe')[0]
        self.driver.switch_to.frame(iframe)

        if matriculas:
            self.fill("matriculas", ";".join(map(str, matriculas)))

        #el = self.driver.find_element(By.XPATH, "//span[@class='title' and text()='Ordenação']")
        el = self.driver.find_element(By.NAME, "Ordena")
        el.click()
        WebDriverWait(self.driver, 10).until(EC.staleness_of(el))

        if frm:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(frm)


    def executar_ordenacao_progressao(self, condicao: int, campo1="Matricula",
                                        matriculas=[]) -> None:
        """Executa a ordenação na tela em que é necessário marcar 'Usar Condição de Processamento'.

        O método deve ser chamado para ordenar as matrículas durante a geração da progressão funcional

        Parameters
        -----------

        campo1: str
            O valor para o Primeiro campo de ordenação. Deve ser usado o texto da <option>.

        matriculas: list
            Uma lista de matrículas para usar como restrição. [opcional]
        """

        frm = self.driver.execute_script("return self.name")
        self.driver.find_element(By.LINK_TEXT, "Ordenação").click()

        self.driver.switch_to.window("popup")

        if not (self.driver.find_element(By.NAME, 'condicao').is_selected()): self.driver.find_element(By.NAME, 'condicao').click()

        el = self.driver.find_element(By.NAME, 'matriculas')
        el.clear()

        if matriculas:
            self.fill("matriculas", ";".join(map(str, matriculas)))
       
        select = Select(self.driver.find_element(By.NAME, 'campo1'))
        select.select_by_value('Matricula')

        #el = self.driver.find_element(By.XPATH, "//span[@class='title' and text()='Ordenação']")
        el = self.driver.find_element(By.XPATH, "//input[@value='Salvar']").click()
        time.sleep(0.1)
        self.handle_alert()
        el = self.driver.find_element(By.XPATH, "//input[@value='Executar']").click()
        time.sleep(0.1)
        self.handle_alert()

        self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.switch_to.default_content()
        if frm:
            self.driver.switch_to.frame(frm)

    # TODO: raise MrhException com o motivo da falha de login
    def login(self, usuario:str, senha:str, url:str=config.LOGIN_URL):
        """Efetua login no sistema.
        
        Parameters
        -----------

        usuario: str
            O nome de usuário do sistema

        senha: str
            A senha do usuário

        url: str
            O endereço da página de login
        """

        self.go_login(url)
        time.sleep(0.1)
        login = self.driver.find_element(By.NAME, "login")
        self.fill("login", usuario)
        time.sleep(1)
        self.fill("senha", senha)
        btn = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
        btn.click()
        try:
            WebDriverWait(self.driver, 20).until(EC.staleness_of(login))
        except TimeoutException: # we're still in the same page
            self.handle_div_message(timeout=10)

    def is_logged_in(self, name=''):
        try:
            el = self.driver.find_element(By.CSS_SELECTOR, '.welcome > .name')
            if name:
                return el.text.strip() == name
            return True
        except NoSuchElementException:
            return False
 
    def close(self):
        self.driver.quit()

    def handle_div_message(self, timeout=60, timeout_ok=False):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.ID, "divMessage")))
        except TimeoutException:
            if timeout_ok:
                return
            else:
                raise
        el = self.driver.find_element(By.ID, "divMessage")
        k = el.get_attribute('class')
        msg = el.text.lstrip('x').strip()
        if 'errorMessage' in k:
            raise MrhException(msg)
        #assert 'successMessage' in k
        el.find_element(By.ID, 'closeButton').click()
        return msg

    def handle_progress_bar(self, close=True):
        self.driver.switch_to.frame("ProgressBarFrame")
        if close:
            #print('Waiting...')
            WebDriverWait(self.driver, 120).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR , ".progress"), "Concluído"))
            #bar = self.driver.find_element(By.CSS_SELECTOR, '.progress')
            #while bar.text != "Concluído":
            #    time.sleep(1)
            self.driver.find_element(By.ID, "progressCloseButton").click()
        else:
            #print('Waiting for progress-bar to disappear...')
            pb = self.driver.find_element(By.CSS_SELECTOR, '.progress-bar')
            #print("PB located")
            #print('waiting...')
            n = 0
            while n < 120:
                try:
                    pb = self.driver.find_element(By.CSS_SELECTOR, '.progress-bar')
                except NoSuchElementException:
                    #print("Gone.")
                    break
                time.sleep(1)
                n += 1 # self.IMPLICITLY_WAIT
            if n >= 120:
                print("Timed out!")
                
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('frame1')
            # WebDriverWait(self.driver, timeout=120).until(
            #     frame_unavailable_cb("ProgressBarFrame"))
