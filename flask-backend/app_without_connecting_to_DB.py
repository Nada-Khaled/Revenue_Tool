import math
import random
from numpy import longdouble
import numpy
import pandas as pd
from cmath import nan
from io import BytesIO
from urllib import response
import json
from importlib.resources import path
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Response, flash, render_template, request, redirect, safe_join, send_file, url_for, jsonify, send_from_directory,abort
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
import datetime
from datetime import date

flaskApp = Flask(__name__)

DB_SERVER_NAME = '.'
DB_NAME = 'TrackRevenue'
DB_DRIVER = 'ODBC Driver 17 for SQL Server'
DB_CONNECTION_STRING = f'mssql://@{DB_SERVER_NAME}/{DB_NAME}?driver={DB_DRIVER}'
print("\n==> Your SQL connection string is:")
print(DB_CONNECTION_STRING)
print("\n")

DB_ENGINE = create_engine(DB_CONNECTION_STRING)
DB_CONNECTION = DB_ENGINE.connect()


CORS(flaskApp)#, support_credentials=True, expose_headers='Authorization', resources={r"/api/*": {"origins": "*"}})
# this secret key is used to protect my form from attacks
flaskApp.config['SECRET_KEY'] = 'form_password' # assign any value I want
# flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alchemyDB/excel.db'
flaskApp.config['CSV_PATH'] = 'E:\\Orange\\React-Flask-Task\\flask-backend'
excelDB = SQLAlchemy(flaskApp)


@flaskApp.route('/api/uploadExcelFiles', methods=['GET', 'POST'])
@cross_origin()
def UploadExcelFiles():

    uploaded_file_names = list(request.form.keys())
    print("\n\n::::::::::uploaded_file_names")
    print(uploaded_file_names)
    site_revenue = list(filter(lambda x: 'revenue' in x.lower(), uploaded_file_names))
    site_revenue_file = site_revenue[0]
    cell_mapping_report = list(filter(lambda x: 'cell' in x.lower(), uploaded_file_names))
    cell_mapping_file = cell_mapping_report[0]
    
    print('---------')
    print("final file names: ", site_revenue_file)
    print("final file names: ", cell_mapping_file)
    print('---------')


    pd_site_revenue = pd.read_excel(site_revenue_file)
    pd_site_revenue = pd_site_revenue.applymap(str)

    pd_cell_mapping = pd.read_excel(cell_mapping_file)
    pd_cell_mapping = pd_cell_mapping.applymap(str)

    DWH_LAC_CI = pd_site_revenue["LAC"] + "-" + pd_site_revenue["Cell_Id"]
    tech_LAC_CI = pd_cell_mapping["LAC"] + "-" + pd_cell_mapping["CI"]

    print(">> site revenue loaded and converted to string.")

    pd_cell_mapping.insert(0, "LAC_CI", tech_LAC_CI, True)
    pd_site_revenue.insert(5, "LAC_CI", DWH_LAC_CI, True)
    pd_cell_mapping.to_csv("cell_mapping_With_LAC_CI.csv", encoding='utf-8', index=False)
    pd_site_revenue.to_csv("site_revenue_With_LAC_CI.csv", encoding='utf-8', index=False)


    # Clean el data before left join
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "No lookup for Cell"), 'Site_Code_DWH'] = '-'
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "Cell with no Site Code"), 'Site_Code_DWH'] = '-'
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "CDR with No Cell"), 'Site_Code_DWH'] = '-'

    # VlookUp Step el mafrod
    left_join_result = pd.merge(pd_site_revenue, pd_cell_mapping, on="LAC_CI", how='left')
    print("left_join_result.shape")
    print(left_join_result.shape)
    left_join_result.to_csv("mergedTables.csv", encoding='utf-8', index=False)

    file_of_interest = left_join_result[["LAC_CI","Site_Code_DWH","SITE CODE","Total_Revenue","Total_MB_REV_EGP","Total_Out_REV_EGP"]]
    print("2bl el rename")
    file_of_interest.rename(columns={"SITE CODE": "Site_Code_tech"}, inplace=True)
    file_of_interest.rename(columns={"Total_MB_REV_EGP": "Total_Data"}, inplace=True)
    file_of_interest.rename(columns={"Total_Out_REV_EGP": "Total_Voice"}, inplace=True)
    print("b3d el rename")

    file_of_interest["Site_Code_tech"] = file_of_interest["Site_Code_tech"].fillna('-')

    file_of_interest.to_csv("file_of_interest.csv", encoding='utf-8', index=False)
    print("\n\nYOUR IMPORTANT FILE IS READY!!!!!!!!!!!!!")
    print("file_of_interest[Site_Code_tech].unique()")
    print(file_of_interest["Site_Code_tech"].unique())


    in_tech_No_DWH = file_of_interest[(file_of_interest["Site_Code_tech"] != "-") & (file_of_interest["Site_Code_DWH"] == "-")]
    in_DWH_No_tech = file_of_interest[(file_of_interest["Site_Code_tech"] == "-") & (file_of_interest["Site_Code_DWH"] != "-")]
    DWH_Not_Match_tech = file_of_interest[(file_of_interest["Site_Code_tech"] != "-") & (file_of_interest["Site_Code_DWH"] != "-") & (file_of_interest["Site_Code_tech"] != file_of_interest["Site_Code_DWH"])]

    in_tech_No_DWH_selected_cols = in_tech_No_DWH[["Site_Code_tech","Site_Code_DWH","Total_Revenue"]]
    in_DWH_No_tech_selected_cols = in_DWH_No_tech[["Site_Code_tech","Site_Code_DWH","Total_Revenue"]]
    DWH_Not_Match_tech_selected_cols = DWH_Not_Match_tech[["Site_Code_tech","Site_Code_DWH","Total_Revenue"]]

    in_tech_No_DWH_selected_cols.to_csv('in_tech_No_DWH.csv', encoding='utf-8', index=False)
    in_DWH_No_tech_selected_cols.to_csv('in_DWH_No_tech.csv', encoding='utf-8', index=False)
    DWH_Not_Match_tech_selected_cols.to_csv('DWH_Not_Match_tech.csv', encoding='utf-8', index=False)

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
    print("in_tech_No_DWH_total_revenue")
    print(in_tech_No_DWH_total_revenue)

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


    print("\n\n\n\nin_DWH_No_tech_list:\n\n")
    print(type(in_DWH_No_tech_list))
    print(len(in_DWH_No_tech_list))
    print(in_DWH_No_tech_list[0])

    in_DWH_No_tech_total_revenue = in_DWH_No_tech_selected_cols["Total_Revenue"].map(float).sum()
    print("in_DWH_No_tech_total_revenue")
    print(in_DWH_No_tech_total_revenue)

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
    print("DWH_Not_Match_tech_total_revenue")
    print(DWH_Not_Match_tech_total_revenue)

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
 
