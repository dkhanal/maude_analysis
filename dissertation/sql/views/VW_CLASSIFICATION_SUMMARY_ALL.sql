/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

View of All Classification Summary
*/

CREATE VIEW [dbo].[VW_CLASSIFICATION_SUMMARY_ALL]
AS
SELECT 2007 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2007]
UNION
SELECT 2008 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2008]
UNION
SELECT 2009 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2009]
UNION
SELECT 2010 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2010]
UNION
SELECT 2011 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2011]
UNION
SELECT 2012 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2012]
UNION
SELECT 2013 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2013]
UNION
SELECT 2014 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2014]
UNION
SELECT 2015 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2015]
UNION
SELECT 2016 AS [YEAR], * FROM [dbo].[CLASSIFICATION_SUMMARY_FOI_TEXT_2016]