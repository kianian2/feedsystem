'''
RPL @ UCSB FEED SYSTEM

Determine the worst case pressures across the injector
which occur at startup

author: Nolan McCarthy
signed off by: 
date: 02/08/20
'''

from math import pi
from TankPres import *
from injector3 import *

Pi = 0 # zero chamber pressure, guage (psi)

loss_Ox = PT_Ox - grav_loss_Ox - Pi/psi2pa

KE_Ox_2 = loss_Ox*psi2pa/(K+ K_pint + f*L/D)

loss_CH4 = PT_CH4 - grav_loss_CH4 - Pi/psi2pa

KE_CH4_2 = loss_CH4*psi2pa/(K + K_an + f*L/D)

print('')
print('Injector Pressures')
print('Max Pressure drop Methane',KE_CH4_2*K_an/psi_2_pascal,' psi')
print('Max Pressure drop Oxygen',KE_Ox_2*K_pint/psi_2_pascal,' psi')
