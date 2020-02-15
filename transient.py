import numpy as np
from scipy.integrate import odeint
from feed import get_PT_CH4
from math import *

'''
script for estimating time from valve open
to when it exits the injector
'''

in2m = 0.0254;          # inches to meters
ft2m = 0.3048;          # feet to meters
psi2pa = 6894.76;       # psi to Pa
m3s2ft3min = 2118.88;   # m**3/s to ft**3/min
rho = 1100
visc = 202e-6
Area = np.pi * (.05/2 * in2m)**2
L0 = 18 * in2m
Lf = 45 * in2m
Press = psi2pa * 550
xInit = [0.0001,rho * Area * L0]
def loss(v,rho,visc):
    D_t = (0.5-0.035*2)*in2m;   # Inner Diameter of tube [in] to [m]
    A_t = pi*(D_t**2)/4
    mdot = A_t*v*rho
    pdrop = get_PT_CH4(mdot,rho,visc) - 420
    return pdrop*psi2pa

def func(x,t):
    dx = [0,0]
    dx[0] = ((Press - loss(x[0],rho,visc))*Area - rho * Area * x[0])
    dx[1] = rho * Area * x[0]
    return dx

time = np.linspace(0,.5,10)
Y = odeint(func,xInit,time)
print(Y)
print(Y[:,1]/(rho * Area))
