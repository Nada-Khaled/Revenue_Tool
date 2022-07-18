-- Specify DB name:
USE TrackRevenue

-- 1) Update the data:
------------------------------

-- delete the old view to fill it with newly updated data:
if object_id('Detailed_Sites_Revenue_Chart','v') is not null
	Drop VIEW Detailed_Sites_Revenue_Chart

GO

-- Create the the view again to fill it with newly updated data:
CREATE VIEW Detailed_Sites_Revenue_Chart 
AS
	SELECT 
	--CAST(Revenue_Tech.YEAR AS nvarchar(4)) + '-' + DATENAME(MONTH, DATEADD(MONTH, Revenue_Tech.month, -1)) AS 'Site_Date',
	--CAST(Revenue_Tech.YEAR AS nvarchar(4)) + '-' + CAST(Revenue_Tech.Month AS nvarchar(2)) AS 'Site_Date',
	CAST(Revenue_Tech.YEAR AS nvarchar(4)) + '-' + RIGHT('0'+ CONVERT(VARCHAR, Revenue_Tech.Month), 2) AS 'Site_Date',

	shortCode,
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
	FROM Revenue_Tech
	GROUP BY Year, Month, ShortCode
--ORDER BY Year, Month, ShortCode

GO


-- 2) Create Pivot Table:
------------------------------

DECLARE @site_National_Roam_Duration_query  VARCHAR(max) -- main query
DECLARE @pivot_columns VARCHAR(8000) -- list to hold dynamically pivot columns

SET @pivot_columns =''

-- Get string columns
SELECT @pivot_columns += '[' + CONVERT(VARCHAR, Site_Date) +'],' FROM (SELECT DISTINCT Site_Date FROM Detailed_Sites_Revenue_Chart) AS pivotColList

-- delete the last comma
SET @pivot_columns = LEFT(@pivot_columns,LEN(@pivot_columns)-1)

-- Main query
SET @site_National_Roam_Duration_query = '
				SELECT * INTO Total_National_Roam_Duration_Pivot_Table
				FROM 
				(SELECT ShortCode, ' + @pivot_columns +
				' FROM
                (
                  SELECT ShortCode, Site_Date, National_Roam_Duration FROM Detailed_Sites_Revenue_Chart
                ) AS tmp_tbl             
                PIVOT
                (
                    SUM(National_Roam_Duration)
                    FOR Site_Date IN ('+ @pivot_columns +')
                ) AS nationalRoamDurationPivotTable)tmp'

--PRINT(@pivot_columns)
--PRINT(@site_voice_revenue_query)
--GO


if object_ID('Total_National_Roam_Duration_Pivot_Table') IS NOT NULL
	DROP TABLE Total_National_Roam_Duration_Pivot_Table;

EXEC (@site_National_Roam_Duration_query)
