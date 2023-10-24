import pandas as pd
import numpy as np
import re

def le_ats_gerados_mentorh(mes, ano):
    df = pd.read_csv('.\\ATS - {}-{}\\ats gerados - {:02}-{}.csv'.format(mes, ano, mes, ano), names=range(12), delimiter=';')
    df_ats_mentorh = pd.DataFrame()
    df_ats_mentorh['Nome'] = [nome[:-8] for indice, nome in enumerate(df[1]) if indice%6 == 0]
    df_ats_mentorh['Matricula'] = [int(matricula[-5:]) for indice, matricula in enumerate(df[1]) if indice%6 == 0]
    adicionais_anteriores = [re.findall('\d+', adicional[-4:-2]) for indice, adicional in enumerate(df[1]) if (indice-2) >= 0 and (indice-2)%6==0]
    df_ats_mentorh['ATS anterior'] = [int(adicional[0]) if len(adicional) > 0 else 0 for adicional in adicionais_anteriores]
    df_ats_mentorh['ATS novo'] = [int(adicional[:-2]) for indice, adicional in enumerate(df[8]) if (indice-4) >= 0 and (indice-4)%6==0]
    df_ats_mentorh['Diferenca ATS'] = df_ats_mentorh['ATS novo'] - df_ats_mentorh['ATS anterior']
    return df_ats_mentorh

def pulou_mais_de_um(df):
    log = open('log.txt', 'a+')
    log.write('\n-----SERVIDORES QUE O ATS AUMENTOU MAIS DE 1%-----\n')
    for index, row in df[df['Diferenca ATS'] > 1].iterrows():
        log.write('\n')
        linha = row
        log.write(f"{linha}\n")
    log.close()

def matriculas_para_incluir_ats(df, mes, ano):
    log = open('log.txt', 'a+')
    log.write('\n-----SERVIDORES QUE O MENTORH NÃO GEROU ATS-----\n')
    df_SQL = pd.read_csv('.\\ATS - {}-{}\\ats gerados - {:02}-{} SQL.csv'.format(mes, ano, mes, ano), delimiter=';')
    df_SQL['Matricula'] = df_SQL['Matricula'].astype(int)
    df_SQL = df_SQL[df_SQL['Ultimo_Ano'] != ano]
    df_SQL['Novo_Inicio'] = df_SQL['Novo_Inicio'].apply(lambda x: int(str(x)[-7:-5]) if len(str(x))>1 else mes)
    matriculas_SQL_fora_do_mentorh = df_SQL[df_SQL['Novo_Inicio'] == mes]
    matriculas_SQL_fora_do_mentorh = matriculas_SQL_fora_do_mentorh[matriculas_SQL_fora_do_mentorh['Matricula'].apply(lambda x: x not in list(df['Matricula']))]
    if len(matriculas_SQL_fora_do_mentorh) > 0:
        for index, row in matriculas_SQL_fora_do_mentorh.iterrows():
            log.write('\n')
            linha = row
            log.write(f"{linha}\n")
        log.close()
        return matriculas_SQL_fora_do_mentorh['Matricula']
    else:
        log.close()
        matriculas_SQL_fora_do_mentorh['Matricula'] = []
        return matriculas_SQL_fora_do_mentorh['Matricula']

def matriculas_para_tirar_ats(df, mes, ano):
    log = open('log.txt', 'a+')
    log.write('\n-----SERVIDORES QUE O MENTORH NÃO CONSIDEROU OS AFASTAMENTOS-----\n')
    df_SQL = pd.read_csv('.\\ATS - {}-{}\\ats gerados - {:02}-{} SQL.csv'.format(mes, ano, mes, ano), delimiter=';')
    df_SQL['Matricula'] = df_SQL['Matricula'].astype(int)
    df_SQL['Novo_Inicio'] = df_SQL['Novo_Inicio'].apply(lambda x: int(str(x)[-7:-5]) if len(str(x))>1 else mes)
    matriculas_com_afastamento = df_SQL[df_SQL['Novo_Inicio'] != mes]
    matriculas_com_afastamento = matriculas_com_afastamento[matriculas_com_afastamento['Matricula'].apply(lambda x: x in list(df['Matricula']))]
    if len(matriculas_com_afastamento) > 0:
        for index, row in matriculas_com_afastamento.iterrows():
            log.write('\n')
            linha = row
            log.write(f"{linha}\n")
        log.close()
        return matriculas_com_afastamento['Matricula']
    else:
        log.close()
        matriculas_com_afastamento['Matricula'] = []
        return matriculas_com_afastamento['Matricula']