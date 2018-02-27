/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

View of Number of Computing Technology-related Events by Year 
*/

CREATE VIEW [dbo].[VW_MDR_FOI_TOTAL_REPORTS_BY_YEAR_COMPUTING]
AS
SELECT        E.YEAR, COUNT(DISTINCT E.MDR_REPORT_KEY) AS COUNT
FROM          dbo.VW_MDR_FOI_2007_THRU_2016_COMPUTING_CAUSE E
GROUP BY E.YEAR
