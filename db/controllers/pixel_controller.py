import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Session
from models.pixel import Pixel
import numpy as np

session = Session()

class PixelController():
    def __init__(pixel):
        self.pixel = pixel

    def get_pixels():
        return session.query(Pixel).all()

    def get_pixel_number(num):
        return session.query(Pixel).filter_by(pixel_number = num).all()[0]

    def nab_trap_filter_results(trap_rise, trap_length, trap_decay):
        run.nab_run.singleWaves().resetCuts()
        run.nab_run.singleWaves().defineCut('pixel', '=', pixel_number)
        trap_filter = run.nab_run.singleWaves().determineEnergyTiming(method='trap', params=[trap_rise, trap_length, trap_decay])
        


