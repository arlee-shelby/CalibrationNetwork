import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import Column, Integer, Boolean, String, JSON, FLOAT, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Pixel(Base):
    __tablename__ = 'pixels'

    id = Column(Integer, primary_key=True)
    run_number = Column(Integer, ForeignKey('runs.run_number'))
    run = relationship('Run', back_populates='pixels')
    pixel_number = Column(Integer)
    peaks = relationship('Peak', back_populates='pixel')
    calibrations = relationship('Calibration', back_populates='pixel')

    detector = Column(String)
    threshold = Column(Integer)
    trap_rise = Column(Integer)
    trap_length = Column(Integer)
    trap_decay = Column(Integer)
    

    def __init__(self, run, pixel_number, trap_rise, trap_length, trap_decay, detector,threshold):
        self.pixel_number = pixel_number
        self.run = run
        self.detector = detector
        self.trap_rise = trap_rise
        self.trap_length = trap_length
        self.trap_decay = trap_decay
        self.threshold = threshold