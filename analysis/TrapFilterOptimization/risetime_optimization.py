from .functions import *
import matplotlib.pyplot as plt

def apply_trap(wave,rise_time,flat_top, tau, t0):
    bl = baseline(wave)
    corrected_wave = falltime_corrected_wave(wave,bl,tau)
    
    blow = t0 - (int(flat_top/2)) - rise_time
    bhigh = t0 - int(flat_top/2)

    Slow = t0 + (int(flat_top/2))
    Shigh = t0 + (int(flat_top/2)) + rise_time

    btot = 0
    for i in range(blow,bhigh):
        btot = corrected_wave[i] + btot
        
    Stot = 0
    for i in range(Slow,Shigh):
        Stot = corrected_wave[i] + Stot
        
    energy = (Stot - btot)/rise_time

    return energy

def energy_list(rise_time, flat_top, tau, t0, waves):      
    energy = []
    for i in range(0,len(waves)):
        wave = waves[i]
        energy.append(apply_trap(wave, rise_time, flat_top, tau, t0))
    return energy

def get_sigma_rt(run, pixel, tau, peak_start, peak_end, t0, rise_times, flat_top_times):
    try:
        run.singleWaves().resetCuts()
        run.singleWaves().defineCut('pixel', '=', pixel)
        results = run.singleWaves().determineEnergyTiming(method='trap', params=[1250, 50, 1250])

        results.defineCut('energy', 'between', peak_start, peak_end)
        energy_cut = results.returnCut()
        run.singleWaves().resetCuts()
        run.singleWaves().defineCut('custom',energy_cut)

        waves = run.singleWaves().waves().compute()

        for flat_top in flat_top_times:
            peakingTimesRecord = np.zeros(0)
            flatTopTimesRecord = np.zeros(0)
            sigmaRecord = np.zeros(0)
            sigErrorRecord = np.zeros(0)

            for rise_time in rise_times:
                energy = energy_list(rise_time, flat_top, tau, t0, waves)
                bins = np.arange(peak_start,peak_end)

                hist_obj = plt.hist(energy,bins=bins,alpha=0.5)
                width = hist_obj[1][1] - hist_obj[1][0]

                center = np.argmax(hist_obj[0]) + peak_start
                peak = max(hist_obj[0])
                alpha = np.sqrt(hist_obj[0])
                for k in range(len(alpha)):
                    if alpha[k]<1:
                        alpha[k]=1

    #             bounds = (np.array([2,300,0,0,0,0,0,0,0]),np.array([5*peak,620,30,peak,2,3e-1,peak,peak,2]))
    #             pars_test = [peak, center, 5, peak*0.3, 0.4, 1e-3,hist_obj[0][-1],peak*0.1,1]
    #             try:
    #                 pars = pars_test
    #                 parameters, errors = curve_fit(F_sn, hist_obj[1][:-1]+width/2, hist_obj[0], p0 = pars,bounds = bounds,sigma = sigma,absolute_sigma=True)
    #                 par_error = np.sqrt(np.diag(errors))
    #                 residuals = (hist_obj[0]- F_sn(hist_obj[1][:-1]+width/2,*parameters))/sigma
    #                 chi2 = sum(residuals**2)/len(hist_obj[0])

    #             except Exception as e:
    #                 print(e)

    #             if chi2 > 0.4 and chi2 < 15:
    #                 peakingTimesRecord = np.append(peakingTimesRecord,risingEdge)
    #                 flatTopTimesRecord = np.append(flatTopTimesRecord,flatTop)
    #                 sigmaRecord = np.append(sigmaRecord, parameters[2])
    #                 sigErrorRecord = np.append(sigErrorRecord,np.sqrt(np.diag(errors))[2])
    #             else:
    #                 peakingTimes = np.delete(peakingTimes,(int(np.where(np.round(peakingTimes,8) == np.round(risingEdge,8))[0])))
                    
    #         physical_peaking_times = peakingTimes / 250

    except Exception as e:
        print(e)

    # return physical_peaking_times, sigmaRecord, sigErrorRecord