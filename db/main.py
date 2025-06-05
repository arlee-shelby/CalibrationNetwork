import sys
import os
import json
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import fnmatch
import time
import nabPy as Nab
from scipy.optimize import curve_fit
from functions import fitter, get_df_values, linear_calibration, quadratic_calibration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Session, engine, Base
from models.run import Run
from models.pixel import Pixel
from models.peak import Peak
from models.fit import Fit
from models.calibration import Calibration

from controllers.peak_controller import PeakController

Base.metadata.create_all(engine)
session = Session()

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-rf', '--run_folder', default=None, help='Run folder name')
parser.add_argument('-r', '--run_number', default=None, help='Run to calibrate')

args = vars(parser.parse_args())

if args['run_folder']==None:
    print('Run folder not specified')
    sys.exit(1)

if args['run_number']==None:
    print('Run number not specified')
    sys.exit(1)

run_folder = args['run_folder']
run_number = int(args['run_number'])
run_filename = 'Run'+args['run_number']

replay_directory = '/nab41/nab/data/ReplayOutput/'
run_path = replay_directory+run_folder+'/'

num_files = len(fnmatch.filter(os.listdir(run_path),run_filename+'*'))
print('There are %d subruns in run %d'%(num_files,run_number))

db_run = Run(run_number, num_files,"False", "False")
session.add(db_run)
session.commit()

start1 = time.time()
subRunMax=50
print('max subrun is',subRunMax)
run = Nab.DataRun(run_path, run_number,subRunMin=0,subRunMax=subRunMax)
# run = Nab.DataRun(run_path, run_number)
end1 = time.time()
print("Time to construct standard nabPy run class:",(end1-start1),"s")

parameters = run.parameterFile()
filter_parameters = parameters.FilterParameters

threshold = filter_parameters[0][0]
trap_dr = filter_parameters[0][1]
trap_ft = filter_parameters[0][2]
trap_rt = filter_parameters[0][3]

start2 = time.time()
run.singleWaves().defineCut('event type', '=', 0)
results = run.singleWaves().determineEnergyTiming(method='trap', params=[trap_rt,trap_ft,trap_dr])
end2 = time.time()
print("Time to apply trap filter:",(end2-start2),"s")

print('Threshold:',threshold)
results.defineCut('energy','>',threshold)
run.singleWaves().resetCuts()
run.singleWaves().defineCut('custom', results.returnCut())

headers = run.singleWaves().headers()

upper_pixels = np.arange(1,128)
counts_upper = []
for i in upper_pixels:
    counts_upper.append(len(headers[headers['pixel']==i]))
upper_cal_pixels = np.argsort(counts_upper)[::-1][0:20]+1
upper_cal_counts = np.sort(counts_upper)[::-1][0:20]
print('Upper detector pixels:',upper_cal_pixels)
print('Upper detector counts:',upper_cal_counts)

lower_pixels = np.arange(1001,1128)
counts_lower = []
for i in lower_pixels:
    counts_lower.append(len(headers[headers['pixel']==i]))
lower_cal_pixels = np.argsort(counts_lower)[::-1][0:20]+1001
lower_cal_counts = np.sort(counts_lower)[::-1][0:20]
print('Lower detector pixels:',lower_cal_pixels)
print('Lower detector counts:',lower_cal_counts)

Bi_region1_nndc_energy = [481.6935,553.8372,565.8473]
Bi_region2_nndc_energy = [975.651,1047.795,1059.805]
Cd_region1_nndc_energy = [62.5196]
Cd_region2_nndc_energy = [84.3161]
Bi_region3_upper_nndc_energy = [52.269661,65.276915,77.748523]
Bi_region3_lower_nndc_energy = [53.104451,65.812561,76.996921]


df1, flags = fitter(run_number,upper_cal_pixels,results,1000,2500,'Bi_region1',Bi_region1_nndc_energy)

df2, upper_detector_important_flags = fitter(run_number,upper_cal_pixels,results,3000,4000,'Bi_region2',Bi_region2_nndc_energy)

df3, flags = fitter(run_number,upper_cal_pixels,results,100,300,'Bi_region3',Bi_region3_upper_nndc_energy,upper_detector_important_flags)

