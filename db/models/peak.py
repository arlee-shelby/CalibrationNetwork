import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import Column, Integer, Boolean, String, JSON, FLOAT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint
from models.base import Base, association_table

class Peak(Base):
    __tablename__ = 'peaks'
    id = Column(Integer, primary_key=True)
    run_number = Column(Integer)
    pixel_number = Column(Integer)
    pixel_id = Column(Integer)
    __table_args__ = (ForeignKeyConstraint(['pixel_id', 'pixel_number','run_number'],['pixels.id', 'pixels.pixel_number','pixels.run_number']),)
    pixel = relationship('Pixel', back_populates='peaks')
    fits = relationship('Fit', back_populates='peak',uselist=False)
    calibrations = relationship( "Calibration", secondary=association_table, back_populates="peaks")

    center = Column(FLOAT)
    center_error = Column(FLOAT)
    sigma = Column(FLOAT)
    sigma_error = Column(FLOAT)
    nndc_energy = Column(FLOAT)
    
    

    def __init__(self, pixel, center,center_error,sigma,sigma_error,nndc_energy):
        self.pixel = pixel
        self.center = center
        self.center_error = center_error
        self.sigma = sigma
        self.sigma_error = sigma_error
        self.nndc_energy = nndc_energy