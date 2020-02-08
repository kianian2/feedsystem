'''
RPL @ UCSB FEED SYSTEM

Determine the necessary outlet areas of the injector

authors: Nolan McCarthy
signed off by: 
date: 02/08/20
'''
from math import pi, sqrt, cos, sin

psi_2_pascal = 6894.757
in_2_meter = 0.0254

cp = 350*psi_2_pascal
dp_pintle = 0.2 * cp #huristic 20% pressure drop
dp_an = 0.2 * cp
mdot_lox = 11.6/12.88
mdot_meth = 4.144/12.88

rho_meth = 422.62
rho_LOX = 1141.0 
rho_water = 1000
visc_meth = 0.000137 
visc_lox = 0.00020182 
visc_water = 0.00089

Dchamber = 3.053
Dpintle = Dchamber/3.3*in_2_meter
Cd_meth = 0.6 
Cd_ox   = 0.6

Ap = mdot_lox/(Cd_ox*sqrt(2*rho_LOX*dp_pintle))
Aan = mdot_meth/(Cd_meth*sqrt(2*rho_meth*dp_an))
Apint = (pi/4)*Dpintle**2
gap_t = sqrt((4/pi)*(Aan+Apint))-Dpintle
gap_t_p = Ap/(Dpintle*pi)


#=========================================

Ap_in = Ap/(in_2_meter**2)
Dpintle_in = Dpintle/in_2_meter

def prat(theta):
    Ulox = mdot_lox/(rho_LOX*Ap)
    Umeth = mdot_meth/(rho_meth*Aan)
    plox = rho_LOX*Ulox
    pmeth = rho_meth*Umeth
    return 1 - (plox*cos(theta))/(pmeth + sin(theta)*plox)
    
    
