/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

Random Sampling for False Positive Rate Assessment
*/


SELECT TOP 1000 *
FROM [dbo].[VW_CLASSIFICATION_SUMMARY_ALL]
WHERE MODEL_NAME = 'overall'
	AND CLASSIFICATION = 'pos'
ORDER BY NEWID()
