
import pandas as pd
from cmath import nan
from io import BytesIO
from urllib import response
from importlib.resources import path
# from flask_sqlalchemy import SQLAlchemy

# import turbodbc
import sqlalchemy
from sqlalchemy import FLOAT, Float, Integer, String, create_engine
from sqlalchemy import types
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import date
import os
from flask import Flask
from sqlalchemy_utils import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy



# DB_SERVER_NAME = '.'
# # DB_SERVER_NAME = 'DESKTOP-HBCILPF'
# # DB_NAME = 'TrackRevenue'
# # DB_DRIVER = 'ODBC Driver 17 for SQL Server'
# # DB_CONNECTION_STRING = f'mssql://@{DB_SERVER_NAME}/{DB_NAME}?driver={DB_DRIVER}'
# # print("\n==> Your SQL connection string is:")
# # print(DB_CONNECTION_STRING)
# # print("\n")

# # DB_ENGINE = create_engine(DB_CONNECTION_STRING, fast_executemany=True)
# # DB_CONNECTION = DB_ENGINE.connect()
# # session = sessionmaker(DB_ENGINE)

database_name = "TrackRevenue"
                        #first parameter: username:password@host:port
database_path = "postgresql://{}/{}".format('postgres:postgres@localhost:5432', database_name)

app = Flask(__name__)

db = SQLAlchemy()
engine = ''
DB_CONNECTION = ''

def setup_db(app, database_path=database_path):
  if not database_exists(database_path):
    print("\nDatabase not found!")
    create_database(database_path)
    print("\nDataBase created.")

  else:
    print("\n >> Database already exists.")

  #To modify the global variable and not to create a local one:
  global engine
  engine = create_engine(database_path)

  session = sessionmaker(bind=engine)()

  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  db.app = app
  db.init_app(app)
  db.create_all()

  return session



