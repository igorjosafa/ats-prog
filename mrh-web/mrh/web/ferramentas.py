# -*- coding: utf-8 -*-

import os.path
import time
import urllib.request
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchWindowException

from . import Mrh
from .exceptions import MrhException


class MrhFerramentas(Mrh):

    def executar_sql(self, nome_consulta, titulo='{default}{random}',
                    fname='consulta.pdf', gera_pdf=True, **kwargs):
        """Executa a consulta sql de nome nome_consulta.

        titulo:
           default corresponde ao 'Titulo para impressao' padrao
           random  uuid.uuid4().hex

        Os eventuais parâmetros :p1, :p2 etc podem ser passados na forma 
        p1=valor, p2=valor (kwargs).
        
        Retorna o titulo usado (após substituição).
        """
        
        self.go_relatorios_sql()
        time.sleep(0.1)
        self.fill("Descricao", nome_consulta, enter=True)
        
        try:
            el = self.driver.find_element(By.ID, 'grid.data.item:0')
        except NoSuchElementException:
            raise MrhException("Consulta nao encontrada!")

        el = self.driver.find_element(By.ID, 'grid')
        el.send_keys(Keys.ARROW_DOWN)
        self.driver.find_element(By.LINK_TEXT, 'Imprimir').click()

        title = self.driver.find_element(By.NAME, 'titulo')
        title = title.get_attribute('value')

        titulo = titulo.format(default=title, random=uuid.uuid4().hex)
        self.fill('titulo', titulo)

        for k, v in kwargs.items():
            self.fill(k, str(v))
        
        if gera_pdf:
            self.driver.find_element(By.ID, 'btn-imprimir').click()
            self.save_file(fname)
        else:
            self.driver.find_element(By.ID, 'btn-preparar').click()
            msg = self.handle_alert()

        return titulo
    
    def executar_explorador_de_dados(self, nome_consulta, titulo='{default}{random}',
                    fname='consulta.pdf', **kwargs):
        """Executa a consulta de nome nome_consulta.

        titulo:
           default corresponde ao 'Titulo para impressao' padrao
           random  uuid.uuid4().hex

        Os eventuais parâmetros :param1, :param2 etc podem ser passados na forma 
        param1=valor, param2=valor (kwargs).
        
        Retorna o titulo usado (após substituição).
        """
        
        self.go_explorador_de_dados()
        time.sleep(0.1)
        self.fill("Descricao", nome_consulta, enter=True)
        
        try:
            el = self.driver.find_element(By.ID, 'grid.data.item:0')
        except NoSuchElementException:
            raise MrhException("Consulta nao encontrada!")

        el = self.driver.find_element(By.ID, 'grid')
        el.send_keys(Keys.ARROW_DOWN)
        self.driver.find_element(By.LINK_TEXT, 'Imprimir').click()

        title = self.driver.find_element(By.NAME, 'titulo')
        title = title.get_attribute('value')

        titulo = titulo.format(default=title, random=uuid.uuid4().hex)
        self.fill('titulo', titulo)

        for k, v in kwargs.items():
            self.fill(k, str(v))
        
        self.driver.find_element(By.XPATH, "//img[@src='/csp/mentorh/imagens/imprimir.png']").click()
        self.save_file(fname)

        return titulo
    
    def exportar_relatorio(self, titulo, tipo=2, fname=None, arquivo=None, fid=None):
        """Exporta Relatórios (Ferramentas -> Exporta Relatórios)

        Tipo de Arquivo: XML Doc (1) XML Xls (2) Texto (5) HTML (6) CSV (7)
        
        """
        self.go_exporta_relatorios()

        # o botao de pesquisa eh uma imagem!
        #el = self.driver.find_element_by_xpath("//img[contains(@src, 'botaoPesquisar.png')]")
        #self.driver.get_screenshot_as_file('/sfiles/botaoPesquisar.png')
        time.sleep(0.1)
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'botaoPesquisar.png')]"))
            )
        except TimeoutException:
            return MrhException("Timeout para o botaoPesquisar!")
        el.click()

        # seleciona o tipo de arquivo para exportacao
        self.select_radio("opcao", tipo)

        # preenche o caminho do arquivo a ser gerado
        el = self.driver.find_element(By.NAME, "arquivo")
        path = el.get_attribute("value")
        if not arquivo:
            # .zip will make it (most likely) downloadable in windows
            arquivo = str(uuid.uuid4().hex) + '.zip'
        if path:
            path = os.path.join(path, arquivo)
        else:
            path = arquivo
        el.clear()
        el.send_keys(path)
        
        if fid == None:
            # seleciona o primeiro item do grid
            el = self.driver.find_element(By.ID, 'grid1')
            el.send_keys(Keys.ARROW_DOWN)
        else:
            #seleciona o relatório pelo valor
            el = self.driver.find_element(By.XPATH, "//div[text()='{}']".format(fid))
            el.click()

        # numero de janelas para depois de gerar o arquivo
        wcount = len(self.driver.window_handles)
        parent_window = self.driver.current_window_handle

        # o botao eh uma imagem e o link so tem um href!
        # executamos o codigo do href
        self.driver.execute_script("geraArquivo();")

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                "Timed out waiting for alert")
            alert = self.driver.switch_to.alert
            alert.dismiss()
        except TimeoutException:
            raise MrhException("Timeout na geracao do arquivo.")
        except NoSuchWindowException:
            #print('taking print...')
            #self.driver.get_screenshot_as_file('/sfiles/nsw.png')
            raise

        # pula pra janela recem aberta
        while len(self.driver.window_handles) == wcount:
            time.sleep(0.1)
        self.driver.switch_to.window(self.driver.window_handles[wcount])

        this_url = self.driver.current_url

        # pega o link do arquivo
        el = self.driver.find_element(By.CSS_SELECTOR, 'a')
        el.click()

        # TODO: Check whether it's text ot not
        # content-type: text retorna o text do elemento pre
        if this_url != self.driver.current_url: # if tipo in (5, 6, 7):
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, 'pre')
            except NoSuchElementException:
                text = ''
            else:
                text = el.text
        else:
            text = None

        # fecha popup e volta para janela anterior
        self.driver.close()
        self.driver.switch_to.window(parent_window)

        if text is None:
            if fname:
                self.save_file(fname, watch_file=arquivo)
        elif fname:
            self.save_text(text or '', fname)
        else:
            return text
