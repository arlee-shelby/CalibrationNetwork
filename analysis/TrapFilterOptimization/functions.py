import numpy as np

def baseline(wave,baseline_start,baseline_end):
    return np.average(wave[baseline_start:baseline_end])

def falltime_corrected_wave(wave,baseline,tau):
    dt = 4e-9
    falltime_corrected = np.zeros(len(wave))
    wave = wave - baseline
    for i in range(len(wave)):
        if i>0:
            wave_t0 = wave[i-1]
            wave_t1 = wave[i]
            falltime_corrected[i] = wave_t1-(wave_t0*np.exp(-dt/tau))+falltime_corrected[i-1]

    return falltime_corrected