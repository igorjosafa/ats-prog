def gera_arquivo_importacao(ferias_acertadas_ats, ferias_acertadas_progressao, mes, ano):
    arq_importacao = open('arq_importacao.txt', 'w')
    for index, row in ferias_acertadas_ats.iterrows():
        if row['R1013_Ajustada'] > 0.01:
            linha = str(int(row['Matricula'])) + '\t' + '1013' + '\t' + '0' + '\t' + str(row['R1013_Ajustada']).replace('.', ',')+ '\t' + '1'+ '\t' + '1'+ '\t' + 'V'+ '\t' + 'N'+ '\t' + 'Acerto de férias em decorrência de progressão e/ou aumento de ATS'+ '\t' + '{:02}{}'.format(mes, ano) + '\t' + '0' + '\t' + '0' + '\t' + '{:02}{}'.format(mes, ano)
            arq_importacao.write(f"{linha}\n")
        if row['R1014_Ajustada'] > 0.01:
            linha = str(int(row['Matricula'])) + '\t' + '1014' + '\t' + '0' + '\t' + str(row['R1014_Ajustada']).replace('.', ',')+ '\t' + '1'+ '\t' + '1'+ '\t' + 'V'+ '\t' + 'N'+ '\t' + 'Acerto de férias em decorrência de progressão e/ou aumento de ATS'+ '\t' + '{:02}{}'.format(mes, ano) + '\t' + '0' + '\t' + '0' + '\t' + '{:02}{}'.format(mes, ano)
            arq_importacao.write(f"{linha}\n")
    for index, row in ferias_acertadas_progressao.iterrows():
        if row['R1013_Ajustada'] > 0.01:
            linha = str(int(row['Matricula'])) + '\t' + '1013' + '\t' + '0' + '\t' + str(row['R1013_Ajustada']).replace('.', ',')+ '\t' + '1'+ '\t' + '1'+ '\t' + 'V'+ '\t' + 'N'+ '\t' + 'Acerto de férias em decorrência de progressão e/ou aumento de ATS'+ '\t' + '{:02}{}'.format(mes, ano) + '\t' + '0' + '\t' + '0' + '\t' + '{:02}{}'.format(mes, ano)
            arq_importacao.write(f"{linha}\n")
        if row['R1014_Ajustada'] > 0.01:
            linha = str(int(row['Matricula'])) + '\t' + '1014' + '\t' + '0' + '\t' + str(row['R1014_Ajustada']).replace('.', ',')+ '\t' + '1'+ '\t' + '1'+ '\t' + 'V'+ '\t' + 'N'+ '\t' + 'Acerto de férias em decorrência de progressão e/ou aumento de ATS'+ '\t' + '{:02}{}'.format(mes, ano) + '\t' + '0' + '\t' + '0' + '\t' + '{:02}{}'.format(mes, ano)
            arq_importacao.write(f"{linha}\n")
    arq_importacao.close()