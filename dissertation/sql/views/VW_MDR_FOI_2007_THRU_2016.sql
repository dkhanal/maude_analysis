/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

View of Events for the Research Date Range 
*/

CREATE VIEW [dbo].[VW_MDR_FOI_2007_THRU_2016]
AS

SELECT *
FROM            
	(
		SELECT  YEAR(DATE_RECEIVED) AS [YEAR], *
		FROM dbo.MDR_FOI_THRU_2016_ORIG
	) AS InnerTable
WHERE [YEAR] BETWEEN 2007 AND 2016
