import numpy as np

def gauss(z,amp):
    return amp*np.exp(-0.5*(z)**2)

def step_function(z,amp):
    return amp/(1+np.exp(z))**2

def lower_expo(z,amp,sig):
    return amp*(np.exp(sig*z))/(1+np.exp(z))**4

def linear_background(x,slope,intercept):
    return slope*x + intercept