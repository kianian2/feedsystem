# RPL @ UCSB FEED SYSTEM
# Mitchell Aslo
## TANK PRESSURES
# DEVELOP A PROGRAM TO DETERMINE TANK PRESSURES AS A FUNCTION OF
#% 1) DISTANCE FROM ENGINE AND 2) HEIGHT DIFFERENCE (CAN CHANGE)
# 3) HEAD LOSSES DUE TO MAJOR AND MINOR LOSSES (DROPS ACROSS VALVES)​

from math import *
from injector3 import *
# Conversion Factors
in2m = 0.0254;          # inches to meters
ft2m = 0.3048;          # feet to meters
psi2pa = 6894.76;       # psi to Pa
m3s2ft3min = 2118.88;   # m**3/s to ft**3/min

# Constants
p_LOx = 1104;           # density Ox Based on Pt = 725 psia and T = 100K [kg/m3]
p_CH4 = 442.5;         # density CH4 Based on Pt = 725 psia and T = 100K [kg/m3]
g = 9.81;              # magnitude of acceleration due to gravity term [m/s**2] 
pg_LOx = p_LOx*g;        # oxygen density times gravity [Pa/s**2]
pg_CH4 = p_CH4*g;      # CH4 density times gravity [Pa/s**2]
MR = 2.8;              # (CH4:Ox) WRONG! mixture ratio
mdot_tot = 1.22;       # Total mass flow rate [kg/s]

D_t = (0.5-0.035*2)*in2m;   # Inner Diameter of tube [in] to [m]
A_t = pi*(D_t**2)/4;         # Inner Area of tube [m2]
D_h = .5*in2m;              # Inner Diameter of hose [in] to [m]
A_h = pi*(D_h**2)/4;        # Inner Area of hose [m2]
Pi = 350*psi2pa;            # Chamber Pressure [Pa]

mdot_LOx = mdot_tot * MR/(MR+1);             # mass flow rate of LOx [kg/s]
Q_LOx = mdot_LOx/p_LOx;                        # Flow Rate [m3/s]
v_LOx_tube = Q_LOx/A_t;                       # Ox tube velocity [m/s]
v_LOx_hose = v_LOx_tube*(A_t/A_h);            # Ox hose velocity [m/s]
KE_LOx_tube = pg_LOx*(v_LOx_tube**2/(2*g));    # Kinetic Energy in tube in Pressure [Pa]
KE_LOx_hose = pg_LOx*(v_LOx_hose**2/(2*g));    # Kinetic Energy in hose in Pressure [Pa]

mdot_CH4 = mdot_tot * 1/(MR+1);         # mass flow rate of CH4 [kg/s]
Q_CH4 = mdot_CH4/p_CH4;                 # Flow Rate [m3/s]
v_CH4_tube = Q_CH4/A_t;                 # CH4 velocity [m/s]
v_CH4_hose = v_CH4_tube*(A_t/A_h);
KE_CH4_tube = pg_CH4*(v_CH4_tube**2/(2*g));     # Kinetic Energy in tube Pressure [Pa]
KE_CH4_hose = pg_CH4*(v_CH4_hose**2/(2*g));     # Kinetic Energy in hose Pressure [Pa]

pg_dv_LOx = (KE_LOx_hose-KE_LOx_tube)/psi2pa;            # Change in velocity change
pg_dv_CH4 = (KE_CH4_hose-KE_CH4_tube)/psi2pa;            # Change in velocity change

zi = 2.5*ft2m;                              # Injector height in meters [ft] to [m]
zT = 10*in2m;                               # Tank Outlet height in meters [in] to [m]
z = zi - zT;                                # height difference [m]
grav_loss_LOx = pg_LOx*z/psi2pa;            # Ox gravitational losses [psi]
grav_loss_CH4 = pg_CH4*z/psi2pa;            # CH4 gravitational losses [psi]

L_tube = (5.5+5.5+2+2.5+3+3.5+2.5+6+2.5+3)*in2m;                  # Tube lengths from tank to hose [m]
L_hose = 24*in2m;                           # Hose length from tube to inj [m]
L = L_tube+L_hose;                          # Total Pipe Length [m]

