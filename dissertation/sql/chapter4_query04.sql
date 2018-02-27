/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

Computing Technology Related Events by Reporter Occupation
*/

SELECT [REPORTER_OCCUPATION_CODE], COUNT (*) AS [COUNT]
FROM [dbo].[VW_MDR_FOI_2007_THRU_2016_COMPUTING_CAUSE_ML]
GROUP BY [REPORTER_OCCUPATION_CODE]
ORDER BY [COUNT] DESC
