
from turtle import left
import numpy as np
import pandas as pd
from cmath import nan
from io import BytesIO
from urllib import response
import json
from importlib.resources import path
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Response, flash, render_template, request, redirect, safe_join, send_file, url_for, jsonify, send_from_directory,abort
from flask_cors import CORS, cross_origin
# import turbodbc
import sqlalchemy
from sqlalchemy import FLOAT, Float, Integer, String, create_engine
from sqlalchemy import types
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import date
from werkzeug.utils import secure_filename
import os
from flask_script import Manager, Server

Revenue_Tech_Table = pd.DataFrame()
Revenue_Dwh_Table = pd.DataFrame()

flaskApp = Flask(__name__)

# manager = Manager(flaskApp)
# @manager.command
# def runserver():

#     flaskApp.run(debug=True,host="0.0.0.0",use_reloader=True)
#     LoadMainTables()


# class CustomServer(Server):
#     def __call__(self, app, *args, **kwargs):
#         LoadMainTables()
#         return Server.__call__(self, app, *args, **kwargs)

# manager.add_command('run', CustomServer(flaskApp))

DB_SERVER_NAME = '.'
DB_NAME = 'TrackRevenue'
DB_DRIVER = 'ODBC Driver 17 for SQL Server'
DB_CONNECTION_STRING = f'mssql://@{DB_SERVER_NAME}/{DB_NAME}?driver={DB_DRIVER}'
print("\n==> Your SQL connection string is:")
print(DB_CONNECTION_STRING)
print("\n")

DB_ENGINE = create_engine(DB_CONNECTION_STRING, fast_executemany=True)
DB_CONNECTION = DB_ENGINE.connect()
session = sessionmaker(DB_ENGINE)

upload_folder = "/uploadedExcelFiles"
if not os.path.exists(upload_folder):
    print("Folder NOT EXIST")
    os.mkdir(upload_folder)
    print("Folder CREATED")

# Temporary folder, will not be created
flaskApp.config['CSV_PATH'] = upload_folder



CORS(flaskApp)#, support_credentials=True, expose_headers='Authorization', resources={r"/api/*": {"origins": "*"}})
# this secret key is used to protect my form from attacks
flaskApp.config['SECRET_KEY'] = 'form_password' # assign any value I want
# flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alchemyDB/excel.db'
excelDB = SQLAlchemy(flaskApp)

