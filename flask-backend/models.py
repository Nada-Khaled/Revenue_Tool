from flask import Flask
from sqlalchemy import Column, String, Integer, Float,create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

database_name = "TrackRevenue"
                        #first parameter: username:password@host:port
database_path = "postgresql://{}/{}".format('postgres:postgres@localhost:5432', database_name)

app = Flask(__name__)

db = SQLAlchemy()
engine = ''

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


class Merged_Revenue_Tech_With_Technology(Base):  
  __tablename__ = 'merged_revenue_tech_with_technology'
  
  id = Column(Integer, primary_key=True)
  year_num = Column(Integer, nullable = True)
  month_num = Column(Integer, nullable = True)
  dwh_cell = Column(Integer, nullable = True)
  cell_id = Column(Integer, nullable = True) 
  lac_dwh = Column(Integer, nullable = True) 

  lac_ci = Column(String, nullable = True) 
  market_zone = Column(String, nullable = True) 
  status = Column(String, nullable = True)
  governorate = Column(String, nullable = True)
  easting = Column(String, nullable = True)
  northing = Column(String, nullable = True)
  geo_lookup = Column(String, nullable = True)
  site_code_dwh = Column(String, nullable = True)
  site_name_dwh = Column(String, nullable = True)
  site_code_tech= Column(String, nullable = True)

  total_out_duration = Column(Float, nullable = True)
  out_international_duration = Column(Float, nullable = True)
  incoming_duration = Column(Float, nullable = True)
  total_mb = Column(Float, nullable = True)
  total_mb_2g = Column(Float, nullable = True)
  total_mb_3g = Column(Float, nullable = True)
  total_mb_4g = Column(Float, nullable = True)
  in_bound_roam_duration = Column(Float, nullable = True)
  national_roam_duration = Column(Float, nullable = True)
  roam_data_mb = Column(Float, nullable = True)
  total_out_rev_egp = Column(Float, nullable = True)
  out_international_egp = Column(Float, nullable = True)
  total_mb_rev_egp = Column(Float, nullable = True)
  total_mb_2g_rev_egp = Column(Float, nullable = True)
  total_mb_3g_rev_egp = Column(Float, nullable = True)
  total_mb_4g_rev_egp = Column(Float, nullable = True)
  in_bound_roaming_rev_egp = Column(Float, nullable = True)
  national_roaming_rev_egp = Column(Float, nullable = True)
  roam_data_mb_rev_egp = Column(Float, nullable = True)
  total_revenue = Column(Float, nullable = True)
  
  
  def __init__(self,year_num,month_num,dwh_cell,cell_id,lac_dwh,lac_ci,market_zone,status,
  governorate,easting,northing,geo_lookup,site_code_dwh,site_name_dwh,site_code_tech,
  total_out_duration,out_international_duration,incoming_duration,total_mb,total_mb_2g,
  total_mb_3g,total_mb_4g,in_bound_roam_duration,national_roam_duration,roam_data_mb,
  total_out_rev_egp,out_international_egp,total_mb_rev_egp,total_mb_2g_rev_egp,
  total_mb_3g_rev_egp,total_mb_4g_rev_egp,in_bound_roaming_rev_egp,
  national_roaming_rev_egp,roam_data_mb_rev_egp,total_revenue):

    self.year_num = year_num
    self.month_num = month_num
    self.dwh_cell = dwh_cell
    self.cell_id = cell_id
    self.lac_dwh = lac_dwh
    self.lac_ci = lac_ci
    self.market_zone = market_zone
    self.status = status
    self.governorate = governorate
    self.easting = easting
    self.northing = northing
    self.geo_lookup = geo_lookup
    self.site_code_dwh = site_code_dwh
    self.site_name_dwh = site_name_dwh
    self.site_code_tech  = site_code_tech
    self.total_out_duration = total_out_duration
    self.out_international_duration = out_international_duration 
    self.incoming_duration = incoming_duration
    self.total_mb = total_mb
    self.total_mb_2g = total_mb_2g
    self.total_mb_3g = total_mb_3g
    self.total_mb_4g = total_mb_4g
    self.in_bound_roam_duration = in_bound_roam_duration
    self.national_roam_duration = national_roam_duration
    self.roam_data_mb = roam_data_mb
    self.total_out_rev_egp = total_out_rev_egp
    self.out_international_egp = out_international_egp
    self.total_mb_rev_egp = total_mb_rev_egp
    self.total_mb_2g_rev_egp = total_mb_2g_rev_egp
    self.total_mb_3g_rev_egp = total_mb_3g_rev_egp
    self.total_mb_4g_rev_egp = total_mb_4g_rev_egp
    self.in_bound_roaming_rev_egp = in_bound_roaming_rev_egp
    self.national_roaming_rev_egp = national_roaming_rev_egp
    self.roam_data_mb_rev_egp = roam_data_mb_rev_egp
    self.total_revenue = total_revenue
    
  
  def insert(self):
    db.session.add(self)
    db.session.commit()
    
  def update(self):
    db.session.commit()
    

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def deactivate(self):
    self.active = False
    db.session.commit()

  def format(self):
    return {
        "id": self.id,
        "year_num": self.year_num,
        "month_num": self.month_num,
        "dwh_cell": self.dwh_cell,
        "cell_id": self.cell_id,
        "lac_dwh": self.lac_dwh,
        "lac_ci": self.lac_ci,
        "market_zone": self.market_zone,
        "status": self.status,
        "governorate": self.governorate,
        "easting": self.easting,
        "northing": self.northing,
        "geo_lookup": self.geo_lookup,
        "site_code_dwh": self.site_code_dwh,
        "site_name_dwh": self.site_name_dwh,
        "site_code_tech": self.site_code_tech,
        "total_out_duration": self.total_out_duration,
        "out_international_duration": self.out_international_duration,
        "incoming_duration": self.incoming_duration,
        "total_mb": self.total_mb,
        "total_mb_2g": self.total_mb_2g,
        "total_mb_3g": self.total_mb_3g,
        "total_mb_4g": self.total_mb_4g,
        "in_bound_roam_duration": self.in_bound_roam_duration,
        "national_roam_duration": self.national_roam_duration,
        "roam_data_mb": self.roam_data_mb,
        "total_out_rev_egp": self.total_out_rev_egp,
        "out_international_egp": self.out_international_egp,
        "total_mb_rev_egp": self.total_mb_rev_egp,
        "total_mb_2g_rev_egp": self.total_mb_2g_rev_egp,
        "total_mb_3g_rev_egp": self.total_mb_3g_rev_egp,
        "total_mb_4g_rev_egp": self.total_mb_4g_rev_egp,
        "in_bound_roaming_rev_egp": self.in_bound_roaming_rev_egp,
        "national_roaming_rev_egp": self.national_roaming_rev_egp,
        "roam_data_mb_rev_egp": self.roam_data_mb_rev_egp,
        "total_revenue": self.total_revenue,
      }


