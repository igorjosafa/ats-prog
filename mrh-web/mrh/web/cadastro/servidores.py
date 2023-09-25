from pydantic import constr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .. import Mrh
from ..exceptions import MrhException
from .models import Servidor


def fmt_date(date) -> str | None:
    if date:
        return date.strftime('%d%m%Y')


class MrhServidor(Mrh):
    def incluir_servidor(self, matricula, cpf, dados):
        raise NotImplementedError()
