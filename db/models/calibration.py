import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import Column, Integer, Boolean, String, JSON, FLOAT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint
from models.base import Base

class Calibration(Base):
    __tablename__ = 'calibrations'
    id = Column(Integer, primary_key=True)
    pixel_id = Column(Integer)
    pixel_number = Column(Integer)
    __table_args__ = (ForeignKeyConstraint(['pixel_id', 'pixel_number'],['pixels.id', 'pixels.pixel_number']),)
    pixel = relationship('Pixel', back_populates='calibrations')

    calibration_flag = Column(String)
    ecap_fit_chi2 = Column(FLOAT)
    xray_fit_chi2 = Column(FLOAT)
    calibration_chi2 = Column(FLOAT)
    

    def __init__(self, pixel):
        self.pixel = pixel
        # self.source = pixel.source()
        # electron_hist = histogram(pixel.energy,pixel.run.source.electron_bins)
        # xray_hist = histogram(energy,run.source.xray_bins)
        # self.electron_hist = electron_hist
        # self.xray_hist = xray_hist