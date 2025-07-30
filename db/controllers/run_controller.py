import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
nab_path = '/storage/home/hcoda1/4/ashelby8/Manitoba/pyNab/src'
sys.path.append(nab_path)
import nabPy as Nab
from models.base import Session
from models.run import Run

session = Session()

class RunController:
    # def __init__(self):
    #     self.run = run
    def get_runs():
        return session.query(Run).all()

    def get_run_by_number(num):
        return session.query(Run).filter_by(run_number = num).all()[0]

    def nab_run(self, run, directory, event_bool):
        run.nab_run = True
        self.nab_run = Nab.DataRun(directory, run.run_number, ignoreEventFile = event_bool)
        session.commit()