######### NOT USED #########
# SiteRevenue ==> DWH
# CellMapping ==> Tech
@flaskApp.route('/api/uploadExcelFiles', methods=['GET', 'POST'])
@cross_origin()
def UploadExcelFiles():

    uploaded_file_names = list(request.form.keys())
    print("\n.................")
    print(request.form)
    print("\n.................")
    print(request.files)
    print("\n.................")
    print("\n\n>> Uploaded_files:")
    print(uploaded_file_names)
    site_revenue = list(filter(lambda x: 'revenue' in x.lower(), uploaded_file_names))
    site_revenue_file = site_revenue[0]
    cell_mapping_report = list(filter(lambda x: 'cell' in x.lower(), uploaded_file_names))
    cell_mapping_file = cell_mapping_report[0]

    # site_revenue_file="Site_Revenue_Jan2022.xlsx"
    # cell_mapping_file="CellMappingReport_Jan2022.xlsx"

    print('---------')
    print("final file names: ", site_revenue_file)
    print("final file names: ", cell_mapping_file)
    print('---------')


    pd_site_revenue = pd.read_excel(site_revenue_file)
    pd_site_revenue = pd_site_revenue.applymap(str)
    print(">> site revenue loaded and converted to string.")


    pd_cell_mapping = pd.read_excel(cell_mapping_file)
    pd_cell_mapping = pd_cell_mapping.applymap(str)
    
    print(">> cell mapping loaded and converted to string.")

    Dwh_LAC_CI = pd_site_revenue["LAC"] + "-" + pd_site_revenue["Cell_Id"]
    print("Dwh_lac_ci created")
    tech_LAC_CI = pd_cell_mapping["LAC"] + "-" + pd_cell_mapping["CI"]
    print("tech_lac_ci created")

    full_date = datetime.datetime.now()
    current_month = full_date.strftime("%b")
    current_year = str(full_date.year)

    pd_cell_mapping.insert(0, "LAC_CI", tech_LAC_CI, True)
    pd_site_revenue.insert(5, "LAC_CI", Dwh_LAC_CI, True)
   
   #TEST
    # pd_cell_mapping.to_csv("cell_mapping_With_LAC_CI_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)
    # pd_site_revenue.to_csv("site_revenue_With_LAC_CI_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)

    pd_cell_mapping.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename("Cell_mapping_"+current_month+"_"+current_year+".csv")))
    pd_site_revenue.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename("Site_revenue_"+current_month+"_"+current_year+".csv")))


    # Clean el data before left join
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "No lookup for Cell"), 'Site_Code_DWH'] = '-'
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "Cell with no Site Code"), 'Site_Code_DWH'] = '-'
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "CDR with No Cell"), 'Site_Code_DWH'] = '-'

    # VlookUp Step el mafrod:
    left_join_result = pd.merge(pd_site_revenue, pd_cell_mapping, on="LAC_CI", suffixes=('_DWH', '_tech'), how="inner")# how='left')
    print("left_join_result.shape")
    print(left_join_result.shape)

    left_join_result.columns = left_join_result.columns.str.strip() #remove white spaces around column names

    left_join_result.rename(columns={"SITE CODE": "Site_Code_tech"}, inplace=True)
    print("site code renamed")
    left_join_result.rename(columns={"Site_Name": "Site_Name_DWH"}, inplace=True)
    print("site name 1 renamed")
    left_join_result.rename(columns={"SITE NAME": "Site_Name_tech"}, inplace=True)
    print("site name 2 renamed")
    left_join_result.rename(columns={"CI": "CI_tech"}, inplace=True)
    print("CI renamed")
    left_join_result.rename(columns={"\\xa0LONG_DEC": "LONG_DEC"}, inplace=True)
    print("long dec renamed")
    left_join_result.rename(columns={"LAT_DEC ": "LAT_DEC"}, inplace=True)
    print("lat dec renamed")

    # left_join_result = lambda left_join_result: (for i in left_join_result : ' '.join(i.split()))


    left_join_result.drop(['Site_Name_tech','CI_tech','LAC_tech','TECHNOLOGY', 'Radio_Frequency_ID','RNC_BSC','LAT_DEC','LONG_DEC','Site Type','Comment'], axis=1, inplace=True)

    print('\n\n\nb3d el drop ady asamy el columns:')
    print(list(left_join_result.columns))
    print('\n\n\n\n')
    

    # Save the merged table to DB:
    """
    if_exists: {'fail', 'replace', 'append'}, default 'fail'
        fail: If table exists, do nothing.
        replace: If table exists, drop it, recreate it, and insert data.
        append: If table exists, insert data. Create if does not exist.
    """
    # left_join_result.to_sql('Revenue_Tech', con=DB_ENGINE, if_exists='append', index=False)
    
    left_join_result["Site_Name_DWH"] = left_join_result["Site_Name_DWH"].fillna('-')
    left_join_result.loc[(left_join_result.Site_Name_DWH == "nan"), 'Site_Name_DWH'] = '-'
    
    left_join_result["Status"] = left_join_result["Status"].fillna('-')
    left_join_result.loc[(left_join_result.Status == "?"), 'Status'] = '-'

    left_join_result = left_join_result.fillna(0);

    left_join_result.to_csv("left_join_result__.csv", encoding='utf-8', index=False)

    print("NaNs handeled")

    left_join_result.to_sql('Merged_DWH_Tech', con=DB_ENGINE, if_exists='append',
    dtype={'Year_Num': Integer(),'Month_Num': Integer(),
        'DWH_CELL': Integer(),
        'Cell_Id': Integer(),
        'LAC_DWH': Integer(),
        'LAC_CI': String(20),
        'Market_Zone': String(20),
        'Status': String(10),
        'Governorate': String(25),
        'Northing': String(20),
        'Easting': String(20),
        'Geo_Lookup': String(50),
        'Site_Code_DWH': String(50),
        'Site_Name_DWH': String(100),
        'Total_Out_Duration': Float(),
        'Out_International_Duration': Float(),
        'Incoming_Duration': Float(),
        'Total_MB':Float(),
        'Total_MB_2G':Float(),
        'Total_MB_3G':Float(),
        'Total_MB_4G':Float(),
        'In_Bound_Roam_Duration':Float(),
        'National_Roam_Duration':Float(),
        'Roam_Data_MB':Float(),
        'Total_Out_REV_EGP':Float(),
        'Out_International_EGP':Float(),
        'Total_MB_REV_EGP':Float(),
        'Total_MB_2G_REV_EGP':Float(),
        'Total_MB_3G_REV_EGP':Float(),
        'Total_MB_4G_REV_EGP':Float(),
        'In_Bound_Roaming_REV_EGP':Float(),
        'National_Roaming_REV_EGP':Float(),
        'Roam_Data_MB_REV_EGP':Float(),
        'Total_Revenue':Float(),
        'Site_Code_tech': String(50)}, index=False, method='multi',chunksize=3000)

    # test = pd.read_sql_query("SELECT * FROM Merged_DWH_Tech", DB_CONNECTION)


    # # cursor = DB_CONNECTION.cursor()
    # query = f"INSERT INTO Merged_DWH_Tech SELECT * FROM {left_join_result}"
    # print("\n\n\n\nSQL query")

    # print(query)
    # print('\n\n\n\n\n')
    # results = DB_CONNECTION.execute(query)#.fetchall()
    
    # # DB_CONNECTION.commit()
    
    # print("\n\n\n\nSQL Result")

    # print(results)
    print('\n\n\n\n\nData Inserted.')
    return ""


    # left_join_result.to_sql('Merged_DWH_Tech', con=DB_ENGINE, if_exists='append', index=False)

    left_join_result.to_csv("NEW_mergedTables_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)

    left_join_result.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename("mergedTables_"+current_month+"_"+current_year+".csv")))

    # file_of_interest = left_join_result[["LAC_CI","Site_Code_DWH","Site_Code_tech","Total_Revenue","Total_MB_REV_EGP","Total_Out_REV_EGP","TECHNOLOGY"]]
    file_of_interest = left_join_result[["LAC_CI","Site_Code_DWH","Site_Code_tech","Total_Revenue","Total_MB_REV_EGP","Total_Out_REV_EGP","Status"]]

    file_of_interest.rename(columns={"Total_MB_REV_EGP": "Total_Data"}, inplace=True)
    file_of_interest.rename(columns={"Total_Out_REV_EGP": "Total_Voice"}, inplace=True)


    file_of_interest["Site_Code_tech"] = file_of_interest["Site_Code_tech"].fillna('-')

    # file_of_interest.to_csv("file_of_interest_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)
    file_of_interest.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename("file_of_interest_"+current_month+"_"+current_year+".csv")))

    print("\n\nYOUR IMPORTANT FILE IS READY!!!!!!!!!!!!!")
    print("file_of_interest[Site_Code_tech].unique()")
    print(file_of_interest["Site_Code_tech"].unique())


    in_tech_No_DWH = file_of_interest[(file_of_interest["Site_Code_tech"] != "-") & (file_of_interest["Site_Code_DWH"] == "-")]
    in_DWH_No_tech = file_of_interest[(file_of_interest["Site_Code_tech"] == "-") & (file_of_interest["Site_Code_DWH"] != "-")]
    DWH_Not_Match_tech = file_of_interest[(file_of_interest["Site_Code_tech"] != "-") & (file_of_interest["Site_Code_DWH"] != "-") & (file_of_interest["Site_Code_tech"] != file_of_interest["Site_Code_DWH"])]

    in_tech_No_DWH_selected_cols = in_tech_No_DWH[["Site_Code_tech","Site_Code_DWH","Total_Revenue"]]
    in_DWH_No_tech_selected_cols = in_DWH_No_tech[["Site_Code_tech","Site_Code_DWH","Total_Revenue"]]
    DWH_Not_Match_tech_selected_cols = DWH_Not_Match_tech[["Site_Code_tech","Site_Code_DWH","Total_Revenue"]]

    # in_tech_No_DWH_selected_cols.to_csv("in_tech_No_DWH_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)
    # in_DWH_No_tech_selected_cols.to_csv("in_DWH_No_tech_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)
    # DWH_Not_Match_tech_selected_cols.to_csv("DWH_Not_Match_tech_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)

    in_tech_No_DWH_selected_cols.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename("in_tech_No_DWH_"+current_month+"_"+current_year+".csv")))
    in_DWH_No_tech_selected_cols.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename("in_DWH_No_tech_"+current_month+"_"+current_year+".csv")))
    DWH_Not_Match_tech_selected_cols.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename("DWH_Not_Match_tech_"+current_month+"_"+current_year+".csv")))

    print(">> All files saved.")
    print("shape of saved files is: ", in_tech_No_DWH_selected_cols.shape, in_DWH_No_tech_selected_cols.shape, DWH_Not_Match_tech_selected_cols.shape)


    print("DWH_Not_Match_tech_selected_cols.shape")
    print(DWH_Not_Match_tech_selected_cols.shape)

    in_tech_No_DWH_list = []
    for rowIndex, row in in_tech_No_DWH_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            "Site_Code_tech":row[0],
            "Site_Code_DWH":row[1],
            "Total_Revenue":row[2]
        }
        in_tech_No_DWH_list.append(row_obj)
    
    in_tech_No_DWH_total_revenue = in_tech_No_DWH_selected_cols["Total_Revenue"].map(float).sum()
    # print("in_tech_No_DWH_total_revenue")
    # print(in_tech_No_DWH_total_revenue)

    in_DWH_No_tech_list = []
    for rowIndex, row in in_DWH_No_tech_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            "Site_Code_tech":row[0],
            "Site_Code_DWH":row[1],
            "Total_Revenue":row[2]
        }
        in_DWH_No_tech_list.append(row_obj)


    # print("\n\n\n\nin_DWH_No_tech_list:\n\n")
    # print(type(in_DWH_No_tech_list))
    # print(len(in_DWH_No_tech_list))
    # print(in_DWH_No_tech_list[0])

    in_DWH_No_tech_total_revenue = in_DWH_No_tech_selected_cols["Total_Revenue"].map(float).sum()
    # print("in_DWH_No_tech_total_revenue")
    # print(in_DWH_No_tech_total_revenue)

    DWH_Not_Match_tech_list = []
    for rowIndex, row in DWH_Not_Match_tech_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            "Site_Code_tech":row[0],
            "Site_Code_DWH":row[1],
            "Total_Revenue":row[2]
        }
        DWH_Not_Match_tech_list.append(row_obj)
    
    DWH_Not_Match_tech_total_revenue = DWH_Not_Match_tech_selected_cols["Total_Revenue"].map(float).sum()

    Total_Revenue = file_of_interest["Total_Revenue"].map(float).sum()
    Total_Data = file_of_interest["Total_Data"].map(float).sum()
    Total_Voice = file_of_interest["Total_Voice"].map(float).sum()

    response ={
        "Total_Revenue":"{:,.2f}".format(Total_Revenue),
        "Total_Data":"{:,.2f}".format(Total_Data),
        "Total_Voice":"{:,.2f}".format(Total_Voice),
        "in_tech_No_DWH":{
            "in_tech_No_DWH_list":in_tech_No_DWH_list,
            "in_tech_No_DWH_total_revenue":"{:,.2f}".format(in_tech_No_DWH_total_revenue),
            # "in_tech_No_DWH_buffer":"in_tech_No_DWH_buffer",
            "in_tech_No_DWH_buffer":"in_tech_No_DWH.csv"
        },
        
        "in_DWH_No_tech":{
            "in_DWH_No_tech_list":in_DWH_No_tech_list,
            "in_DWH_No_tech_total_revenue":"{:,.2f}".format(in_DWH_No_tech_total_revenue),
            # "in_DWH_No_tech_buffer":"in_DWH_No_tech_buffer"
            "in_DWH_No_tech_buffer":"in_DWH_No_tech.csv"
        },
        "DWH_Not_Match_tech":{
            "DWH_Not_Match_tech_list":DWH_Not_Match_tech_list,
            "DWH_Not_Match_tech_total_revenue":"{:,.2f}".format(DWH_Not_Match_tech_total_revenue),
            "DWH_Not_Match_tech_buffer":"DWH_Not_Match_tech.csv"
            # "DWH_Not_Match_tech_buffer":""
        },

    }

    return response
 

 # I am getting data from DWH table, Should I use it or Revenue_tech or the new merged table ???
