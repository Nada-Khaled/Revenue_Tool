USE TrackRevenue

SELECT 
	   Revenue_Tech_ORG_BackUp.[Year] AS Year_Num
	  ,Revenue_Tech_ORG_BackUp.[Month] AS Month_Num
	  ,Revenue_DWH_ORG_BackUp.[DWH_CELL]
	  ,Revenue_DWH_ORG_BackUp.[Cell_Id]
	  ,Revenue_DWH_ORG_BackUp.LAC AS LAC_DWH
      --,Revenue_Tech_ORG_BackUp.[LAC]
      --,Revenue_Tech_ORG_BackUp.[Cell_Id] ===CI
      ,Revenue_Tech_ORG_BackUp.[LAC-CI] AS LAC_CI
	  ,Revenue_DWH_ORG_BackUp.Market_Zone
	  ,Revenue_DWH_ORG_BackUp.[Status]
	  ,Revenue_DWH_ORG_BackUp.Governorate
	  ,Revenue_DWH_ORG_BackUp.Northing
	  ,Revenue_DWH_ORG_BackUp.Easting
	  ,Revenue_DWH_ORG_BackUp.Geo_Lookup
	  ,Revenue_DWH_ORG_BackUp.Site_Code_DWH
	  ,Revenue_DWH_ORG_BackUp.Site_Name AS Site_Name_DWH
      ,Revenue_Tech_ORG_BackUp.[Total_Out_Duration]
      ,Revenue_Tech_ORG_BackUp.[Out_International_Duration]
      ,Revenue_Tech_ORG_BackUp.[Incoming_Duration]
      ,Revenue_Tech_ORG_BackUp.[Total_MB]
      ,Revenue_Tech_ORG_BackUp.[Total_MB_2G]
      ,Revenue_Tech_ORG_BackUp.[Total_MB_3G]
      ,Revenue_Tech_ORG_BackUp.[Total_MB_4G]
      ,Revenue_Tech_ORG_BackUp.[In_Bound_Roam_Duration]
      ,Revenue_Tech_ORG_BackUp.[National_Roam_Duration]
      ,Revenue_Tech_ORG_BackUp.[Roam_Data_MB]
      ,Revenue_Tech_ORG_BackUp.[Total_Out_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[Out_International_EGP]
      ,Revenue_Tech_ORG_BackUp.[Total_MB_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[Total_MB_2G_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[Total_MB_3G_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[Total_MB_4G_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[In_Bound_Roaming_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[National_Roaming_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[Roam_Data_MB_REV_EGP]
      ,Revenue_Tech_ORG_BackUp.[Total_Revenue]
      ,Revenue_Tech_ORG_BackUp.[ShortCode] AS Site_Code_tech

	  INTO Merged_Revenue_Tech_With_Technology
	  
FROM Revenue_Tech_ORG_BackUp
LEFT JOIN Revenue_DWH_ORG_BackUp
ON Revenue_Tech_ORG_BackUp.[LAC-CI] = (CAST(Revenue_DWH_ORG_BackUp.LAC AS NVARCHAR(10))+CAST('-' AS NVARCHAR(1))+CAST(Revenue_DWH_ORG_BackUp.Cell_Id AS NVARCHAR(10)))
AND Revenue_Tech_ORG_BackUp.[Year] = Revenue_DWH_ORG_BackUp.[Year]
AND Revenue_Tech_ORG_BackUp.[Month] = Revenue_DWH_ORG_BackUp.[Month]


--INSERT INTO Merged_Revenue_Tech_With_Technology
--SELECT * FROM Merged_DWH_Tech

----SELECT @@VERSION



