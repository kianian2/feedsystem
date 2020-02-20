
from math import *

# ----- Conversion Constants -----
in_to_m = 0.0254

# ----- Tank Properties ------
r_tank = 10.63/2*in_to_m
L_tank = 17*in_to_m

# ----- Styrofoam Properties -----
t_sty = 1*in_to_m
r_sty = r_tank + t_sty
k_sty = 0.4 # W/m^2K
A_sty = L_tank*2*r_sty*pi + 4*pi*r_sty**2

# ----- Convection Properties ------
h_sty = 11.97 # uses matlab, assumes 2m/s crosswind

# ----- Temperatures ------
T0_CH4 = 111.7 # Boil point of methane in Kelvin
T0_LOx = 90.19 # Same but for oxygen
env_temp = 310 # aronud 100 F, but in K

# ----- Resistive Network -----
TR_sty_cyl = log(r_sty/r_tank)/(2*pi*L_tank*k_sty)
TR_sty_sph = (r_sty-r_tank)/(4*pi*r_tank*r_sty*k_sty)
TR_sty_cond = 1/(1/TR_sty_cyl+1/TR_sty_sph)
TR_sty_conv = 1/h_sty/A_sty
TR_total = TR_sty_cond + TR_sty_conv

# ----- Heat Fluxes -----
Q_CH4 = (env_temp - T0_CH4) / TR_total
Q_LOx = (env_temp - T0_LOx) / TR_total

# ----- Temp Changes -----


print("styrofoam resistance =", TR_sty_cond)
print("convection resistance =", TR_sty_conv)
print("T of outside of styrofoam =", T0_LOx + (310-T0_LOx)*(TR_sty_cond)/(TR_sty_cond+TR_sty_conv))
print("Heat flux out of CH4", Q_CH4)
print("Heat flux out of LOx", Q_LOx)

