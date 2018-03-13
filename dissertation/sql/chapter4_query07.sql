/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

Computing Technology-related Medical Device Events associated with patient death
*/

SELECT COUNT(DISTINCT MDR_REPORT_KEY) AS TOTAL_DEATH
FROM [dbo].[VW_MDR_FOI_2007_THRU_2016]
WHERE EVENT_TYPE IN ('D')
OR MDR_REPORT_KEY IN (
	SELECT MDR_REPORT_KEY FROM PATIENT_THRU_2016_ORIG
	WHERE SEQUENCE_NUMBER_OUTCOME LIKE '%D%'
)
GO
SELECT COUNT(DISTINCT MDR_REPORT_KEY) AS TOTAL_DEATH_COMPUTING
FROM [dbo].[VW_MDR_FOI_2007_THRU_2016_COMPUTING_CAUSE_ML]
WHERE EVENT_TYPE IN ('D')
OR MDR_REPORT_KEY IN (
	SELECT MDR_REPORT_KEY FROM PATIENT_THRU_2016_ORIG
	WHERE SEQUENCE_NUMBER_OUTCOME LIKE '%D%'
)
GO