class Detailed_Network_Revenue_Chart(Base):
    __tablename__ = 'detailed_network_revenue_chart'

    id = Column(Integer, primary_key=True)
    year_num = Column(Integer, nullable = True)
    month_num = Column(Integer, nullable = True)
    total_revenue = Column(Float, nullable=True)
    total_data = Column(Float, nullable=True)
    total_voice = Column(Float, nullable=True)
    total_out_duration = Column(Float, nullable=True)
    incoming_duration = Column(Float, nullable=True)
    total_mb = Column(Float, nullable=True)
    in_bound_roam_duration = Column(Float, nullable=True)
    national_roam_duration = Column(Float, nullable=True)
    roam_data_mb = Column(Float, nullable=True)
    out_international_egp = Column(Float, nullable=True)
    in_bound_roaming_rev_egp = Column(Float, nullable=True)
    national_roaming_rev_egp = Column(Float, nullable=True)
    roaming_data = Column(Float, nullable=True)


    def __init__(self,year_num,month_num,total_revenue,total_data,total_voice,
    total_out_duration,incoming_duration,total_mb,in_bound_roam_duration,
    national_roam_duration,roam_data_mb,out_international_egp,in_bound_roaming_rev_egp,
    national_roaming_rev_egp,roaming_data):
        
        self.id= id
        self.year_num= year_num
        self.month_num= month_num
        self.total_revenue= total_revenue
        self.total_data= total_data
        self.total_voice= total_voice
        self.total_out_duration= total_out_duration
        self.incoming_duration= incoming_duration
        self.total_mb= total_mb
        self.in_bound_roam_duration= in_bound_roam_duration
        self.national_roam_duration= national_roam_duration
        self.roam_data_mb= roam_data_mb
        self.out_international_egp= out_international_egp
        self.in_bound_roaming_rev_egp= in_bound_roaming_rev_egp
        self.national_roaming_rev_egp= national_roaming_rev_egp
        self.roaming_data= roaming_data

    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()     

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def deactivate(self):
        self.active = False
        db.session.commit()


    def format(self):

        return {
            "id": self.id,
            "year_num": self.year_num,
            "month_num": self.month_num,
            "total_revenue": self.total_revenue,
            "total_data": self.total_data,
            "total_voice": self.total_voice,
            "total_out_duration": self.total_out_duration,
            "incoming_duration": self.incoming_duration,
            "total_mb": self.total_mb,
            "in_bound_roam_duration": self.in_bound_roam_duration,
            "national_roam_duration": self.national_roam_duration,
            "roam_data_mb": self.roam_data_mb,
            "out_international_egp": self.out_international_egp,
            "in_bound_roaming_rev_egp": self.in_bound_roaming_rev_egp,
            "national_roaming_rev_egp": self.national_roaming_rev_egp,
            "roaming_data": self.roaming_data,
        }