@flaskApp.route('/api/getAllYearsMonths', methods=['GET','POST'])
@cross_origin()
def GetYearsMonths():

    ALL_Years_Months = pd.read_sql_query("SELECT DISTINCT (Year_Month) FROM Merged_DWH_Tech_Jan_March ORDER BY Year_Month", DB_CONNECTION)

    result = {}
    result["YearsMonthsList"] = list(ALL_Years_Months["Year_Month"])
    # Years_Months_Table = pd.read_sql_query("SELECT DISTINCT (Revenue_DWH_ORG_BackUp.[Year]), Revenue_DWH_ORG_BackUp.[Month] FROM Revenue_DWH_ORG_BackUp ORDER BY Revenue_DWH_ORG_BackUp.[Year], Revenue_DWH_ORG_BackUp.[Month]", DB_CONNECTION)
    # ALL_Years_Months = Years_Months_Table["Year"].astype(str)+'-'+Years_Months_Table["Month"].astype(str).str.zfill(2)

    # result = {}
    # result["YearsMonthsList"] = list(ALL_Years_Months)
    return result


@flaskApp.route("/api/getMonthRevenues/<string:YearMonth>", methods=['GET','POST'])
@cross_origin()
def GetRevenuePerMonth(YearMonth):

    year = YearMonth.split('-')[0]
    month = YearMonth.split('-')[1]
    
    print(year, " ", month)
    # query = "SELECT * FROM Merged_DWH_Tech_Jan_March WHERE Year_Month = '"+YearMonth+"'"
    # query = "SELECT * FROM in_tech_No_DWH WHERE Year_Month = '"+YearMonth+"'"

    # Dwh_Revenue_Table = pd.read_sql_query("SELECT * FROM Revenue_DWH_ORG_BackUp WHERE Revenue_DWH_ORG_BackUp.[Year] = "+year+" AND Revenue_DWH_ORG_BackUp.[Month] = "+ month, DB_CONNECTION)
    Dwh_Revenue_Table = pd.read_sql_query("SELECT * FROM Merged_DWH_Tech_Jan_March WHERE Year_Month = '"+YearMonth+"'", DB_CONNECTION)
    in_tech_No_DWH_selected_cols = pd.read_sql_query("SELECT * FROM in_tech_No_DWH WHERE Year_Month = '"+YearMonth+"'", DB_CONNECTION)
    in_DWH_No_tech_selected_cols = pd.read_sql_query("SELECT * FROM in_DWH_No_tech WHERE Year_Month = '"+YearMonth+"'", DB_CONNECTION)
    Dwh_Not_Match_tech_selected_cols = pd.read_sql_query("SELECT * FROM DWH_Not_Match_tech WHERE Year_Month = '"+YearMonth+"'", DB_CONNECTION)


    in_tech_No_DWH_list = []
    for rowIndex, row in in_tech_No_DWH_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            "Site_Code_tech":row[2],
            "Site_Code_DWH":'-',
            "Total_Revenue":row[3]
        }
        in_tech_No_DWH_list.append(row_obj)
    
    in_tech_No_DWH_total_revenue = in_tech_No_DWH_selected_cols["Total_Revenue"].map(float).sum()
    # print("in_tech_No_DWH_total_revenue")
    # print(in_tech_No_DWH_total_revenue)

    in_DWH_No_tech_list = []
    for rowIndex, row in in_DWH_No_tech_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            # "Site_Code_tech":row[0],
            "Site_Code_tech":'-',
            "Site_Code_DWH":row[2],
            "Total_Revenue":row[3]
        }
        in_DWH_No_tech_list.append(row_obj)

    in_DWH_No_tech_total_revenue = in_DWH_No_tech_selected_cols["Total_Revenue"].map(float).sum()

    Dwh_Not_Match_tech_list = []
    for rowIndex, row in Dwh_Not_Match_tech_selected_cols.iterrows():
        # Iterate through each cell in each row
        row_obj = {}
        row_obj = {
            "Site_Code_tech":row[3],
            "Site_Code_DWH":row[2],
            "Total_Revenue":row[4]
        }
        Dwh_Not_Match_tech_list.append(row_obj)
    
    Dwh_Not_Match_tech_total_revenue = Dwh_Not_Match_tech_selected_cols["Total_Revenue"].map(float).sum()

    Dwh_Revenue_Table.rename(columns={"Total_MB_REV_EGP": "Total_Data"}, inplace=True)
    Dwh_Revenue_Table.rename(columns={"Total_Out_REV_EGP": "Total_Voice"}, inplace=True)

    print("\n\n")
    print(Dwh_Revenue_Table)
    print("\n\n")


    Total_Revenue = Dwh_Revenue_Table["Total_Revenue"].map(float).sum()
    Total_Data = Dwh_Revenue_Table["Total_Data"].map(float).sum()
    Total_Voice = Dwh_Revenue_Table["Total_Voice"].map(float).sum()

    response ={
        "Total_Revenue":"{:,.2f}".format(Total_Revenue),
        "Total_Data":"{:,.2f}".format(Total_Data),
        "Total_Voice":"{:,.2f}".format(Total_Voice),
        "in_tech_No_DWH":{
            "in_tech_No_DWH_list":in_tech_No_DWH_list,
            "in_tech_No_DWH_total_revenue":"{:,.2f}".format(in_tech_No_DWH_total_revenue),
            # "in_tech_No_DWH_buffer":"in_tech_No_DWH_buffer",
            "in_tech_No_DWH_buffer":"in_tech_No_DWH.csv"
        },
        
        "in_DWH_No_tech":{
            "in_DWH_No_tech_list":in_DWH_No_tech_list,
            "in_DWH_No_tech_total_revenue":"{:,.2f}".format(in_DWH_No_tech_total_revenue),
            # "in_DWH_No_tech_buffer":"in_DWH_No_tech_buffer"
            "in_DWH_No_tech_buffer":"in_DWH_No_tech.csv"
        },
        "DWH_Not_Match_tech":{
            "DWH_Not_Match_tech_list":Dwh_Not_Match_tech_list,
            "DWH_Not_Match_tech_total_revenue":"{:,.2f}".format(Dwh_Not_Match_tech_total_revenue),
            "DWH_Not_Match_tech_buffer":"DWH_Not_Match_tech.csv"
            # "DWH_Not_Match_tech_buffer":""
        },

    }

    return response

