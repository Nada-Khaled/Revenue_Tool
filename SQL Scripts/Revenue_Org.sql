CREATE TABLE [dbo].[Revenue_Org](
	[Year] [int] NULL,
	[Month] [int] NULL,
	[DWH_CELL] [int] NULL,
	[Cell_Id] [int] NULL,
	[LAC] [int] NULL,
	[Market_Zone] [nvarchar](20) NULL,
	[Status] [nvarchar](10) NULL,
	[Governorate] [nvarchar](25) NULL,
	[Northing] [nvarchar](20) NULL,
	[Easting] [nvarchar](20) NULL,
	[Geo_Lookup] [nvarchar](50) NULL,
	[Fin_Lookup] [nvarchar](10) NULL,
	[Site_Code_DWH] [nvarchar](50) NULL,
	[Site_Name] [nvarchar](100) NULL,
	[Total_Out_Duration] [float] NULL,
	[Out_International_Duration] [float] NULL,
	[Incoming_Duration] [float] NULL,
	[Roam_SDR] [float] NULL,
	[Total_MB] [float] NULL,
	[Total_MB_2G] [float] NULL,
	[Total_MB_3G] [float] NULL,
	[Total_MB_4G] [float] NULL,
	[In_Bound_Roam_Duration] [float] NULL,
	[National_Roam_Duration] [float] NULL,
	[Roam_Data_MB] [float] NULL,
	[Inc_Vodafone_Duration] [float] NULL,
	[Inc_Etisalat_Duration] [float] NULL,
	[Inc_WE_Duration] [float] NULL,
	[Inc_PSTN_Duration] [float] NULL,
	[Inc_International_Duration] [float] NULL,
	[Inc_InfoServices_Duration] [float] NULL,
	[Inc_Others_Duration] [float] NULL,
	[Total_Out_REV_EGP] [float] NULL,
	[Out_International_EGP] [float] NULL,
	[Total_MB_REV_EGP] [float] NULL,
	[Total_MB_2G_REV_EGP] [float] NULL,
	[Total_MB_3G_REV_EGP] [float] NULL,
	[Total_MB_4G_REV_EGP] [float] NULL,
	[In_Bound_Roaming_REV_EGP] [float] NULL,
	[National_Roaming_REV_EGP] [float] NULL,
	[Roam_Data_MB_REV_EGP] [float] NULL,
	[Total_Revenue] [float] NULL
) ON [PRIMARY]
GO

