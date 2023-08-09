
from config import access_token, user_id
import requests
from pprint import pprint
from datetime import date
import schedule
import time

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

#This creates classes to represent schema of our database
class Steps(Base):
    __tablename__ = 'intraday_steps'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    steps = Column(Integer)
    
    
class Runs(Base):
    __tablename__ = 'Runs'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    duration = Column(Integer)
    distance= Column(Float)
    pace = Column(Float)

class Heartrate(Base):
    __tablename__ = 'intraday_heartrate'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    rate = Column(Integer)
    
Base.metadata.tables

# This creates our database engine
engine = create_engine('sqlite:///fitbit.sqlite')
conn = engine.connect()


# This is where we create our tables in the database
Base.metadata.create_all(conn)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

#THIS DEFINES A FUNCTION TO MAKE API CALLS / ADD TO DATABASE
def fetch_and_save_fitbit_data():
    today = date.today()
    today=today.strftime("%Y-%m-%d")

    header = {'Authorization': 'Bearer '+access_token}
    url = f'https://api.fitbit.com/1/user/{user_id}/'

    #THIS MAKES STEPS INTRADAY INSTANCE#
    steps_request = 'activities/steps/date/today/today/5min.json'
    steps_response = requests.get(f'{url}{steps_request}',headers=header).json()
    session = Session()
    for row in steps_response['activities-steps-intraday']['dataset']:
        session.add(Steps(date=today,time=row['time'],steps=row['value']))
    session.commit()
    session.close()
    
    #THIS MAKES RUN REQUEST
    request = f'activities/list.json?afterDate={today}&sort=asc&offset=0&limit=10'
    run_request = requests.get(f'{url}{request}',headers=header).json()
    session = Session()
    #THIS CREATES RUN INSTANCE
    for row in run_request['activities']:
        if row['activityName']=='Run':
            session.add(Runs(date=today,duration=row['activeDuration'],distance=row['distance'],pace=row['pace']))
    session.commit()
    session.close()     



    #THIS MAKES HEART RATE INTRADAY REQUEST
    request = f'activities/heart/date/{today}/1d/5min.json'
    heart_response=requests.get(f'{url}{request}',headers=header).json()
    session = Session()
    #THIS MAKES HEART RATE INTRADAY INSTANCE#
    for row in heart_response['activities-heart-intraday']['dataset']:
        session.add(Heartrate(date=today,time=row['time'], rate=row['value']))
    session.commit()
    session.close()    

#THIS SCHEDULES THE FUNCTION TO RUN EVERY DAY AT 11:59PM ON AN INFINTE LOOP
schedule.every().day.at("23:55").do(fetch_and_save_fitbit_data)

while True:
    schedule.run_pending()
    time.sleep(1)