@flaskApp.route("/api/downloadFiles/<path:file_name>", methods=['GET','POST'])
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

    fle = f_name+file_date

    for filename in os.listdir(flaskApp.config['CSV_PATH']):
        print("\n\n>>", filename)
        print("\n")
        if filename == fle:
            print("\n\n\nl2etooooooooo\n\n\n")
            return send_from_directory(flaskApp.config['CSV_PATH'], filename=fle, as_attachment=True)

    selected_table = ""

    if "in_tech_no_dwh" in f_name.lower():
        selected_table = pd.read_sql_query("SELECT * FROM in_tech_No_DWH WHERE Year_Month = '"+file_date+"'", DB_CONNECTION)
    elif "in_dwh_no_tech" in f_name.lower():
        selected_table = pd.read_sql_query("SELECT * FROM in_DWH_No_tech WHERE Year_Month = '"+file_date+"'", DB_CONNECTION)
    else:
        selected_table = pd.read_sql_query("SELECT * FROM DWH_Not_Match_tech WHERE Year_Month = '"+file_date+"'", DB_CONNECTION)

    selected_table.to_csv(os.path.join(flaskApp.config['CSV_PATH'], secure_filename(file_name)))
    
    return send_from_directory(flaskApp.config['CSV_PATH'], filename=file_name, as_attachment=True)
    # return "Done"

