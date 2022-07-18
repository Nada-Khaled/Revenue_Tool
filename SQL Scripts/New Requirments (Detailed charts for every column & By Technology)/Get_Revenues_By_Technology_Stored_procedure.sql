USE TrackRevenue
---- First change the data type for the columns from text to float:

---- When creating this table from flask server, the default data type
---- for the columns is text, so, I should change them,
---- but I can't change them directly from text to FLOAT or INT,
---- I should change them first to NVARCHAR(any_size) >>> if I didn't specify the size of NVARCHAR, the default will be 1, so I will not be able to hold any values that contains more than one digit
---- then change them to any data type I want
--BEGIN

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_MB_2G_REV_EGP NVARCHAR(50) NULL; 
--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_MB_2G_REV_EGP FLOAT; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_MB_3G_REV_EGP NVARCHAR(50) NULL; 
--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_MB_3G_REV_EGP FLOAT; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_MB_4G_REV_EGP NVARCHAR(50) NULL; 
--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_MB_4G_REV_EGP FLOAT; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_Out_REV_EGP NVARCHAR(50) NULL; 
--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_Out_REV_EGP FLOAT; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_Revenue NVARCHAR(50) NULL; 
--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Total_Revenue FLOAT; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Site_Code_tech NVARCHAR(15) NULL; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN TECHNOLOGY NVARCHAR(2) NULL; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Year_Num NVARCHAR(50) NULL; 
--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Year_Num INT; 

--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Month_Num NVARCHAR(50) NULL; 
--ALTER TABLE Revenue_Tech_ORG_BackUp ALTER COLUMN Month_Num INT;

--END
--GO

-- Without passing technology as a parameter, and returning all 3 technologies for
-- the specified siteCode
ALTER PROCEDURE Get_Revenues_By_Technology @siteCode NVARCHAR(15)
AS

	SELECT [Year], [Month], TECHNOLOGY
	,SUM(Total_Revenue) AS Total_Revenue
	,SUM(Total_MB_2G_REV_EGP) AS Total_MB_2G_REV_EGP
	,SUM(Total_MB_3G_REV_EGP) AS Total_MB_3G_REV_EGP
	,SUM(Total_MB_4G_REV_EGP) AS Total_MB_4G_REV_EGP
	,SUM(Total_Out_REV_EGP) AS Total_Out_REV_EGP

	FROM Revenue_Tech_ORG_BackUp
	GROUP BY Year_Num, Month_Num, TECHNOLOGY, Site_Code_tech
	HAVING Site_Code_tech = @siteCode			

GO

EXECUTE Get_Revenues_By_Technology @siteCode='0001AL'




---------------------------------------

-- With passing technology as a parameter
----ALTER PROCEDURE Get_Revenues_By_Technology @technology NVARCHAR(10), @siteCode NVARCHAR(15)
----AS

----	IF(@technology = '2G')
----	BEGIN

----		SELECT Year_Num, TECHNOLOGY
----		,SUM(Total_Revenue) AS Total_Revenue
----		,SUM(Total_MB_2G_REV_EGP) AS Total_MB_2G_REV_EGP
----		,SUM(Total_MB_3G_REV_EGP) AS Total_MB_3G_REV_EGP
----		,SUM(Total_MB_4G_REV_EGP) AS Total_MB_4G_REV_EGP
----		,SUM(Total_Out_REV_EGP) AS Total_Out_REV_EGP

----		FROM Revenue_Tech_ORG_BackUp
----		GROUP BY Year_Num, TECHNOLOGY, Site_Code_tech
----		HAVING Site_Code_tech = @siteCode
----		--AND TECHNOLOGY = @technology

----		--PRINT('I AM 2G')
----	END

----	ELSE IF(@technology = '3G')
----	BEGIN

----		SELECT Year_Num, TECHNOLOGY
----		,SUM(Total_Revenue) AS Total_Revenue
----		,SUM(Total_MB_3G_REV_EGP) AS Total_MB_3G_REV_EGP
----		,SUM(Total_Out_REV_EGP) AS Total_Out_REV_EGP

----		FROM Revenue_Tech_ORG_BackUp
----		GROUP BY Year_Num, TECHNOLOGY, Site_Code_tech
----		HAVING Site_Code_tech = @siteCode
----		--AND TECHNOLOGY = @technology

----		--PRINT('I AM 3G')
----	END

----	ELSE IF(@technology = '4G')
----	BEGIN

----		SELECT Year_Num, TECHNOLOGY
----		,SUM(Total_Revenue) AS Total_Revenue
----		,SUM(Total_MB_4G_REV_EGP) AS Total_MB_4G_REV_EGP
----		,SUM(Total_Out_REV_EGP) AS Total_Out_REV_EGP

----		FROM Revenue_Tech_ORG_BackUp
----		GROUP BY Year_Num, TECHNOLOGY, Site_Code_tech
----		HAVING Site_Code_tech = @siteCode
----		--AND TECHNOLOGY = @technology
----		--PRINT('I AM 4G')
----	END
	

----GO

----EXECUTE Get_Revenues_By_Technology @technology='2G', @siteCode='0001AL'

