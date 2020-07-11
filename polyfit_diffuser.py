import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

datapoints = np.array([[10,.05],
                       [40,.1],
                       [85,.15],
                       [200,.225],
                       [300,.275]])

x = datapoints[:,0]
y = datapoints[:,1]

def func(x,cd):
    return cd * x**(1/2)

params = curve_fit(func, x, y)

xarr = np.linspace(0,300,100)
plt.plot(x,y,'o')
plt.plot(xarr, func(xarr,params[0]))
print("CV is {}gpm/psi with covariance {}".format(params[0],params[1]))
plt.show()