# Retrieve all data for all site codes
@flaskApp.route("/api/getAllSitesRevenues", methods=['GET', 'POST'])
@cross_origin()
def Show_Sites_Charts():

    Total_Revenue_Pivot_Table = pd.read_sql_query("SELECT * FROM Total_Revenue_Pivot_Table", DB_CONNECTION)
    Data_Revenue_Pivot_Table = pd.read_sql_query("SELECT * FROM Data_Revenue_Pivot_Table", DB_CONNECTION)
    Roaming_Data_Revenue_Pivot_Table = pd.read_sql_query("SELECT * FROM Roaming_Data_Revenue_Pivot_Table", DB_CONNECTION)
    Roaming_Voice_Revenue_Pivot_Table = pd.read_sql_query("SELECT * FROM Roaming_Voice_Revenue_Pivot_Table", DB_CONNECTION)
    Voice_Revenue_Pivot_Table = pd.read_sql_query("SELECT * FROM Voice_Revenue_Pivot_Table", DB_CONNECTION)


    Total_Revenue_Pivot_Table = Total_Revenue_Pivot_Table.reindex(sorted(Total_Revenue_Pivot_Table.columns), axis=1)
    Data_Revenue_Pivot_Table = Data_Revenue_Pivot_Table.reindex(sorted(Data_Revenue_Pivot_Table.columns), axis=1)
    Roaming_Data_Revenue_Pivot_Table = Roaming_Data_Revenue_Pivot_Table.reindex(sorted(Roaming_Data_Revenue_Pivot_Table.columns), axis=1)
    Roaming_Voice_Revenue_Pivot_Table = Roaming_Voice_Revenue_Pivot_Table.reindex(sorted(Roaming_Voice_Revenue_Pivot_Table.columns), axis=1)
    Voice_Revenue_Pivot_Table = Voice_Revenue_Pivot_Table.reindex(sorted(Voice_Revenue_Pivot_Table.columns), axis=1)
    print("Tables' columns sorted")
    print(Total_Revenue_Pivot_Table.shape[0])
    
    Total_Revenue_Pivot_Table.set_index('ShortCode', inplace=True)
    Data_Revenue_Pivot_Table.set_index('ShortCode', inplace=True)
    Roaming_Data_Revenue_Pivot_Table.set_index('ShortCode', inplace=True)
    Roaming_Voice_Revenue_Pivot_Table.set_index('ShortCode', inplace=True)
    Voice_Revenue_Pivot_Table.set_index('ShortCode', inplace=True)
    print("set indexes")

    # Handling NaN values
    Total_Revenue_Pivot_Table = Total_Revenue_Pivot_Table.fillna(0);
    Data_Revenue_Pivot_Table = Data_Revenue_Pivot_Table.fillna(0);
    Roaming_Data_Revenue_Pivot_Table = Roaming_Data_Revenue_Pivot_Table.fillna(0);
    Roaming_Voice_Revenue_Pivot_Table = Roaming_Voice_Revenue_Pivot_Table.fillna(0);
    Voice_Revenue_Pivot_Table = Voice_Revenue_Pivot_Table.fillna(0);
    print("NaNs handeled")

    all_sites_revenue_list = {}
    stop = 0

    for row_index, row in Total_Revenue_Pivot_Table.iterrows():
        site_list = []
        if stop == 100:
            break
        stop = stop + 1

        # how to handle NULL site code
        if type(row_index) == type(None):
            print("NULL SITE_CODE!!!!!!!!!!!")
            continue
        
        for cell_index in range(len(row)):

            if Total_Revenue_Pivot_Table.columns[cell_index] == 'ShortCode':
                # site_code = row_index
                continue
            maxRevenue = max(max(row),
            max(Data_Revenue_Pivot_Table.loc[row_index]),
            max(Voice_Revenue_Pivot_Table.loc[row_index]),
            max(Roaming_Voice_Revenue_Pivot_Table.loc[row_index]),
            max(Roaming_Data_Revenue_Pivot_Table.loc[row_index]))

            obj = {
                "Date": Total_Revenue_Pivot_Table.columns[cell_index],
                "Revenue": "{:,.3f}".format(maxRevenue),
                "Total_Revenue": "{:,.3f}".format(row[cell_index]),
                "Total_Data":"{:,.3f}".format(Data_Revenue_Pivot_Table.loc[row_index][cell_index]),
                "Total_Voice":"{:,.3f}".format(Voice_Revenue_Pivot_Table.loc[row_index][cell_index]),
                "Roaming_Voice":"{:,.3f}".format(Roaming_Voice_Revenue_Pivot_Table.loc[row_index][cell_index]),
                "Roaming_Data":"{:,.3f}".format(Roaming_Data_Revenue_Pivot_Table.loc[row_index][cell_index])
            }

            site_list.append(obj)

        all_sites_revenue_list[row_index] = site_list

    return all_sites_revenue_list

@flaskApp.route("/api/getAllSiteCodes",methods=['GET','POST'])
@cross_origin()
def GetSiteCodes():
    Site_codes = pd.read_sql_query("SELECT ShortCode FROM Total_Revenue_Pivot_Table", DB_CONNECTION)
    # Convert the returned datframe into list
    Site_codes = list(Site_codes["ShortCode"])

    result = {}
    result["SiteCodes"] = Site_codes
    return result