u_LOx = 202e-6;                             # dynamic viscosity oxygen [Ns/m2]
Re_LOx_tube = p_LOx*v_LOx_tube*D_t/u_LOx;   # Reynolds Number oxygen tube
Re_LOx_hose = p_LOx*v_LOx_hose*D_h/u_LOx;   # Reynolds Number oxygen hose

u_CH4 = 122e-6;                             # dynamic viscosity CH4 [Ns/m2]
Re_CH4_tube = p_CH4*v_CH4_tube*D_t/u_CH4;   # Reynolds Number CH4 tube
Re_CH4_hose = p_CH4*v_CH4_hose*D_h/u_CH4;   # Reynolds Number CH4 hose

e = 0.03e-3;                                # Roughness coefficient for Steel commercial pipe [m]
Rg_tube = e/D_t;                            # Relative Roughness tube
Rg_hose = e/D_h;

f = 0.0225;                                 # friction factor from Moody Digram
f_lox_tube = 0.0055*(1+(2e4*Rg_tube + (10**6)/Re_LOx_tube)**(1/3));
f_lox_hose = 0.0055*(1+(2e4*Rg_hose + (10**6)/Re_LOx_hose)**(1/3));
f_ch4_tube = 0.0055*(1+(2e4*Rg_tube + (10**6)/Re_CH4_tube)**(1/3));
f_ch4_hose = 0.0055*(1+(2e4*Rg_hose + (10**6)/Re_CH4_hose)**(1/3));

pg_hf_LOx = (KE_LOx_tube*f_lox_tube*L_tube/D_t + KE_LOx_hose*f_lox_hose*L_hose/D_h)/psi2pa;        # friction head losses oxygen [psi]
pg_hf_CH4 = (KE_CH4_tube*f_ch4_tube*L_tube/D_t + KE_CH4_tube*f_ch4_hose*L_hose/D_h)/psi2pa;        # friction head losses CH4 [psi]

Ko = 0.78;          # Pipe entrances 
no = 1;             # # of entrances
Ke = 1;             # Pipe Exits
ne = 0;             # # of exits
KEb = 1.5;          # Elbows 90deg
nEb = 1;            # # of elbows
K90 = 0.2;          # Long Radius 90deg
n90 = 4;            # # of long radius 90deg
K45 = 0.4;          # 45 deg bends
n45 = 0;            # # of 45 deg bends
KTL = 0.9;          # Tee (Line Flow)
nTL = 0;            # # of Tee (Line Flow)
KTB = 2.0;          # Tee (Branch Flow)
nTB = 2;            # # of Tee (Branch Flow)
Kb  = 0.08;         # Ball Valve
KFt = 0.08;         # Union Fittings
nFt = 5;            # # of union fittings
Kc = 10;            # Check Valve

Cd_CH4 = 0.6        # Meth reservoir discharge coeff
K_CH4=1/(Cd_CH4**2) # Meth reservoir 
Cd_CH4 = 0.6        # Meth reservoir discharge coeff
Cd_Ox = 0.6       # Ox annulus discharge coeff 
K_pint = (A_t/(Ap*Cd_Ox))**2
K_an = (A_t/(Aan*Cd_CH4))**2


K = no*Ko+ne*Ke+nEb*KEb+n90*K90+n45*K45+nTL*KTL+nTB*KTB+Kb+nFt*KFt+Kc;   # minor losses coefficient
K_tube = K-KFt;
K_hose = KFt;
pg_hm_LOx = (KE_LOx_tube*(K_tube+K_pint)+KE_LOx_hose*K_hose)/psi2pa;   # minor losses due to valves, bends, and fittings [psi]
pg_hm_CH4 = (KE_CH4_tube*(K_tube+K_an)+KE_CH4_tube*K_hose)/psi2pa;   # minor losses due to valves, bends, and fittings [psi]

PT_LOx = Pi/psi2pa+grav_loss_LOx+pg_hm_LOx+pg_hf_LOx+pg_dv_LOx; # Oxidizer Tank Pressure [psi]
PT_CH4 = Pi/psi2pa+grav_loss_CH4+pg_hm_CH4+pg_hf_CH4+pg_dv_CH4; # CH4 Tank Pressure [psi]

