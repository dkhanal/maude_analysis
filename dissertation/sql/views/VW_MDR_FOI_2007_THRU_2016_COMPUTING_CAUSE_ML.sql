/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

View of Events Related to Computing Technology Causes based on Machine Learning 
*/ 

CREATE VIEW [dbo].[VW_MDR_FOI_2007_THRU_2016_COMPUTING_CAUSE_ML]
AS
SELECT *
FROM	[dbo].VW_MDR_FOI_2007_THRU_2016 
WHERE MDR_REPORT_KEY 
IN 
(
	SELECT DISTINCT MDR_REPORT_KEY
	FROM 
	[dbo].[VW_CLASSIFICATION_SUMMARY_ALL]
	WHERE 
		MODEL_NAME = 'overall'
		AND CLASSIFICATION = 'pos'
)
