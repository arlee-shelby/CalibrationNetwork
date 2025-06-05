import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import Column, Integer, Boolean, String, JSON, FLOAT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint
from models.base import Base

class Fit(Base):
    __tablename__ = 'fits'
    id = Column(Integer, primary_key=True)
    run_number = Column(Integer)
    pixel_number = Column(Integer)
    peak_id = Column(Integer)
    __table_args__ = (ForeignKeyConstraint(['peak_id', 'pixel_number','run_number'],['peaks.id', 'peaks.pixel_number','peaks.run_number']),)
    peak = relationship('Peak', back_populates='fits')

    peak_center = Column(FLOAT)
    chi2 = Column(FLOAT)
    pars = Column(JSON)
    par_errors = Column(JSON)
    energy_hist = Column(JSON)
    bin_edges = Column(JSON)

    
    

    def __init__(self, peak, chi2, pars,par_errors,energy_hist, bin_edges):
        self.peak = peak
        self.peak_center = peak.center
        self.chi2 = chi2
        self.pars = pars
        self.par_errors = par_errors
        self.energy_hist = energy_hist
        self.bin_edges = bin_edges