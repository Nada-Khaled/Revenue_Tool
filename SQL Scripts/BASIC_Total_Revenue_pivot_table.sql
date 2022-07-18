SELECT shortCode, [2020], [2021], [2022]
FROM (
	SELECT shortCode, Year, Total_Revenue
	FROM Sites_Total_Revenue_Chart
)  AS Tmp_Sites_Total_Revenue_Chart
PIVOT  
(  
	SUM(Total_Revenue) 
	FOR year
	IN ([2020], [2021], [2022])
) AS pivotTable  
WHERE ShortCode IS NOT NULL AND ShortCode <> '-' AND shortCode <> ''