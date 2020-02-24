import numpy as np
from scipy.integrate import odeint
from feed import get_PT_CH4
from feed import get_PT_LOx
from math import *
import matplotlib.pyplot as plt
'''
script for estimating time from valve open
to when it exits the injector
'''

in2m = 0.0254;          # inches to meters
ft2m = 0.3048;          # feet to meters
psi2pa = 6894.76;       # psi to Pa
m3s2ft3min = 2118.88;
p_LOx = 1104;     # m**3/s to ft**3/min
p_CH4 = 442.5;   
u_LOx = 202e-6;  
u_CH4 = 122e-6;
Area = np.pi * (.5/2 * in2m)**2
L0 = 18 * in2m
Lf = 45 * in2m
Press = psi2pa * 550
xInitLOx = [0.001,p_LOx * Area * L0]
xInitLCH4 = [0.001,p_CH4 * Area * L0]
def loss(v,rho,visc,prop = ''):
    D_t = (0.5-0.035*2)*in2m;   # Inner Diameter of tube [in] to [m]
    A_t = pi*(D_t**2)/4
    mdot = A_t*v*rho
    if(prop == 'meth'):
        pdrop = get_PT_CH4(mdot,rho,visc) - 420
    elif(prop == 'lox'):
        pdrop = get_PT_LOx(mdot,rho,visc) - 420
    return pdrop*psi2pa

def func(x,t,rho = 1, visc = 1,prop = ''):
    dx = [0,0]
    dx[0] = ((Press - loss(x[0],rho,visc,prop))*Area - rho * Area * x[0])
    dx[1] = rho * Area * x[0]   
    return dx


time = np.linspace(0,.07,500)
yLox = odeint(func,xInitLOx,time,args=(p_LOx, u_LOx,'lox'))
yMeth = odeint(func,xInitLCH4,time,args=(p_CH4, u_CH4,'meth'))

distLox = yLox[:,1]/(p_LOx * Area)
distMeth = yMeth[:,1]/(p_CH4 * Area)
plt.plot(time,distLox,label = 'LOx')
plt.plot(time,distMeth,label = 'LCH4')
plt.plot([0,max(time)],[Lf,Lf],label = 'Injector')
plt.xlabel("Time")
plt.ylabel("Distance from main valve (m)")
plt.legend()
print("Time for LOX " + str(time[distLox == Lf - np.min(np.abs(distLox-Lf))])+ str(time[distLox == Lf + np.min(np.abs(distLox-Lf))]))
print("Time for Methane " + str(time[distMeth == Lf - np.min(np.abs(distMeth-Lf))]) + str(time[distMeth == Lf + np.min(np.abs(distMeth-Lf))]))