@flaskApp.route("/api/downloadFiles/<path:file_name>", methods=['GET','POST'])
@cross_origin()
def get_file(file_name):

    print("file_name to be downloaded")
    print(file_name)
    print("flaskApp.config['CSV_PATH']")
    print(flaskApp.config['CSV_PATH'])

    safe_path = safe_join(flaskApp.config["CSV_PATH"], file_name)

    print("safe path")
    print(safe_path)
    # return send_file(safe_path, as_attachment=True)
    return send_from_directory(flaskApp.config['CSV_PATH'], path=file_name,as_attachment=True)

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

@flaskApp.route("/api/showChartBySite/<string:siteCode>", methods=['GET','POST'])
@cross_origin()
def ShowSiteCharts(siteCode):

    Total_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Total_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Data_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Data_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Roaming_Data_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Roaming_Data_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Roaming_Voice_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Roaming_Voice_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    Voice_Revenue_Pivot_Record = pd.read_sql_query("SELECT * FROM Voice_Revenue_Pivot_Table WHERE ShortCode = '"+siteCode+"'", DB_CONNECTION)
    
    print("Shape of pivot records: ", Total_Revenue_Pivot_Record.shape)

    Total_Revenue_Pivot_Record = Total_Revenue_Pivot_Record.reindex(sorted(Total_Revenue_Pivot_Record.columns), axis=1)
    Data_Revenue_Pivot_Record = Data_Revenue_Pivot_Record.reindex(sorted(Data_Revenue_Pivot_Record.columns), axis=1)
    Roaming_Data_Revenue_Pivot_Record = Roaming_Data_Revenue_Pivot_Record.reindex(sorted(Roaming_Data_Revenue_Pivot_Record.columns), axis=1)
    Roaming_Voice_Revenue_Pivot_Record = Roaming_Voice_Revenue_Pivot_Record.reindex(sorted(Roaming_Voice_Revenue_Pivot_Record.columns), axis=1)
    Voice_Revenue_Pivot_Record = Voice_Revenue_Pivot_Record.reindex(sorted(Voice_Revenue_Pivot_Record.columns), axis=1)
    print("Records' columns sorted")

    # Handling NaN values
    Total_Revenue_Pivot_Record = Total_Revenue_Pivot_Record.fillna(0);
    Data_Revenue_Pivot_Record = Data_Revenue_Pivot_Record.fillna(0);
    Roaming_Data_Revenue_Pivot_Record = Roaming_Data_Revenue_Pivot_Record.fillna(0);
    Roaming_Voice_Revenue_Pivot_Record = Roaming_Voice_Revenue_Pivot_Record.fillna(0);
    Voice_Revenue_Pivot_Record = Voice_Revenue_Pivot_Record.fillna(0);
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
            # "Roaming_Data":"{:,.3f}".format(Roaming_Data_Revenue_Pivot_Record.loc[0][cell_index])
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

# if I executed this file directly(by running the command: python app.py), run this function:
if __name__ == '__main__':
    flaskApp.run(debug=True,host="0.0.0.0",use_reloader=True)#10.110.129.96

