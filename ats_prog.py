import argparse
import pandas as pd
import re
from gera_ats_progressao import gera_ats, gera_progressao, gera_relatorio_ferias, gera_relatorio_bases
from confere_ats import le_ats_gerados_mentorh, pulou_mais_de_um, matriculas_para_tirar_ats, matriculas_para_incluir_ats
from confere_progressao import le_progressoes_geradas_mentorh, matriculas_para_tirar_progressao, matriculas_para_incluir_progressao
from acerta_ferias import acerta_ferias_ats, acerta_ferias_progressao
from gera_importacao import gera_arquivo_importacao
from datetime import datetime, timedelta
import numpy as np

def gera(mes, ano):
    gera_ats(mes, ano)
    gera_progressao(mes, ano)
    print("\nATS e progressões gerados.")
    print("Congele e recalcule a folha. Em seguida execute novamente o script a opção -c para conferir os lançamentos e calcular os acertos de férias.")

def confere_ats_gerados(mes, ano):
    df_ats_mentorh = le_ats_gerados_mentorh(mes, ano)
    matriculas_ats = df_ats_mentorh['Matricula']
    pulou_mais_de_um(df_ats_mentorh)
    matriculas_tirar_ats = matriculas_para_tirar_ats(df_ats_mentorh, mes, ano)
    matriculas_ats = matriculas_ats[matriculas_ats.apply(lambda x: int(x) not in matriculas_tirar_ats.values)]
    matriculas_incluir_ats = matriculas_para_incluir_ats(df_ats_mentorh, mes, ano)
    for value in matriculas_incluir_ats.values:
        matriculas_ats.at[len(matriculas_ats)+1] = value
    return matriculas_ats

def confere_progressoes_geradas(mes, ano):
    df_progressoes_mentorh = le_progressoes_geradas_mentorh(mes, ano)
    matriculas_progressao = df_progressoes_mentorh['Matricula']
    matriculas_tirar_progressao = matriculas_para_tirar_progressao(df_progressoes_mentorh, mes, ano)
    matriculas_progressao = matriculas_progressao[matriculas_progressao.apply(lambda x: x not in matriculas_tirar_progressao.values)]
    matriculas_incluir_progressao = matriculas_para_incluir_progressao(df_progressoes_mentorh, mes, ano)
    for value in matriculas_incluir_progressao.values:
        matriculas_progressao.at[len(matriculas_progressao)+1] = value
    return matriculas_progressao

def exclui_repetidos(matriculas_ats, matriculas_progressao):
    matriculas_ats = matriculas_ats[matriculas_ats.apply(lambda x: x not in matriculas_progressao.values)]
    return matriculas_ats

def acerta_ferias(mes, ano, matriculas_ats, matriculas_progressao):
    ferias = pd.read_csv('./FERIAS - {}-{}/FERIAS - {}-{}.csv'.format(mes, ano, mes, ano), delimiter=';')
    matriculas_ferias = ferias['Matr'][:-2].astype(int)
    matriculas_ferias

    bases = pd.read_csv('./relatorios/bases_ats_prog {}-{}.csv'.format(mes, ano), delimiter=';')
    bases['Matricula'] = bases['Matricula'].astype(int)

    ferias_acertadas_ats = acerta_ferias_ats(matriculas_ats, matriculas_ferias, bases)

    ferias_acertadas_progressao = acerta_ferias_progressao(matriculas_progressao, matriculas_ferias, bases)

    return ferias_acertadas_ats, ferias_acertadas_progressao

def incluir_matriculas_manualmente(matriculas, tipo):
    while True:
        matriculas_a_acrescentar = input(f"Caso haja lançamentos manuais de {tipo}, informe as matriculas separadas por ponto e virgula para conferência de férias.\nCaso não haja, pressione enter: ")
        if re.match('^(\d{5};{0,1})*$', matriculas_a_acrescentar):
            matriculas_a_acrescentar = matriculas_a_acrescentar.split(';')
            print("Matriculas a acrescentar: ", matriculas_a_acrescentar)
            if matriculas_a_acrescentar[0] != '':
                for matricula in matriculas_a_acrescentar:
                    matriculas.at[len(matriculas)+1] = int(matricula)
            return matriculas
        else:
            print("\nFormato inadequado. Insira novamente\n")

def confere_lancamentos_acerta_ferias(mes, ano):
    gera_relatorio_ferias(mes, ano)
    gera_relatorio_bases(mes, ano)
    matriculas_ats = confere_ats_gerados(mes, ano)
    matriculas_progressao = confere_progressoes_geradas(mes, ano)
    matriculas_progressao = incluir_matriculas_manualmente(matriculas_progressao, 'progressão')
    matriculas_ats = exclui_repetidos(matriculas_ats, matriculas_progressao)
    matriculas_ats = incluir_matriculas_manualmente(matriculas_ats, 'ATS')
    ferias_acertadas_ats, ferias_acertadas_progressao = acerta_ferias(mes, ano, matriculas_ats, matriculas_progressao)
    mes_ferias = datetime(day=1, month=mes, year=ano)
    mes_folha = mes_ferias - timedelta(days=2)
    gera_arquivo_importacao(ferias_acertadas_ats, ferias_acertadas_progressao, mes_folha.month, mes_folha.year)


def main():
    log = open('log.txt', 'w')
    log.close()
    parser = argparse.ArgumentParser(
        prog='ats-prog',
        description = "Gera ATS e Progressão na folha normal e os acertos de férias na folha complementar."
    )
    parser.add_argument('mes', type=int, help="mes da folha normal sendo processada")
    parser.add_argument('ano', type=int, help="ano da folha normal sendo processada")
    parser.add_argument('-g', '--gera', action='store_true', help='gera ats e progressão na folha normal')
    parser.add_argument('-c', '--confere', action='store_true', help='confere lançamentos e gera acerto de ferias. somente utilizar após ter utilizado a opção -g anteriormente nesta folha')
    args = parser.parse_args()

    if args.gera == True:
        mes = int(args.mes)
        ano = int(args.ano)
        if input("\n\nConfirma a geração de ATS e progressão para o mês {:02}/{}? Digite S para continuar ou qualquer outra tecla para sair...".format(mes, ano)).upper() == 'S':
            gera(mes, ano)

    elif args.confere == True:
        mes = int(args.mes)
        ano = int(args.ano)
        confere_lancamentos_acerta_ferias(mes, ano)

if __name__ == '__main__':
    main()