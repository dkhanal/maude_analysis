/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

View of Events with an Computing Technology-related Cause for the Research Date Range 
*/ 

CREATE VIEW [dbo].[VW_MDR_FOI_2007_THRU_2016_COMPUTING_CAUSE]
AS
SELECT DISTINCT E.*
FROM	dbo.VW_MDR_FOI_2007_THRU_2016 AS E INNER JOIN
        dbo.FOI_DEV_PROBLEM_ORIG AS EP ON E.MDR_REPORT_KEY = EP.MDR_REPORT_KEY
WHERE   (EP.DEVICE_PROBLEM_CODE IN
            (SELECT        DEVICE_PROBLEM_CODE
            FROM            dbo.VW_DEVICE_PROBLEM_CODES_COMPUTING))
