
from math import *
import matplotlib.pyplot as plt
import sys
from helium_pressurization import compute_He_T_rise
from materials import Methane

# ----- Conversion Constants -----
in_to_m = 0.0254

class Steel:
    cp =  502.416 #J/kg-K
    rho = 8030 #kg/m^3 density

class Styrofoam:
    k = 0.037 # W/m^2K
    cp = 1136 #J/kg-K
    rho = 50 #kg/m^3 density
    
class LOx:
    rho = 1047 # see above     properties at 110K at pressure
    cp = 1760
    T0 = 90.2 # boiling temp at 1 atm
    bp_at_P = 147.33
    Hv = 3.4 / 16.0 * 1000 * 1000 # kJ/mol / g/mol * g/kg * J/kJ = J/kg

class CH4:
    rho = 397 # kg/m^3     properties at 130K at pressure
    cp = 3500  # J/kgK
    T0 = 111.7
    bp_at_P = 180.2
    Hv = 8.5 / 16.04 * 1000 * 1000 # kJ/mol / g/mol * g/kg * J/kJ= J/kg

class LN2:
    rho = 806
    cp = -1 #unapplicable
    T0 = 80 # just for starting the unchilling
    Hv = 6 / 28.01 * 1000 * 1000 # see above

class Air:
    rho = 1 # literally just guesses
    cp = 1.2


class Vessel: # only coding difference between pipes and tanks is whether the ends are capped
    def __init__(self, L, t, r_out, mat_fill, cap_ends): # all inputs in inches
        self.mat_fill = mat_fill
        self.cap_ends = cap_ends
        self.mat_wall = Steel()
        self.L = L*in_to_m
        self.t = t*in_to_m
        self.r_out = r_out*in_to_m
        self.r_in = self.r_out - self.t
        self.V_fill = pi*self.r_in**2*self.L + self.cap_ends*4/3*pi*self.r_in**3
        self.hc_fill = self.V_fill * self.mat_fill.rho * self.mat_fill.cp
        self.V_wall = pi*(self.r_out**2 - self.r_in**2)*self.L + self.cap_ends*4/3*pi*(self.r_out**3 - self.r_in**3)
        self.hc_wall = self.V_wall * self.mat_wall.rho * self.mat_wall.cp
        self.hc = self.hc_fill + self.hc_wall

class Insulation:
    def __init__(self, vessel, thickness, h):
        self.mat = Styrofoam()
        self.cap_ends = vessel.cap_ends
        self.h = h
        self.L = vessel.L
        self.r_in = vessel.r_out
        self.t = thickness*in_to_m
        self.r_out = self.r_in + self.t
        self.A = self.L*2*self.r_out*pi + 4*pi*self.r_out**2 #m^2
        self.V = pi * (self.r_out**2 - self.r_in**2) * self.L + self.cap_ends*4/3*pi*(self.r_out**3 - self.r_in**3)
        self.hc = self.V * self.mat.rho * self.mat.cp
        self.calc_tr()
    def calc_tr(self):
        tr_cyl = log(self.r_out/self.r_in)/(2*pi*self.L*self.mat.k)
        tr_sph = (self.r_out-self.r_in)/(4*pi*self.r_out*self.r_in*self.mat.k)
        tr_cond = 1/(1/tr_cyl+self.cap_ends*1/tr_sph)
        tr_conv = 1/self.h/self.A
        self.tr = tr_cond + tr_conv

#h = 11.97 # uses matlab, assumes 2m/s crosswind
#h = 25 for pipe

TANK_R = 8.63/2 #inches
TANK_L = 17
TANK_T = 5/16

PIPE_R = 0.5/2
PIPE_L = 0.8/0.0254 # I only know it in meters so this is a conversion
PIPE_T = 0.035

env_temp = 310 # aronud 100 F, but in K

# ----- Temp Changes -----
def timestep_sim(T0,tr,hc,dt,t_end):
    time_span = list(range(dt,t_end,dt))
    Temp = [T0]
    for t in time_span:
        Q = (env_temp - Temp[-1]) / tr
        dT = Q/hc*dt
        Temp.append(Temp[-1]+dT)
    return [0]+time_span, Temp

