-- Specify DB name:
USE TrackRevenue

-- 1) Update the data:
------------------------------

-- delete the old views to fill them with newly updated data:
if object_id('Enhanced_Network_Revenue_Chart','v') is not null
	Drop VIEW Enhanced_Network_Revenue_Chart
if object_id('Network_Revenue_Chart','v') is not null
	Drop VIEW Network_Revenue_Chart

GO

-- Create the 2 views again to fill them with newly updated data:
CREATE VIEW Enhanced_Network_Revenue_Chart
AS
	SELECT 
	--CAST(Revenue_Tech.YEAR AS nvarchar(4)) + '-' + DATENAME(MONTH, DATEADD(MONTH, Revenue_Tech.month, -1)) AS 'Site_Date',
	--CAST(Revenue_Tech.YEAR AS nvarchar(4)) + '-' + CAST(Revenue_Tech.Month AS nvarchar(2)) AS 'Site_Date',
	CAST(Revenue_Tech.YEAR AS nvarchar(4)) + '-' + RIGHT('0'+ CONVERT(VARCHAR, Revenue_Tech.Month), 2) AS 'Site_Date',

	--shortCode,
	SUM(Total_Revenue) AS Total_Revenue,
	SUM(Total_MB_REV_EGP) AS Total_Data,
	SUM(Total_Out_REV_EGP) AS Total_Voice,
	-- COALESCE: Before summing the 2 columns, replace NULL values with 0
	SUM(COALESCE(National_Roaming_REV_EGP,0) + COALESCE(In_Bound_Roaming_REV_EGP,0)) AS Roaming_Voice,
	SUM(Roam_Data_MB_REV_EGP) AS Roaming_Data
	FROM Revenue_Tech
	GROUP BY Year, Month
--ORDER BY Year, Month

GO

CREATE VIEW Network_Revenue_Chart
AS
	SELECT Year, Month,
	--ShortCode,
	SUM(Total_Revenue) AS Total_Revenue,
	SUM(Total_MB_REV_EGP) AS Total_Data,
	SUM(Total_Out_REV_EGP) AS Total_Voice,
	-- COALESCE: Before summing the 2 columns, replace NULL values with 0
	SUM(COALESCE(National_Roaming_REV_EGP,0) + COALESCE(In_Bound_Roaming_REV_EGP,0)) AS Roaming_Voice,
	SUM(Roam_Data_MB_REV_EGP) AS Roaming_Data
	FROM Revenue_Tech
	GROUP BY Year, Month
	--ORDER BY Year, Month

GO


-- 2) Create Pivot Table:
------------------------------

DECLARE @network_roaming_voice_revenue_query  VARCHAR(max) -- main query
DECLARE @pivot_columns VARCHAR(8000) -- list to hold dynamically pivot columns

SET @pivot_columns =''

-- Get string columns
SELECT @pivot_columns += '[' + CONVERT(VARCHAR, Site_Date) +'],' FROM (SELECT DISTINCT Site_Date FROM Enhanced_Network_Revenue_Chart) AS pivotColList

-- delete the last comma
SET @pivot_columns = LEFT(@pivot_columns,LEN(@pivot_columns)-1)
--print(@pivot_columns)

-- Main query
SET @network_roaming_voice_revenue_query = '
				SELECT * INTO Network_Roaming_Voice_Revenue_Pivot_Table
				FROM 
				(SELECT ' + @pivot_columns +
				' FROM
                (
                  SELECT Site_Date, Roaming_Voice FROM Enhanced_Network_Revenue_Chart
                ) AS tmp_tbl             
                PIVOT
                (
                    SUM(Roaming_Voice)
                    FOR Site_Date IN ('+ @pivot_columns +')
                ) AS networkRoamingVoiceRevPivotTable)tmp'

--PRINT(@pivot_columns)
--PRINT(@network_roaming_voice_revenue_query)
--GO


if object_ID('Network_Roaming_Voice_Revenue_Pivot_Table') IS NOT NULL
	DROP TABLE Network_Roaming_Voice_Revenue_Pivot_Table;

EXEC (@network_roaming_voice_revenue_query)
