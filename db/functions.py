import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import least_squares
import json

def gauss(z,p1):
    return p1*np.exp(-0.5*(z)**2)

def cd_double_gauss(z1,z2,p1):
    return p1*np.exp(-0.5*(z1)**2) + p1*(10.46/44.2)*np.exp(-0.5*(z2)**2)

def step_function(z,p6):
    return p6/(1+np.exp(z))**2

def lower_exp(z,p4,p5):
    return p4*(np.exp(p5*z))/(1+np.exp(z))**4

def upper_exp(z,p9,p10):
    return p9*(np.exp(p10*z))/(1+np.exp(-z))**4

def background(x,p7,p8):
    return p7*x+p8

def F(x,pars):
    z = (x-pars[1])/pars[2]
    return gauss(z,pars[0])+lower_exp(z,pars[3],pars[4])+step_function(z,pars[5])+background(x,pars[6],pars[7])

def F_cd_double_gauss(x,pars):
    z1 = (x-pars[1])/pars[2]
    z2 = (x-pars[1]*(87.39998556405354/84.2278))/pars[2]
    return gauss(z1,pars[0])+lower_exp(z2,pars[3],pars[4])+step_function(z2,pars[5])+background(x,pars[6],pars[7]) + cd_double_gauss(z1,z2,pars[0])

def fun(pars,x,y,alpha):
    return (F(x,pars)-y)/alpha

def fun_cd_double_gauss(pars,x,y,alpha):
    return (F_cd_double_gauss(x,pars)-y)/alpha

def get_Bi_region_prominence(hist_max,background,amplitude_ratio1,amplitude_ratio2):
    max_prominence = hist_max - background
    lowest_peak_estimate = hist_max*amplitude_ratio1
    min_prominence = lowest_peak_estimate - background
    middle_peak_estimate = hist_max*amplitude_ratio2
    middle_prominence = middle_peak_estimate-background
    prominence = min_prominence

    if min_prominence<=0 or min_prominence<25:
        print('Bi min prom too small')
        prominence = middle_prominence
    if middle_prominence<=0 or middle_prominence<25:
        print('Bi middle prom too small')
        prominence = max_prominence
    if max_prominence<25:
        prominence=25

    return prominence

def get_peak_props(hist,source,height=None,threshold=None,distance=15,prominence=25,width=3,wlen=None,rel_height=0.5,plateau_size=None):
    hist_max = max(hist)
    if source=='Bi_region1':
        print('Getting Bi region1 prom')
        background = np.average(hist[0:200])*2
        amplitude_ratio1 = 0.111/1.537
        amplitude_ratio2 = 0.442/1.537
        prominence = get_Bi_region_prominence(hist_max,background,amplitude_ratio1,amplitude_ratio2)
    
    if source=='Bi_region2':
        print('Getting Bi region 2 prom')
        background = np.average(hist[:100])*2
        amplitude_ratio1 = 0.44/7.08
        amplitude_ratio2 = 1.84/7.08
        prominence = get_Bi_region_prominence(hist_max,background,amplitude_ratio1,amplitude_ratio2)

    if source=='Bi_region3':
        background = np.average(hist[:20])
        max_prominence = hist_max - background
        amplitude_ratio1 = 0.16/2.9
        amplitude_ratio2 = 0.6/2.9
        lowest_peak_estimate = hist_max*amplitude_ratio1
        min_prominence = lowest_peak_estimate
        middle_peak_estimate = hist_max*amplitude_ratio2
        middle_prominence = middle_peak_estimate
        prominence = min_prominence
        if min_prominence<=0 or min_prominence<=25:
            print('min prom too small')
            prominence = middle_prominence
        if middle_prominence<=0 or min_prominence<=25:
            print('middle prom too small')
            prominence=max_prominence

        if max_prominence<25:
            prominence=25
        
    if source=='Cd_region1':
        background = np.average(hist[:20])
        if hist_max-background<25:
            print('Cd region1 peak not found')
            return [],[],0,background
        else:
            amplitude = 0.418
            prominence = hist_max*amplitude - background/2

    if source=='Cd_region2':
        background = np.average(hist[80:])
        amplitude = 0.442
        amplitude_ratio1 = (9.05+1.41)/44.2
        lowest_peak_estimate = hist_max*amplitude_ratio1
        min_prominence = lowest_peak_estimate - background*2
        max_prominence = hist_max*amplitude - background*2
        prominence = min_prominence
        if min_prominence<=0 or min_prominence<=25:
            print('Cd region2 min prom too small')
            prominence = max_prominence

        if max_prominence<25:
            prominence=25
    peaks, props = find_peaks(hist, height=height, threshold=threshold, 
                            distance=distance, prominence=prominence, width=width, 
                            wlen=wlen, rel_height=rel_height, plateau_size=plateau_size)
    
    return peaks, props, prominence, background


