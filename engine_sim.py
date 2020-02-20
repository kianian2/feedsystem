# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 20:18:53 2020

@author: mitchellaslo
"""

from feed import *
from thermo import get_tank_properties
from materials import Oxygen, Methane
import numpy as np

def get_MR(t_end, pressure_LOx, pressure_CH4):
    TLOx,TCH4 = get_tank_properties(t_end, pressure_LOx, pressure_CH4)
    ox = Oxygen(pressure_LOx,TLOx)
    ch4 = Methane(pressure_CH4,TCH4)
    rho_LOx = ox.get_density()
    rho_CH4 = ch4.get_density()
    visc_LOx = ox.get_viscosity()
    visc_CH4 = ch4.get_viscosity()
    mdot_LOX = get_mdot_LOx(pressure_LOx, rho_LOx, visc_LOx)
    mdot_CH4 = get_mdot_CH4(pressure_CH4, rho_CH4, visc_CH4)
    MR = mdot_LOX/mdot_CH4
    return MR

ts = np.arange(0,20*60,60)
MRs = []
for t in ts:
    Mr = get_MR(t,538,461)
    print(Mr)
    MRs.append(Mr)

import matplotlib.pyplot as plt
plt.plot(ts/60,MRs)
plt.ylabel("Mixture Ratio")
plt.xlabel("time after pressurization (min)")
plt.show()

# MR = 2.8;               # (Ox:CH4) mixture ratio
# mdot_tot = 1.22; 
# mdot_LOx = mdot_tot * MR/(MR+1);                # mass flow rate of LOx [kg/s]
# mdot_CH4 = mdot_tot * 1/(MR+1);  
# p_LOx = 1142           # density LOx Based on Pt = 725 psia and T = 100K [kg/m3]
# p_CH4 = 423          # density CH4 Based on P = 473.6 psia and T = [100 111.7]K [kg/m3]
# u_LOx = 202e-6; 
# u_CH4 = 122e-6; 
# TP_LOx = get_PT_LOx(mdot_LOx,p_LOx,u_LOx)
# TP_CH4 = get_PT_CH4(mdot_CH4,p_CH4,u_CH4)

# mdot_LOX_2 = get_mdot_LOx(TP_LOx, p_LOx, u_LOx)
# mdot_CH4_2 = get_mdot_CH4(TP_CH4, p_CH4, u_CH4)

# TP_range_ox = np.linspace(500,600,100)
# p_range_ox = np.linspace(722,1150,100)

# MRs = np.zeros((100,100))

# for i,tp in enumerate(TP_range_ox):
#     for j,p in enumerate(p_range_ox):
#         MRs[i][j] =  get_mdot_LOx(tp, p, u_LOx)/mdot_CH4_2

# MR = mdot_LOX_2/mdot_CH4_2
# import matplotlib.pyplot as plt

# plt.imshow(MRs)
# plt.colorbar()
# plt.show()
