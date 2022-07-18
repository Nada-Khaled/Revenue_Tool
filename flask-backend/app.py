
from turtle import left
# from types import NoneType
import numpy as np
import pandas as pd
from cmath import nan
from io import BytesIO
from urllib import response
import json
from flask import Flask, Response, flash, render_template, request, redirect, send_file, url_for, jsonify, send_from_directory, abort
from importlib.resources import path
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import sqlalchemy
from sqlalchemy import FLOAT, Float, Integer, String, create_engine
from sqlalchemy import types
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import date
from werkzeug.utils import secure_filename
import os
from models import *
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

flaskApp = Flask(__name__)
setup_db(flaskApp)
dbConnection = engine.connect()

upload_folder = "/uploadedExcelFiles"
if not os.path.exists(upload_folder):
    print("Folder NOT EXIST")
    os.mkdir(upload_folder)
    print("Folder CREATED")

# Temporary folder, will not be created
flaskApp.config['CSV_PATH'] = upload_folder
CORS(flaskApp)
# jwt = JWTManager(flaskApp)

# ? I am getting data from DWH table, Should I use it or Revenue_tech or the new merged table ???
@flaskApp.route('/api/getAllYearsMonths', methods=['GET', 'POST'])
@cross_origin()
def GetYearsMonths():

    print('\n\n\nIn BACKEND /api/getAllYearsMonths')

    ALL_Years_Months = pd.read_sql(
        "SELECT DISTINCT (year_num), (month_num) FROM Merged_Revenue_Tech_With_Technology ORDER BY year_num, month_num", dbConnection)
    ALL_Years_Months['month_num'] = ALL_Years_Months['month_num'].astype(
        str).str.zfill(2)
    Year_Month = ALL_Years_Months['year_num'].astype(
        str) + "-" + ALL_Years_Months['month_num'].astype(str)

    result = {}
    # result["YearsMonthsList"] = list(ALL_Years_Months["Year_Month"])
    result["YearsMonthsList"] = list(Year_Month)

    # qry = db.session.query(Merged_Revenue_Tech_With_Technology.year_num,
    #     Merged_Revenue_Tech_With_Technology.month_num).distinct().order_by(
    #     Merged_Revenue_Tech_With_Technology.year_num,
    #     Merged_Revenue_Tech_With_Technology.month_num).all()
    
    
    return result


