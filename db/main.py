import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import pandas as pd
import numpy as np
import re
from datetime import date
from models.base import Session, engine, Base
from models.run import Run
from models.pixel import Pixel
# from controllers.run_controller import RunController
# from controllers.pixel_controller import PixelController

Base.metadata.create_all(engine)
session = Session(bind=engine)

cwd = os.getcwd()

file_name = "db/manitobametadata_filters.csv"

file_path = os.path.join(cwd, file_name)

df = pd.read_table(file_path,delimiter = '|')
match = re.match(r"(\d{4})-(\d{2})-(\d{2})",df[df['RunID']==1072]['Date Time [UTC]'].iloc[0])

run_number = 1389
bias_voltage = int(df[df['RunID']==run_number]['Detector Bias Voltage [V]'].iloc[0])
sn_source = str(df[df['RunID']==run_number]['Sn113'].iloc[0])
cd_source = str(df[df['RunID']==run_number]['Cd109'].iloc[0])
average_temp = np.mean(df[df['RunID']==run_number]['Detector Armor Temperature [K]'])
number_subruns = len(df[df['RunID']==run_number])

match = re.match(r"(\d{4})-(\d{2})-(\d{2})",df[df['RunID']==run_number]['Date Time [UTC]'].iloc[0])
year, month, day = match.groups()
run_date = date(int(year),int(month),int(day))

pulser = str(df[df['RunID']==run_number]['Pulser'].iloc[0])
proton = str(df[df['RunID']==run_number]['Proton'].iloc[0])
proton_energy = int(df[df['RunID']==run_number]['Proton Energy'].iloc[0])

directory = '/storage/home/hcoda1/4/ashelby8/scratch/ManitobaData/'

run = Run(run_number, bias_voltage, sn_source, cd_source, average_temp, number_subruns, run_date, pulser, proton, proton_energy, directory, True)

pixel = Pixel(run, 76, 1250, 50, 1250)

session.add(run)
session.add(pixel)

session.commit()
session.close() 