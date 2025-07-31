import numpy as np
from lmfit import Minimizer

def get_hist_uncertainty(data):
    alpha = np.sqrt(data)
    for k in range(len(alpha)):
        if alpha[k]<1:
            alpha[k]=1
    return alpha

def linear_background(x,slope,intercept):
    return slope*x + intercept

def gauss(z,amp):
    return amp*np.exp(-0.5*(z)**2)

def get_fit(model,residuals,params,xdat,ydat,alpha):
    mini = Minimizer(residuals, params, fcn_args=(xdat, ydat, alpha))
    result = mini.minimize()
    bestfit = model(result.params, xdat)
    return bestfit, result