from .functions import *
from scipy import special

def modified_expo_gauss(x,n,x0,beta,sig):
    return n*np.exp((x-x0)/beta)*(1-special.erf((x-x0)/(np.sqrt(2)*sig) + sig/(np.sqrt(2)*beta)))

def cd_model(params, x):
    cen1 = params['cen1'].value
    sig1 = params['sig1'].value
    cen2 = params['cen2'].value
    sig2 = params['sig2'].value
    peak3_peak2_cen_ratio = params['peak3_peak2_cen_ratio'].value
    peak3_peak2_amp_ratio = params['peak3_peak2_amp_ratio'].value
    t1 = params['t1'].value
    t2 = params['t2'].value
    n1 = params['n1'].value
    n2 = params['n2'].value
    n3 = params['n3'].value
    A = params['A'].value
    B = params['B'].value
    
    z3 = (x-(peak3_peak2_cen_ratio*cen2))/sig2
    
    peak1 = A*(modified_expo_gauss(x,n1,cen1,t1,sig1) + modified_expo_gauss(x,n2,cen1,t2,sig1))
    peak2 = B*(modified_expo_gauss(x,n1,cen2,t1,sig2)+ modified_expo_gauss(x,n3,cen2,t2,sig2) + gauss(z3,peak3_peak2_amp_ratio*n1))
    return peak1 + peak2

def cd_residuals_UDET(params, x, y, alpha):
    model = cd_peak_model_UDET(params, x)
    return (model - y) / alpha

def add_cd_params_UDET(params):

    params.add('cen1',value=170,min=0)
    params.add('sig1',value=5,min=0)

    params.add('cen2',value=230,min=0)
    params.add('sig2',min=0,value=5)

    params.add('A',value = 6000, min=0)
    params.add('B',value = 8000, min=0)

    params.add('delta10', value=30, min=0)
    params.add('t1',value = 10.2, min = 0)
    params.add('t2',min=0,expr='t1+delta10')

    params.add('peak3_peak2_cen_ratio',min = 1,max=1.3,value=1.05)
    params.add('peak3_peak2_amp_ratio', min = 0.1,max = 1,value = 0.25)

    params.add('n1', value=0.8,min=0,max=1)
    params.add('n2', expr='1-n1',max=1,min=0)
    params.add('n3', expr='1 - n1 - n1*peak3_peak2_amp_ratio',min=0,max=1)