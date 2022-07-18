USE [TrackRevenue]
GO

/****** Object:  Table [dbo].[Revenue_Tech_ORG_BackUp]    Script Date: 08-May-22 09:33:23 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[x](
	[Year] [int] NULL,
	[Month] [int] NULL,
	[LAC] [int] NULL,
	[Cell_Id] [int] NULL,
	[LAC-CI] [nvarchar](20) NULL,
	[ShortCode] [nvarchar](50) NULL,
	[Total_Out_Duration] [float] NULL,
	[Out_International_Duration] [float] NULL,
	[Incoming_Duration] [float] NULL,
	[Total_MB] [float] NULL,
	[Total_MB_2G] [float] NULL,
	[Total_MB_3G] [float] NULL,
	[Total_MB_4G] [float] NULL,
	[In_Bound_Roam_Duration] [float] NULL,
	[National_Roam_Duration] [float] NULL,
	[Roam_Data_MB] [float] NULL,
	[Total_Out_REV_EGP] [float] NULL,
	[Out_International_EGP] [float] NULL,
	[Total_MB_REV_EGP] [float] NULL,
	[Total_MB_2G_REV_EGP] [float] NULL,
	[Total_MB_3G_REV_EGP] [float] NULL,
	[Total_MB_4G_REV_EGP] [float] NULL,
	[In_Bound_Roaming_REV_EGP] [float] NULL,
	[National_Roaming_REV_EGP] [float] NULL,
	[Roam_Data_MB_REV_EGP] [float] NULL,
	[Total_Revenue] [float] NULL,
	[Technoloogy] [nvarchar](2) NULL
) ON [PRIMARY]
GO


