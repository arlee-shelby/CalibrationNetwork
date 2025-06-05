import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Session
from models.run import Run

class RunController():
    def __init__(self,run):
        self.run = run
    
    def get_all():
        session = Session()
        try:
            return session.query(Run).all()
        finally:
            session.close()
    
    def get_by_id(id):
        session = Session()
        try:
            return session.query(Run).filter_by(id = id).all()[0]
        finally:
            session.close()
        

    def get_by_run_number(run_number):
        session = Session()
        try:
            return session.query(Run).filter_by(run_number = run_number).all()
        finally:
            session.close()