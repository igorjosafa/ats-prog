SELECT ATS.Servidor->Matricula,
ATS.Servidor->Nome,
ATS.DtInicioFormatada as Dt_Inicio,
ATS.DtFimFormatada as Dt_Fim,
Af.Dias_Afastado,
CASE
 WHEN ATS.DtFim >= TO_DATE(:p1, 'MM/YYYY') & ATS.DtFim <= LAST_DAY(TO_DATE(:p1, 'MM/YYYY')) THEN YEAR(TO_DATE(:p1, 'MM/YYYY'))
 ELSE YEAR(TO_DATE(:p1, 'MM/YYYY'))-1
END as Ultimo_Ano,
CASE
 WHEN ATS.DtFim < TO_DATE(:p1, 'MM/YYYY') THEN TOCHAR(DATEADD('dd', ATS.DtFim, Dias_Afastado), 'DD/MM/YYYY')
 ELSE NULL
END as Novo_Inicio
 FROM RHCadAdicionalTempoServico as ATS
 LEFT JOIN (
 SELECT Servidor,
  SUM(CASE
   WHEN DataInicial >= DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY')) THEN DATEDIFF('d', DataInicial, DataFinal) + 1
   WHEN DataInicial < DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY')) THEN DATEDIFF('d', DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY')), DataFinal) + 1
  ELSE NULL
  END) as Dias_Afastado
  FROM RHCadAfastamento
  WHERE Servidor->Funcional->TipoServidor->Codigo IN (1, 4)
  AND Afastamento->Adicional->Codigo != 0
  AND (DataInicial >= DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY'))
  OR DataFinal >= DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY')))
  GROUP BY Servidor
 ) as Af on ATS.Servidor = Af.Servidor
 WHERE (ATS.DtFim >= TO_DATE(:p1, 'MM/YYYY') AND ATS.DtFim <= LAST_DAY(TO_DATE(:p1, 'MM/YYYY')))
 OR (ATS.DtFim >= DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY')) AND ATS.DtFim <= LAST_DAY(DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY'))))
 AND ATS.Servidor->Financeiro->DataDesligamento is NULL
 GROUP BY ATS.Servidor->Matricula
 ORDER BY ATS.DtFim DESC