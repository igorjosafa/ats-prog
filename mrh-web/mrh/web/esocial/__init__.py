# -*- coding: utf-8 -*-

import datetime
import logging
import os
import os.path
import random
import re
import time

from typing import Callable
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

from bs4 import BeautifulSoup

from ..exceptions import MrhException
from ..webdriver import Browser


logger = logging.getLogger(__name__)


LOGIN_URL = 'http://cos7esocial1.cl.df.gov.br:8080/esocial/'


def vigencia2str(dt:datetime.date|str):
    if hasattr(dt, 'year'):
        vg = f'{dt.month:02}/{dt.year:04}'
        return vg
    dt = datetime.datetime.strptime(dt, "%m/%Y")
    return f'{dt.month:02}/{dt.year:04}'

class ESocialWeb(Browser):
    login_url = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver.maximize_window() # ha um bug que esconde a navbar com d-md-none

    def go_login(self, url=LOGIN_URL):
        self.login_url = url
        self.driver.get(self.login_url)

    def go_processamento_fila(self):
        #e = self.driver.find_element(By.LINK_TEXT, 'Fila')
        e = self.driver.find_element(By.XPATH, "//a[text()='Fila']")
        href = e.get_attribute('href')
        self.driver.get(href)

    def go_gerenciar_lotes(self):
        e = self.driver.find_element(By.XPATH, "//a[text()='Gerenciar Lotes']")
        href = e.get_attribute('href')
        self.driver.get(href)

    def go_carga_inicial_eventos(self):
        e = self.driver.find_element(By.XPATH, "//a[text()='Carga Inicial']")
        href = e.get_attribute('href')
        self.driver.get(href)

    def go_relatorios_totalizadores(self):
        e = self.driver.find_element(
            By.XPATH,
            '//a[@id="relatorios"]//following-sibling::ul//'
            'a[contains(text(), "Totalizadores")]'
            )
        href = e.get_attribute("href")
        self.driver.get(href)

    def go_trabalhador_folha_pagamento(self):
        e = self.driver.find_element(By.XPATH, '//a[@id="trabalhador"]//following-sibling::ul//a[contains(text(), "Folha de pagamento")]')
        href = e.get_attribute("href")
        self.driver.get(href)

    def login(self, usuario, senha, url=LOGIN_URL):
        self.go_login(url)
        time.sleep(0.1)
        login = self.driver.find_element(By.NAME, "login")
        self.fill("login", usuario)
        time.sleep(1)
        self.fill("senha", senha)
        btn = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
        btn.click()
        try:
            WebDriverWait(self.driver, 5).until(lambda x: x.execute_script("return document.readyState === 'complete'"))
            el = self.driver.find_element(By.CSS_SELECTOR, '.alert')
            if 'alert-success' in el.get_attribute('class'):
                return
            msg = el.text
            raise MrhException('Erro de login: {}'.format(msg))
        except TimeoutException:
            MrhException("A pagina demorou demais para responder.")
    
    def filtrar_fila_eventos(self, grupo_evento=None, tipo_evento=None, status=None,
        acao=None, detalhe=None, id_fila=None, id_lote=None,
        mes_apur:int=None, ano_apur:int=None, ind_apur=None):
        self.select('grupoEvento', grupo_evento, ignore_if_none=True, by_text=True)
        self.select('tipoEvento', tipo_evento, ignore_if_none=True, by_text=True)
        self.select('status', status, ignore_if_none=True, by_text=True)

        self.select('mesPerApur', mes_apur and f'{mes_apur:02}',
                    ignore_if_none=True, by_text=False)
        self.select('anoPerApur', ano_apur and f'{ano_apur:04}',
                    ignore_if_none=True, by_text=False)
        self.select('indApuracao', ind_apur, ignore_if_none=True, by_text=True)

        self.select('acaoEvento', acao, ignore_if_none=True, by_text=True)
        self.fill('detalhe', detalhe, ignore_if_none=True)
        self.fill('idFila', id_fila, ignore_if_none=True)
        self.fill('idLote', id_lote, ignore_if_none=True)
        self.driver.find_element(By.ID, 'btnConsultar').click()

    def recuperar_tabela_eventos(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        rows = soup.select('#frm tr')
        if len(rows) == 2: # nenhum registro encontrado?
            if rows[1].text.strip() == "Nenhum Registro Encontrado":
                return
        e = rows[0]
        colunas = [str(x.string) for x in e.find_all('th')[1:]]
        tabela = dict()
        for row in rows[1:]:
            cols = row.find_all('td')
            check_id = cols[0].select_one('input')['id']
            d = dict(zip(colunas, [str(x.string) for x in cols[1:-1]]))
            btns = cols[-1].find_all('button')
            for btn in btns:
                d[btn.attrs['title']] = {k: v for k, v in btn.attrs.items() if k.startswith('data-')}

            mat, nome = d['Detalhe'].split(' - ')
            d['Matricula'] = int(mat)
            d['Nome'] = nome
            d['CPF'] = "".join(filter(lambda x: x in "0123456789", d["CPF"]))
            tabela[check_id] = d
            
        return tabela
    
    def enviar_eventos(self, filtro:Callable=lambda evt: True, timeout=20):
        """Envia os eventos da fila filtrados pela função filtro. O filtro 
        recebe o evento como parâmetro e deve retornar True caso o evento deva ser enviado.
        
        """      

        enviados = {}
        inconsistentes = []
        while True:
            eventos = self.recuperar_tabela_eventos()
            if not eventos:
                break
            selected = 0
            selected_list = []
            for evt_id, evt in eventos.items():
                if not filtro(evt): continue
                if 'Inconsistências' in evt:
                    inconsistentes.append(evt['Inconsistências'])
                    continue
                element = self.driver.find_element(By.ID, evt_id)
                self.check(evt_id, True, by_id=True)
                selected += 1
                selected_list.append(evt)
            if selected:
                el = self.driver.find_element(By.ID, 'enviar')
                self.driver.execute_script("arguments[0].click();", el)
                try:
                    WebDriverWait(self.driver, timeout).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert")))
                except TimeoutException:
                    raise MrhException("Timeout enquanto enviava lotes da fila de eventos do eSocial.")
                el = self.driver.find_element(By.CSS_SELECTOR, "div.alert")
                msg = el.text.strip()
                r = re.match("Lote Recebido com Sucesso. - Protocolo: (?P<protocolo>[\d\.]+)", msg)
                if r:
                    protocolo = r.groupdict()["protocolo"]
                    enviados[protocolo] = selected_list
                else:
                    logger.debug("Protocolo de envio do eSocial não encontrado: '{}'".format(msg))
            else:
                if not self.next_page():
                    break
        return dict(enviados=enviados, inconsistentes=inconsistentes)
        
    def next_page(self):
        el = self.driver.find_element(By.XPATH, "//a[@title='Info']")
        m = re.match('\d+\sat.\s(?P<to>\d+)\s\-\sTotal:\s(?P<total>\d+)', el.text)
        m = m.groupdict()
        if m['to'] == m['total']:
            return False # we're finished
        el = self.driver.find_element(By.XPATH, "//a[@title='Próximo']")
        self.click(el)
        return True
    
    def filtrar_fila_lotes(self, id_lote=None, usuario=None, protocolo=None,
                          status=None, dt_envio_inicial=None, dt_envio_final=None):
        self.fill('idLote', id_lote, ignore_if_none=True)
        self.fill('usuarioNome', usuario, ignore_if_none=True)
        self.fill('protocolo', protocolo, ignore_if_none=True)
        self.select('status', status, ignore_if_none=True, by_text=True)
        if dt_envio_inicial:
            self.fill('dtEnvioInicial', dt_envio_inicial.strftime('%d%m%Y'))
        if dt_envio_final:
            self.fill('dtEnvioFinal', dt_envio_final.strftime('%d%m%Y'))
        self.driver.find_element(By.ID, 'btnConsultar').click()

    def recuperar_tabela_lotes(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        rows = soup.select("#tabelaLote tr")
        if len(rows) == 2: # nenhum registro encontrado?
            if rows[1].text.strip() == "Nenhum Lote Encontrado":
                return
        e = rows[0]
        colunas = [str(x.string) for x in e.find_all('th')[1:-1]]
        tabela = dict()
        for row in rows[1:]:
            cols = row.find_all('td')
            d = dict(zip(colunas, [str(x.string) for x in cols[1:-1]]))
            d['acao_id'] = cols[-1].attrs['id']
            tabela[d['Protocolo']] = d
        return tabela
    
    def enviar_lotes(self, filtro:Callable=lambda evt: True, timeout=20):
        def status_finder(lote_id):
            def find_status(driver):
                def handle_modal(driver):
                    try:
                        el = driver.find_element(By.ID, "modal-informacao-msg")
                    except NoSuchElementException:
                        pass
                    else:
                        if el.is_displayed():
                            return el
                
                try:
                    el = driver.find_element(By.XPATH, "//table[@id='tabelaLote']/tbody/tr[@id='tr_lote_{}']/td[4]".format(lote_id))
                except NoSuchElementException:
                    el = handle_modal(driver)
                    if el:
                        return el
                else:
                    if el.text != 'Pendente':
                        return el
                    else:
                        el = handle_modal(driver)
                        if el:
                            return el
            return find_status
        by_status = dict()
        while True:
            lotes = self.recuperar_tabela_lotes()
            if not lotes:
                break
            for protocolo, lote in lotes.items():
                if not filtro(lote): continue
                td = self.driver.find_element(By.ID, lote['acao_id'])
                buttons = td.find_elements(By.TAG_NAME, 'button')
                if buttons:
                    self.click(buttons[0])
                    try:
                        el = WebDriverWait(self.driver, timeout).until(status_finder(lote['Id']))
                    except TimeoutException:
                        raise MrhException("Timeout enquanto aguardava retorno de consulta ao lote eSocial {}.".format(lote['Id']))
                    if 'modal' in el.get_attribute('id'):
                        btn = self.driver.find_element(By.CSS_SELECTOR, ".btn.fechar")
                        self.click(btn)
                        status = 'Em processamento'
                    else:
                        status = el.text.strip()
                    status_list = by_status.setdefault(status, [])
                    status_list.append(lote)
            if not self.next_page():
                    break
        return by_status

    def efetuar_carga_inicial(self, eventos:list[str]=[]):
        self.go_carga_inicial_eventos()
        # torna todos os accordions visiveis
        botoes = self.driver.find_elements(By.CSS_SELECTOR, ".accordion-button.collapsed")
        for botao in botoes:
            botao.click()
        # marca os eventos
        for evt in eventos:
            el = self.driver.find_element(
                By.XPATH,
                f'//label[contains(text(),"{evt}")]//'
                'preceding-sibling::input')
            el.click()
        # executa importacao
        el = self.driver.find_element(By.ID, "execImportacao")
        self.click(el)

        # recupera status da importacao
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '(//table[@id="statusImportacao"]//tr)[2]')))
        except TimeoutException:
            pass
        el = self.driver.find_element(By.ID, "statusImportacao")
        html = el.get_attribute("outerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select("tr")
        captions = [str(col.string) for col in rows[0].find_all("th")]
        retorno = []
        for row in rows[1:]:
            cols = [str(col.string) for col in row.find_all("td")]
            retorno.append(dict(zip(captions, cols)))
        return retorno
    
    def gerar_relatorio_totalizadores(self, tipo_evento:str, ano_apur:int,
                                     mes_apur:int, ind_apur:str):
        self.go_relatorios_totalizadores()
        self.select('tipoEvento', tipo_evento, ignore_if_none=True, by_text=True)
        self.select('mesPerApur', mes_apur, ignore_if_none=True, by_text=False)
        self.select('anoPerApur', ano_apur, ignore_if_none=True, by_text=True)
        self.select('indApuracao', ind_apur, ignore_if_none=True, by_text=True)

        el = self.driver.find_element(By.NAME, "Filtrar")
        el.click()

    def handle_modal_confirmacao(self, confirmar:bool,
                                 timeout_msg='Modal de confirmação não encontrada!',
                                 ):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "div-modal-confirmacao")))
        except TimeoutException:
            raise MrhException(timeout_msg)
        el = self.driver.find_element(By.CSS_SELECTOR, "div.modal")
        msg = el.text.strip()
        if confirmar:
            el = self.driver.find_element(By.ID, "btn-confirmacao-sim")
            el.click()
        else:
            el = el.find_element(By.CSS_SELECTOR, "btn.fechar")
            el.click()

    def handle_modal_informacao(self, timeout_msg='Modal de informação não encontrada!',
                                fechar=True):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "modal-informacao-msg")))
        except TimeoutException:
            raise MrhException(timeout_msg)
        el = self.driver.find_element(By.ID, "modal-informacao-msg")
        msg = el.text.strip()
        if fechar:
            el = self.driver.find_element(By.CSS_SELECTOR, ".btn.fechar")
            self.click(el)
        return msg
    
    def importar_eventos_folha(self, vigencia:datetime.date|str, evento, ind_apur,
        matricula=None, cpf=None):

        self.go_trabalhador_folha_pagamento()
        self.fill('dtVigencia', vigencia2str(vigencia), tab=True) 
        self.select('sltEvento', evento, ignore_if_none=True, by_text=True)
        self.select('indApuracao', ind_apur, ignore_if_none=True, by_text=True)
        self.fill('matricula', matricula, ignore_if_none=True)
        self.fill('cpf ', cpf, ignore_if_none=True)

        el = self.driver.find_element(By.ID, "importar")
        self.click(el)

        self.handle_modal_confirmacao(
            True, 
            timeout_msg="Timeout enquanto importava"
            " eventos de folha do eSocial.")
        return self.handle_modal_informacao(
            timeout_msg="Timeout enquanto aguardava resultados de "
                    "importação de eventos de folha do eSocial.")

    def recuperar_tabela_trabalhador(self):
        # TODO: goto and filter (same as importe_eventos_folha)?
        el = self.driver.find_element(By.ID, "tabelaTrabalhador")
        html = el.get_attribute("outerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select("tr")
        if len(rows)==2:
            if rows[1].text.strip() == "Nenhum Registro Encontrado":
                return {}
        captions = [str(col.string) for col in rows[0].find_all("th")]
        retorno = []
        for row in rows[1:]:
            cols = [str(col.string) for col in row.find_all("td")]
            retorno.append(dict(zip(captions, cols)))
        return retorno