class Detailed_Sites_Revenue_With_Technology_Chart(Base):
    __tablename__ = 'detailed_sites_revenue_with_technology_chart'

    id = Column(Integer, primary_key=True)
    year_num = Column(Integer, nullable = True)
    month_num = Column(Integer, nullable = True)
    site_code_dwh = Column(String, nullable = True)
    status = Column(String, nullable = True)
    total_revenue = Column(Float, nullable=True)
    total_data = Column(Float, nullable=True)
    total_voice = Column(Float, nullable=True)
    total_out_duration = Column(Float, nullable=True)
    incoming_duration = Column(Float, nullable=True)
    total_mb = Column(Float, nullable=True)
    in_bound_roam_duration = Column(Float, nullable=True)
    national_roam_duration = Column(Float, nullable=True)
    roam_data_mb = Column(Float, nullable=True)
    out_international_egp = Column(Float, nullable=True)
    in_bound_roaming_rev_egp = Column(Float, nullable=True)
    national_roaming_rev_egp = Column(Float, nullable=True)
    roaming_data = Column(Float, nullable=True)


    def __init__(self,year_num,month_num,site_code_dwh,status,total_revenue,total_data,total_voice,
    total_out_duration,incoming_duration,total_mb,in_bound_roam_duration,
    national_roam_duration,roam_data_mb,out_international_egp,in_bound_roaming_rev_egp,
    national_roaming_rev_egp,roaming_data):
        
        self.id= id
        self.year_num= year_num
        self.month_num= month_num
        self.site_code_dwh= site_code_dwh
        self.status= status
        self.total_revenue= total_revenue
        self.total_data= total_data
        self.total_voice= total_voice
        self.total_out_duration= total_out_duration
        self.incoming_duration= incoming_duration
        self.total_mb= total_mb
        self.in_bound_roam_duration= in_bound_roam_duration
        self.national_roam_duration= national_roam_duration
        self.roam_data_mb= roam_data_mb
        self.out_international_egp= out_international_egp
        self.in_bound_roaming_rev_egp= in_bound_roaming_rev_egp
        self.national_roaming_rev_egp= national_roaming_rev_egp
        self.roaming_data= roaming_data

    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()     

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def deactivate(self):
        self.active = False
        db.session.commit()


    def format(self):

        return {
            "id": self.id,
            "year_num": self.year_num,
            "month_num": self.month_num,
            "total_revenue": self.total_revenue,
            "total_data": self.total_data,
            "total_voice": self.total_voice,
            "total_out_duration": self.total_out_duration,
            "incoming_duration": self.incoming_duration,
            "total_mb": self.total_mb,
            "in_bound_roam_duration": self.in_bound_roam_duration,
            "national_roam_duration": self.national_roam_duration,
            "roam_data_mb": self.roam_data_mb,
            "out_international_egp": self.out_international_egp,
            "in_bound_roaming_rev_egp": self.in_bound_roaming_rev_egp,
            "national_roaming_rev_egp": self.national_roaming_rev_egp,
            "roaming_data": self.roaming_data,
        }


setup_db(app)