######### NOT USED #########
@flaskApp.route("/api/showChartBySite/<string:siteCode>", methods=['GET','POST'])
@cross_origin()
def ShowSiteCharts(siteCode):

    Total_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Data_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Data_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Roaming_Data_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Roaming_Data_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Roaming_Voice_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Roaming_Voice_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Voice_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Voice_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    
    # Additional Requirements:
    Total_In_Bound_Roam_Duration_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_In_Bound_Roam_Duration_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Total_MB_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_MB_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Total_National_Roam_Duration_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_National_Roam_Duration_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Total_Out_International_EGP_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Out_International_EGP_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Total_Roam_Data_MB_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Roam_Data_MB_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    
    print("Shape of pivot records: ", Total_Revenue_Pivot_Record.shape)

    Total_Revenue_Pivot_Record = Total_Revenue_Pivot_Record.reindex(sorted(Total_Revenue_Pivot_Record.columns), axis=1)
    Data_Revenue_Pivot_Record = Data_Revenue_Pivot_Record.reindex(sorted(Data_Revenue_Pivot_Record.columns), axis=1)
    Roaming_Data_Revenue_Pivot_Record = Roaming_Data_Revenue_Pivot_Record.reindex(sorted(Roaming_Data_Revenue_Pivot_Record.columns), axis=1)
    Roaming_Voice_Revenue_Pivot_Record = Roaming_Voice_Revenue_Pivot_Record.reindex(sorted(Roaming_Voice_Revenue_Pivot_Record.columns), axis=1)
    Voice_Revenue_Pivot_Record = Voice_Revenue_Pivot_Record.reindex(sorted(Voice_Revenue_Pivot_Record.columns), axis=1)
    
    # Additional Requirements:
    Total_In_Bound_Roam_Duration_Pivot_Record = Total_In_Bound_Roam_Duration_Pivot_Record.reindex(sorted(Total_In_Bound_Roam_Duration_Pivot_Record.columns), axis=1)
    Total_MB_Pivot_Record = Total_MB_Pivot_Record.reindex(sorted(Total_MB_Pivot_Record.columns), axis=1)
    Total_National_Roam_Duration_Pivot_Record = Total_National_Roam_Duration_Pivot_Record.reindex(sorted(Total_National_Roam_Duration_Pivot_Record.columns), axis=1)
    Total_Out_International_EGP_Pivot_Record = Total_Out_International_EGP_Pivot_Record.reindex(sorted(Total_Out_International_EGP_Pivot_Record.columns), axis=1)
    Total_Roam_Data_MB_Pivot_Record = Total_Roam_Data_MB_Pivot_Record.reindex(sorted(Total_Roam_Data_MB_Pivot_Record.columns), axis=1)
    
    
    print("Records' columns sorted")

    # Handling NaN values
    Total_Revenue_Pivot_Record = Total_Revenue_Pivot_Record.fillna(0)
    Data_Revenue_Pivot_Record = Data_Revenue_Pivot_Record.fillna(0)
    Roaming_Data_Revenue_Pivot_Record = Roaming_Data_Revenue_Pivot_Record.fillna(0)
    Roaming_Voice_Revenue_Pivot_Record = Roaming_Voice_Revenue_Pivot_Record.fillna(0)
    Voice_Revenue_Pivot_Record = Voice_Revenue_Pivot_Record.fillna(0)

    # Additional Requirements:
    Total_In_Bound_Roam_Duration_Pivot_Record = Total_In_Bound_Roam_Duration_Pivot_Record.fillna(0)
    Total_MB_Pivot_Record = Total_MB_Pivot_Record.fillna(0)
    Total_National_Roam_Duration_Pivot_Record = Total_National_Roam_Duration_Pivot_Record.fillna(0)
    Total_Out_International_EGP_Pivot_Record = Total_Out_International_EGP_Pivot_Record.fillna(0)
    Total_Roam_Data_MB_Pivot_Record = Total_Roam_Data_MB_Pivot_Record.fillna(0)
    
    print("NaNs handeled")

    site_list = []
    site_obj = {}
    for cell_index in range(len(Total_Revenue_Pivot_Record.columns)):

        if Total_Revenue_Pivot_Record.columns[cell_index] == 'ShortCode':
            continue

        obj = {
            "Date": Total_Revenue_Pivot_Record.columns[cell_index],
            # "Revenue": "{:,.3f}".format(maxRevenue),
            "Total_Revenue": "{:.3f}".format(Total_Revenue_Pivot_Record.loc[0][cell_index]),
            "Total_Data":"{:.3f}".format(Data_Revenue_Pivot_Record.loc[0][cell_index]),
            "Total_Voice":"{:.3f}".format(Voice_Revenue_Pivot_Record.loc[0][cell_index]),
            "Roaming_Voice":"{:.3f}".format(Roaming_Voice_Revenue_Pivot_Record.loc[0][cell_index]),
            "Roaming_Data":"{:.3f}".format(Roaming_Data_Revenue_Pivot_Record.loc[0][cell_index]),
            "In_Bound_Roam_Duration":"{:.3f}".format(Total_In_Bound_Roam_Duration_Pivot_Record.loc[0][cell_index]),
            "Total_MB":"{:.3f}".format(Total_MB_Pivot_Record.loc[0][cell_index]),
            "National_Roam_Duration":"{:.3f}".format(Total_National_Roam_Duration_Pivot_Record.loc[0][cell_index]),
            "Out_International_EGP":"{:.3f}".format(Total_Out_International_EGP_Pivot_Record.loc[0][cell_index]),
            "Roam_Data_MB":"{:.3f}".format(Total_Roam_Data_MB_Pivot_Record.loc[0][cell_index]),
            # "Roaming_Data":"{:.3f}".format(Roaming_Data_Revenue_Pivot_Record.loc[0][cell_index]),
        }

        site_list.append(obj)

    site_obj[siteCode] = site_list
    return site_obj

