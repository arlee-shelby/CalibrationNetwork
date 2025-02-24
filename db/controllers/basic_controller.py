import numpy as np

def histogram(variable,bins):
    hist, bin_edges = np.histogram(variable, bins = bins)
    width = bin_edges[1]-bin_edges[0]
    return hist, bin_edges, width