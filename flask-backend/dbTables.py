# from app import excelDB
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request, redirect, url_for


flaskApp = Flask(__name__)
excelDB = SQLAlchemy(flaskApp)


class InTechNoDWH(excelDB.Model):
    id = excelDB.Column(excelDB.Integer, primary_key=True)
    # File_Date = excelDB.Column(excelDB.Date)

    Tech_Site_Code = excelDB.Column(excelDB.String(10))
    Tech_LAC_CI = excelDB.Column(excelDB.Integer)
    Tech_Total_Revenue = excelDB.Column(excelDB.Integer)

    # to return the string representation for this table
    def __str__(self):
        return f'{self.Tech_Site_Code}, {self.Tech_Total_Revenue}, {self.id}'

class InDWHNoTech(excelDB.Model):
    id = excelDB.Column(excelDB.Integer, primary_key=True)
    # File_Date = excelDB.Column(excelDB.Date)

    DWH_Site_Code = excelDB.Column(excelDB.String(10))
    DWH_Total_Revenue = excelDB.Column(excelDB.Integer)

    # to return the string representation for this table
    def __str__(self):
        return f'{self.DWH_Site_Code}, {self.DWH_Total_Revenue}, {self.id}'

class CellMappingReport(excelDB.Model):
    id = excelDB.Column(excelDB.Integer, primary_key=True)
    # File_Date = excelDB.Column(excelDB.Date)

    Site_Code = excelDB.Column(excelDB.String(10))
    Site_Name = excelDB.Column(excelDB.String(100))
    CI = excelDB.Column(excelDB.Integer)
    LAC = excelDB.Column(excelDB.Integer)   
    Technology = excelDB.Column(excelDB.String(2))
    Radio_Frequency_ID = excelDB.Column(excelDB.Integer)   
    RNC_BSC = excelDB.Column(excelDB.String(50))
    LAT_DEC = excelDB.Column(excelDB.Float)
    LONG_DEC = excelDB.Column(excelDB.Float)
    Site_Type = excelDB.Column(excelDB.String(50))
    Comment = excelDB.Column(excelDB.String(100))

class SiteRevenue(excelDB.Model):
    id = excelDB.Column(excelDB.Integer, primary_key=True)
    # File_Date = excelDB.Column(excelDB.Date)

    Year_Num = excelDB.Column(excelDB.Integer)
    Month_Num = excelDB.Column(excelDB.Integer)
    DWH_Cell = excelDB.Column(excelDB.Integer)
    Cell_Id = excelDB.Column(excelDB.Integer)
    LAC = excelDB.Column(excelDB.Integer)
    Market_Zone = excelDB.Column(excelDB.String(50))
    Status = excelDB.Column(excelDB.String(2))
    Governorate = excelDB.Column(excelDB.String(50))
    Northing = excelDB.Column(excelDB.Float)
    Easting = excelDB.Column(excelDB.Float)
    Geo_Lookup = excelDB.Column(excelDB.String(10))
    DWH_Site_Code = excelDB.Column(excelDB.String(10))
    Site_Name = excelDB.Column(excelDB.String(100))
    Total_Out_Duration = excelDB.Column(excelDB.Integer)
    Out_International_Duration = excelDB.Column(excelDB.Float)
    Incoming_Duration = excelDB.Column(excelDB.Float)
    Total_MB = excelDB.Column(excelDB.Float)
    Total_MB_2G = excelDB.Column(excelDB.Float)
    Total_MB_3G = excelDB.Column(excelDB.Float)
    Total_MB_4G = excelDB.Column(excelDB.Float)
    Inbound_Roam_Duration = excelDB.Column(excelDB.Float)
    National_Roam_Duration = excelDB.Column(excelDB.Float)
    Roam_Data_MB = excelDB.Column(excelDB.Float)
    Total_Out_Rev_EGP = excelDB.Column(excelDB.Float)
    Out_International_EGP = excelDB.Column(excelDB.Float)
    Total_MB_Rev_EGP = excelDB.Column(excelDB.Float)
    Total_MB_2G_Rev_EGP = excelDB.Column(excelDB.Float)
    Total_MB_3G_Rev_EGP = excelDB.Column(excelDB.Float)
    Total_MB_4G_Rev_EGP = excelDB.Column(excelDB.Float)
    In_Bound_Roaming_Rev_EGP = excelDB.Column(excelDB.Float)
    National_Roaming_Rev_EGP = excelDB.Column(excelDB.Float)
    Roam_Data_MB_Rev_EGP = excelDB.Column(excelDB.Float)
    Total_Revenue = excelDB.Column(excelDB.Float)

