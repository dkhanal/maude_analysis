/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

Number of Events in MAUDE Database by Year 
*/

SELECT YEAR(DATE_RECEIVED) AS [Year], COUNT(*) AS Reports
FROM [dbo].[MDR_FOI_THRU_2016_ORIG]
GROUP BY YEAR(DATE_RECEIVED)
ORDER BY YEAR(DATE_RECEIVED)