df4, flags = fitter(run_number,upper_cal_pixels,results,100,210,'Cd_region1',Cd_region1_nndc_energy,upper_detector_important_flags)

df5, flags = fitter(run_number,upper_cal_pixels,results,210,300,'Cd_region2',Cd_region2_nndc_energy,upper_detector_important_flags)

df6, flags = fitter(run_number,lower_cal_pixels,results,1000,2500,'Bi_region1',Bi_region1_nndc_energy)

df7, lower_detector_important_flags = fitter(run_number,lower_cal_pixels,results,3000,4000,'Bi_region2',Bi_region2_nndc_energy)

df8, flags = fitter(run_number,lower_cal_pixels,results,100,300,'Bi_region3',Bi_region3_lower_nndc_energy,lower_detector_important_flags)

df9, flags = fitter(run_number,lower_cal_pixels,results,100,210,'Cd_region1',Cd_region1_nndc_energy,lower_detector_important_flags)

df10, flags = fitter(run_number,lower_cal_pixels,results,210,300,'Cd_region2',Cd_region2_nndc_energy,lower_detector_important_flags)

df = [df1,df2,df3,df4,df5,df6,df7,df8,df9,df10]
fitted_pixels = np.unique(list(df1.keys())+list(df2.keys())+list(df3.keys())+
                          list(df4.keys())+list(df5.keys())+list(df6.keys())+
                          list(df7.keys())+list(df8.keys())+list(df9.keys())+
                          list(df10.keys()))


for i in range(len(fitted_pixels)):
    if int(fitted_pixels[i])<129:
        detector = 'upper'
    else:
        detector = 'lower'
    db_pixel = Pixel(db_run, int(fitted_pixels[i]), int(trap_rt), int(trap_ft), int(trap_dr), detector, int(threshold))
    session.add(db_pixel)
    session.commit()

    for j in range(len(df)):
        if np.any(np.array(list(df[j].keys()))==fitted_pixels[i]):
            for k in range(len(df[j][fitted_pixels[i]])):
                hist, bin_edges, pars, par_errors, chi2, nndc_energy = get_df_values(df[j],k,fitted_pixels[i])

                db_peak = Peak(db_pixel,pars[1],par_errors[1],pars[2],par_errors[2], nndc_energy)
                db_fit = Fit(db_peak,chi2,json.dumps(pars),json.dumps(par_errors),hist,bin_edges)

                session.add(db_peak)
                session.add(db_fit)
                session.commit()
                
    session.close()
    peaks = PeakController.get_by_run_and_pixel_number(run_number,fitted_pixels[i])
    centers = []
    errors = []
    nndc_energy = []
    for peak in peaks:
        centers.append(peak.center)
        errors.append(peak.center_error)
        nndc_energy.append(peak.nndc_energy)
    sorted_peaks = np.sort(centers)
    sorted_peak_indicies = np.argsort(centers)

    sorted_errors = np.array(errors)[sorted_peak_indicies]
    sorted_nndc_energy = np.array(nndc_energy)[sorted_peak_indicies]
    try:
        pars,err = curve_fit(linear_calibration,sorted_nndc_energy,sorted_peaks,sigma = sorted_errors)
        errors = np.sqrt(np.diag(err))
        db_calibration = Calibration(db_pixel, peaks, 'linear',pars[0],errors[0],pars[1],errors[1])
        session.add(db_calibration)
        session.commit()
    except Exception as e:
        print(e)
        print('Could not get linear calibration fit', fitted_pixels[i])
        pass
    try:
        pars,err = curve_fit(quadratic_calibration,sorted_nndc_energy,sorted_peaks,sigma = sorted_errors)
        errors = np.sqrt(np.diag(err))
        print(pars[0])
        db_calibration = Calibration(db_pixel, peaks, 'quadratic', pars[1],errors[1],pars[2],errors[2],pars[0],errors[0])
        session.add(db_calibration)
        session.commit()
    except Exception as e:
        print(e)
        print('Could not get quadratic calibration fit',fitted_pixels[i])
        pass
session.close()

filename = 'test_figures/testdata.json'
with open(filename, 'w') as file:
    json.dump(df, file, indent=4)
