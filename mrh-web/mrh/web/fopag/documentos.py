# -*- coding: utf-8 -*-

import datetime
import time

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

    def gerar_elemento_despesa(self, condicao, tipoImpressao='1',
        tipoClassificacao="2", titulo=None, fname="Elemento de Despesa.pdf"):
      
        self.go_elemento_despesa()
        
        if condicao:
            self.executar_condicao(condicao)

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='tipoImpressao'][value='{}']".format(
                tipoImpressao)).click()

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='tipoClassificacao'][value='{}']".format(
                tipoClassificacao)).click()

        self.driver.find_element(By.LINK_TEXT, "Executar").click()

        self.handle_progress_bar()

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame1")

        if titulo is not None:
            cabecalho = self.get_especificacao_cabecalho()
            self.fill("especificacaoCabecalho", titulo.format(cabecalho=cabecalho))

        impressao_id = self._imprimir()
        self.save_file(fname)
        return impressao_id

    def gerar_liquido_banco_agencia(self, condicao, banco_impressao=None, 
        tipo_impressao="2", tipo_classificacao="2", gera_servidores=True,
        gera_pensao=True, gera_consignataria=True, titulo=None,
        fname="Liquido Banco Agencia.pdf"):

        self.go_liquido_banco_agencia()

        if condicao:
            self.executar_condicao(condicao)

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='tipoImpressao'][value='{}']".format(
                tipo_impressao)).click()

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='tipoClassificacao'][value='{}']".format(
                tipo_classificacao)).click()
        
        if banco_impressao is not None:
            self.select('bancoImpressao', banco_impressao)

        self.check("geraServidores", gera_servidores)
        self.check("geraPensao", gera_pensao)
        self.check("geraConsignataria", gera_consignataria)

        if titulo is not None:
            cabecalho = self.get_especificacao_cabecalho()
            self.fill("especificacaoCabecalho", titulo.format(cabecalho=cabecalho))

        el = self.driver.find_element(By.LINK_TEXT, "Executar")
        self.driver.execute_script("arguments[0].click();", el)

        alert = self.driver.switch_to.alert
        alert.dismiss()

        impressao_id = self._imprimir()
        self.save_file(fname)
        return impressao_id

    def gerar_liquidos_totalizadores(self, condicao, tipo_impressao="1",
        totalizadores=["Líquido", "Bruto", "Desconto"], matriculas=[], total0=False,
        titulo=None, fname="Liquidos Totalizadores.pdf"):

        self.go_liquidos_totalizadores()

        self.executar_ordenacao_com_condicao(condicao, matriculas=matriculas)

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame1")

        time.sleep(1)

        self.check("total0", total0)

        for tot in totalizadores:
            self.driver.find_element(By.CSS_SELECTOR,
                "input[type='checkbox'][value='{}']".format(tot)).click()

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='tipoImpressao'][value='{}']".format(
                tipo_impressao)).click()

        if titulo is not None:
            cabecalho = self.get_especificacao_cabecalho('cabecalho')
            self.fill("cabecalho", titulo.format(cabecalho=cabecalho))

        #TODO: self.processProgressBar() or handle alert
        impressao_id = self._imprimir()
        self.save_file(fname)
        return impressao_id
    
    def gerar_relacao_consignatarias(self, condicao, tipoImpressao="2",
        consignatariaInicial="1", consignatariaFinal="9999", titulo=None,
        fname="Relacao de Consignatarias.pdf"):
        
        self.go_relacao_consignatarias()

        if condicao:
            self.executar_condicao(condicao)
        
        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='tipoImpressao'][value='{}']".format(
                tipoImpressao)).click()

        self.fill("consignatariaInicial", consignatariaInicial, tab=True)
        self.fill("consignatariaFinal", consignatariaFinal, tab=True)

        self.driver.find_element(By.LINK_TEXT, "Executar").click()
        alert = self.driver.switch_to.alert
        alert.dismiss()

        if titulo is not None:
            cabecalho = self.get_especificacao_cabecalho()
            self.fill("especificacaoCabecalho", titulo.format(cabecalho=cabecalho))

        impressao_id = self._imprimir()
        self.save_file(fname)
        return impressao_id

    def gerar_resumo_geral(self, condicao, titulo=None, fname="Resumo Geral.pdf"):
        self.go_resumo_geral()

        if condicao:
            self.executar_condicao(condicao)

        self.driver.find_element(By.LINK_TEXT, "Executar").click()

        self.driver.switch_to.frame("ProgressBarFrame")
        bar = self.driver.find_element(By.CSS_SELECTOR, '.progress')
        while bar.text[:6] != "Conclu":
            time.sleep(0.1)
        self.driver.find_element(By.ID, "progressCloseButton").click()

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame1")

        if titulo is not None:
            cabecalho = self.get_especificacao_cabecalho()
            self.fill("especificacaoCabecalho", titulo.format(cabecalho=cabecalho))

        #self.driver.execute_script("imprimir()")
        impressao_id = self._imprimir()
        self.save_file(fname)
        return impressao_id
    
    def gerar_rubricas_calculadas(self, condicao, quebra_pagina="1",
        ordenacao_rubricas="1", ordenacao_servidores="1", titulo=None,
        fname="Rubricas Calculadas.pdf", rubricas=[], fatores=[]):

        self.go_rubricas_calculadas()

        if condicao:
            self.executar_condicao(condicao)

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='quebraPagina'][value='{}']".format(
                quebra_pagina)).click()

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='ordenacaoRubricas'][value='{}']".format(
                ordenacao_rubricas)).click()

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='ordenacaoServidores'][value='{}']".format(
                ordenacao_servidores)).click()

        if rubricas:
            rubs = ";".join(map(str, rubricas))
            self.fill('rubricasCodigos', rubs)

        if fatores:
            fats = ";".join(map(str, fatores))
            self.fill('fatores', fats)

        self.driver.find_element(By.LINK_TEXT, "Executar").click()
        self.handle_progress_bar()

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame1")

        if titulo is not None:
            cabecalho = self.get_especificacao_cabecalho()
            self.fill("cabecalho", titulo.format(cabecalho=cabecalho))

        time.sleep(1)
        impressao_id = self._imprimir(handle_alert=False)
        self.save_file(fname)
        return impressao_id

    def gerar_arquivo_bancario(self, condicao, data:datetime.date|str, banco, parametro,
        com_servidores=True, com_pensao=True, com_consignatarias=True,
        cnab240=False, path_arquivo='{default}creditos.txt', fname='creditos.txt'):
        """Gera Arquivo Bancário (Folha de Pagamento -> Entidades Externas -> Gera Arquivo Bancário)

        data: datetime.date | ddmmyyyy
        banco: BRB (6)
        parametro: Consignações (4) Folha Pagamento (2) PA (3)
        
        """

        self.go_gera_arquivo_bancario()

        if condicao:
            self.executar_condicao(condicao)

        if hasattr(data, 'strftime'):
            data = data.strftime('%d%m%Y')

        self.fill('data', data, tab=True)
        self.raise_if_alert(timeout=3)

        self.select('banco', str(banco))
        self.select('parametro', str(parametro))
        self.check('servidor', com_servidores)
        self.check('pensao', com_pensao)
        self.check('consignataria', com_consignatarias)
        self.select_radio('cnab240', "1" if cnab240 else "2")

        self.driver.find_element(By.LINK_TEXT, "Executar").click()

        self.handle_div_message(timeout=60 * 5)

        if path_arquivo is not None:
            default_path = self.driver.find_element(By.NAME, 'arquivo').get_attribute('value')
            self.fill('arquivo', path_arquivo.format(default=default_path))

        # numero de janelas para depois de gerar o arquivo
        wcount = len(self.driver.window_handles)
        main_window = self.driver.current_window_handle

        self.driver.execute_script("gravarArquivo()")

        self.raise_if_alert()

        # pula pra janela recem aberta
        while len(self.driver.window_handles) == wcount:
            time.sleep(0.1)
        self.driver.switch_to.window(self.driver.window_handles[wcount])

        # pega o link do arquivo
        el = self.driver.find_element(By.CSS_SELECTOR, 'a')
        el.click()

        try:
            el = self.driver.find_element(By.CSS_SELECTOR, 'pre')
        except NoSuchElementException:
            text = None
        else:
            text = el.text

        self.save_text(text or '', fname)

        # fecha popup e volta para janela anterior
        self.driver.close()
        self.driver.switch_to.window(main_window)

        return text

    def gerar_resumo_bases(self, condicao, base1, matriculas=[], tipo_impressao=1,
        base2=None, periodo_inicial=None, periodo_final=None, operacao=None, base1_compara="1", base1_valor=None,
        base2_compara="1", base2_valor=None, titulo=None, fname="resumo_bases.pdf"):
        """Resumo das Bases (Folha de Pagamento -> Relatórios de Fechamento -> Resumo das Bases)

        Opções de impressão: Sintético (1)  Analítico (2) Compara Bases (3)

        Tipo Impressão: + (1) - (2) * (3) / (4)

        Se condicao is None, será usada a condição ativa. ATENÇÃO: isso pode ser um erro de lógica!

        """

        self.go_resumo_bases()
        self.executar_ordenacao_com_condicao(condicao, matriculas=matriculas)

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame1")
        time.sleep(1)

        self.driver.find_element(By.CSS_SELECTOR,
            "input[type='radio'][name='tipoImpressao'][value='{}']".format(
                tipo_impressao)).click()

        self.driver.find_element(By.CSS_SELECTOR, "#tab12 a").click()

        if periodo_inicial:
            self.fill("periodoInicial", periodo_inicial)

        if periodo_final:
            self.fill("periodoFinal", periodo_final)

        if base1:
            self.fill("base1Codigo", str(base1), tab=True)

            if base1_compara:
                self.driver.find_element(By.CSS_SELECTOR,
                    "input[type='radio'][name='base2Compara'][value='{}']".format(
                        base1_compara)).click()

            if base2_valor:
                self.fill("base1Valor", str(base1_valor))

        if base2:
            self.fill("base2Codigo", str(base2), tab=True)
            
            if operacao:
                self.driver.find_element(By.CSS_SELECTOR,
                    "input[type='radio'][name='tipoOperacao'][value='{}']".format(
                        operacao)).click()

            if base2_compara:
                self.driver.find_element(By.CSS_SELECTOR,
                    "input[type='radio'][name='base2Compara'][value='{}']".format(
                        base2_compara)).click()

                if base2_valor:
                    self.fill("base2Valor", str(base2_valor))

        self.driver.find_element(By.LINK_TEXT, "Executar").click()
        self.handle_progress_bar()

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame1")

        if titulo is not None:
            cabecalho = self.get_especificacao_cabecalho()
            self.fill("cabecalho", titulo.format(cabecalho=cabecalho))

        time.sleep(1)
        impressao_id = self._imprimir()
        if fname:
            self.save_file(fname)
        return impressao_id
