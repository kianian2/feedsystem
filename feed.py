# RPL @ UCSB FEED SYSTEM
# Mitchell Aslo
# TANK PRESSURES
# DEVELOP A PROGRAM TO DETERMINE TANK PRESSURES AS A FUNCTION OF
# 1) mass flow rate: m_dot [kg/s]
# 2) density: rho [kg/m3]
# 3) visc: [Pa*s]

from math import *
import numpy as np
from scipy.optimize import fsolve

in2m = 0.0254;          # inches to meters
ft2m = 0.3048;          # feet to meters
psi2pa = 6894.76;       # psi to Pa
m3s2ft3min = 2118.88;   # m**3/s to ft**3/min

def get_PT(m_dot,rho,visc,L_tube,L_hose,K_tube,K_hose):
    '''
    Get's required tank pressure
    
    Inputs:
        mass flow rate: m_dot [kg/s]
        density: rho [kg/m3]
        visc: [Pa*s]
    
    Returns:
        Tanks Pressure, PT [psi]
        
    '''
    
    # Conversion Factors
    
    
    g = 9.81;               # magnitude of acceleration due to gravity term [m/s**2] 
    pg = rho*g;       # oxygen density times gravity [Pa/s**2]
    
    D_t = (0.5-0.035*2)*in2m;   # Inner Diameter of tube [in] to [m]
    A_t = pi*(D_t**2)/4;        # Inner Area of tube [m2]
    D_h = .5*in2m;              # Inner Diameter of hose [in] to [m]
    A_h = pi*(D_h**2)/4;        # Inner Area of hose [m2]
    Pi = 420*psi2pa;            # Chamber Pressure [Pa]
    
    Q = m_dot/rho;                         # Flow Rate [m3/s]
    v_tube = Q/A_t;                         # Ox tube velocity [m/s]
    v_hose = v_tube*(A_t/A_h);              # Ox hose velocity [m/s]
    KE_tube = pg*(v_tube**2/(2*g));     # Kinetic Energy in tube in Pressure [Pa]
    KE_hose = pg*(v_hose**2/(2*g));     # Kinetic Energy in hose in Pressure [Pa]
    
    pg_dv = (KE_hose-KE_tube)/psi2pa;            # Change in velocity change
    
    zi = 29.65*in2m;                              # Injector height in meters [ft] to [m]
    zT = 37.76*in2m;                               # Tank Outlet height in meters [in] to [m]
    z = zi - zT;                                # height difference [m]
    grav_loss = pg*z/psi2pa;            # Ox gravitational losses [psi]
    
    
    u = visc;                             # dynamic viscosity oxygen [Ns/m2]
    Re_tube = rho*v_tube*D_t/u;   # Reynolds Number oxygen tube
    Re_hose = rho*v_hose*D_h/u;   # Reynolds Number oxygen hose
    
    e = 0.03e-3;                                # Roughness coefficient for Steel commercial pipe [m]
    Rg_tube = e/D_t;                            # Relative Roughness tube
    Rg_hose = e/D_h;
    
    f_tube = 0.0055*(1+(2e4*Rg_tube + (10**6)/Re_tube)**(1/3));
    f_hose = 0.0055*(1+(2e4*Rg_hose + (10**6)/Re_hose)**(1/3));
    
    pg_hf = (KE_tube*f_tube*L_tube/D_t + KE_hose*f_hose*L_hose/D_h)/psi2pa;        # friction head losses oxygen [psi]
   
    pg_hm = (KE_tube*(K_tube)+KE_hose*K_hose)/psi2pa;   # minor losses due to valves, bends, and fittings [psi]
    
    PT = Pi/psi2pa+grav_loss+pg_hm+pg_hf+pg_dv; #  Tank Pressure [psi]
    
    return PT

def get_PT_CH4(mdot,rho,visc):
    
    g = 9.81; 
    Ko = 0.78;          # Pipe entrances 
    no = 1;             # # of entrances
    Ke = 1;             # Pipe Exits
    ne = 0;             # # of exits
    KEb = 1.5;          # Elbows 90deg
    nEb = 2;            # # of elbows
    K90 = 0.2;          # Long Radius 90deg
    n90 = 4;            # # of long radius 90deg
    K45 = 0.4;          # 45 deg bends
    n45 = 0;            # # of 45 deg bends
    KTL = 0.9;          # Tee (Line Flow)
    nTL = 0;            # # of Tee (Line Flow)
    KTB = 2.0;          # Tee (Branch Flow)
    nTB = 1;            # # of Tee (Branch Flow)
    Kb  = 0.08;         # Ball Valve
    KFt = 0.08;         # Union Fittings
    nFt = 5;            # # of union fittings
    Kc = 10;            # Check Valve
    
    
    K = no*Ko+ne*Ke+nEb*KEb+n90*K90+n45*K45+nTL*KTL+nTB*KTB+Kb+nFt*KFt+Kc;   # minor losses coefficient
    K_tube = K-KFt;
    K_hose = KFt;
    
    L_tube = (11+3*pi+2.5+2.15+3.75+20+3+pi*.75)*in2m;                  # Tube lengths from tank to hose [m]
    L_hose = (14.34+3)*in2m; 
    return get_PT(mdot,rho,visc,L_tube,L_hose,K_tube,K_hose)

def get_PT_LOx(mdot,rho,visc):
    
    g = 9.81; 
    Ko = 0.78;          # Pipe entrances 
    no = 1;             # # of entrances
    Ke = 1;             # Pipe Exits
    ne = 0;             # # of exits
    KEb = 1.5;          # Elbows 90deg
    nEb = 2;            # # of elbows
    K90 = 0.2;          # Long Radius 90deg
    n90 = 4;            # # of long radius 90deg
    K45 = 0.4;          # 45 deg bends
    n45 = 0;            # # of 45 deg bends
    KTL = 0.9;          # Tee (Line Flow)
    nTL = 0;            # # of Tee (Line Flow)
    KTB = 2.0;          # Tee (Branch Flow)
    nTB = 1;            # # of Tee (Branch Flow)
    Kb  = 0.08;         # Ball Valve
    KFt = 0.08;         # Union Fittings
    nFt = 5;            # # of union fittings
    Kc = 10;            # Check Valve
    
    
    K = no*Ko+ne*Ke+nEb*KEb+n90*K90+n45*K45+nTL*KTL+nTB*KTB+Kb+nFt*KFt+Kc;   # minor losses coefficient
    K_tube = K-KFt;
    K_hose = KFt;
    
    L_tube = (11+3*pi+2.5+2.15+5.75+17+3+pi*.75)*in2m;                  # Tube lengths from tank to hose [m]
    L_hose = (13.07+3)*in2m; 
    return get_PT(mdot,rho,visc,L_tube,L_hose,K_tube,K_hose)
    


def get_mdot_CH4(PT,rho_,visc_):
    def temp(mdot_):
        return get_PT_CH4(mdot_,rho_,visc_) - PT
    return fsolve(temp,0.6)[0]

def get_mdot_LOx(PT,rho_,visc_):
    def temp(mdot_):
        return get_PT_LOx(mdot_,rho_,visc_) - PT
    return fsolve(temp,0.6)[0]