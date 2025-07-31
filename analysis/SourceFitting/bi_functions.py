from .functions import *
from lmfit import Parameters
from scipy.signal import find_peaks
import pylab as py

def step_function(z,amp):
    return amp/(1+np.exp(z))**2

def lower_expo(z,amp,sig):
    return amp*(np.exp(sig*z))/(1+np.exp(z))**4

def bi_model(params, x):
    num_peaks = params['num_peaks'].value
    sig_ratio = params['sig_ratio'].value
    amp_ratio = params['amp_ratio'].value
    intercept = params['intercept'].value
    slope = params['slope'].value

    peak_func = 0
    for i in range(num_peaks):
        i+=1
        amp = params['amp%d'%i].value
        cen = params['cen%d'%i].value
        sig = params['sig%d'%i].value
        step_ratio = params['step%d_ratio'%i].value
        z = (x-cen)/sig
        peak = gauss(z,amp) + lower_expo(z,amp_ratio*amp,sig_ratio*sig) + step_function(z,step_ratio*amp)
        peak_func += peak

    background = linear_background(x, slope, intercept)

    return peak_func + background

def bi_residual(params, x, y, alpha):
    model = bi_model(params, x)
    return (model - y) / alpha

def add_bi_params(params,initial_peak_props):

    params.add('sig_ratio',value=0.05,min=0)
    params.add('amp_ratio',value=0.6,min=0, max=1)

    params.add('slope',value=-1e-3)
    params.add('intercept',value=0)

    for i in range(params['num_peaks'].value):
        i+=1
        params.add('amp%d'%i,value=initial_peak_props['amp%d'%i],min=0)
        params.add('cen%d'%i,value=initial_peak_props['cen%d'%i],min=0)
        params.add('sig%d'%i,value=initial_peak_props['sig%d'%i],min=0)
        params.add('step%d_ratio'%i, value=0.01,min=-1e-1, max=1)

def get_initial_peak_props(xdat,ydat,peak_finder_props,num_peaks,initial_peak_sigmas):
    initial_peak_props = {}
    find_peaks.__defaults__ = peak_finder_props
    peaks, props = find_peaks(ydat)
    while len(peaks)>num_peaks:
        prop_list = list(peak_finder_props)
        prop_list[3] += 10
        peak_finder_props = tuple(prop_list)
        find_peaks.__defaults__ = peak_finder_props
        peaks, props = find_peaks(ydat)
    for i in range(num_peaks):
        i += 1
        if len(peaks)==num_peaks:
            initial_peak_props['amp%d'%i] = props['peak_heights'][i-1]
            initial_peak_props['cen%d'%i] = xdat[peaks[i-1]]
            initial_peak_props['sig%d'%i] = initial_peak_sigmas['sig%d'%i]
        
        elif len(peaks)==num_peaks-1:
            if i!=num_peaks:
                initial_peak_props['amp%d'%i] = props['peak_heights'][i-1]
                initial_peak_props['cen%d'%i] = xdat[peaks[i-1]]
                initial_peak_props['sig%d'%i] = initial_peak_sigmas['sig%d'%i]
            else:
                initial_peak_props['amp%d'%i] = props['peak_heights'][-1]*0.5
                initial_peak_props['cen%d'%i] = xdat[peaks[-1]]+36
                initial_peak_props['sig%d'%i] = initial_peak_sigmas['sig%d'%i]
        else:
            if num_peaks==2:
                if i<num_peaks:
                    initial_peak_props['amp%d'%i] = max(ydat)
                    initial_peak_props['cen%d'%i] = (np.argmax(ydat)+xdat[0])
                    initial_peak_props['sig%d'%i] = initial_peak_sigmas['sig%d'%i]
                else:
                    initial_peak_props['amp%d'%i] = max(ydat)*0.5
                    initial_peak_props['cen%d'%i] = (np.argmax(ydat)+xdat[0])+36
                    initial_peak_props['sig%d'%i] = initial_peak_sigmas['sig%d'%i]
            if num_peaks==3:
                if i==1:
                    amp_scale = 1
                    cen_shift = 0
                if i==2:
                    amp_scale = 1/3
                    cen_shift = 216
                if i==3:
                    amp_scale = 1/6
                    cen_shift = 252
                initial_peak_props['amp%d'%i] = max(ydat)*amp_scale
                initial_peak_props['cen%d'%i] = (np.argmax(ydat)+xdat[0]) + cen_shift
                initial_peak_props['sig%d'%i] = initial_peak_sigmas['sig%d'%i]
    return initial_peak_props

def get_bi_fit(data,num_groups,pixel,low_region,up_region,num_peaks,peak_finder_props,initial_peak_sigmas,plot=False):
    cnt = 0
    nrows,ncols=8,4
    py.figure(figsize=(8*ncols,6*nrows))
    df = {}
    df['time'] = {}
    for i in range(num_groups):
        df[i] = {}
        xdat = np.array(data['bin_edges']['%d'%i][pixel][low_region:up_region])
        ydat = np.array(data['hist']['%d'%i][pixel][low_region:up_region])
        alpha = get_hist_uncertainty(ydat)

        initial_peak_props = get_initial_peak_props(xdat,ydat,peak_finder_props,num_peaks,initial_peak_sigmas)

        params = Parameters()
        params.add('num_peaks', value=num_peaks,vary=False)
        add_bi_params(params,initial_peak_props)

        model=bi_model
        residual_model = bi_residual
        bestfit, result = get_fit(model,residual_model, params, xdat, ydat,alpha)
        if plot:
            cnt+=1
            ax=py.subplot(nrows,ncols,cnt)
            ax.step(xdat, ydat, alpha=0.5)
            ax.plot(xdat, bestfit, label='fit, no x error')

        for key in result.params.keys():
            df[i]['%s'%key] = {}
            df[i]['%s'%key] = {}
            df[i]['%s'%key]['value'] = result.params['%s'%key].value
            df[i]['%s'%key]['error'] = result.params['%s'%key].stderr
    return df