DATA_SOURCE_PATH = "./source_files"
RESULT_PATH = "./results"
# SiteRevenue ==> DWH
# CellMapping ==> Tech
def UploadExcelFiles():

    # df_first_n = pd.read_csv("C:\\Users\\Public\\Orange\\Revenue-Tech-DWH-Tables\\Revenue_Original_DWH_ORG_BackUp\\Revenue_DWH_ORG_BackUp.csv", nrows=1)
    # df2_first_n = pd.read_csv("C:\\Users\\Public\\Orange\\Revenue-Tech-DWH-Tables\\Revenue_Tech_ORG_BackUp.csv", nrows=1)

    # print(list(df_first_n.columns))
    # print(df_first_n.head())
    # print("\n\n\n\n")
    # print(df2_first_n.head())
    # print(list(df2_first_n.columns))
    # return ""

    setup_db(app)
    global DB_CONNECTION
    DB_CONNECTION = engine.connect()
    
    added_files = os.listdir(DATA_SOURCE_PATH)
    first_file_extension = os.path.splitext(DATA_SOURCE_PATH + "\\" + added_files[0])[1]
    second_file_extension = os.path.splitext(DATA_SOURCE_PATH + "\\" + added_files[1])[1]

    print("\n", "File extension: ", first_file_extension)
    print("\n", "File extension: ", second_file_extension)

    site_revenue_file = list(filter(lambda x: 'site' in x.lower(), added_files))[0]
    cell_mapping_file = list(filter(lambda x: 'cell' in x.lower(), added_files))[0]
    print("site_revenue_file ==> ", site_revenue_file)
    print("cell_mapping_file ==> ", cell_mapping_file)

    site_revenue_path = os.path.join(DATA_SOURCE_PATH, site_revenue_file)
    cell_mapping_path = os.path.join(DATA_SOURCE_PATH, cell_mapping_file)

    if first_file_extension == ".xlsx":
        pd_site_revenue = pd.read_excel(site_revenue_path)
        pd_cell_mapping = pd.read_excel(cell_mapping_path)
    else:
        pd_site_revenue = pd.read_csv(site_revenue_path)
        pd_cell_mapping = pd.read_csv(cell_mapping_path)
    
    pd_site_revenue = pd_site_revenue.applymap(str)
    pd_cell_mapping = pd_cell_mapping.applymap(str)

    
    Dwh_LAC_CI = pd_site_revenue["LAC"] + "-" + pd_site_revenue["Cell_Id"]
    print("Dwh_lac_ci column created")
    tech_LAC_CI = pd_cell_mapping["LAC"] + "-" + pd_cell_mapping["CI"]
    print("tech_lac_ci column created")

    pd_cell_mapping.insert(0, "LAC_CI", tech_LAC_CI, True)
    pd_site_revenue.insert(5, "LAC_CI", Dwh_LAC_CI, True)
   
    # Clean el data before left join
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "No lookup for Cell"), 'Site_Code_DWH'] = '-'
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "Cell with no Site Code"), 'Site_Code_DWH'] = '-'
    pd_site_revenue.loc[(pd_site_revenue.Site_Code_DWH == "CDR with No Cell"), 'Site_Code_DWH'] = '-'


    # VlookUp Step el mafrod:
    left_join_result = pd.merge(pd_site_revenue, pd_cell_mapping, on="LAC_CI", suffixes=('_DWH', '_tech'), how="inner")# how='left')
    print("left_join_result.shape")
    print(left_join_result.shape)

    # remove white spaces around column names
    left_join_result.columns = left_join_result.columns.str.strip()

    left_join_result.rename(columns={"SITE CODE": "Site_Code_tech"}, inplace=True)
    left_join_result.rename(columns={"Site_Name": "Site_Name_DWH"}, inplace=True)
    left_join_result.rename(columns={"SITE NAME": "Site_Name_tech"}, inplace=True)
    left_join_result.rename(columns={"CI": "CI_tech"}, inplace=True)
    left_join_result.rename(columns={"\\xa0LONG_DEC": "LONG_DEC"}, inplace=True)
    left_join_result.rename(columns={"LAT_DEC ": "LAT_DEC"}, inplace=True)

    '''
        make month column consist of 2 digits: 01 instead of 1, 
        to be sorted correctly in DB table
    '''
    # left_join_result['Month_Num'] = left_join_result['Month_Num'].astype(str).str.zfill(2)
    # Year_Month = left_join_result['Year_Num'] + "-" + left_join_result['Month_Num'].astype(str)
    # left_join_result.insert(0, "Year_Month", Year_Month, True)

    print(left_join_result.dtypes)

    #? which is more accurate? TECHNOLOGY column or status column??
    #? a-drop el TECHNOLOGY column wala l2?
    left_join_result.drop(['Site_Name_tech','CI_tech','LAC_tech','TECHNOLOGY','Radio_Frequency_ID','RNC_BSC','LAT_DEC','LONG_DEC','Site Type','Comment'], axis=1, inplace=True)

    print('\nb3d el drop ady asamy el columns:')
    print(list(left_join_result.columns))
    print('\n')
      
    left_join_result["Site_Name_DWH"] = left_join_result["Site_Name_DWH"].fillna('-')
    left_join_result.loc[(left_join_result.Site_Name_DWH == "nan"), 'Site_Name_DWH'] = '-'
    
    left_join_result["Status"] = left_join_result["Status"].fillna('-')
    left_join_result.loc[(left_join_result.Status == "?"), 'Status'] = '-'
    left_join_result.loc[(left_join_result.Status == "2g"), 'Status'] = '2G'
    left_join_result.loc[(left_join_result.Status == "3g"), 'Status'] = '3G'

    left_join_result.loc[(left_join_result.Site_Code_tech == "No lookup for Cell"), 'Site_Code_tech'] = '-'
    left_join_result.loc[(left_join_result.Site_Code_tech == "Cell with no Site Code"), 'Site_Code_tech'] = '-'
    left_join_result.loc[(left_join_result.Site_Code_tech ==
                          "CDR with No Cell"), 'Site_Code_tech'] = '-'

    
    left_join_result["Market_Zone"] = left_join_result["Market_Zone"].fillna('-')
    left_join_result.loc[(left_join_result.Market_Zone == "?"), 'Market_Zone'] = '-'
    
    left_join_result["Governorate"] = left_join_result["Governorate"].fillna('-')
    left_join_result.loc[(left_join_result.Governorate == "?"), 'Governorate'] = '-'
    
    left_join_result["Northing"] = left_join_result["Northing"].fillna('-')
    left_join_result.loc[(left_join_result.Northing == "?"), 'Northing'] = '0'

    left_join_result["Easting"] = left_join_result["Easting"].fillna('-')
    left_join_result.loc[(left_join_result.Easting == "?"), 'Easting'] = '0'

    left_join_result["Site_Code_tech"] = left_join_result["Site_Code_tech"].fillna('-')
    left_join_result.loc[(left_join_result.Site_Code_tech == "?"), 'Site_Code_tech'] = '-'
    left_join_result.loc[(left_join_result.Site_Code_tech == "nan"), 'Site_Code_tech'] = '-'
    
    left_join_result["Site_Code_DWH"] = left_join_result["Site_Code_DWH"].fillna('-')
    left_join_result.loc[(left_join_result.Site_Code_DWH == "?"), 'Site_Code_DWH'] = '-'
    left_join_result.loc[(left_join_result.Site_Code_DWH == "nan"), 'Site_Code_DWH'] = '-'


    left_join_result = left_join_result.fillna(0)

    print("NaNs handled")
    '''
     Convert the datatype of the numeric columns,
     to be able to push them to DB with correct datatypes:
     '''
    left_join_result[['Year_Num','Month_Num','DWH_CELL','Cell_Id','LAC_DWH','Total_Out_Duration','Out_International_Duration','Incoming_Duration','Total_MB','Total_MB_2G','Total_MB_3G','Total_MB_4G','In_Bound_Roam_Duration','National_Roam_Duration','Roam_Data_MB','Total_Out_REV_EGP','Out_International_EGP','Total_MB_REV_EGP','Total_MB_2G_REV_EGP','Total_MB_3G_REV_EGP','Total_MB_4G_REV_EGP','In_Bound_Roaming_REV_EGP','National_Roaming_REV_EGP','Roam_Data_MB_REV_EGP','Total_Revenue']] = left_join_result[['Year_Num','Month_Num','DWH_CELL','Cell_Id','LAC_DWH','Total_Out_Duration','Out_International_Duration','Incoming_Duration','Total_MB','Total_MB_2G','Total_MB_3G','Total_MB_4G','In_Bound_Roam_Duration','National_Roam_Duration','Roam_Data_MB','Total_Out_REV_EGP','Out_International_EGP','Total_MB_REV_EGP','Total_MB_2G_REV_EGP','Total_MB_3G_REV_EGP','Total_MB_4G_REV_EGP','In_Bound_Roaming_REV_EGP','National_Roaming_REV_EGP','Roam_Data_MB_REV_EGP','Total_Revenue']].apply(pd.to_numeric)
    # left_join_result.to_csv(os.path.join(RESULT_PATH, "left_join_result.csv"), encoding='utf-8', index=False)

    print("Numeric datatypes handled")

    # print("type of left join result: ", type(left_join_result))
    # # # to get column names which contains a certain value
    # p = left_join_result.isin(["-"]).any()
    # cols = p.index[p].tolist()
    # print("problems in:")
    # print(cols)

    print(left_join_result.dtypes)
    # Save the merged table to DB:
    """
    if_exists: {'fail', 'replace', 'append'}, default 'fail'
        fail: If table exists, do nothing.
        replace: If table exists, drop it, recreate it, and insert data.
        append: If table exists, insert data. Create if does not exist.
    """  
    """
        Keep in mind an appropriate chunk size
    """
    #! ana zwdt '_Num' f Year_Num & Month_Num hna f esm el key
    left_join_result.to_sql('Merged_Revenue_Tech_With_Technology', con=DB_CONNECTION, if_exists='append',
    dtype={
        'Year_Num': Integer(),
        'Month_Num': Integer(),
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
        'Site_Code_tech': String(50)}, index=False, chunksize=1000)


    print('\n\nData Inserted.')
    # return ""

    # file_of_interest = left_join_result[["LAC_CI","Site_Code_DWH","Site_Code_tech","Total_Revenue","Total_MB_REV_EGP","Total_Out_REV_EGP","TECHNOLOGY"]]
    # file_of_interest = left_join_result[['Year_Num','Month_Num',"LAC_CI","Site_Code_DWH","Site_Code_tech","Total_Revenue","Total_MB_REV_EGP","Total_Out_REV_EGP","Status"]]

    # file_of_interest.rename(columns={"Total_MB_REV_EGP": "Total_Data"}, inplace=True)
    # file_of_interest.rename(columns={"Total_Out_REV_EGP": "Total_Voice"}, inplace=True)


    # file_of_interest["Site_Code_tech"] = file_of_interest["Site_Code_tech"].fillna('-')
    # file_of_interest["Site_Code_DWH"] = file_of_interest["Site_Code_DWH"].fillna('-')

    # file_of_interest.to_csv("file_of_interest_"+current_month+"_"+current_year+".csv", encoding='utf-8', index=False)
    # file_of_interest.to_csv(os.path.join(RESULT_PATH, "file_of_interest.csv"), encoding='utf-8', index=False)

    # print("\n\nYOUR IMPORTANT FILE IS READY!!!!!!!!!!!!!")
    # print("file_of_interest[Site_Code_tech].unique()")
    # print(file_of_interest["Site_Code_tech"].unique())

    # #! should remove this step, and NOT create 3 new tables, 3shan size el DB msh na2s ykbr aktr mn kda
    # in_tech_No_DWH = file_of_interest[(file_of_interest["Site_Code_tech"] != "-") & (file_of_interest["Site_Code_DWH"] == "-")]
    # in_DWH_No_tech = file_of_interest[(file_of_interest["Site_Code_tech"] == "-") & (file_of_interest["Site_Code_DWH"] != "-")]
    # DWH_Not_Match_tech = file_of_interest[(file_of_interest["Site_Code_tech"] != "-") & (file_of_interest["Site_Code_DWH"] != "-") & (file_of_interest["Site_Code_tech"] != file_of_interest["Site_Code_DWH"])]

    # in_tech_No_DWH_selected_cols = in_tech_No_DWH.drop(["Site_Code_DWH","Total_Data","Total_Voice"], axis=1)#, inplace=True)

    # in_DWH_No_tech_selected_cols = in_DWH_No_tech.drop(["Site_Code_tech","Total_Data","Total_Voice"], axis=1)#, inplace=True)

    # DWH_Not_Match_tech_selected_cols = DWH_Not_Match_tech.drop(["Total_Data","Total_Voice"], axis=1)#, inplace=True)

    # print("shape of in_tech_No_DWH_selected_cols is: ", in_tech_No_DWH_selected_cols.shape)
    # print("Cols of in_tech_No_DWH_selected_cols are: ", list(in_tech_No_DWH_selected_cols.columns))
    # print("Datatypes of in_tech_No_DWH_selected_cols are: ", in_tech_No_DWH_selected_cols.dtypes)
    # print("\n")

    # print("shape of in_DWH_No_tech_selected_cols is: ", in_DWH_No_tech_selected_cols.shape)
    # print("Cols of in_DWH_No_tech_selected_cols are: ", list(in_DWH_No_tech_selected_cols.columns))
    # print("Datatypes of in_DWH_No_tech_selected_cols are: ", in_DWH_No_tech_selected_cols.dtypes)
    # print("\n")

    # print("shape of DWH_Not_Match_tech_selected_cols is: ", DWH_Not_Match_tech_selected_cols.shape)
    # print("Cols of DWH_Not_Match_tech_selected_cols are: ", list(DWH_Not_Match_tech_selected_cols.columns))
    # print("Datatypes of DWH_Not_Match_tech_selected_cols are: ", DWH_Not_Match_tech_selected_cols.dtypes)


    # in_tech_No_DWH_selected_cols.to_sql('in_tech_No_DWH', con=DB_ENGINE, if_exists='append',
    # dtype={
    #     'Year': Integer(),
    #     'Month': Integer(),
    #     'LAC_CI': String(20),
    #     'Site_Code_tech': String(50),
    #     'Site_Code_DWH': String(50),
    #     'Total_Revenue':Float(),
    #     'Status': String(10)
    # }, index=False, chunksize=1000)


    # in_DWH_No_tech_selected_cols.to_sql('in_DWH_No_tech', con=DB_ENGINE, if_exists='append',
    # dtype={
    #     'Year': Integer(),
    #     'Month': Integer(),
    #     'LAC_CI': String(20),
    #     'Site_Code_tech': String(50),
    #     'Site_Code_DWH': String(50),
    #     'Total_Revenue':Float(),
    #     'Status': String(10)
    # }, index=False, chunksize=1000)


    # DWH_Not_Match_tech_selected_cols.to_sql('DWH_Not_Match_tech', con=DB_ENGINE, if_exists='append',
    # dtype={
    #     'Year': Integer(),
    #     'Month': Integer(),
    #     'LAC_CI': String(20),
    #     'Site_Code_tech': String(50),
    #     'Site_Code_DWH': String(50),
    #     'Total_Revenue':Float(),
    #     'Status': String(10)
    # }, index=False, chunksize=1000)


    # print("\n\n******** All tables uploaded.********")

    return ""

    # in_tech_No_DWH_list = []
    # for rowIndex, row in in_tech_No_DWH_selected_cols.iterrows():
    #     # Iterate through each cell in each row
    #     row_obj = {}
    #     row_obj = {
    #         "Site_Code_tech":row[0],
    #         "Site_Code_DWH":row[1],
    #         "Total_Revenue":row[2]
    #     }
    #     in_tech_No_DWH_list.append(row_obj)
    
    # in_tech_No_DWH_total_revenue = in_tech_No_DWH_selected_cols["Total_Revenue"].map(float).sum()
    # # print("in_tech_No_DWH_total_revenue")
    # # print(in_tech_No_DWH_total_revenue)

    # in_DWH_No_tech_list = []
    # for rowIndex, row in in_DWH_No_tech_selected_cols.iterrows():
    #     # Iterate through each cell in each row
    #     row_obj = {}
    #     row_obj = {
    #         "Site_Code_tech":row[0],
    #         "Site_Code_DWH":row[1],
    #         "Total_Revenue":row[2]
    #     }
    #     in_DWH_No_tech_list.append(row_obj)


    # # print("\n\n\n\nin_DWH_No_tech_list:\n\n")
    # # print(type(in_DWH_No_tech_list))
    # # print(len(in_DWH_No_tech_list))
    # # print(in_DWH_No_tech_list[0])

    # in_DWH_No_tech_total_revenue = in_DWH_No_tech_selected_cols["Total_Revenue"].map(float).sum()
    # # print("in_DWH_No_tech_total_revenue")
    # # print(in_DWH_No_tech_total_revenue)

    # DWH_Not_Match_tech_list = []
    # for rowIndex, row in DWH_Not_Match_tech_selected_cols.iterrows():
    #     # Iterate through each cell in each row
    #     row_obj = {}
    #     row_obj = {
    #         "Site_Code_tech":row[0],
    #         "Site_Code_DWH":row[1],
    #         "Total_Revenue":row[2]
    #     }
    #     DWH_Not_Match_tech_list.append(row_obj)
    
    # DWH_Not_Match_tech_total_revenue = DWH_Not_Match_tech_selected_cols["Total_Revenue"].map(float).sum()
    # # print("DWH_Not_Match_tech_total_revenue")
    # # print(DWH_Not_Match_tech_total_revenue)

    # Total_Revenue = file_of_interest["Total_Revenue"].map(float).sum()
    # Total_Data = file_of_interest["Total_Data"].map(float).sum()
    # Total_Voice = file_of_interest["Total_Voice"].map(float).sum()

    # response ={
    #     "Total_Revenue":"{:,.2f}".format(Total_Revenue),
    #     "Total_Data":"{:,.2f}".format(Total_Data),
    #     "Total_Voice":"{:,.2f}".format(Total_Voice),
    #     "in_tech_No_DWH":{
    #         "in_tech_No_DWH_list":in_tech_No_DWH_list,
    #         "in_tech_No_DWH_total_revenue":"{:,.2f}".format(in_tech_No_DWH_total_revenue),
    #         # "in_tech_No_DWH_buffer":"in_tech_No_DWH_buffer",
    #         "in_tech_No_DWH_buffer":"in_tech_No_DWH.csv"
    #     },
        
    #     "in_DWH_No_tech":{
    #         "in_DWH_No_tech_list":in_DWH_No_tech_list,
    #         "in_DWH_No_tech_total_revenue":"{:,.2f}".format(in_DWH_No_tech_total_revenue),
    #         # "in_DWH_No_tech_buffer":"in_DWH_No_tech_buffer"
    #         "in_DWH_No_tech_buffer":"in_DWH_No_tech.csv"
    #     },
    #     "DWH_Not_Match_tech":{
    #         "DWH_Not_Match_tech_list":DWH_Not_Match_tech_list,
    #         "DWH_Not_Match_tech_total_revenue":"{:,.2f}".format(DWH_Not_Match_tech_total_revenue),
    #         "DWH_Not_Match_tech_buffer":"DWH_Not_Match_tech.csv"
    #         # "DWH_Not_Match_tech_buffer":""
    #     },

    # }

    # return response
 

# if I executed this file directly(by running the command: python app.py), run this function:
if __name__ == '__main__':
    UploadExcelFiles()

