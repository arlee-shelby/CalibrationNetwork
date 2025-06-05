import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Session
from models.calibration import Calibration

class CalibrationController():
    def __init__(self,peak):
        self.peak = peak

    def get_all():
        session = Session()
        try:
            return session.query(Calibration).all()
        finally:
            session.close()
            
    def get_by_id(id):
        session = Session()
        try:
            return session.query(Calibration).filter_by(id = id).all()[0]
        finally:
            session.close()

    def get_by_run_number(run_number):
        session = Session()
        try:
            return session.query(Calibration).filter_by(run_number = run_number).all()[0]
        finally:
            session.close()
    
    def get_by_pixel_number(pixel_number):
        session = Session()
        try:
            return session.query(Calibration).filter_by(pixel_number = pixel_number).all()[0]
        finally:
            session.close()
    
    def get_by_run_and_pixel_number(run_number,pixel_number):
        session = Session()
        try:
            return session.query(Calibration).filter_by(run_number = run_number,pixel_number = pixel_number).all()
        finally:
            session.close()

    def get_by_run_and_pixel_number_and_calibration_type(run_number,pixel_number,calibration_type):
        session = Session()
        try:
            return session.query(Calibration).filter_by(run_number = run_number,pixel_number = pixel_number,calibration_type=calibration_type).all()
        finally:
            session.close()