@flaskApp.route("/api/getMonthRevenues/<string:YearMonth>", methods=['GET', 'POST'])
@cross_origin()
def GetRevenuePerMonth(YearMonth):

    year = YearMonth.split('-')[0]
    month = YearMonth.split('-')[1]

    # print(year, " ", month)
    # query = "SELECT * FROM Merged_DWH_Tech_Jan_March WHERE Year_Month = '"+YearMonth+"'"
    # query = "SELECT * FROM in_tech_No_DWH WHERE Year_Month = '"+YearMonth+"'"

    # Dwh_Revenue_Table = pd.read_sql_query("SELECT * FROM Revenue_DWH_ORG_BackUp WHERE Revenue_DWH_ORG_BackUp.[Year] = "+year+" AND Revenue_DWH_ORG_BackUp.[Month] = "+ month, DB_CONNECTION)
    Dwh_Revenue_Table = pd.read_sql(
        "SELECT * FROM Merged_Revenue_Tech_With_Technology WHERE year_num = "+year+" AND month_num = "+month, dbConnection)
  
    # print("\n\n\n\nDwh_Revenue_Table")
    # print(Dwh_Revenue_Table)
    # print('\n\n\n\n')

    Dwh_Revenue_Table.rename(
        columns={"total_mb_rev_egp": "total_data"}, inplace=True)
    Dwh_Revenue_Table.rename(
        columns={"total_out_rev_egp": "total_voice"}, inplace=True)

    Dwh_Revenue_Table["total_revenue"] = Dwh_Revenue_Table["total_revenue"].fillna(
        0)
    Dwh_Revenue_Table["total_data"] = Dwh_Revenue_Table["total_data"].fillna(0)
    Dwh_Revenue_Table["total_voice"] = Dwh_Revenue_Table["total_voice"].fillna(0)

    Dwh_Revenue_Table["site_name_dwh"] = Dwh_Revenue_Table["site_name_dwh"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.site_name_dwh == "nan"), 'site_name_dwh'] = '-'

    Dwh_Revenue_Table["site_code_tech"] = Dwh_Revenue_Table["site_code_tech"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.site_code_tech == "nan"), 'site_code_tech'] = '-'

    Dwh_Revenue_Table["site_code_dwh"] = Dwh_Revenue_Table["site_code_dwh"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.site_code_dwh == "?"), 'site_code_dwh'] = '-'
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.site_code_dwh == "nan"), 'site_code_dwh'] = '-'
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.site_code_dwh == "No lookup for Cell"), 'site_code_dwh'] = '-'
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.site_code_dwh == "Cell with no Site Code"), 'site_code_dwh'] = '-'
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.site_code_dwh == "CDR with No Cell"), 'site_code_dwh'] = '-'
   
    
    Dwh_Revenue_Table["status"] = Dwh_Revenue_Table["status"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.status == "?"), 'status'] = '-'
    
    Dwh_Revenue_Table["market_zone"] = Dwh_Revenue_Table["market_zone"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.market_zone == "?"), 'market_zone'] = '-'
    
    Dwh_Revenue_Table["governorate"] = Dwh_Revenue_Table["governorate"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.governorate == "?"), 'governorate'] = '-'
    
    Dwh_Revenue_Table["northing"] = Dwh_Revenue_Table["northing"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.northing == "?"), 'northing'] = '0'

    Dwh_Revenue_Table["easting"] = Dwh_Revenue_Table["easting"].fillna('-')
    Dwh_Revenue_Table.loc[(Dwh_Revenue_Table.easting == "?"), 'easting'] = '0'

    Dwh_Revenue_Table = Dwh_Revenue_Table.fillna(0)

    in_tech_No_DWH_selected_cols = Dwh_Revenue_Table[(Dwh_Revenue_Table["site_code_tech"] != "-") & (Dwh_Revenue_Table["site_code_dwh"] == "-")]
    in_DWH_No_tech_selected_cols = Dwh_Revenue_Table[(Dwh_Revenue_Table["site_code_tech"] == "-") & (Dwh_Revenue_Table["site_code_dwh"] != "-")]
    Dwh_Not_Match_tech_selected_cols = Dwh_Revenue_Table[(Dwh_Revenue_Table["site_code_tech"] != "-") & (Dwh_Revenue_Table["site_code_dwh"] != "-")& (Dwh_Revenue_Table["site_code_dwh"] != Dwh_Revenue_Table["site_code_tech"])]

    in_tech_No_DWH_list = []
    for rowIndex, row in in_tech_No_DWH_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            "Site_Code_tech": row[2],
            "Site_Code_DWH": '-',
            "Total_Revenue": row[3]
        }
        in_tech_No_DWH_list.append(row_obj)

    in_tech_No_DWH_total_revenue = in_tech_No_DWH_selected_cols["total_revenue"].map(
        float).sum()
    # print("in_tech_No_DWH_total_revenue")
    # print(in_tech_No_DWH_total_revenue)

    in_DWH_No_tech_list = []
    for rowIndex, row in in_DWH_No_tech_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            # "Site_Code_tech":row[0],
            "Site_Code_tech": '-',
            "Site_Code_DWH": row[2],
            "Total_Revenue": row[3]
        }
        in_DWH_No_tech_list.append(row_obj)

    in_DWH_No_tech_total_revenue = in_DWH_No_tech_selected_cols["total_revenue"].map(
        float).sum()

    # print('\n\n\n\n\n >>> ZERO LEH!!')
    # print(in_DWH_No_tech_selected_cols['total_revenue'])
    # print('\n\n\n\n\n\n =======> el SUM()')
    # print(in_DWH_No_tech_total_revenue)

    Dwh_Not_Match_tech_list = []
    for rowIndex, row in Dwh_Not_Match_tech_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            "Site_Code_tech": row[3],
            "Site_Code_DWH": row[2],
            "Total_Revenue": row[4]
        }
        Dwh_Not_Match_tech_list.append(row_obj)

    Dwh_Not_Match_tech_total_revenue = Dwh_Not_Match_tech_selected_cols["total_revenue"].map(
        float).sum()
    Total_Revenue = Dwh_Revenue_Table["total_revenue"].map(float).sum()
    Total_Data = Dwh_Revenue_Table["total_data"].map(float).sum()
    Total_Voice = Dwh_Revenue_Table["total_voice"].map(float).sum()

    response = {
        "Total_Revenue": "{:,.2f}".format(Total_Revenue),
        "Total_Data": "{:,.2f}".format(Total_Data),
        "Total_Voice": "{:,.2f}".format(Total_Voice),
        "in_tech_No_DWH": {
            "in_tech_No_DWH_list": in_tech_No_DWH_list,
            "in_tech_No_DWH_total_revenue": "{:,.2f}".format(in_tech_No_DWH_total_revenue),
            # "in_tech_No_DWH_buffer":"in_tech_No_DWH_buffer",
            "in_tech_No_DWH_buffer": "in_tech_No_DWH.csv"
        },

        "in_DWH_No_tech": {
            "in_DWH_No_tech_list": in_DWH_No_tech_list,
            "in_DWH_No_tech_total_revenue": "{:,.2f}".format(in_DWH_No_tech_total_revenue),
            # "in_DWH_No_tech_buffer":"in_DWH_No_tech_buffer"
            "in_DWH_No_tech_buffer": "in_DWH_No_tech.csv"
        },
        "DWH_Not_Match_tech": {
            "DWH_Not_Match_tech_list": Dwh_Not_Match_tech_list,
            "DWH_Not_Match_tech_total_revenue": "{:,.2f}".format(Dwh_Not_Match_tech_total_revenue),
            "DWH_Not_Match_tech_buffer": "DWH_Not_Match_tech.csv"
            # "DWH_Not_Match_tech_buffer":""
        },

    }

    return response


