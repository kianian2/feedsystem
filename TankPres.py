## RPL @ UCSB FEED SYSTEM

# DEVELOP A PROGRAM TO DETERMINE TANK PRESSURES AS A FUNCTION OF
# 1) DISTANCE FROM ENGINE AND 2) HEIGHT DIFFERENCE (CAN CHANGE)
# 3) HEAD LOSSES DUE TO MAJOR AND MINOR LOSSES (DROPS ACROSS VALVES)

from math import pi
from injector_real import *



# Conversion Factors
in2m = 0.0254  # inches to meters
ft2m = 0.3048  # feet to meters
psi2pa = 6894.76  # psi to Pa

# Constants
p_Ox = 1104            # density Ox Based on Pt = 725 psia and T = 100K [kg/m3]
p_CH4 = 442.5          # density CH4 Based on Pt = 725 psia and T = 100K [kg/m3]
g = 9.81               # magnitude of acceleration due to gravity term [m/s **2] 
pg_Ox = p_Ox*g         # oxygen density times gravity [Pa/s **2]
pg_CH4 = p_CH4*g       # CH4 density times gravity [Pa/s **2]
MR = 2.8               # CH4:Ox mixture ratio
mdot_tot = 1.22        # Total mass flow rate [kg/s]

D = (0.5-0.049*2)*in2m      # Diameter of pipe [in] to [m]
A = pi*D **2/4                # Area of pipe [m2]
Pi = 350*psi2pa             # Pressure at injector inlet [Pa]

mdot_Ox = mdot_tot * MR/(MR+1)       # mass flow rate of LOx [kg/s]
Q_Ox = mdot_Ox/p_Ox                  # Flow Rate [m3/s]
v_Ox = Q_Ox/A                        # Ox velocity [m/s]
KE_Ox = pg_Ox*(v_Ox **2/(2*g))         # Kinetic Energy in Pressure [Pa]

mdot_CH4 = mdot_tot * 1/(MR+1)       # mass flow rate of CH4 [kg/s]
Q_CH4 = mdot_CH4/p_CH4               # Flow Rate [m3/s]
v_CH4 = Q_CH4/A                      # CH4 velocity [m/s]
KE_CH4 = pg_CH4*(v_CH4 **2/(2*g))      # Kinetic Energy in Pressure [Pa]

zi = 2.5*ft2m           # Injector height in meters [ft] to [m]
zT = 10*in2m            # Tank Outlet height in meters [in] to [m]
z = zi - zT             # height difference [m]
grav_loss_Ox  = pg_Ox*z/psi2pa   # Ox gravitational losses [psi]
grav_loss_CH4 = pg_CH4*z/psi2pa  # CH4 gravitational losses [psi]

Tube_Lengths = (6+4+1+7+2)*in2m     # Tube lengths from tank to hose [m]
Hose_Length  = 45*in2m              # Hose length from tube to inj [m]
L = Tube_Lengths+Hose_Length        # Total Pipe Length [m]

u_Ox = 195e-6               # dynamic viscosity oxygen [Ns/m2]
Re_Ox = p_Ox*v_Ox*D/u_Ox    # Reynolds Number oxygen

u_CH4 = 157e-6                  # dynamic viscosity CH4 [Ns/m2]
Re_CH4 = p_CH4*v_CH4*D/u_CH4    # Reynolds Number CH4

e = 0.015e-3        # Roughness coefficient for Steel commercial pipe [m]
Rg = e/D            # Relative Roughness

f = 0.023           # friction factor of oxygen from moody diagram

pg_hf_Ox  = KE_Ox *f*L/D/psi2pa  # friction head losses oxygen [psi]
pg_hf_CH4 = KE_CH4*f*L/D/psi2pa  # friction head losses CH4 [psi]

Ko = 0.78           # Pipe entrances 
no = 2              # # of entrances
Ke = 1              # Pipe Exits
ne = 2              # # of exits
KEb = 1.5           # Elbows 90deg
nEb = 1             # # of elbows
K90 = 0.7           # Long Radius 90deg
n90 = 5             # # of long radius 90deg
K45 = 0.4           # 45 deg bends
n45 = 2             # # of 45 deg bends
KTL = 0.9           # Tee (Line Flow)
nTL = 0             # # of Tee (Line Flow)
KTB = 2.0           # Tee (Branch Flow)
nTB = 1             # # of Tee (Branch Flow)
Kb  = 0.08          # Ball Valve
KFt = 0.08          # Union Fittings
nFt = 8             # # of union fittings
Kc = 10             # Check Valve
Cd_CH4 = 0.6        # Meth reservoir discharge coeff
K_CH4=1/(Cd_CH4**2) # Meth reservoir 
Cd_CH4 = 0.6        # Meth reservoir discharge coeff
Cd_Ox = 0.6       # Ox annulus discharge coeff 
K_pint = (A/(Ap*Cd_Ox))**2
K_an = (A/(Aan*Cd_CH4))**2


K = no*Ko+ne*Ke+nEb*KEb+n90*K90+n45*K45+nTL*KTL+nTB*KTB+Kb+nFt*KFt+Kc#+K_pint+ K_an   # minor losses coefficient
pg_hm_Ox  = KE_Ox *(K+K_pint)/psi2pa    # minor losses due to valves, bends, and fittings [psi]
pg_hm_CH4 = KE_CH4*(K+K_an)/psi2pa    # minor losses due to valves, bends, and fittings [psi]

# pg_hm_Ox = pg_hm_Ox + dPoxinj
# pg_hm_CH4 = pg_hm_CH4 + dPch4inj
PT_Ox  = Pi/psi2pa+ grav_loss_Ox+ pg_hm_Ox+ pg_hf_Ox # Oxidizer Tank Pressure [psi]
PT_CH4 = Pi/psi2pa+grav_loss_CH4+pg_hm_CH4+pg_hf_CH4  # CH4 Tank Pressure [psi]

print(' ') 
print('LOX VALUES') 
print('Grav  Losses  = ',float(grav_loss_Ox),' psi') 
print('Minor Losses  = ',float(pg_hm_Ox),' psi') 
print('Major Losses  = ',float(pg_hf_Ox),' psi') 
print('Tank Pressure = ',float(PT_Ox),' psi') 
print(' ') 
print('LCH4 VALUES') 
print('Grav  Losses  = ',float(grav_loss_CH4),' psi') 
print('Minor Losses  = ',float(pg_hm_CH4),' psi') 
print('Major Losses  = ',float(pg_hf_CH4),' psi') 
print('Tank Pressure = ',float(PT_CH4),' psi') 
print('KE_Ox',KE_Ox)
print('KE_CH4',KE_CH4)
print('dPoxinj',KE_Ox*K_pint/psi2pa)
print('dPch4inj',KE_CH4*K_an/psi2pa)
# return PT_Ox,PT_CH4
##print('Tank Pressure = ',float(PT_CH4),' psi') 
