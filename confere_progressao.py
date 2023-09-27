import pandas as pd
import numpy as np
import re

def le_progressoes_geradas_mentorh(mes, ano):
    df = pd.read_csv('.\\PROGRESSAO - {}-{}\\progressoes geradas - {:02}-{}.csv'.format(mes, ano, mes, ano), names=range(8), delimiter=';')
    df_progressoes_mentorh = pd.DataFrame()
    df_progressoes_mentorh['Matricula'] = [int(matricula) for indice, matricula in enumerate(df[1]) if indice%2-1 == 0]
    df_progressoes_mentorh['Nome'] = [nome for indice, nome in enumerate(df[2]) if indice%2-1 == 0]
    df_progressoes_mentorh['Padrao Atual'] = [padrao for indice, padrao in enumerate(df[6]) if indice%2-1 == 0]
    df_progressoes_mentorh['Padrao Novo'] = [padrao for indice, padrao in enumerate(df[7]) if indice%2-1 == 0]
    return df_progressoes_mentorh

def matriculas_para_incluir_progressao(df, mes, ano):
    log = open('log.txt', 'a+')
    log.write('\n-----SERVIDORES QUE O MENTORH NÃO GEROU PROGRESSÃO-----\n')
    df_SQL = pd.read_csv('.\\PROGRESSAO - {}-{}\\progressoes geradas - {:02}-{} SQL.csv'.format(mes, ano, mes, ano), delimiter=';')
    df_SQL['Matricula'] = df_SQL['Matricula'].astype(int)
    fim_da_carreira = ['A69', 'B69', 'C54', 'D39', 'E24']
    matriculas_SQL_fora_do_mentorh = df_SQL[df_SQL['Matricula'].apply(lambda x: x not in list(df['Matricula']))]
    matriculas_SQL_fora_do_mentorh = matriculas_SQL_fora_do_mentorh[list(map(lambda x: x not in fim_da_carreira, matriculas_SQL_fora_do_mentorh['Padrao'].values))]
    if len(matriculas_SQL_fora_do_mentorh) > 0:
        for index, row in matriculas_SQL_fora_do_mentorh.iterrows():
            log.write('\n')
            linha = row
            log.write(f"{linha}\n")
    log.close()
    return matriculas_SQL_fora_do_mentorh['Matricula']

def matriculas_para_tirar_progressao(df, mes, ano):
    log = open('log.txt', 'a+')
    log.write('\n-----SERVIDORES QUE O MENTORH NÃO CONSIDEROU OS AFASTAMENTOS-----\n')
    df_SQL = pd.read_csv('.\\PROGRESSAO - {}-{}\\progressoes geradas - {:02}-{} SQL.csv'.format(mes, ano, mes, ano), delimiter=';')
    df_SQL['Matricula'] = df_SQL['Matricula'].astype(int)
    matriculas_mentorh_fora_do_SQL = df[df['Matricula'].apply(lambda x: x not in list(df_SQL['Matricula']))]
    if len(matriculas_mentorh_fora_do_SQL) > 0:
        for index, row in matriculas_mentorh_fora_do_SQL.iterrows():
            log.write('\n')
            linha = row
            log.write(f"{linha}\n")
    log.close()
    return matriculas_mentorh_fora_do_SQL['Matricula']