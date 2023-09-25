import datetime
import time
from pydantic import constr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .. import Mrh
from ..exceptions import MrhException


def fmt_date(date) -> str | None:
    if date:
        return date.strftime('%d%m%Y')


class MrhCadFunpresp(Mrh):
    
    MrhException = MrhException

    def incluir_servidor(self, matricula, data_inicio:datetime.date=None,
        data_fim:datetime.date=None, percentual:float=8.5, plano:int=1):
        self.go_funpresp_cadastro()
        self.fill('servMatr', str(matricula), tab=True)
        time.sleep(1) # TODO: wait properly
        el = self.driver.find_element(By.NAME, 'servNome')
        if not el.get_attribute('value'):
            raise MrhException('Servidor não cadastrado: {}'.format(matricula))
        el = self.driver.find_element(By.LINK_TEXT, "Incluir")
        el.click()
        self.fill('dtIni', fmt_date(data_inicio), ignore_if_none=True)
        self.fill('dtFim', fmt_date(data_fim), ignore_if_none=True)
        if percentual is not None:
            self.fill('percentual', "{:.2f}".format(percentual).replace('.', ''))
        self.select('planoFunpresp', str(plano), ignore_if_none=True)

        self.driver.find_element(By.NAME, "Submit").click()

        msg = self.handle_alert()
        if 'com sucesso' in msg:
            return
        else:
            raise MrhException(msg)
