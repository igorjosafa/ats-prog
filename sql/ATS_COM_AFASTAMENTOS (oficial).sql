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
    SELECT inneraf.Servidor, DtInicio, DtFim,
    SUM(CASE
    WHEN inneraf.DataInicial <= innerATS.DtFim AND inneraf.DataFinal <= DATEADD(YYYY, 1, innerATS.DtFim) THEN DATEDIFF('d', innerATS.DtFim, inneraf.DataFinal) + 1
    WHEN inneraf.DataInicial <= innerATS.DtFim AND inneraf.DataFinal > DATEADD(YYYY, 1, innerATS.DtFim) THEN DATEDIFF('d', innerATS.DtFim, DATEADD(YYYY, 1, innerATS.DtFim)) + 1
    WHEN inneraf.DataInicial >= innerATS.DtFim AND inneraf.DataFinal <= DATEADD(YYYY, 1, innerATS.DtFim) THEN DATEDIFF('d', inneraf.DataInicial, inneraf.DataFinal) + 1
    WHEN inneraf.DataInicial >= innerATS.DtFim AND inneraf.DataFinal > DATEADD(YYYY, 1, innerATS.DtFim) THEN DATEDIFF('d', inneraf.DataInicial, DATEADD(YYYY, 1, innerATS.DtFim)) + 1
    ELSE NULL
    END) as Dias_Afastado
    FROM RHCadAfastamento as inneraf
    LEFT JOIN (
        SELECT Servidor, DtInicio, DtFim
        FROM RHCadAdicionalTempoServico
        WHERE YEAR(DtFim) = YEAR(TO_DATE(:p1, 'MM/YYYY')) - 1
        AND MONTH(DtFim) = MONTH((TO_DATE(:p1, 'MM/YYYY')))
        GROUP BY Servidor
    ) as innerATS on inneraf.Servidor = innerATS.Servidor
    WHERE inneraf.Servidor->Funcional->TipoServidor->Codigo IN (1, 4)
    AND inneraf.Afastamento->Adicional->Codigo != 0
    AND (
        (inneraf.DataInicial <= innerATS.DtFim AND inneraf.DataFinal > innerATS.DtFim)
        OR (inneraf.DataInicial >= innerATS.DtFim AND inneraf.DataInicial <= DATEADD(YYYY, 1, innerATS.DtFim))
    )
    GROUP BY inneraf.Servidor
 ) as Af on ATS.Servidor = Af.Servidor
 WHERE (ATS.DtFim >= TO_DATE(:p1, 'MM/YYYY') AND ATS.DtFim <= LAST_DAY(TO_DATE(:p1, 'MM/YYYY')))
 OR (ATS.DtFim >= DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY')) AND ATS.DtFim <= LAST_DAY(DATEADD(YYYY, -1, TO_DATE(:p1, 'MM/YYYY'))))
 AND ATS.Servidor->Financeiro->DataDesligamento is NULL
 GROUP BY ATS.Servidor->Matricula
 ORDER BY ATS.DtFim DESC