@flaskApp.route("/api/downloadFiles/<path:file_name>", methods=['GET', 'POST'])
@cross_origin()
def get_file(file_name):

    # for filename in os.listdir(flaskApp.config['CSV_PATH']):
    #     f = os.path.join(flaskApp.config['CSV_PATH'], filename)
    # # #     # checking if it is a file
    #     if os.path.isfile(f):
    #         os.remove(f)

    # return ""

    f_name = file_name.split('|')[0]
    file_date = file_name.split('|')[1]

    year = file_date.split('-')[0]
    month = file_date.split('-')[1]

    fle = f_name+file_date

    # for filename in os.listdir(flaskApp.config['CSV_PATH']):
    #     print("\n\n>>", filename)
    #     print("\n")
    #     if filename == fle:
    #         print("\n\n\nl2etooooooooo\n\n\n")
    #         return send_from_directory(flaskApp.config['CSV_PATH'], path=fle, as_attachment=True)

    selected_table = ""
    Dwh_Revenue_Table = pd.read_sql(
        "SELECT * FROM Merged_Revenue_Tech_With_Technology WHERE year_num = "+year+" AND month_num = "+month, dbConnection)
    
    # file_of_interest = Dwh_Revenue_Table[["lac_ci", "site_code_dwh", "site_code_tech",
    #                                      "total_revenue", "total_mb_rev_egp", "total_out_rev_egp"]]#, "technology"]]
    file_of_interest = Dwh_Revenue_Table[['year_num','month_num',"lac_ci","site_code_dwh","site_code_tech","total_revenue","total_mb_rev_egp","total_out_rev_egp","status"]]

    file_of_interest.rename(columns={"total_mb_rev_egp": "total_data"}, inplace=True)
    file_of_interest.rename(columns={"total_out_rev_egp": "total_voice"}, inplace=True)

    file_of_interest["site_code_tech"] = file_of_interest["site_code_tech"].fillna('-')
    file_of_interest["site_code_dwh"] = file_of_interest["site_code_dwh"].fillna('-')

    in_tech_No_DWH = file_of_interest[(file_of_interest["site_code_tech"] != "-") & (file_of_interest["site_code_dwh"] == "-")]
    in_DWH_No_tech = file_of_interest[(file_of_interest["site_code_tech"] == "-") & (file_of_interest["site_code_dwh"] != "-")]
    DWH_Not_Match_tech = file_of_interest[(file_of_interest["site_code_tech"] != "-") & (file_of_interest["site_code_dwh"] != "-") & (file_of_interest["site_code_tech"] != file_of_interest["site_code_dwh"])]

    in_tech_No_DWH_selected_cols = in_tech_No_DWH.drop(["site_code_dwh","total_data","total_voice"], axis=1)#, inplace=True)

    in_DWH_No_tech_selected_cols = in_DWH_No_tech.drop(["site_code_tech","total_data","total_voice"], axis=1)#, inplace=True)


    
    DWH_Not_Match_tech_selected_cols = DWH_Not_Match_tech.drop(["total_data","total_voice"], axis=1)#, inplace=True)

    if "in_tech_no_dwh" in f_name.lower():

        # print('in_tech_No_DWH_selected_cols')
        # selected_table = pd.read_sql(
        #     "SELECT * FROM in_tech_No_DWH WHERE year_num = "+year+" AND month_num = "+month, dbConnection)
        selected_table = in_tech_No_DWH_selected_cols

    elif "in_dwh_no_tech" in f_name.lower():

        # print('in_DWH_No_tech_selected_cols')
        # selected_table = pd.read_sql(
            # "SELECT * FROM in_DWH_No_tech WHERE year_num = "+year+" AND month_num = "+month, dbConnection)
        selected_table = in_DWH_No_tech_selected_cols
    else:

        # print("DWH_Not_Match_tech_selected_cols")
        # selected_table = pd.read_sql(
        #     "SELECT * FROM DWH_Not_Match_tech WHERE year_num = "+year+" AND month_num = "+month, dbConnection)
        
        selected_table = DWH_Not_Match_tech_selected_cols

    selected_table.to_csv(os.path.join(
        flaskApp.config['CSV_PATH'], secure_filename(f_name)))
    # selected_table.to_csv(os.path.join(
    #     flaskApp.config['CSV_PATH'], secure_filename(fle)))

    print("file saved.")

    return send_from_directory(flaskApp.config['CSV_PATH'], path=f_name, as_attachment=True)
    # return send_from_directory(flaskApp.config['CSV_PATH'], path=fle, as_attachment=True)
    # return "Done"


