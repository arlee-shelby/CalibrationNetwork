import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Session
from models.pixel import Pixel


class PixelController():
    def __init__(self,pixel):
        self.pixel = pixel

    def get_all():
        session = Session()
        try:
            return session.query(Pixel).all()
        finally:
            session.close()
        
    
    def get_by_id(id):
        session = Session()
        try:
            return session.query(Pixel).filter_by(id = id).all()[0]
        finally:
            session.close()

    def get_by_pixel_number(pixel_number):
        session = Session()
        try:
            return session.query(Pixel).filter_by(pixel_number = pixel_number).all()[0]
        finally:
            session.close()

    def get_by_run_number(run_number):
        session = Session()
        try:
            return session.query(Pixel).filter_by(run_number = run_number).all()
        finally:
            session.close()
