import pandas as pd
import numpy as np
import re
TETO = 37589.95

def acerta_ferias_ats(matriculas_ats, matriculas_ferias, bases):

    bases_ats = bases[bases['Matricula'].apply(lambda x: x in matriculas_ats.values)]
    bases_ats_ferias = bases_ats[bases_ats['Matricula'].apply(lambda x: x in matriculas_ferias.values)]
    bases_ats_ferias = bases_ats_ferias[['Matricula', 'R1028_Antiga', 'R1028_Nova', 'R1013_Antiga', 'R1014_Antiga']]

    ferias_acertadas = bases_ats_ferias
    ferias_acertadas['R1013_Ajustada'] = np.where(ferias_acertadas['R1013_Antiga'].astype(float) > 0.0, np.trunc((ferias_acertadas['R1028_Nova'] - ferias_acertadas['R1028_Antiga'])*100/3)/100, ferias_acertadas['R1013_Antiga'])
    ferias_acertadas['R1013_Ajustada'] = np.where((ferias_acertadas['R1013_Antiga'].astype(float) + ferias_acertadas['R1013_Ajustada'].astype(float) > TETO/3), np.trunc((TETO/3 - ferias_acertadas['R1013_Antiga'].astype(float))*100)/100, ferias_acertadas['R1013_Ajustada'])
    ferias_acertadas['R1014_Ajustada'] = np.where(ferias_acertadas['R1014_Antiga'].astype(float) > 0.0, np.trunc((ferias_acertadas['R1028_Nova'] - ferias_acertadas['R1028_Antiga'])*133.33/3)/100, ferias_acertadas['R1014_Antiga'])
    ferias_acertadas['R1014_Ajustada'] = np.where((ferias_acertadas['R1014_Antiga'].astype(float) + ferias_acertadas['R1014_Ajustada'].astype(float) > 1.3333*TETO/3), np.trunc((1.3333*TETO/3 - ferias_acertadas['R1014_Antiga'].astype(float))*100)/100, ferias_acertadas['R1014_Ajustada'])

    log = open('log.txt', 'a+')
    log.write('\n-----SERVIDORES COM FERIAS MARCADAS E MUDANCA DE ATS, MAS SEM 1013 E 1014 NA FOLHA NORMAL-----\n')
    for index, row in ferias_acertadas[ferias_acertadas['R1013_Antiga'].astype(float) < 1].iterrows():
        log.write('\n')
        linha = row
        log.write(f"{linha}\n")

    log.write('\n-----SERVIDORES COM FERIAS MARCADAS E MUDANCA DE ATS, MAS JÁ NO TETO DO 1013 E 1014-----\n')
    for index, row in ferias_acertadas[TETO/3 - ferias_acertadas['R1013_Antiga'].astype(float) < 1].iterrows():
        log.write('\n')
        linha = row
        log.write(f"{linha}\n")
    log.close()

    return ferias_acertadas
    

def acerta_ferias_progressao(matriculas_progressao, matriculas_ferias, bases):
    

    bases_progressao = bases[bases['Matricula'].apply(lambda x: x in matriculas_progressao.values)]
    bases_progressao_ferias = bases_progressao[bases_progressao['Matricula'].apply(lambda x: x in matriculas_ferias.values)]
    bases_progressao_ferias = bases_progressao_ferias[['Matricula', 'R1002_Antiga', 'R1007_Antiga', 'R1028_Antiga', 'R1170_Antiga', 'R1013_Antiga', 'R1014_Antiga', 'R1002_Nova', 'R1007_Nova', 'R1028_Nova', 'R1170_Nova']]

    ferias_acertadas = bases_progressao_ferias
    ferias_acertadas['R1013_Ajustada'] = np.where(ferias_acertadas['R1013_Antiga'].astype(float) > 0.0, np.trunc((ferias_acertadas['R1002_Nova'] + ferias_acertadas['R1007_Nova'] + ferias_acertadas['R1028_Nova'] + ferias_acertadas['R1170_Nova'] - ferias_acertadas['R1002_Antiga'] - ferias_acertadas['R1007_Antiga'] - ferias_acertadas['R1028_Antiga'] - ferias_acertadas['R1170_Antiga'])*100/3)/100, ferias_acertadas['R1013_Antiga'])
    ferias_acertadas['R1013_Ajustada'] = np.where((ferias_acertadas['R1013_Antiga'].astype(float) + ferias_acertadas['R1013_Ajustada'].astype(float) > TETO/3), np.trunc((TETO/3 - ferias_acertadas['R1013_Antiga'].astype(float))*100)/100, ferias_acertadas['R1013_Ajustada'])
    ferias_acertadas['R1014_Ajustada'] = np.where(ferias_acertadas['R1014_Antiga'].astype(float) > 0.0, np.trunc((ferias_acertadas['R1002_Nova'] + ferias_acertadas['R1007_Nova'] + ferias_acertadas['R1028_Nova'] + ferias_acertadas['R1170_Nova'] - ferias_acertadas['R1002_Antiga'] - ferias_acertadas['R1007_Antiga'] - ferias_acertadas['R1028_Antiga'] - ferias_acertadas['R1170_Antiga'])*133.33/3)/100, ferias_acertadas['R1014_Antiga'])
    ferias_acertadas['R1014_Ajustada'] = np.where((ferias_acertadas['R1014_Antiga'].astype(float) + ferias_acertadas['R1014_Ajustada'].astype(float) > 1.3333*TETO/3), np.trunc((1.3333*TETO/3 - ferias_acertadas['R1014_Antiga'].astype(float))*100)/100, ferias_acertadas['R1014_Ajustada'])
    
    log = open('log.txt', 'a+')
    log.write('\n-----SERVIDORES COM FERIAS MARCADAS E MUDANCA DE PADRAO, MAS SEM 1013 E 1014 NA FOLHA NORMAL-----\n')
    for index, row in ferias_acertadas[ferias_acertadas['R1013_Antiga'].astype(float) < 1].iterrows():
        log.write('\n')
        linha = row
        log.write(f"{linha}\n")


    log.write('\n-----SERVIDORES COM FERIAS MARCADAS E MUDANCA DE PADRAO, MAS JÁ NO TETO DO 1013 E 1014-----\n')
    for index, row in ferias_acertadas[TETO/3 - ferias_acertadas['R1013_Antiga'].astype(float) < 1].iterrows():
        log.write('\n')
        linha = row
        log.write(f"{linha}\n")

    log.close()

    return ferias_acertadas