@flaskApp.route("/api/getAllSiteCodes", methods=['GET', 'POST'])
@cross_origin()
def GetSiteCodes():
    Site_codes = pd.read_sql(
        "SELECT DISTINCT Site_Code_tech FROM Merged_Revenue_Tech_With_Technology", dbConnection)

    # print("\n\n\nSite_codes")
    # print(Site_codes)
    # print('\n\n\n')

    # Convert the returned dataframe into list
    # Site_codes = Site_codes.fillna('-')
    Site_codes = list(Site_codes["site_code_tech"])
    # types = []
    # for s in Site_codes:
    #     # if type(s) is None:
    #     #     print("type(s) is None: ", s)
    #     # if type(s) is type(None):
    #     #     print("type(s) is type(None): ", s)
    #     if type(s) != str:
    #         print("type(s) != type(str): ", s)
                
    #     if isinstance(s, None):# s is None:
    #         print("s isinstance: ", s)

    #     # if len(s) < 2:
    #     #     print("\n <2: ", s)
    #     types.append(type(s))


    # print(set(types))

        
    # .sort()

    result = {}
    result["SiteCodes"] = Site_codes
    return result


# Done using site view which contains all data for all sites
# ? Does this view occupy permanent space, OR ONLY when I call it?????
@flaskApp.route("/api/showChartBySiteAndTechnology/<string:siteCode>/<string:technology>")
@cross_origin()
def ShowSiteChartsByTechnology(siteCode, technology):

    print("\n\nin api/showChartBySiteAndTechnology, selected technology is:")
    print(technology)

    if technology == 'no_technology_selected':
        print('no technology selected')
        Site_Revenues = pd.read_sql("SELECT * FROM Detailed_Sites_Revenue_With_Technology_Chart WHERE Site_Code_DWH = '" +
                                    siteCode + "'", dbConnection)

    else:
        Site_Revenues = pd.read_sql("SELECT * FROM Detailed_Sites_Revenue_With_Technology_Chart WHERE Site_Code_DWH = '" +
                                      siteCode + "' AND Status = '" + technology + "'", dbConnection)

    Site_Revenues = Site_Revenues.fillna(0)
    Site_Dates = Site_Revenues['year_num'].map(
        str) + "-" + Site_Revenues['month_num'].map(str).str.zfill(2)
    Site_Revenues.insert(2, "Site_Date", Site_Dates, True)

    Site_Revenues.sort_values(by="Site_Date", inplace=True)

    site_list = []
    site_obj = {}
    for rowIndex, row in Site_Revenues.iterrows():
        # Iterate through each cell in each row

        obj = {}
        obj = {
            "Date": row[2],
            # "Revenue": "{:,.3f}".format(maxRevenue),
            "Total_Revenue": "{:.3f}".format(row[5]),
            "Total_Data": "{:.3f}".format(row[6]),
            "Total_Voice": "{:.3f}".format(row[7]),
            "Roaming_Voice": "{:.3f}".format(row[17]),
            "Roaming_Data": "{:.3f}".format(row[18]),
            "In_Bound_Roam_Duration": "{:.3f}".format(row[11]),
            "Total_MB": "{:.3f}".format(row[10]),
            "National_Roam_Duration": "{:.3f}".format(row[12]),
            "Out_International_EGP": "{:.3f}".format(row[14]),
            "Roam_Data_MB": "{:.3f}".format(row[13]),

        }
        site_list.append(obj)

    site_obj[siteCode] = site_list
    return site_obj