# Use same queries as above, but with the new tables "_With_Technology"
@flaskApp.route("/api/showChartBySiteAndTechnology/<string:siteCode>/<string:technology>")
@cross_origin()
def ShowSiteChartsByTechnology(siteCode, technology):

    
    Total_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Revenue_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Data_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Data_Revenue_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Roaming_Data_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Roaming_Data_Revenue_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Roaming_Voice_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Roaming_Voice_Revenue_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Voice_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Voice_Revenue_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    
    # Additional Requirements:
    Total_In_Bound_Roam_Duration_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_In_Bound_Roam_Duration_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Total_MB_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_MB_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Total_National_Roam_Duration_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_National_Roam_Duration_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Total_Out_International_EGP_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Out_International_EGP_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    Total_Roam_Data_MB_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Roam_Data_MB_With_Technology_Pivot_Table WHERE Site_Code_DWH = '"+siteCode+"' AND Status = '"+technology+"'", DB_CONNECTION)
    
    print("Shape of pivot records: ", Total_Revenue_Pivot_Record.shape)

    Total_Revenue_Pivot_Record = Total_Revenue_Pivot_Record.reindex(sorted(Total_Revenue_Pivot_Record.columns), axis=1)
    Data_Revenue_Pivot_Record = Data_Revenue_Pivot_Record.reindex(sorted(Data_Revenue_Pivot_Record.columns), axis=1)
    Roaming_Data_Revenue_Pivot_Record = Roaming_Data_Revenue_Pivot_Record.reindex(sorted(Roaming_Data_Revenue_Pivot_Record.columns), axis=1)
    Roaming_Voice_Revenue_Pivot_Record = Roaming_Voice_Revenue_Pivot_Record.reindex(sorted(Roaming_Voice_Revenue_Pivot_Record.columns), axis=1)
    Voice_Revenue_Pivot_Record = Voice_Revenue_Pivot_Record.reindex(sorted(Voice_Revenue_Pivot_Record.columns), axis=1)
    
    # Additional Requirements:
    Total_In_Bound_Roam_Duration_Pivot_Record = Total_In_Bound_Roam_Duration_Pivot_Record.reindex(sorted(Total_In_Bound_Roam_Duration_Pivot_Record.columns), axis=1)
    Total_MB_Pivot_Record = Total_MB_Pivot_Record.reindex(sorted(Total_MB_Pivot_Record.columns), axis=1)
    Total_National_Roam_Duration_Pivot_Record = Total_National_Roam_Duration_Pivot_Record.reindex(sorted(Total_National_Roam_Duration_Pivot_Record.columns), axis=1)
    Total_Out_International_EGP_Pivot_Record = Total_Out_International_EGP_Pivot_Record.reindex(sorted(Total_Out_International_EGP_Pivot_Record.columns), axis=1)
    Total_Roam_Data_MB_Pivot_Record = Total_Roam_Data_MB_Pivot_Record.reindex(sorted(Total_Roam_Data_MB_Pivot_Record.columns), axis=1)
    
    
    print("Records' columns sorted")

    # Handling NaN values
    Total_Revenue_Pivot_Record = Total_Revenue_Pivot_Record.fillna(0)
    Data_Revenue_Pivot_Record = Data_Revenue_Pivot_Record.fillna(0)
    Roaming_Data_Revenue_Pivot_Record = Roaming_Data_Revenue_Pivot_Record.fillna(0)
    Roaming_Voice_Revenue_Pivot_Record = Roaming_Voice_Revenue_Pivot_Record.fillna(0)
    Voice_Revenue_Pivot_Record = Voice_Revenue_Pivot_Record.fillna(0)

    # Additional Requirements:
    Total_In_Bound_Roam_Duration_Pivot_Record = Total_In_Bound_Roam_Duration_Pivot_Record.fillna(0)
    Total_MB_Pivot_Record = Total_MB_Pivot_Record.fillna(0)
    Total_National_Roam_Duration_Pivot_Record = Total_National_Roam_Duration_Pivot_Record.fillna(0)
    Total_Out_International_EGP_Pivot_Record = Total_Out_International_EGP_Pivot_Record.fillna(0)
    Total_Roam_Data_MB_Pivot_Record = Total_Roam_Data_MB_Pivot_Record.fillna(0)
    
    print("NaNs handeled")

    site_list = []
    site_obj = {}

    for cell_index in range(len(Total_Revenue_Pivot_Record.columns)):

        if Total_Revenue_Pivot_Record.columns[cell_index] == 'Site_Code_DWH' or Total_Revenue_Pivot_Record.columns[cell_index] == 'Status':
            continue

        obj = {
            "Date": Total_Revenue_Pivot_Record.columns[cell_index],
            # "Revenue": "{:,.3f}".format(maxRevenue),
            "Total_Revenue": "{:.3f}".format(Total_Revenue_Pivot_Record.loc[0][cell_index]),
            "Total_Data":"{:.3f}".format(Data_Revenue_Pivot_Record.loc[0][cell_index]),
            "Total_Voice":"{:.3f}".format(Voice_Revenue_Pivot_Record.loc[0][cell_index]),
            "Roaming_Voice":"{:.3f}".format(Roaming_Voice_Revenue_Pivot_Record.loc[0][cell_index]),
            "Roaming_Data":"{:.3f}".format(Roaming_Data_Revenue_Pivot_Record.loc[0][cell_index]),
            "In_Bound_Roam_Duration":"{:.3f}".format(Total_In_Bound_Roam_Duration_Pivot_Record.loc[0][cell_index]),
            "Total_MB":"{:.3f}".format(Total_MB_Pivot_Record.loc[0][cell_index]),
            "National_Roam_Duration":"{:.3f}".format(Total_National_Roam_Duration_Pivot_Record.loc[0][cell_index]),
            "Out_International_EGP":"{:.3f}".format(Total_Out_International_EGP_Pivot_Record.loc[0][cell_index]),
            "Roam_Data_MB":"{:.3f}".format(Total_Roam_Data_MB_Pivot_Record.loc[0][cell_index]),
            # "Roaming_Data":"{:.3f}".format(Roaming_Data_Revenue_Pivot_Record.loc[0][cell_index]),
        }

        site_list.append(obj)

    site_obj[siteCode] = site_list
    return site_obj

