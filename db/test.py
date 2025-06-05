



#%%
import sys
import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from functions import quadratic_calibration, linear_calibration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Session, engine, Base
from models.run import Run
from models.pixel import Pixel
from models.peak import Peak
from models.fit import Fit
from models.calibration import Calibration

from controllers.run_controller import RunController
from controllers.pixel_controller import PixelController
from controllers.peak_controller import PeakController
from controllers.calibration_controller import CalibrationController

session = Session()
pixels = PixelController.get_by_run_number(7485)

for pixel in pixels:
    peaks = PeakController.get_by_run_and_pixel_number(7485,pixel.pixel_number)
    centers = []
    errors = []
    nndc_energy = []
    for peak in peaks:
        centers.append(peak.center)
        errors.append(peak.center_error)
        nndc_energy.append(peak.nndc_energy)

    plt.scatter([pixel.pixel_number]*len(centers),centers,label='%d'%pixel.pixel_number)
    plt.xlabel('pixel')
    plt.ylabel('ADC')
    plt.title('Upper Detector')
    plt.xlim(100,130)
plt.show()

for pixel in pixels:
    peaks = PeakController.get_by_run_and_pixel_number(7485,pixel.pixel_number)
    centers = []
    errors = []
    nndc_energy = []
    for peak in peaks:
        centers.append(peak.center)
        errors.append(peak.center_error)
        nndc_energy.append(peak.nndc_energy)

    plt.scatter([pixel.pixel_number-1000]*len(centers),centers,label='%d'%pixel.pixel_number)
    plt.xlabel('pixel')
    plt.ylabel('ADC')
    plt.title('Lower Detector')
    plt.xlim(20,60)
plt.show()


for pixel in pixels:
    calibration = CalibrationController.get_by_run_and_pixel_number_and_calibration_type(7485,pixel.pixel_number,calibration_type='linear')
    # print(calibration)
    if len(calibration)==0:
        pass
    else:
        plt.scatter(pixel.pixel_number,calibration[0].linear_term,label='%d'%pixel.pixel_number)
        plt.xlabel('pixel')
        plt.ylabel('linear_term')
        plt.title('Upper Detector')
        plt.xlim(100,130)
plt.show()

for pixel in pixels:
    calibration = CalibrationController.get_by_run_and_pixel_number_and_calibration_type(7485,pixel.pixel_number,calibration_type='linear')
    if len(calibration)==0:
        pass
    else:
        plt.scatter(pixel.pixel_number-1000,calibration[0].linear_term,label='%d'%pixel.pixel_number)

        plt.xlabel('pixel')
        plt.ylabel('linear term')
        plt.title('Lower Detector')
        plt.xlim(20,60)
plt.show()
# peaks = PeakController.get_by_run_and_pixel_number(7485,116)
# centers = []
# errors = []
# nndc_energy = []
# for peak in peaks:
#     centers.append(peak.center)
#     errors.append(peak.center_error)
#     nndc_energy.append(peak.nndc_energy)

# plt.errorbar(nndc_energy,centers,yerr = errors,fmt='o',color='C1',label = '116')


# sorted_nndc_energy = np.sort(nndc_energy)
# plt.plot(sorted_nndc_energy,linear_calibration(sorted_nndc_energy,calibration[0].linear_term,calibration[0].constant_term),color = 'C0', linestyle = ':')

# peaks = PeakController.get_by_run_and_pixel_number(7485,116)
# # calibration = CalibrationController.get_by_run_and_pixel_number_and_calibration_type(7485,1033,calibration_type='linear')
# centers = []
# errors = []
# nndc_energy = []
# for peak in peaks:
#     centers.append(peak.center)
#     errors.append(peak.center_error)
#     nndc_energy.append(peak.nndc_energy)

# plt.errorbar(nndc_energy,centers,yerr = errors,fmt='o',color='C1',label = '116')
# sorted_nndc_energy = np.sort(nndc_energy)
# plt.plot(sorted_nndc_energy,linear_calibration(sorted_nndc_energy,calibration[0].linear_term,calibration[0].constant_term),color='C1',linestyle = ':')


# %%
np.array(errors)[sorted_peak_indicies]

# %%
pars,err = curve_fit(linear_calibration,sorted_nndc_energy,sorted_peaks,sigma = sorted_errors)
errors = np.sqrt(np.diag(err))
# %%
import matplotlib.pyplot as plt


plt.errorbar(sorted_nndc_energy,sorted_peaks,yerr = sorted_errors,fmt='o')
plt.plot(sorted_nndc_energy,linear_calibration(sorted_nndc_energy,pars[0],pars[1]))
# %%


cal = Calibration('linear', pars[0],errors[0],pars[1],errors[1])
for peak in peaks:
    cal.peaks.append(peak)
session.add(cal)
session.commit()
# %%
errors
# %%
# runs = RunController.get_by_run_number(7485)
# print(runs)
# for run in runs:
#     session.delete(run)
#     session.commit()
# session.close()
# print(peaks)
# %%
