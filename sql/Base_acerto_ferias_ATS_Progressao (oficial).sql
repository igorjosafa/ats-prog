SELECT Servidor->Matricula, MesAnoCompetencia as Mes_Recebimento, ServidorCongelado->Padrao->Sigla as Padrao_Antigo,
 SUM(CASE
  WHEN Rubrica->Codigo = 1002 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p2 THEN Valor/100
  ELSE 0
 END) as R1002_Antiga,
 SUM(CASE
  WHEN Rubrica->Codigo = 1007 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p2 THEN Valor/100
  ELSE 0
 END) as R1007_Antiga,
 SUM(CASE
  WHEN Rubrica->Codigo = 1028 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p2 THEN Valor/100
  ELSE 0
 END) as R1028_Antiga,
 SUM(CASE
  WHEN Rubrica->Codigo = 1170 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p2 THEN Valor/100
  ELSE 0
 END) as R1170_Antiga,
 SUM(CASE
  WHEN Rubrica->Codigo = 1013 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p2 THEN Valor/100
  ELSE 0
 END) as R1013_Antiga,
 SUM(CASE
  WHEN Rubrica->Codigo = 1014 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p2 THEN Valor/100
  ELSE 0
 END) as R1014_Antiga,
 SUM(CASE
  WHEN Rubrica->Codigo = 1002 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p4 THEN Valor/100
  ELSE 0
 END) as R1002_Nova,
 SUM(CASE
  WHEN Rubrica->Codigo = 1007 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p4 THEN Valor/100
  ELSE 0
 END) as R1007_Nova,
 SUM(CASE
  WHEN Rubrica->Codigo = 1028 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p4 THEN Valor/100
  ELSE 0
 END) as R1028_Nova,
 SUM(CASE
  WHEN Rubrica->Codigo = 1170 & MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p4 THEN Valor/100
  ELSE 0
 END) as R1170_Nova
 FROM RhFolCalculo
 WHERE (Folha->FolhaAno = :p1
 AND MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p2
 OR
 Folha->FolhaAno = :p3
 AND MONTH(TO_DATE(Folha->FolhaMes, 'MM')) = :p4)
 AND Rubrica->Codigo IN (1002, 1007, 1013, 1014, 1028, 1170)
 GROUP BY Servidor->Matricula