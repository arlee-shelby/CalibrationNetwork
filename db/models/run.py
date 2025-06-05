import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import Column, String, Integer, Date, FLOAT, Table
from sqlalchemy.orm import relationship
from models.base import Base

class Run(Base):
    __tablename__ = 'runs'

    id = Column(Integer, primary_key=True)
    run_number = Column(Integer)
    number_subruns = Column(Integer)
    pixels_calibrated = Column(Integer)
    pulser = Column(String)
    proton = Column(String)
    pixels = relationship('Pixel', back_populates='run')

    def __init__(self, run_number, number_subruns, pulser, proton):
        self.run_number = run_number
        self.number_subruns = number_subruns
        self.pulser = pulser
        self.proton = proton