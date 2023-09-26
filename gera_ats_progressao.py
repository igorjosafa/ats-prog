from datetime import datetime, timedelta
import calendar
from mrh.web.scripts.fopag_ats import fopag_ats
from mrh.web.scripts.fopag_progressao import fopag_progressao
from mrh.web.scripts.fopag_ferias_ats_prog import fopag_ferias
from mrh.web.scripts.fopag_sql import fopag_sql
from dotenv import load_dotenv
import getpass
import os
TETO = 37589.95


def recebe_usuario_mentorh():
    load_dotenv('.env')
    usuario=os.environ.get('MENTORH_U')
    senha=os.environ.get('MENTORH_P')
    usuario=getpass("Digite o usuário do Mentorh: ") if usuario == None else usuario
    senha=getpass("Digite o usuário do Mentorh: ") if senha == None else senha
    return usuario, senha

def encontra_data_limite(mes, ano):
    dia = calendar.monthrange(year=ano, month=mes)[1]
    data_limite = datetime(day=dia, month=mes, year=ano)
    return data_limite

def gera_ats(mes, ano):
    usuario, senha = recebe_usuario_mentorh()
    data_limite = encontra_data_limite(mes, ano)
    fopag_ats(usuario=usuario, senha=senha, data_limite=data_limite)

def gera_progressao(mes, ano):
    usuario, senha = recebe_usuario_mentorh()
    data_limite = encontra_data_limite(mes, ano)
    fopag_progressao(usuario=usuario, senha=senha, data_limite=data_limite)

def gera_relatorio_ferias(mes, ano):
    usuario, senha = recebe_usuario_mentorh()
    mes_inicio = datetime(day=1,month=mes,year=ano)
    mes_fim = encontra_data_limite(mes, ano)
    fopag_ferias(usuario=usuario, senha=senha, data_inicio=mes_inicio, data_fim=mes_fim)

def gera_relatorio_bases(mes, ano):
    usuario, senha = recebe_usuario_mentorh()
    mes_anterior = datetime(day=1,month=mes,year=ano) - timedelta(days=2)
    fopag_sql(usuario=usuario, senha=senha, destino=os.path.join(os.getcwd(), 'relatorios'), csv = True, arquivo='bases_ats_prog {}-{}'.format(mes, ano), relatorio='Base_acerto_ferias_ATS_Progressao (oficial)', argumentos_p={'p1': mes_anterior.year, 'p2': mes_anterior.month, 'p3': ano, 'p4': mes})