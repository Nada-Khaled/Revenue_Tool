-- Save the needed data in a table.
-- I have replaced this table with 2 views, in file:
-- create_views_instead_of_tables_for_sites_revenue.sql
-- So, this table IS NOT USED
INSERT INTO Sites_Total_Revenue_Chart 
SELECT Year, Month, ShortCode, SUM(Total_Revenue)
FROM Revenue_Tech
GROUP BY Year, Month, ShortCode
ORDER BY Year, Month, ShortCode