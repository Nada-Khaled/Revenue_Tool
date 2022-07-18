-- I used Revenue_Tech_ORG_BackUp at first

USE [TrackRevenue]
GO

ALTER VIEW Detailed_Network_Revenue_Chart
AS
	SELECT 
	 Merged_Revenue_Tech_With_Technology.[Year_Num]
	,Merged_Revenue_Tech_With_Technology.[Month_Num],
	SUM(Total_Revenue) AS Total_Revenue,
	--Total revenue for Data usage (money)
	SUM(Total_MB_REV_EGP) AS Total_Data,
	SUM(Total_Out_REV_EGP) AS Total_Voice,
	SUM(Total_Out_Duration) AS Total_Out_Duration,
	SUM(Incoming_Duration) AS Incoming_Duration,
	--Total used Data (quantity)
	SUM(Total_MB) AS Total_MB,
	SUM(In_Bound_Roam_Duration) AS In_Bound_Roam_Duration,
	SUM(National_Roam_Duration) AS National_Roam_Duration,
	--Total used Roaming Data (quantity)
	SUM(Roam_Data_MB) AS Roam_Data_MB,
	SUM(Out_International_EGP) AS Out_International_EGP,
	SUM(In_Bound_Roaming_REV_EGP) AS In_Bound_Roaming_REV_EGP,
	SUM(National_Roaming_REV_EGP) AS National_Roaming_REV_EGP,

	-- COALESCE: Before summing the 2 columns, replace NULL values with 0
	SUM(COALESCE(National_Roaming_REV_EGP,0) + COALESCE(In_Bound_Roaming_REV_EGP,0)) AS Roaming_Voice,
	--Total revenue for Roaming Data (money)
	SUM(Roam_Data_MB_REV_EGP) AS Roaming_Data

	FROM Merged_Revenue_Tech_With_Technology

	GROUP BY Merged_Revenue_Tech_With_Technology.[Year_Num]
	        ,Merged_Revenue_Tech_With_Technology.[Month_Num]
--ORDER BY Year, Month

GO

--if object_id('Detailed_Network_Revenue_Chart','v') is not null
--	Drop VIEW Detailed_Network_Revenue_Chart
