/* 
Copyright (c) 2017 Deepak Khanal
All Rights Reserved
dkhanal AT gmail DOT com

Percentage of Computing Technology-related Events
*/

SELECT 
AllEvents.YEAR as [Year],
AllEvents.COUNT as AllEventsCount, 
ComputingEvents.COUNT as ComputingEventsCount,
ROUND(((ComputingEvents.COUNT * 1.0)/AllEvents.COUNT) * 100, 2) as [Percentage]
FROM 
[dbo].[VW_MDR_FOI_TOTAL_REPORTS_BY_YEAR] AS AllEvents,
[dbo].[VW_MDR_FOI_TOTAL_REPORTS_BY_YEAR_COMPUTING_ML] AS ComputingEvents
WHERE AllEvents.YEAR = ComputingEvents.YEAR
ORDER BY [Year]