def fitter(run_number, pixels, results, left_region, right_region, source, nndc_energy, flags={},height=None,threshold=None,distance=15,prominence=25,width=4,wlen=None,rel_height=0.5,plateau_size=None):
    df = {}
    for j in range(len(pixels)):
        if len(flags) != 0:
            if source=='Bi_region3' and flags['%d'%pixels[j]]==False:
                pass
            
            if source=='Cd_region1' or source=='Cd_region2' and flags['%d'%pixels[j]]==True:
                pass

        else:

            results.resetCuts()
            results.defineCut('pixel', '=', pixels[j])
            hist,bin_edges = np.histogram(results.data()['energy'],bins=np.arange(left_region,right_region))
            peaks, props, prominence, background = get_peak_props(hist,source,height=height,threshold=threshold,distance=distance,prominence=prominence,width=width,wlen=wlen,rel_height=rel_height,plateau_size=plateau_size)
            
            if len(peaks)==0:
                if source=='Bi_region2':
                    flags['%d'%pixels[j]] = False
                print('Run %d:No peaks found for pixel %d for %s'%(run_number,pixels[j],source))
                pass

            else:
                print(pixels[j])
                if source=='Bi_region2':
                    flags['%d'%pixels[j]] = True
                sorted_prominence_indicies = np.argsort(props['prominences'])[::-1]
                if source=='Bi_region1' or source=='Bi_region2' or source=='Bi_region3':
                    if len(peaks)>3:
                        peaks = peaks[sorted_prominence_indicies][0:3]
                        props['left_bases'] = props['left_bases'][sorted_prominence_indicies][0:3]
                        props['right_bases'] = props['right_bases'][sorted_prominence_indicies][0:3]
                if source=='Cd_region1' or source=='Cd_region2' and len(peaks)>1:
                    if len(peaks)>1:
                        peaks = peaks[sorted_prominence_indicies][0]
                        props['left_bases'] = props['left_bases'][sorted_prominence_indicies][0]
                        props['right_bases'] = props['right_bases'][sorted_prominence_indicies][0]
                
                plt.figure()
                df['%d'%pixels[j]] = {}
                amps = []
                for i in peaks:
                    amps.append(hist[i])
                
                for i in range(len(peaks)):
                    df['%d'%pixels[j]][i] = {}
                    df['%d'%pixels[j]][i]['hist'] = hist.tolist()
                    df['%d'%pixels[j]][i]['bin_edges'] = bin_edges.tolist()
                    df['%d'%pixels[j]][i]['nndc energy'] = nndc_energy[i]

                    if i<len(peaks)-1:
                        if props['left_bases'][i]>=props['left_bases'][i+1]:
                            print('one of the peaks is not real',i)
                            pass
                        else:
                            t_train = bin_edges[props['left_bases'][i]:props['left_bases'][i+1]]
                            y_train = hist[props['left_bases'][i]:props['left_bases'][i+1]]
                    else:
                        if props['left_bases'][i]>=props['right_bases'][i]:
                            print('last peak is not real',i)
                            pass
                        else:
                            t_train = bin_edges[props['left_bases'][i]:props['right_bases'][i]]
                            y_train = hist[props['left_bases'][i]:props['right_bases'][i]]

                    alpha = np.sqrt(y_train)
                    for k in range(len(alpha)):
                        if alpha[k]<1:
                            alpha[k]=1
                    
                    bounds =(np.array([1,0,2,0,0.3,0,-1,0]), np.array([np.inf,np.inf,np.inf,np.inf,2,np.inf,1,np.inf]))
                    x0 = [amps[i]-y_train[-1], peaks[i]+left_region, 5 , 0.7*amps[i], 0.5, y_train[1], 1e-3, y_train[-1]]

                    if source=='Cd_region2':
                        res_lsq = least_squares(fun_cd_double_gauss, x0, loss='soft_l1', f_scale=0.1,jac='3-point',args=(t_train, y_train,alpha),bounds=bounds)
                    else:
                        res_lsq = least_squares(fun, x0, loss='soft_l1', f_scale=0.1,jac='3-point',args=(t_train, y_train,alpha),bounds=bounds)
                    
                    df['%d'%pixels[j]][i]['pars'] = res_lsq.x.tolist()

                    jacobian = res_lsq.jac
                    covariance_matrix = np.linalg.inv(jacobian.T @ jacobian)
                    standard_errors = np.sqrt(np.diag(covariance_matrix))
                    df['%d'%pixels[j]][i]['par_errors'] = standard_errors.tolist()

                    chi2 = np.sum(res_lsq.fun**2)/(len(t_train)-len(x0))
                    df['%d'%pixels[j]][i]['chi2'] = chi2
                    plt.step(t_train, y_train,alpha=0.5,label = '%d'%pixels[j])
                    if source=='Cd_region2':
                        plt.plot(t_train,F_cd_double_gauss(t_train,res_lsq.x))
                    else:
                        plt.plot(t_train,F(t_train,res_lsq.x))
                    plt.legend()
                plt.savefig('test_figures/Run%dPixel%d%s'%(run_number,pixels[j],source))
    return df, flags

def get_df_values(df,i,pixel):
    hist = json.dumps(df[pixel][i]['hist'])
    bin_edges = json.dumps(df[pixel][i]['bin_edges'])
    pars = df[pixel][i]['pars']
    par_errors = df[pixel][i]['par_errors']
    chi2 = df[pixel][i]['chi2']
    nndc_energy = df[pixel][i]['nndc energy']

    return hist, bin_edges, pars, par_errors, chi2, nndc_energy

def quadratic_calibration(x,a,b,c):
    return a*x**2 + b*x+c

def linear_calibration(x,a,b):
    return a*x + b
