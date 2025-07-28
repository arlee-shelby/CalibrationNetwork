from .functions import *
from scipy.optimize import curve_fit

def tau_region_func(x, a, b):
    return a + (b * x)

def tau_calc_waves(waves,min_wave_energy,num_waves):
    cnt = 0
    waves_for_tau_calc = []
    for i in range(len(waves)):
        if cnt < num_waves:
            wave = waves[i]
            if np.absolute(wave[4000] - wave[3000]) > min_wave_energy:
                cnt+=1
                waves_for_tau_calc.append(wave)         
    return waves_for_tau_calc

def optimal_tau(wave,tau_list,tau_region_start,tau_region_end):
    time_bins = np.arange(0,7001)
    slopes = []
    for tau in tau_list:
        bl = baseline(wave)
        corrected_wave = falltime_corrected_wave(wave,bl,tau)
        param, param_cov = curve_fit(tau_region_func, time_bins[tau_region_start:tau_region_end], corrected_wave[tau_region_start:tau_region_end])
        slopes.append(param[1])
    
    min_slope_index = np.argmin(slopes)
            
    opt_tau = tau_list[min_slope_index]
    return opt_tau

def average_optimal_tau(run, pixel, min_wave_energy, num_waves, tau_list,tau_region_start,tau_region_end):
    run.singleWaves().resetCuts()
    run.singleWaves().defineCut('pixel', '=', pixel)

    waves = run.singleWaves().waves().compute()
    waves_for_calc = tau_calc_waves(waves,min_wave_energy,num_waves)
        
    tau_list = []
    for wave in waves_for_calc:
        tau_list.append(optimal_tau(wave,tau_list,tau_region_start,tau_region_end))
        
    return np.average(tau_list)