DECLARE @pivot_columns VARCHAR(8000) -- list to hold dynamically pivot columns

SET @pivot_columns =''

-- Get string columns
SELECT @pivot_columns += '[' + CONVERT(VARCHAR, Site_Date) +'],' FROM (SELECT DISTINCT Site_Date FROM Enhanced_Sites_Total_Revenue_Chart) AS pivotColList

-- delete the last comma
SET @pivot_columns = LEFT(@pivot_columns,LEN(@pivot_columns)-1)


--SELECT * INTO TEST_TEST FROM
--				(SELECT ShortCode, [2020-October],[2020-December],[2021-December],[2021-May],[2020-January]
--				FROM
--                (
--                    SELECT ShortCode, Site_Date, Total_Revenue FROM Enhanced_Sites_Total_Revenue_Chart
--                ) AS tmp_tbl      
--                PIVOT
--                (
--                    SUM(Total_Revenue)
--                    FOR Site_Date IN ([2020-October],[2020-December],[2021-December],[2021-May],[2020-January])
--                ) AS totalRevpivotTable)tmp
				
---------------------------------------------------------

SELECT * INTO final_test
				FROM
				(SELECT ShortCode, @pivot_columns
				FROM
                (
                    SELECT ShortCode, Site_Date, Total_Revenue FROM Enhanced_Sites_Total_Revenue_Chart
                ) AS tmp_tbl      
                PIVOT
                (
                    SUM(Total_Revenue)
                    FOR Site_Date IN (@pivot_columns)
                ) AS totalRevpivotTable)tmp_tmp