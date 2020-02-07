import numpy as np
from scipy.optimize import fsolve,root

psi_2_pascal = 6894.757
in_2_meter = 0.0254

cp = 350*psi_2_pascal
dp_pintle = 0.2 * cp #huristic 20% pressure drop
dp_an = 0.2 * cp
#mdot_lox = 11.6/12.88
mdot_lox = 11.6/12.88
#mdot_lox = 0.92
#mdot_meth = 4.144/12.88
mdot_meth = 4.144/12.88
#mdot_meth = 0.33

rho_meth = 422.62
rho_LOX = 1141.0 
rho_water = 1000
visc_meth = 0.000137 
visc_lox = 0.00020182 
visc_water = 0.00089

Dchamber = 3.053

Dpintle = Dchamber/3.3*in_2_meter

Cd = 0.6 #assume more resistance

Ap = mdot_lox/(Cd*np.sqrt(2*rho_LOX*dp_pintle))

Aan = mdot_meth/(Cd*np.sqrt(2*rho_meth*dp_an))

Apint = (np.pi/4)*Dpintle**2

gap_t = np.sqrt((4/np.pi)*(Aan+Apint))-Dpintle

gap_t_p = Ap/(Dpintle*np.pi)


#=========================================

Ap_in = Ap/(in_2_meter**2)
Dpintle_in = Dpintle/in_2_meter

Nholes = 40

# intv = np.vectorize(int)

def get_pdrop(A):
    one = mdot_lox/(Cd*A*np.sqrt(2*rho_LOX))
    return one**2

# def dp_ox(c):
#     d1 = c/64
#     d2 = (np.pi*Dpintle_in)/Nholes - d1
#     d2 = intv(d2*64)/64
#     area_eq = Ap_in - Nholes*(d1**2 + d2**2)*(np.pi/4)
#     return area_eq


def prat(theta):
    Ulox = mdot_lox/(rho_LOX*Ap)
    Umeth = mdot_meth/(rho_meth*Aan)
    plox = rho_LOX*Ulox
    pmeth = rho_meth*Umeth
    return 1 - (plox*np.cos(theta))/(pmeth + np.sin(theta)*plox)
    
    
