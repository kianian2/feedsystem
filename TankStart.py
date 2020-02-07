## RPL @ UCSB FEED SYSTEM

# DEVELOP A PROGRAM TO DETERMINE TANK PRESSURES AS A FUNCTION OF
# 1) DISTANCE FROM ENGINE AND 2) HEIGHT DIFFERENCE (CAN CHANGE)
# 3) HEAD LOSSES DUE TO MAJOR AND MINOR LOSSES (DROPS ACROSS VALVES)

from math import pi
from TankPres import *
from injector3 import *

in2m = 0.0254  # inches to meters
ft2m = 0.3048  # feet to meters
psi2pa = 6894.76  # psi to Pa

Pi = 0*psi2pa #no chamber pressure

loss_Ox = PT_Ox - grav_loss_Ox - Pi/psi2pa

KE_Ox_2 = loss_Ox*psi2pa/(K+ K_pint + f*L/D)

loss_CH4 = PT_CH4 - grav_loss_CH4 - Pi/psi2pa

KE_CH4_2 = loss_CH4*psi2pa/(K + K_an + f*L/D)

print('Max Pressure drop Methane',KE_CH4_2*K_an/psi_2_pascal,' psi')
print('Max Pressure drop Oxygen',KE_Ox_2*K_pint/psi_2_pascal,' psi')