@flaskApp.route("/api/getAllNetworkDates", methods=['GET','POST'])
@cross_origin()
def GetNetworkDates():
    # get the column headers of any network table
    sql_query = pd.read_sql_query("SELECT * FROM Network_Total_Revenue_Pivot_Table", DB_CONNECTION)
    
    sorted_columns = sorted(list(sql_query))
    result = {}
    result["Dates"] = sorted_columns

    return result

@flaskApp.route("/api/getNetworkRevenues", methods=['GET','POST'])
@cross_origin()
def GetNetworkRevenues():

    total_revenue_query = pd.read_sql_query("SELECT * FROM Network_Total_Revenue_Pivot_Table", DB_CONNECTION)
    total_revenue_query = total_revenue_query.fillna(0)
    
    voice_revenue_query = pd.read_sql_query("SELECT * FROM Network_Voice_Revenue_Pivot_Table", DB_CONNECTION)
    voice_revenue_query = voice_revenue_query.fillna(0)
    
    data_revenue_query = pd.read_sql_query("SELECT * FROM Network_Data_Revenue_Pivot_Table", DB_CONNECTION)
    data_revenue_query = data_revenue_query.fillna(0)
    
    roaming_data_revenue_query = pd.read_sql_query("SELECT * FROM Network_Roaming_Data_Revenue_Pivot_Table", DB_CONNECTION)
    roaming_data_revenue_query = roaming_data_revenue_query.fillna(0)
    
    roaming_voice_revenue_query = pd.read_sql_query("SELECT * FROM Network_Roaming_Voice_Revenue_Pivot_Table", DB_CONNECTION)
    roaming_voice_revenue_query = roaming_voice_revenue_query.fillna(0)

    # order dates ascending 
    total_revenue_query = total_revenue_query.reindex(sorted(total_revenue_query.columns), axis=1)

    print("After sorting:")
    print(total_revenue_query)

    result = {}
    result_lst = []
    for date, revenue in total_revenue_query.iteritems():

        obj = {}
        obj ={
            "Date":date,
            "Total_Revenue":"{:.3f}".format(total_revenue_query.loc[0][date]),
            "Total_Data":"{:.3f}".format(data_revenue_query.loc[0][date]),
            "Total_Voice":"{:.3f}".format(voice_revenue_query.loc[0][date]),
            "Roaming_Voice":"{:.3f}".format(roaming_voice_revenue_query.loc[0][date]),
            "Roaming_Data":"{:.3f}".format(roaming_data_revenue_query.loc[0][date])
        }
        result_lst.append(obj)

    result["Network_Chart"] = result_lst
    return result

@flaskApp.route("/api/testPivotTable", methods=['GET'])
@cross_origin()
def TestPivotTable():

    Revenue_Tech_Table['Month'] = Revenue_Tech_Table['Month'].astype(str).str.zfill(2)

    Revenue_Tech_Table.groupby(['Year','Month'])
    site_date = Revenue_Tech_Table['Year'].astype(str) + '-' + Revenue_Tech_Table['Month']
    total_revenue = Revenue_Tech_Table['Total_Revenue'].map(float).sum()
    total_data = Revenue_Tech_Table['Total_MB_REV_EGP'].map(float).sum()
    total_voice = Revenue_Tech_Table['Total_Out_REV_EGP'].map(float).sum()
    roaming_voice = Revenue_Tech_Table['National_Roaming_REV_EGP'].map(float).sum() + Revenue_Tech_Table['In_Bound_Roaming_REV_EGP'].map(float).sum()
    roaming_data= Revenue_Tech_Table['Roam_Data_MB_REV_EGP'].map(float).sum()

    Enhanced_Network_Revenue_Chart = pd.DataFrame()
    Enhanced_Network_Revenue_Chart.insert(0, "Site_Date", site_date, True)
    Enhanced_Network_Revenue_Chart.insert(1, "Total_Revenue", total_revenue, True)
    Enhanced_Network_Revenue_Chart.insert(2, "Total_Data", total_data, True)
    Enhanced_Network_Revenue_Chart.insert(3, "Total_Voice", total_voice, True)
    Enhanced_Network_Revenue_Chart.insert(4, "Roaming_Voice", roaming_voice, True)
    Enhanced_Network_Revenue_Chart.insert(5, "Roaming_Data", roaming_data, True)


    Network_Total_Revenue_Pivot_Table = pd.pivot_table(Enhanced_Network_Revenue_Chart, columns=['Site_Date'] ,values=['Total_Revenue'], aggfunc=np.sum)
    
    print(Network_Total_Revenue_Pivot_Table)

    return "Network_Total_Revenue_Pivot_Table"



def LoadMainTables():

    print("in LoadMainTables()...")
    global Revenue_Tech_Table
    # Revenue_Tech_Table = pd.read_sql_query("SELECT TOP 200 * FROM Revenue_Tech_ORG_BackUp", DB_CONNECTION)
    Revenue_Tech_Table = pd.read_sql_query("SELECT * FROM Detailed_Sites_Revenue_Chart", DB_CONNECTION)
    print("Revenue Tech loaded.  ", Revenue_Tech_Table.shape)

    # global Revenue_Dwh_Table
    # Revenue_Dwh_Table = pd.read_sql_query("SELECT TOP 200 * FROM Revenue_DWH_ORG_BackUp", DB_CONNECTION)
    # print("Revenue DWH loaded.  ", Revenue_Dwh_Table.shape)

    # print("Columns:")
    # print(Revenue_Tech_Table.columns)
    # print(Revenue_Dwh_Table.columns)

# To load Revenue tables just after starting the server
with flaskApp.app_context():
    LoadMainTables()

# if I executed this file directly(by running the command: python app.py), run this function:
if __name__ == '__main__':
    flaskApp.run(debug=True,host="0.0.0.0",use_reloader=True)#10.110.129.96
    # manager.run()


