/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

View of Overall Classification Summary
*/

CREATE VIEW [dbo].[VW_CLASSIFICATION_SUMMARY_OVERALL] 
AS
SELECT * FROM dbo.[VW_CLASSIFICATION_SUMMARY_ALL]
WHERE MODEL_NAME = 'overall'

