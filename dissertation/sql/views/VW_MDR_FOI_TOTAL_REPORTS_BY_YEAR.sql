/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

View of Number of All Events by Year 
*/

CREATE VIEW [dbo].[VW_MDR_FOI_TOTAL_REPORTS_BY_YEAR]
AS
SELECT	YEAR, COUNT(*) AS COUNT
FROM   dbo.VW_MDR_FOI_2007_THRU_2016
GROUP BY YEAR