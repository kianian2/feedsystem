import numpy as np
import itertools

def size(x):
    if type(x) == np.ndarray:
        return x.shape
    else:
        return 1

def isempty(arr):
    return len(arr) == 0

def find(cond):
    return np.where(cond)

def Pick(V,k):
    c = list(itertools.combinations(V, k))
    unq = set(c)
    return np.array([list(s) for s in unq])