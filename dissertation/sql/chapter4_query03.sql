/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

Source of Medical Device Event Reports
*/

SELECT YEAR, E.REPORT_SOURCE_CODE, COUNT (*) AS [COUNT] 
FROM [dbo].[VW_MDR_FOI_2007_THRU_2016_COMPUTING_CAUSE_ML] E
GROUP BY YEAR, E.REPORT_SOURCE_CODE
ORDER BY YEAR, COUNT DESC
