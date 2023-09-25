import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import config

class Links:

    login_url = None

    def go_login(self, url=config.LOGIN_URL):
        self.login_url = url
        self.driver.get(self.login_url)

    def go_menu(self, menu):
        self.driver.switch_to.default_content()
        el = self.driver.find_element(By.XPATH, 
            '//li/a[text()="{}"]'.format(menu))
        self.driver.get(el.get_attribute("href"))
 
    def go_submenu(self, submenu):
        link = self.driver.find_element(By.LINK_TEXT, submenu)
        link.click()
 
    def go_content(self):
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                self.driver.find_element(By.ID, "frame1"))
        )
        
        WebDriverWait(self.driver, 10, 0.5, [NoSuchWindowException,]).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div"))
        )

    def go_home(self):
        self.driver.switch_to.default_content()
        el = self.driver.find_element(By.CSS_SELECTOR, "#homeMenu>a")
        el.click()

    def go_contracheque_servidor(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Contracheque Servidor").click()
        self.go_content()

    def go_previa_servidor(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Prévia Servidor").click()
        self.go_content()

    def go_contracheque_pa(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Contracheque P. Alimentícia").click()
        self.go_content()

    def go_email_contracheque(self):
        self.go_entidades_externas()
        self.driver.find_element(By.LINK_TEXT, "Email Contracheque").click()
        self.go_content()

    def go_elemento_despesa(self):
        self.go_relatorios_fechamento()
        link = self.driver.find_element(By.LINK_TEXT, "Elemento de Despesa")
        link.click()
        self.go_content()

    def go_entidades_externas(self):
        self.go_folha_pagamento()
        assert self.is_at_folha_pagamento()
        link = self.driver.find_element(By.LINK_TEXT, "Entidades Externas")
        link.click()

    def go_gera_arquivo_bancario(self):
        self.go_entidades_externas()
        self.driver.find_element(By.LINK_TEXT, "Gera Arquivo Bancário").click()
        time.sleep(0.1)
        self.go_content()

    def go_liquido_banco_agencia(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Líquido Banco/Agência").click()
        self.go_content()

    def go_liquidos_totalizadores(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Líquidos / Totalizadores").click()
        self.go_content()

    def go_relacao_consignatarias(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Relação de Consignatária").click()
        self.go_content()

    def go_resumo_geral(self):
        self.go_relatorios_fechamento()
        link = self.driver.find_element(By.LINK_TEXT, "Resumo Geral")
        link.click()
        self.go_content()

    def go_rubricas_calculadas(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Rubricas Calculadas").click()
        self.go_content()
   
    def go_folha_pagamento(self):
        self.driver.switch_to.default_content()
        el = self.driver.find_element(By.XPATH,
            '//li/a[text()="Folha de Pagamento"]')
        self.driver.get(el.get_attribute("href"))

    def go_relatorios_fechamento(self):
        self.go_folha_pagamento()
        assert self.is_at_folha_pagamento()
        link = self.driver.find_element(By.LINK_TEXT, "Relatórios de Fechamento")
        link.click()

    def go_selecao_folha(self):
        self.go_folha_pagamento()
        link = self.driver.find_element(By.LINK_TEXT, "Seleção de Folha")
        link.click()
        self.go_content()
    
    def go_relatorios_sql(self):
        self.go_menu(config.MENU_FERRAMENTAS)
        self.go_submenu(config.SUBMENU_RELATORIOS_SQL)
        self.go_content()

    def go_explorador_de_dados(self):
        self.go_menu(config.MENU_FERRAMENTAS)
        self.go_submenu('Explorador de Dados')
        self.go_content()

    def go_resumo_bases(self):
        self.go_relatorios_fechamento()
        self.driver.find_element(By.LINK_TEXT, "Resumo das Bases").click()
        self.go_content()

    def go_exporta_relatorios(self):
        self.go_menu(config.MENU_FERRAMENTAS)
        self.go_submenu(config.SUBMENU_EXPORTA_RELATORIOS)
        self.go_content()
    
    def go_portal_usuarios(self):
        self.go_menu(config.MENU_ADMINISTRACAO)
        self.go_submenu(config.SUBMENU_PARAMETRIZACAO_PORTAL)
        self.go_submenu(config.SUBMENU_PORTAL_USUARIOS)
        self.go_content()
      
    def get_modulo_heading(self):
        frm = self.driver.execute_script("return self.name")
        if frm:
            self.driver.switch_to.default_content()
        
        el = self.driver.find_element(By.CSS_SELECTOR, '.side-menu div.panel-heading')
        heading = el.text.strip()
        
        if frm:
            self.driver.switch_to.frame(frm)

        return heading
                
    def is_at_folha_pagamento(self):
        return self.get_modulo_heading() == 'Folha de Pagamento'

    def get_titulo_conteudo_paginas(self):
        el = self.driver.find_element(By.CSS_SELECTOR, '.tituloConteudoPaginas')
        return el.text.strip()

    def is_at_contracheque_servidor(self):
        return self.get_titulo_conteudo_paginas() == 'Contracheque Servidor'

    def is_at_previa_servidor(self):
        return self.get_titulo_conteudo_paginas() == 'Prévia do Servidor'

    def is_at_contracheque_pa(self):
        return self.get_titulo_conteudo_paginas() == 'Contracheque Pensão Alimentícia'

    def is_at_email_contracheque(self):
        return self.get_titulo_conteudo_paginas() == 'Envia Emails de Contracheques'

    def is_at_elemento_despesa(self):
        return self.get_titulo_conteudo_paginas() == 'Resumo por Elemento de Despesa'

    def is_at_entidades_externas(self):
        if self.is_at_folha_pagamento():
            link = self.driver.find_element(By.LINK_TEXT, "Entidades Externas")
            return link.get_attribute('aria-expanded') == "true"
        return False

    def is_at_gera_arquivo_bancario(self):
        return self.get_titulo_conteudo_paginas() == 'Gera Disquete Bancário'

    def is_at_liquido_banco_agencia(self):
        return self.get_titulo_conteudo_paginas() == 'Relação de Líquido Banco / Agência'

    def is_at_liquidos_totalizadores(self):
        return self.get_titulo_conteudo_paginas() == 'Relação de Líquidos / Totalizadores'

    def is_at_relacao_consignatarias(self):
        return self.get_titulo_conteudo_paginas() == 'Relação de Consignatárias'

    def is_at_resumo_geral(self):
        return self.get_titulo_conteudo_paginas() == 'Resumo Geral da Folha'

    def is_at_rubricas_calculadas(self):
        return self.get_titulo_conteudo_paginas() == 'Relação de Rubricas Calculadas'

    def is_at_relatorios_fechamento(self):
        if self.is_at_folha_pagamento():
            link = self.driver.find_element(By.LINK_TEXT, "Relatórios de Fechamento")
            return link.get_attribute('aria-expanded') == "true"
        return False

    def is_at_selecao_folha(self):
        return self.get_titulo_conteudo_paginas() == 'Seleção de Folha'

    def is_at_relatorios_sql(self):
        return self.get_titulo_conteudo_paginas() == 'Relatórios SQL'

    def is_at_exporta_relatorios(self):
        return self.get_titulo_conteudo_paginas() == 'Exporta Relatórios'

    def is_at_portal_usuarios(self):
        return self.get_titulo_conteudo_paginas() == 'Administração Usuário'

    # Dados Funcionais

    def go_cadastro_pessoas(self):
        self.go_menu('Dados Funcionais')
        self.go_submenu('Pessoas')
        self.go_submenu('Cadastro')
        self.go_content()

    def go_cadastro_servidores(self):
        self.go_menu('Dados Funcionais')
        self.go_submenu('Servidores')
        self.go_submenu('Cadastro')
        self.go_content()
    
    def go_cadastro_cargo_efetivo(self):
        self.go_menu('Dados Funcionais')
        self.go_submenu('Cargo Efetivo')
        self.go_submenu('Cadastro')
        self.go_content()

    def go_cadastro_cargo_funcao(self):
        self.go_menu('Dados Funcionais')
        self.go_submenu('Cargo/Função Comissionada')
        self.go_submenu('Titular/Interino')
        self.go_content()
    
    def go_cadastro_movimentacao(self):
        self.go_menu('Dados Funcionais')
        self.go_submenu('Movimentação')
        self.go_submenu('Movimentação')
        self.go_content()

    def go_calculo_efetivacao_ats(self):
        self.go_menu('Dados Funcionais')
        self.go_submenu('Adicional por Tempo de Serviço')
        self.go_submenu('Cálculo/Efetivação')
        self.go_content()

    def go_nivel_letra(self):
        self.go_menu('Dados Funcionais')
        self.go_submenu('Cargo Efetivo')
        self.go_submenu('Nível/Letra')
        self.go_content()

    # Registro Funcional

    def go_funpresp_cadastro(self):
        self.go_menu('Registro Funcional')
        self.go_submenu('Funpresp')
        self.go_submenu('Cadastro')
        self.go_content()