print(' ') 
print('LOX VALUES') 
print('Grav  Losses  = ',float(grav_loss_LOx),' psi') 
print('Minor Losses  = ',float(pg_hm_LOx),' psi') 
print('Major Losses  = ',float(pg_hf_LOx),' psi') 
print('Tank Pressure = ',float(PT_LOx),' psi') 
print(' ') 
print('LCH4 VALUES') 
print('Grav  Losses  = ',float(grav_loss_CH4),' psi') 
print('Minor Losses  = ',float(pg_hm_CH4),' psi') 
print('Major Losses  = ',float(pg_hf_CH4),' psi') 
print('Tank Pressure = ',float(PT_CH4),' psi') 

# REGULATOR SETTING

# Find the pressure setting for both regulators into each
# tank. Use Helium values to determine flow

R_He = 2077.1;                  # Gas constant [J/kg/K]
Z_0 = 1.04;                     # Compressibility factor in HE tank

D_t = 8*in2m;                   # Tank Inner Diameter [m]
A_t = pi/4*(D_t**2);             # Tank cross-sectional area [m2]
D_Tube = (.25-2*0.049)*in2m;    # Tube inner diameter [m]
A_Tube = pi/4*(D_Tube**2);      # Tube area [m2]

Q_He_Ox = Q_LOx;                 # Volumetric flow of Helium in tank [m3/s]
v_He_Ox = Q_He_Ox/A_t;          # Helium plane velocity [m/s]

P_0 = 2214.7*psi2pa;            # Helium Pressure in Tank [Pa]
T_0 = 310;                      # Helium Temperature in tank at desert [K]

P_T_LOx = PT_LOx*psi2pa;          # Required Prop Tank Pressure [Pa]

p_He_Tank = P_0/R_He/T_0/Z_0;   # Density of Helium leaving tank [kg/m3]

N2 = 22.67;     # numerical constant (std ft3/min, psia,R)
p1 = 2214.7;    # absolute pressure
pox = 554.7;    
pch4  = 460+14.7;
dp_ox = p1-pox;
dp_ch4 = p1 - pch4;
Gg = .138;      # gas specific gravity
T_R = 558;      # inlet temp Rankine
T_Std = 273.15; # standard temp [K]
P_Std = 101325; # standard pressure [Pa]

# oxygen side
Q_He_Ox = 0.7898/1000;
actual_ft_ox = Q_He_Ox*m3s2ft3min;             # flow rate req in ft3/min
q_ft_ox = actual_ft_ox*(pox*psi2pa/P_Std)*(T_Std/T_0); 	# flow rate in std ft3/min
Cv_sonic_ox = (q_ft_ox/(0.471*N2*p1))*sqrt(Gg*T_R);  # cv at sonic flow
nitrogen_scfm_ox = q_ft_ox/2.65;

# methane side
Q_CH4 = 0.75906/1000;
q_act_ch4 = Q_CH4*m3s2ft3min;       # actual flow rate
q_ft_ch4 = q_act_ch4*(pch4*psi2pa/P_Std)*(T_Std/T_0);   # flow rate in scfm
Cv_sonic_ch4 = (q_ft_ch4/(0.471*N2*p1))*sqrt(Gg*T_R);# cv at sonic flow
nitrogen_scfm_ch4 = q_ft_ch4/2.65;

print(' ') 
print('Helium LOX SIDE paramters')
print('flow rate of helium',float(actual_ft_ox),'ft3/min')
print('flow rate of helium in SCFM',float(q_ft_ox),'ft3/min')
print('Cv at choked flow',float(Cv_sonic_ox))
print('equivalent flow rate of nitrogen in SCFM',float(nitrogen_scfm_ox),'ft3/min')

print(' ') 
print('Helium CH4 SIDE paramters')
print('flow rate of helium',float(q_act_ch4),'ft3/min')
print('flow rate of helium in SCFM',float(q_ft_ch4),'ft3/min')
print('Cv at choked flow',float(Cv_sonic_ch4))
print('equivalent flow rate of nitrogen in SCFM',float(nitrogen_scfm_ch4),'ft3/min')
