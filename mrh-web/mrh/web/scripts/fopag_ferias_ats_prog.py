import argparse
from datetime import datetime, timedelta
import calendar
import os
import sys
import logging
logger = logging.getLogger(__file__)
from mrh.web.fopag.ats_prog import MrhDocumentos
import time

def fopag_ferias(usuario:str, senha:str, data_inicio:datetime, data_fim:datetime, download_dir = ''):
    if download_dir == '':
        download_dir=os.path.join(os.getcwd(), f'FERIAS - {data_inicio.month}-{data_inicio.year}')

    m = MrhDocumentos(download_dir=download_dir)
    ocorreu_excecao = False

    try:
        m.login(usuario, senha)

        arquivo = f'FERIAS - {data_inicio.month}-{data_inicio.year}'

        parametros = {
            'Param1': '{:02}{:02}{}'.format(data_inicio.day, data_inicio.month, data_inicio.year),
            'Param2': '{:02}{:02}{}'.format(data_fim.day, data_fim.month, data_fim.year),
            'Param3': '1',
            'Param4': '99999',
            'Param5': '1',
            'Param6': '1',
            'Param7': '1',
            'Param8': '99'
            }

        #realiza consulta no explorador de dados
        m.executar_explorador_de_dados(nome_consulta='ESCALA  DE FÉRIAS (GERAL)', titulo=arquivo, fname=arquivo+'.pdf', **parametros)

        #gera relatório CSV para comparação
        m.exportar_relatorio(titulo=None, tipo=7, fname=arquivo+'.csv')

        #gera relatório CSV para comparação
        relatorio = 'Base_acerto_ferias_ATS_Progressao (oficial)'
        data_folha = data_inicio - timedelta(days=1)
        argumentos_p = {'p1': '{}'.format(data_folha.year), 'p2': '{}'.format(data_folha.month), 'p3': '{}'.format(data_inicio.year), 'p4': '{}'.format(data_inicio.month)}
        m.executar_sql(nome_consulta=relatorio, titulo=arquivo, fname=arquivo+' bases SQL.pdf', **argumentos_p)
        m.exportar_relatorio(titulo=None, tipo=7, fname=arquivo+' bases SQL.csv')

    finally:
        m.close()

    return ocorreu_excecao

def main():
    parser = argparse.ArgumentParser(
        "fopag-ferias-ats-progressao",
        description="Script para geração de relatório de férias para ATS e progressão",
        )
    parser.add_argument('--usuario', help="default: $MRH_USER (env_var)")
    parser.add_argument('--senha', help="default: $MRH_PASSWORD (env_var)")    
    parser.add_argument('mes', type=int, help="mes da folha normal sendo processada")
    parser.add_argument('ano', type=int, help="ano da folha normal sendo processada")
    args = parser.parse_args()

    usuario = args.usuario or os.getenv('MRH_USER')
    senha = args.senha or os.getenv('MRH_PASSWORD')

    data_inicio = datetime(day = calendar.monthrange(args.ano, args.mes)[1], month=args.mes, year=args.ano) + timedelta(days = 1)
    data_fim = datetime(day = calendar.monthrange(data_inicio.year, data_inicio.month)[1], month=data_inicio.month, year=data_inicio.year)

    erro = fopag_ferias(
        usuario=usuario, senha=senha,
        data_inicio=data_inicio,
        data_fim=data_fim
        )

    sys.exit(int(erro))

if __name__ == '__main__':
    main()