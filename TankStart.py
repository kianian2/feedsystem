'''
RPL @ UCSB FEED SYSTEM

Determine the worst case pressures across the injector
which occur at startup

author: Nolan McCarthy
signed off by: 
date: 02/08/20
'''

from math import pi
from TankPres_2 import *
from injector3 import *

Pi = 0 # zero chamber pressure, guage (psi)

loss_LOx = PT_LOx - grav_loss_LOx - Pi/psi2pa

KE_LOx_2 = loss_LOx*psi2pa/(K+ K_pint + f*L/D_t)

loss_CH4 = PT_CH4 - grav_loss_CH4 - Pi/psi2pa

KE_CH4_2 = loss_CH4*psi2pa/(K + K_an + f*L/D_t)

print('')
print('Injector Pressures')
print('Max Pressure drop Methane',KE_CH4_2*K_an/psi_2_pascal,' psi')
print('Max Pressure drop Oxygen',KE_Ox_2*K_pint/psi_2_pascal,' psi')
