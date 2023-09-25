# coding: utf-8 -*-

import argparse
import datetime
import logging
logger = logging.getLogger(__file__)
import os
import os.path
import sys
import yaml
from yaml.loader import SafeLoader as SafeYamlLoader

from mrh.web.fopag.documentos import MrhDocumentos


def fopag_sql(usuario:str, senha:str, destino:str, csv:bool, arquivo:str, relatorio:str, argumentos_p:dict):
    
    logger.info("Pasta de destino:", destino)

    m = MrhDocumentos(download_dir=destino)

    try:
        m.login(usuario, senha)
        m.executar_sql(nome_consulta=relatorio, titulo=arquivo, fname=arquivo+'.pdf', **argumentos_p)
        m.exportar_relatorio(titulo=None, tipo=7, fname=arquivo+'.csv')

    finally:
        m.close()

    return

    
def main():
    parser = argparse.ArgumentParser(
        "fopag-sql",
        description="Gera relatórios de consultas SQL"
    )

    parser.add_argument('--usuario', help="default: $MRH_USER (env_var)")
    parser.add_argument('--senha', help="default: $MRH_PASSWORD (env_var)")
    parser.add_argument('--csv', help="utilizar para gerar arquivos em csv; default = False")
    parser.add_argument('--destino', help="pasta de destino; default: SQL")
    parser.add_argument('--arquivo', help="nome final do arquivo no destino")
    parser.add_argument('--relatorio', help="nome do relatorio no mentorh seguido dos argumentos")

    args = parser.parse_args()

    # Acesse os argumentos passados após --relatorio como uma única string
    if args.relatorio:
        args_relatorio = args.relatorio.split()
        argumentos_p = {}
        
        # Verifique se há argumentos após --relatorio
        if len(args_relatorio) > 1:
            relatorio = args_relatorio[0]
            outros_argumentos = args_relatorio[1:]

            for i, argumento in enumerate(outros_argumentos):
                argumentos_p['p{}'.format(i+1)] = argumento

    # Agora, você pode processar os argumentos conforme necessário na sua lógica de script.

    usuario = args.usuario or os.getenv('MRH_USER')
    senha = args.senha or os.getenv('MRH_PASSWORD')
    arquivo = args.arquivo

    if args.destino:
        destino = args.destino
    else:
        destino = os.path.join(
            os.getcwd(),
            'SQL')
    
    if args.csv:
        csv = True
    else:
        csv = False


    erro = fopag_sql(
        usuario=usuario, senha=senha,
        destino=destino,
        csv=csv,
        arquivo=arquivo,
        relatorio=relatorio,
        argumentos_p=argumentos_p
        )

    sys.exit(int(erro))


if __name__ == '__main__':
    main()