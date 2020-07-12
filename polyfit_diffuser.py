import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

disp = False
datapoints = np.array([[12.5,2],
                      [30,4],
                      [50,5.5],
                      [100,7.8],
                      [200,11],
                      [300,13.5]])
x = datapoints[:,0]
y = datapoints[:,1]

def q_of_p(x,cd):
    return cd * x**(1/2)

params = curve_fit(q_of_p, x, y)

def q_of_p(x):
    return params[0] * x**(1/2)

if(disp):
    xarr = np.linspace(0,300,100)
    plt.plot(x,y,'o')
    plt.plot(xarr, q_of_p(xarr))
    print("CV is {}gpm/psi with covariance {}".format(params[0],params[1]))
    plt.show()