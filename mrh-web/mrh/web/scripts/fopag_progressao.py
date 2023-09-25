import argparse
from datetime import datetime
import calendar
import os
import sys
import logging
logger = logging.getLogger(__file__)
from mrh.web.fopag.ats_prog import MrhDocumentos
import time

def fopag_progressao(usuario:str, senha:str, data_limite:datetime, download_dir = ''):
    if download_dir == '':
        download_dir=os.path.join(os.getcwd(), f'PROGRESSAO - {data_limite.month}-{data_limite.year}')

    m = MrhDocumentos(download_dir=download_dir)
    ocorreu_excecao = False

    try:
        m.login(usuario, senha)

        #seleciona a folha normal
        folha_ok = m.selecionar_folha(data_limite.month, data_limite.year, 1) is not None
        if not folha_ok:
            logger.warning("Falha na seleção da folha: {:02}/{}.{:03}".format(
                data_limite.month, data_limite.year, 1))
            sys.exit(1)

        #gera progressao com codicao 259 - FOLHA - SERVIDORES CONCURSADOS (Ativos e Cedidos)
        arquivo, fid = m.gerar_progressao(condicao = 259, data_limite='{:02}{:02}{}'.format(data_limite.day, data_limite.month, data_limite.year))

        #exporta csv das progressoes
        m.exportar_relatorio(titulo=None, tipo=7, fname=arquivo+'.csv', fid = fid)

        #gera relatório CSV para comparação
        relatorio = 'PROGRESSAO FUNCIONAL (oficial)'
        argumentos_p = {'p1': '{:02}'.format(data_limite.month), 'p2': '{}'.format(data_limite.year)}
        m.executar_sql(nome_consulta=relatorio, titulo=arquivo, fname=arquivo+' SQL.pdf', **argumentos_p)
        m.exportar_relatorio(titulo=None, tipo=7, fname=arquivo+' SQL.csv')

        m.efetivar_progressao()

    finally:
        m.close()

    return ocorreu_excecao

def main():
    parser = argparse.ArgumentParser(
        "fopag-progressao",
        description="Script para geração mensal de progressão",
        )
    parser.add_argument('--usuario', help="default: $MRH_USER (env_var)")
    parser.add_argument('--senha', help="default: $MRH_PASSWORD (env_var)")    
    parser.add_argument('mes', type=int, help="mes da folha normal")
    parser.add_argument('ano', type=int, help="ano da folha normal")
    args = parser.parse_args()

    usuario = args.usuario or os.getenv('MRH_USER')
    senha = args.senha or os.getenv('MRH_PASSWORD')

    data_limite = datetime(day = calendar.monthrange(args.ano, args.mes)[1], month=args.mes, year=args.ano)

    erro = fopag_progressao(
        usuario=usuario, senha=senha,
        data_limite=data_limite
        )

    sys.exit(int(erro))

if __name__ == '__main__':
    main()