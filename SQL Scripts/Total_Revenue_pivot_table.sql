-- Specify the DB name:
USE TrackRevenue

-- 1) Update the data:
------------------------------

-- delete the old views to fill them with newly updated data:
if object_id('Enhanced_Sites_Total_Revenue_Chart','v') is not null
	Drop VIEW Enhanced_Sites_Total_Revenue_Chart
if object_id('Sites_Total_Revenue_Chart','v') is not null
	Drop VIEW Sites_Total_Revenue_Chart

GO

-- Create the 2 views again to fill them with newly updated data:
CREATE VIEW Enhanced_Sites_Total_Revenue_Chart 
AS
	SELECT 
	CAST(Revenue_Tech.YEAR AS nvarchar(4)) + '-' + DATENAME(MONTH, DATEADD(MONTH, Revenue_Tech.month, -1)) AS 'Site_Date',
	shortCode,
	SUM(Total_Revenue) AS Total_Revenue
	FROM Revenue_Tech
	GROUP BY Year, Month, ShortCode
--ORDER BY Year, Month, ShortCode

GO

CREATE VIEW Sites_Total_Revenue_Chart 
AS
	SELECT Year, Month, ShortCode, SUM(Total_Revenue) AS Total_Revenue
	FROM Revenue_Tech
	GROUP BY Year, Month, ShortCode
	--ORDER BY Year, Month, ShortCode

GO


-- 2) Create Pivot Table:
------------------------------

DECLARE @site_total_revenue_query  VARCHAR(8000) -- main query
DECLARE @pivot_columns VARCHAR(8000) -- list to hold dynamically pivot columns

SET @pivot_columns =''

-- Get string columns
SELECT @pivot_columns += '[' + CONVERT(VARCHAR, Site_Date) +'],' FROM (SELECT DISTINCT Site_Date FROM Enhanced_Sites_Total_Revenue_Chart) AS pivotColList

-- delete the last comma
SET @pivot_columns = LEFT(@pivot_columns,LEN(@pivot_columns)-1)

-- Main query
SET @site_total_revenue_query = 'SELECT ShortCode, ' + @pivot_columns +' FROM
                (
                    SELECT ShortCode, Site_Date, Total_Revenue FROM Enhanced_Sites_Total_Revenue_Chart
                ) AS tmp_tbl             
                PIVOT
                (
                    SUM(Total_Revenue)
                    FOR Site_Date IN ('+ @pivot_columns +')
                ) AS pivotTable'

if object_ID('Total_Revenue_Pivot_Table') IS NOT NULL
	DROP TABLE Total_Revenue_Pivot_Table;


SELECT * INTO Total_Revenue_Pivot_Table FROM  (@site_total_revenue_query) ;
