from enum import Enum
from pydantic import BaseModel, condate, conint, constr
from typing import Literal, ClassVar


class Sexo(Enum):
    FEMININO = 1
    MASCULINO = 2

class EstadoCivil(Enum):
    SOLTEIRO = 1
    CASADO = 2
    SEPARADO = 3
    DIVORCIADO = 4
    VIUVO = 5
    UNIAO_ESTAVEL = 6
    OUTROS = 7

class RGTipo(Enum):
    CIVIL = 1
    MILITAR = 2
    OAB = 3

class UF(Enum):
    AL = 2
    AC = 1
    AM = 3
    AP = 4
    BA = 5
    CE = 6
    DF = 7
    EN = 8
    ES = 9
    GO = 11
    MA = 12
    MG = 13
    MS = 14
    MT = 15
    PA = 16
    PB = 17
    PE = 18
    PI = 19
    PR = 20
    RJ = 21
    RN = 22
    RO = 23
    RR = 24
    RS = 25
    SC = 26
    SE = 27
    SP = 28
    TO = 29

class Pessoal(BaseModel):
    Sexo: ClassVar = Sexo
    EstadoCivil: ClassVar = EstadoCivil

    nome_registro: constr() | None = None
    nome_social: constr() | None = None
    nome_personalizado: constr() | None = None
    data_nascimento: condate() | None = None
    data_obito: condate() | None = None
    sexo: Sexo | None = None
    idade: conint() | None = None
    estado_civil: EstadoCivil | None = None
    uniao_estavel: bool | None = None
    endereco_cep: constr() | None = None
    #endereco_pais = 
    endereco_numero: constr() | None = None
    endereco_bairro: constr() | None = None
    endereco_complemento: constr() | None = None
    endereco_municipio: conint() | None = None
    telefone: constr() | None = None
    celular: constr() | None = None
    email: constr() | None = None
    pai: constr() | None = None
    mae: constr() | None = None
    conjuge: constr() | None = None
    data_casamento: condate() | None = None

    escolaridade: constr() | None = None
    graduacao: constr() | None = None
    pos_graduacao: constr() | None = None

    raca: constr() | None = None
    cor: constr() | None = None
    doador_orgao: bool | None = None
    doador_sangue: bool | None = None

    #portador_deficiencia_rais
    # tipo_sanguineo

    naturalidade: conint() | None = None
    nacionalidade: constr() | None = None
    pais_nascimento: constr() | None = None

    # data_primeiro_emprego
    # referencia_nome
    # referencia_telefone
    # referencia_parentesco

    # data_provavel_admissao
    # portador_deficiencia_esocial


class Documentacao(BaseModel):
    UF: ClassVar = UF
    RGTipo: ClassVar = RGTipo

    rg_tipo: RGTipo | None = None
    rg_numero: constr() | None = None
    rg_orgao: constr() | None = None
    rg_uf: UF | None = None
    rg_expedicao: condate() | None = None

    cmil_numero: constr() | None = None
    cmil_categoria: constr() | None = None
    cmil_regiao: constr() | None = None
    cmil_expedicao: condate() | None = None
    cmil_emissor: constr() | None = None
    cmil_serie: constr() | None = None

    rp_numero: constr() | None = None
    rp_registro: constr() | None = None
    rp_regiao: constr() | None = None
    rp_uf: UF | None = None
    rp_expedicao: condate() | None = None
    rp_validade: condate() | None = None
    rp_emissor: constr() | None = None
    #rp_emissor_outros: 

    eleitor_numero: constr() | None = None
    eleitor_zona: constr() | None = None
    eleitor_secao: constr() | None = None
    eleitor_uf: UF | None = None
    eleitor_expedicao: condate() | None = None
    #eleitor_situacao: 

    cnh_numero: constr() | None = None
    cnh_categoria: constr() | None = None
    cnh_registro: constr() | None = None
    cnh_expedicao: condate() | None = None
    cnh_validade: condate() | None = None
    cnh_1a_habilitacao: condate() | None = None
    cnh_uf: UF | None = None

    nit: constr() | None = None


class Servidor(BaseModel):
    regime_juridico: int | None = None
    data_regime_juridico: condate() | None = None
    tipo_servidor: int | None = None
    email_institucional: str | None = None
    usuario_ldap: str | None = None
    categoria_trabalhador: int | None = None
    indicativo_provimento: int | None = None
    plano_segregacao_massa: int | None = None
    observacoes: str | None = None

    possui_decisao_judicial: bool | None = None
    possui_acumulacao: bool | None = None
    menor_aprendiz: bool | None = None
    trabalhador_temporario: bool | None = None

    calcula_folha: bool | None = None
    data_onus: condate() | None = None
    data_suspensao_pagamento: condate() | None = None
    ats: int | None = None
    regime_previdenciario: int | None = None
    ir_op_calculo: int | None = None
    horario: int | None = None
    jornada_clt: int | None = None
    tipo_contrato: int | None = None
    indicativo_teto_rgps: bool | None = None
    data_isencao_irpf: condate() | None = None
    data_laudo_irpf: condate() | None = None

    rais_tipo_salario: int | None = None
    rais_tipo_admissao: int | None = None
    rais_vinculo: int | None = None
    rais_situacao: int | None = None
    rais_desligamento: int | None = None

    banco: int | None = None
    agencia: int | None = None
    operacao: str | None = None
    conta: str | None = None
    conta_dv: str | None = None
