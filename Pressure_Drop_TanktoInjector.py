"""
Created on Sat Oct 24 10:41:01 2020

@author: Yael y Ian
"""

import math
def log_base_ten(x):
    log = math.log10(x)
    return log

# conversion factors
in2m = 0.0254;          # inches to meters
ft2m = 0.3048;          # feet to meters
psi2pa = 6894.76;       # psi to Pa
Pa2psi = 1/6894.76      # Pa to psi
###m3s2ft3min = 2118.88;   # m**3/s to ft**3/min

mes=input('Input propelant type: (oxygen/methane) ')
if mes=='oxygen':
  flow_rate=0.93
  density=1141
  viscosity= 0.1713E-6
elif mes=='methane':
  flow_rate=0.31
  density=424
  viscosity=0.2857E-6
else: 
  print('\n \n  Incorrect input  \n \n ')
	### mass flow rates in [kg/s]
	### density in [kg/m^3]
	### viscosity in [Pa s]

	### Mass flow rate of LCH4 = 0.31
	### Mass flow rate of LOX = 0.93

	### Desnity of LOX = 1141
	### Desnity of LCH4 = 424

diameter = 0.43*in2m        # meters
	### diameter of piping
length = 24*in2m            # meters
	### total length of plumbing
epsilon = 2.13E-6           # meters
	### mean height of roughnessof tubing
minor_loss_coeff = 10.64
	### 6-right anlgle elbows(1.5)
	### 2-entrances(0.78)
	### 1-fully open ball valve(0.08)

velocity=4*flow_rate/(density*math.pi*diameter**2)
	### average velocity of flow
Rg = epsilon/diameter
	### dimensionless quantity used for ease of caluclation

	### get dynamic pressure and use that for total pressure drop
def dyn_pressure(density, velocity):
    dynamic_press = 0.5*density*(velocity**2)
    return dynamic_press

### def total_pressure(static_press, dynamic_press):
    ### total_press = static_press + dynamic_press
    ### return total_press
    ### total_press not needed

# find reynolds number
def reynolds(velocity, density, diameter, viscosity):
    reynolds_number = (density*velocity*diameter)/(viscosity)
    return reynolds_number

### find friction factor
### using the Zigrang-Sylvester approximation of the Colebrook equation; error < 0.13%
def friction(Rg, Re):
    friction_factor = (1/(-2*log_base_ten((Rg/3.7)-(5.02/Re)*log_base_ten((Rg/3.7)-(5.02/Re)*log_base_ten(Rg/3.7)+(13/Re)))))**2
    return friction_factor

### find pressure drop
def pressure_losses(minor_loss_coeff, dynamic_press, length, diameter, friction_factor):
    pressure_drop = (minor_loss_coeff+(friction_factor*(length/diameter)))*(dynamic_press)
    return pressure_drop
### This pressure drop includes major and minor losses
### Minor losses dominates

inject_press=input('Desired pressure at injector: ')
inject_press=int(inject_press)
### Desired pressure at the injector

### find pressure drop from tank to injector
dynamic_press = dyn_pressure(density, velocity)
reynolds_number = reynolds(velocity, density, diameter, viscosity)
friction_factor = friction(Rg, reynolds_number)
pressure_drop = -pressure_losses(minor_loss_coeff, dynamic_press, length, diameter, friction_factor)
###total_press = total_pressure(static_press, dynamic_press) (Don't need this)
Pressure_Drop_PSI = pressure_drop*Pa2psi
### We want 420 psi at outlet pressure
inlet_press = inject_press - Pressure_Drop_PSI
print('Required tank pressure in psi (',mes,'): ',inlet_press)
print('Pressure Drop (psi):', Pressure_Drop_PSI)