@flaskApp.route("/api/getNetworkRevenues", methods=['GET', 'POST'])
@cross_origin()
def GetNetworkRevenues():

    Network_Revenues = pd.read_sql(
        "SELECT * FROM Detailed_Network_Revenue_Chart", dbConnection)

    Network_Revenues = Network_Revenues.fillna(0)
    Years_Months = Network_Revenues['year_num'].map(
        str) + "-" + Network_Revenues['month_num'].map(str).str.zfill(2)
    Network_Revenues.insert(2, "Years_Months", Years_Months, True)

    # order dates ascending
    Network_Revenues.sort_values(by="Years_Months", inplace=True)

    # print(Network_Revenues.dtypes)
    # return ""

    network_list = []
    network_obj = {}
    for rowIndex, row in Network_Revenues.iterrows():
        # Iterate through each cell in each row

        obj = {}
        obj = {
            "Date": row[2],
            # "Revenue": "{:,.3f}".format(maxRevenue),
            "Total_Revenue": "{:.3f}".format(row[5]),
            "Total_Data": "{:.3f}".format(row[3]),
            "Total_Voice": "{:.3f}".format(row[5]),
            "Roaming_Voice": "{:.3f}".format(row[15]),
            "Roaming_Data": "{:.3f}".format(row[16]),
            "In_Bound_Roam_Duration": "{:.3f}".format(row[9]),
            "Total_MB": "{:.3f}".format(row[8]),
            "National_Roam_Duration": "{:.3f}".format(row[10]),
            "Out_International_EGP": "{:.3f}".format(row[12]),
            "Roam_Data_MB": "{:.3f}".format(row[11]),

        }
        network_list.append(obj)

    network_obj["Network_Chart"] = network_list
    return network_obj
