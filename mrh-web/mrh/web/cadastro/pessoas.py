from pydantic import constr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .. import Mrh
from ..exceptions import MrhException
from .models import Pessoal, Documentacao


def fmt_date(date) -> str | None:
    if date:
        return date.strftime('%d%m%Y')


class MrhPessoa(Mrh):
    def incluir_pessoa(self, cpf: constr, pessoal: Pessoal, documentacao: Documentacao):
        self.go_cadastro_pessoas()
        self.driver.find_element(By.LINK_TEXT, "Incluir").click()

        self.fill('cpf', cpf)
        self.preencher_dados_pessoais1(pessoal)
        
        self.driver.find_element(By.ID, "td_pessoais2").click()
        self.preencher_dados_pessoais2(pessoal)

        self.driver.find_element(By.ID, "td_documentacao").click()
        # todo: preencher Documentacao
       
        self.driver.find_element(By.ID, "td_pispasep").click()
        # todo: preencher PIS/FGTS

        self.driver.find_element(By.NAME, "Submit").click()
        self.handle_div_message()

    def editar_pessoa(self, cpf, pessoal: Pessoal, documentacao: Documentacao):
        raise NotImplementedError

    def preencher_dados_pessoais1(self, pessoal: Pessoal):

        self.driver.execute_script("$('.mascData').datepicker('remove');")

        self.fill('NomeRegistro', pessoal.nome_registro, ignore_if_none=True)
        self.fill('NomeSocial', pessoal.nome_registro, ignore_if_none=True)
        self.fill('nomePersonalizado', pessoal.nome_personalizado, ignore_if_none=True)

        if pessoal.data_nascimento is not None: # avoid date-picker hanging loose
            self.fill('dataNascimento', fmt_date(pessoal.data_nascimento), tab=True)

        if pessoal.data_obito is not None: # avoid date-picker hanging loose
            self.fill('dataObito', fmt_date(pessoal.data_obito), tab=True)

        if pessoal.sexo:
            self.select('sexo', str(pessoal.sexo.value), ignore_if_none=True)

        self.fill('idade', pessoal.idade, ignore_if_none=True)

        if pessoal.estado_civil:
            self.select('estadoCivil', str(pessoal.estado_civil.value))

        self.select_radio('uniaoEstavel', pessoal.uniao_estavel)

        self.fill('cep', pessoal.endereco_cep, tab=True, ignore_if_none=True)
        self.handle_div_message(timeout=2, timeout_ok=True) # todo: handle cep nao encontrado?

        self.fill('complemento', pessoal.endereco_complemento)
        self.fill('numero', pessoal.endereco_numero, ignore_if_none=True)

        self.fill('telefone', pessoal.telefone, ignore_if_none=True)
        self.fill('celular', pessoal.celular, ignore_if_none=True)

        self.fill('email', pessoal.email, ignore_if_none=True)

        self.fill('nomePai', pessoal.pai, ignore_if_none=True)
        self.fill('nomeMae', pessoal.mae, ignore_if_none=True)
        self.fill('nomeConjuge', pessoal.conjuge, ignore_if_none=True)
        if pessoal.data_casamento is not None: # avoid date-picker hanging loose
            self.fill('dataCasamento', fmt_date(pessoal.data_casamento), tab=True)

    def preencher_dados_pessoais2(self, pessoal: Pessoal):
        pass # todo
