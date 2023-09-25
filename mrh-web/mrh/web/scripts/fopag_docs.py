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


def parse_roteiro(path:str) -> dict:
    with open(path, 'rb') as f:
        data = yaml.load(f, Loader=SafeYamlLoader)
    # todo: validate
    return data


def gerar_arquivo_bancario(mrh, condicao:int, data, banco, parametro,
                           com_servidores=True, com_pensao=True,
                           com_consignatarias=True, cnab240=False):
    if isinstance(data, str) and '/' in data:
        data = datetime.datetime.strptime(data, '%d/%m/%Y')
    mrh.gerar_arquivo_bancario(condicao, data, banco,
                               parametro, com_servidores, com_pensao,
                               com_consignatarias, cnab240)


doc_meth = {
    'arquivo_bancario': 'gerar_arquivo_bancario',
    'resumo_geral': 'gerar_resumo_geral',
    'elemento_despesa': 'gerar_elemento_despesa',
    'relacao_consignatarias': 'gerar_relacao_consignatarias',
    'liquido_banco_agencia': 'gerar_liquido_banco_agencia',
    'liquidos_totalizadores': 'gerar_liquidos_totalizadores',
    'rubricas_calculadas': 'gerar_rubricas_calculadas',
}

def fopag_docs(usuario:str, senha:str, folha_ano:int, folha_mes:int,
         folha_seq:int, roteiro:str, destino:str, csv:bool):
    
    logger.info("Pasta de destino:", destino)
    roteiro = parse_roteiro(roteiro)

    m = MrhDocumentos(download_dir=destino)
    ocorreu_excecao = False

    try:
        m.login(usuario, senha)
        folha_ok = m.selecionar_folha(
            folha_mes, folha_ano, folha_seq) is not None
        if not folha_ok:
            logger.warning("Falha na seleção da folha: {:02}/{}.{:03}".format(
                folha_mes, folha_ano, folha_seq))
            sys.exit(1)
        for fname, args in roteiro["documentos"].items():
            if os.path.exists(os.path.join(destino, fname)):
                logger.info("Pulando arquivo existente: ", fname)
                continue
            meth_name = doc_meth[args['tipo']]
            if isinstance(meth_name, str):
                method = getattr(m, doc_meth[args['tipo']])
            else:
                method = meth_name(m)
            try:
                ret = method(fname=fname, **args.get('params', {}))
                if csv == True and meth_name != 'gerar_arquivo_bancario':
                    if not os.path.exists(os.path.join(destino, 'relatorios_csv')):
                        os.mkdir(os.path.join(destino, 'relatorios_csv'))
                    m.exportar_relatorio(titulo=None, tipo=7, fname=fname[:-4]+'.csv', fid = ret) #exportando relatórios em csv
                    os.replace(os.path.join(destino, fname[:-4]+'.csv'), os.path.join(os.path.join(destino, 'relatorios_csv'), fname[:-4]+'.csv'))
            except:
                ocorreu_excecao = True
                logger.exception("Erro ao gerar {}".format(fname))
    finally:
        m.close()

    return ocorreu_excecao

    
def main():
    parser = argparse.ArgumentParser(
        "fopag-docs",
        description="Gera documentos de folha"
        )
    parser.add_argument('--usuario', help="default: $MRH_USER (env_var)")
    parser.add_argument('--senha', help="default: $MRH_PASSWORD (env_var)")
    parser.add_argument('--destino', help="pasta de destino; default: f'{ano}-{mes}-{seq}'")
    parser.add_argument('--csv', help="utilizar para gerar arquivos em csv; default = False")
    parser.add_argument('mes', type=int, help='mês da folha')
    parser.add_argument('ano', type=int, help='ano da folha')
    parser.add_argument('seq', type=int, help='sequência da folha')
    parser.add_argument('roteiro', help="arquivo de configuracao")
    args = parser.parse_args()

    usuario = args.usuario or os.getenv('MRH_USER')
    senha = args.senha or os.getenv('MRH_PASSWORD')

    if args.destino:
        destino = args.destino
    else:
        destino = os.path.join(
            os.getcwd(),
            '{ano}-{mes:02d}-{seq:03d}'.format(
                ano=args.ano, mes=args.mes, seq=args.seq))
    
    if args.csv:
        csv = True
    else:
        csv = False

    erro = fopag_docs(
        usuario=usuario, senha=senha,
        folha_ano=args.ano, folha_mes=args.mes, folha_seq=args.seq,
        roteiro=args.roteiro,
        destino=destino,
        csv=csv
        )

    sys.exit(int(erro))


if __name__ == '__main__':
    main()