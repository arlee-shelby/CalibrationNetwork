import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import Column, Integer, Boolean, String, JSON, FLOAT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint
from models.base import Base, association_table

class Calibration(Base):
    __tablename__ = 'calibrations'
    id = Column(Integer, primary_key=True)
    run_number = Column(Integer)
    pixel_number = Column(Integer)
    pixel_id = Column(Integer)
    __table_args__ = (ForeignKeyConstraint(['pixel_id', 'run_number','pixel_number'],['pixels.id', 'pixels.run_number','pixels.pixel_number']),)
    pixel = relationship('Pixel', back_populates='calibrations')
    peaks = relationship('Peak', secondary=association_table, back_populates='calibrations')

    calibration_type = Column(String)
    # chi2 = Column(FLOAT)
    quadratic_term = Column(FLOAT)
    quadratic_error = Column(FLOAT)
    linear_term = Column(FLOAT)
    linear_error = Column(FLOAT)
    constant_term = Column(FLOAT)
    constant_error = Column(FLOAT)
    
    

    def __init__(self, pixel, peaks, calibration_type, linear_term, linear_error, constant_term, constant_error, quadratic_term=None, quadratic_error=None):
        self.pixel = pixel
        self.peaks = peaks
        self.calibration_type = calibration_type
        # self.chi2 = chi2
        self.quadratic_term = quadratic_term
        self.quadratic_error = quadratic_error
        self.linear_term = linear_term
        self.linear_error = linear_error
        self.constant_term = constant_term
        self.constant_error = constant_error