def get_tank_properties(t_end):
    dt = 0.5
    Tank_LOx = Vessel(TANK_L, TANK_T, TANK_R, LOx(), True)
    Tank_CH4 = Vessel(TANK_L, TANK_T, TANK_R, CH4(), True)
    Tank_ins = Insulation(Tank_LOx, 1, 11.97)
    t, temp_tank_LOx = timestep_sim(LOx().T0+compute_He_T_rise(LOx), Tank_ins.tr, Tank_ins.hc + Tank_LOx.hc, dt, t_end)
    t, temp_tank_CH4 = timestep_sim(CH4().T0+compute_He_T_rise(CH4), Tank_ins.tr, Tank_ins.hc + Tank_CH4.hc, dt, t_end)
    return temp_tank_LOx[-1], temp_tank_CH4[-1]


if __name__ == "__main__":
    dt = 2
    t_end = 2000
    Tank_LOx = Vessel(TANK_L, TANK_T, TANK_R, LOx(), True)
    Pipe_LOx = Vessel(PIPE_L, PIPE_T, PIPE_R, LOx(), False)
    Tank_CH4 = Vessel(TANK_L, TANK_T, TANK_R, CH4(), True)
    Pipe_CH4 = Vessel(PIPE_L, PIPE_T, PIPE_R, CH4(), False)
    Tank_LN2 = Vessel(TANK_L, TANK_T, TANK_R, LN2(), True)
    Pipe_LN2 = Vessel(PIPE_L, PIPE_T, PIPE_R, LN2(), False)
    Tank_Air = Vessel(TANK_L, TANK_T, TANK_R, Air(), True)
    Pipe_Air = Vessel(PIPE_L, PIPE_T, PIPE_R, Air(), False)
    Late_Pipe = Vessel(50, PIPE_T, PIPE_R, Air(), False)

    Tank_ins = Insulation(Tank_LOx, 1, 11.97)
    Pipe_ins = Insulation(Pipe_LOx, 1, 25)
    Late_ins = Insulation(Late_Pipe, 1, 25)

    t, temp_tank_LOx = timestep_sim(LOx().T0, Tank_ins.tr, Tank_ins.hc + Tank_LOx.hc, dt, t_end)
    t, temp_pipe_LOx = timestep_sim(LOx().T0, Pipe_ins.tr, Pipe_ins.hc + Pipe_LOx.hc, dt, t_end)
    t, temp_tank_CH4 = timestep_sim(CH4().T0, Tank_ins.tr, Tank_ins.hc + Tank_CH4.hc, dt, t_end)
    t, temp_pipe_CH4 = timestep_sim(CH4().T0, Pipe_ins.tr, Pipe_ins.hc + Pipe_CH4.hc, dt, t_end)
    t, temp_tank_Air = timestep_sim(LN2().T0, Tank_ins.tr, Tank_ins.hc + Tank_Air.hc, dt, t_end)
    t, temp_pipe_Air = timestep_sim(LN2().T0, Pipe_ins.tr, Pipe_ins.hc + Pipe_Air.hc, dt, t_end)

    plt.figure(figsize=(6,4), dpi=400)
    plt.plot(t, temp_tank_LOx, 'b-')
    plt.plot(t, temp_tank_CH4, 'r-')
    plt.plot(t, temp_pipe_LOx, 'b-')
    plt.plot(t, temp_pipe_CH4, 'r-')
    plt.plot(t, temp_tank_Air, 'k-')
    plt.plot(t, temp_pipe_Air, 'k-')

    print("Open LN2 boil rate in tank = ", ((env_temp - LN2().T0) / Tank_ins.tr)/(LN2().Hv) * 3600, "kg/hr")
    print("Open LOx boil rate in tank = ", ((env_temp - LOx().T0) / Tank_ins.tr)/(LOx().Hv) * 3600, "kg/hr")
    print("Open CH4 boil rate in tank = ", ((env_temp - CH4().T0) / Tank_ins.tr)/(CH4().Hv) * 3600, "kg/hr")
    print("Open LN2 boil rate in pipe = ", ((env_temp - LN2().T0) / Pipe_ins.tr)/(LN2().Hv) * 3600, "kg/hr")
    print("Open LOx boil rate in pipe = ", ((env_temp - LOx().T0) / Pipe_ins.tr)/(LOx().Hv) * 3600, "kg/hr")
    print("Open CH4 boil rate in pipe = ", ((env_temp - CH4().T0) / Pipe_ins.tr)/(CH4().Hv) * 3600, "kg/hr")
    print("Max CH4 boiloff in line = ", (env_temp - CH4.T0)*(Late_Pipe.hc+Late_ins.hc) / CH4.Hv, "kg")

    plt.legend(["Tank LOx", "Tank CH4", "Pipe LOx", "Pipe CH4", "Tank Air", "Pipe Air"])
    plt.show()

