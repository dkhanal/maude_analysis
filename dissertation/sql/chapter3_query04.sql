/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

Gets classification on all Seed Data

*/

SELECT
C.[MDR_REPORT_KEY], C.MDR_TEXT_KEY, C.CLASSIFICATION AS LABEL_PREDICTED,
A.LABEL as LABEL_ACTUAL
FROM 
[dbo].[VW_CLASSIFICATION_SUMMARY_ALL] C,
[dbo].[VW_FOI_TEXT_SEED_DATA] A
WHERE 
C.MDR_REPORT_KEY = A.MDR_REPORT_KEY
AND C.MDR_TEXT_KEY = A.MDR_TEXT_KEY
AND C.MODEL_NAME = 'overall'