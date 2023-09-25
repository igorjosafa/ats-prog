# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import config
from . import Mrh
from .exceptions import MrhException


class PortalUsuarios(Mrh):
 
    def registrar(self, cpf, senha, expira=False):
        self.go_portal_usuarios()

        self.fill("pessoaCpf", cpf, tab=True)
 
        def check_registered():
            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                    'Timed out waiting for alert')
                alert = self.driver.switch_to.alert
                alert.dismiss()
            except TimeoutException:
                return False
            return True
 
        if check_registered():
            self.driver.find_element(By.LINK_TEXT, config.PORTAL_INCLUIR).click()
            self.fill("cpf", cpf, tab=True)
            self.fill("senha", senha)
            self.fill("contraSenha", senha)
            self.check("nuncaExpira", not expira)
            self.driver.find_element(By.NAME, "Submit").click()
 
            msg = self.driver.find_element(By.ID, "divMessage")
            klasses = (msg.get_attribute("class") or "").split(" ")
            if "successMessage" in klasses:
                return True
            else:
                raise MrhException(msg.text)
        else:
            return False
