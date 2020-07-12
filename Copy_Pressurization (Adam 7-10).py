''' 
Feed System 
Copyright (C) 2020 RPL at UCSB 
Author: Sebastian Vargas

The purpose of this code is to calculate the time required to pressurize our Methane tank. 

First assumption: it is very easy for the helium to initially fill the eulage volume and takes little time. Therefore, I will consider the time 
it takes to pressurize from that point. Second assumption: At the very first instant that the helium fills the eulage volume, it still maintains 
its initial temperature, so I will update the temperature after this point. Important notes: I am going to be tracking moles inside the eulage volume, 
using PV= nRT I will update the pressure as a function of moles and the temperature of the gas, the temperature will be updated by using the equation from BETE.
I will run the simulation based on a while loop influenced by the pressure difference, and it will stop once the tanks reach the desired pressure. 

''' 
from polyfit_diffuser import q_of_p
from materials import Helium 
import matplotlib.pyplot as plt
import numpy as np

pressurant = Helium(540,100)


cv = 0.01593484

gallons_to_liters = 3.78541;  # [L/gal] This will be used to convert flow rate into liters per minute 
helium_density_eul = pressurant.get_density() ;  # [g/L] This will be used for a conversion from flow rate into grams/s
grams_to_moles =  4.003  ;  # [mol/g] This converts our flowrate from grams/s to mol/s 
v_eul = 25       ;  # [L]   Fixed quantity throughout pressurization 
P_reg = 540     ;  # [psi] This is a fixed inlet pressure from the regulator 
P_eul = 14.7    ;  # [psi} This is the INITIAL gauge pressure inside the tank, ambient pressure
psi_to_atm = 0.068046    ;  # [psi/atm] This converts our gauge pressure of psi to atm when we use PV=nrt, but remember to add 1 atm because we are using gauge pressures; 

P_diff = P_reg - P_eul ;  # [psi] This is the pressure difference that influences flow rate across our diffuser 

Ti =  310.928       ;  # [K] Ambient room temperature 
Tf =  111.7         ;  # [K] Methane Cryogenic temperature, this is once pressurant reaches thermal equilibrium 
T = Ti              ;  # [K] Setting up the initial temperature of our pressurant, it is at ambient temperature (assumption) 
t = 0               ;  # [s] Setting up euler time step problem
dt = 0.001            ;  # [s] Setting up time step 
R  = 0.08205        ;  # [L atm/mol k]
moles = P_eul*v_eul/(R*T)         ;  # [mol] Initial moles in the tank of pressurant 
lamb = 1.6667; 

p_eul_array = []
p_f_array = []
moles_array = [] 

def T_gas(P_f,P_i): 
    return (P_f/P_i)*T*((P_f/P_i-1)/lamb + 1)**(-1)

def converging_temp_pressure(moles,T,P_eul): 
    for x in range(30): 
        new_press = (moles*R*T/v_eul)/psi_to_atm
        #T = (T * moles + T_gas(new_press, P_eul) * mdot * dt)/moles
        T = T_gas(new_press, P_eul)
        P_eul = new_press 
        
    return T, new_press

while P_diff > 1:
    p_eul_array.append(P_eul)
    p_f_array.append(T)
    moles_array.append(moles)
    #helium_density_eul = Helium(P_eul,T).get_density()
    mdot = q_of_p(P_diff)*gallons_to_liters*helium_density_eul*grams_to_moles/60 # [mol/s] Based on the curve fit as a function of pressure difference from the company 
    moles = moles + mdot * dt
    new_press = (moles*R*T/v_eul)/psi_to_atm
    T = (T * (moles - mdot * dt) + T_gas(new_press, P_eul) * mdot * dt)/moles #[K] Temperature averaging
    #T = T_gas(new_press, P_eul)
    P_eul = new_press          
    temp_pressure_var = converging_temp_pressure(moles,T,P_eul)                                         # [mol/s] This updates our moles inside the eulage volume and prepares for pv=nrt                                          
    #T = temp_pressure_var[0]
    #P_eul = temp_pressure_var[1]
    P_diff =  P_reg - P_eul                                                   # [psi] Preparation to update mdot                                                      # [k] Use the function inside of the BETE pdf to update the temperature inside the tank as a function of the eulage pressure
    t = t + dt                                                                # [s] updating the time step 
    

fig, ax  = plt.subplots()
plt.plot(np.arange(0,dt * len(p_eul_array), dt),p_eul_array)
plt.plot(np.arange(0,dt * len(p_eul_array), dt),p_f_array)
plt.plot(np.arange(0,dt*len(p_eul_array),dt),moles_array)
ax.legend(["Eulage Press (psi)", "Temp", "Moles"])
print(t) 
plt.show()