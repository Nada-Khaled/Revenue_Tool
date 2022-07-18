-- delete the old views to fill them with newly data
if object_id('Enhanced_Sites_Total_Revenue_Chart','v') is not null
	Drop VIEW Enhanced_Sites_Total_Revenue_Chart
if object_id('Sites_Total_Revenue_Chart','v') is not null
	Drop VIEW Sites_Total_Revenue_Chart

GO

--Preferably to be either a view or a tmp table rather than a normal table
--in case the original underlying table (Revenue_tech) changed

-- I am tring to concatenate the month & year in a single column to use it the pivot table,
-- So, I have used the 2 functions:
--1) DATENAME(): which takes as the first parameter the part of the date that I want to return,
-- and takes as the second parameter the date it self.
-- 2) DATEADD(): which takes as the first parameter what part of the date that I want to add the value to
-- it, and takes as the second parameter the value that I want to add,
-- and takes as the third parameter the date it self.
-- the 3rd parameter of function DATEADD can be any date with 12th month
-- Or it can simply be -1 as below:

-- I have casted the year to string to be able to concatenate it with the month name.
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

-- To see the result of the 2 views:
SELECT * FROM Sites_Total_Revenue_Chart ORDER BY ShortCode
SELECT * FROM Enhanced_Sites_Total_Revenue_Chart ORDER BY ShortCode

