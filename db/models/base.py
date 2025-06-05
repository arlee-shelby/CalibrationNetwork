from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import Column, Integer, ForeignKey, Table

if os.path.exists('test1.db'):
   os.remove('test1.db')

engine = create_engine('sqlite:///test1.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

association_table = Table('calibration_peaks', Base.metadata,
    Column('peak_id', Integer, ForeignKey('peaks.id'), primary_key=True),
    Column('calibration_id', Integer, ForeignKey('calibrations.id'), primary_key=True)
)