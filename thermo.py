
from math import *
import matplotlib.pyplot as plt
from conversions import *
import sys
from helium_pressurization import compute_He_T_rise
from materials import Methane, Oxygen, Nitrogen, Air

class Steel:
    def get_density(self):
        return 8030 #kg/m^3 density
    def get_Cp(self):
        return 502.416 #J/kg-K

class Styrofoam:
    def get_density(self):
        return 50 #kg/m^3 density
    def get_Cp(self):
        return 1136 #J/kg-K
    def get_thermal_conductivity(self):
        return 0.037 # W/m^2K


LN2_T0 = 77
LOx_T0 = 90.3 # boiling temp at 1 atm
CH4_T0 = 111.7


class Vessel: # only coding difference between pipes and tanks is whether the ends are capped
    def __init__(self, L, t, r_out, mat_fill, cap_ends): # all inputs in inches
        self.mat_fill = mat_fill
        self.cap_ends = cap_ends
        self.mat_wall = Steel()
        self.L = L*in2m
        self.t = t*in2m
        self.r_out = r_out*in2m
        self.r_in = self.r_out - self.t
        self.V_fill = pi*self.r_in**2*self.L + self.cap_ends*4/3*pi*self.r_in**3
        self.hc_fill = self.V_fill * self.mat_fill.get_density() * self.mat_fill.get_Cp()
        self.V_wall = pi*(self.r_out**2 - self.r_in**2)*self.L + self.cap_ends*4/3*pi*(self.r_out**3 - self.r_in**3)
        self.hc_wall = self.V_wall * self.mat_wall.get_density() * self.mat_wall.get_Cp()
        self.hc = self.hc_fill + self.hc_wall

class Insulation:
    def __init__(self, vessel, thickness, h):
        self.mat = Styrofoam()
        self.cap_ends = vessel.cap_ends
        self.h = h
        self.L = vessel.L
        self.r_in = vessel.r_out
        self.t = thickness*in2m
        self.r_out = self.r_in + self.t
        self.A = self.L*2*self.r_out*pi + 4*pi*self.r_out**2 #m^2
        self.V = pi * (self.r_out**2 - self.r_in**2) * self.L + self.cap_ends*4/3*pi*(self.r_out**3 - self.r_in**3)
        self.hc = self.V * self.mat.get_density() * self.mat.get_Cp()
        self.calc_tr()
    def calc_tr(self):
        tr_cyl = log(self.r_out/self.r_in)/(2*pi*self.L*self.mat.get_thermal_conductivity())
        tr_sph = (self.r_out-self.r_in)/(4*pi*self.r_out*self.r_in*self.mat.get_thermal_conductivity())
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

def get_tank_properties(t_end, pressure_LOx, pressure_CH4):
    dt = 0.5
    Tank_LOx = Vessel(TANK_L, TANK_T, TANK_R, Oxygen(pressure_LOx, LOx_T0), True)
    Tank_CH4 = Vessel(TANK_L, TANK_T, TANK_R, Methane(pressure_CH4, CH4_T0), True)
    Tank_ins = Insulation(Tank_LOx, 1, 11.97)
    t, temp_tank_LOx = timestep_sim(LOx_T0 + compute_He_T_rise(Tank_LOx.mat_fill, LOx_T0), Tank_ins.tr, Tank_ins.hc + Tank_LOx.hc, dt, t_end)
    t, temp_tank_CH4 = timestep_sim(CH4_T0 + compute_He_T_rise(Tank_CH4.mat_fill, CH4_T0), Tank_ins.tr, Tank_ins.hc + Tank_CH4.hc, dt, t_end)
    return temp_tank_LOx[-1], temp_tank_CH4[-1]


if __name__ == "__main__":
    dt = 2
    t_end = 2000
    LOx_pressure = 538.
    CH4_pressure = 461.
    Tank_LOx = Vessel(TANK_L, TANK_T, TANK_R, Oxygen(LOx_pressure, LOx_T0), True)
    Pipe_LOx = Vessel(PIPE_L, PIPE_T, PIPE_R, Oxygen(LOx_pressure, LOx_T0), False)
    Tank_CH4 = Vessel(TANK_L, TANK_T, TANK_R, Methane(CH4_pressure, CH4_T0), True)
    Pipe_CH4 = Vessel(PIPE_L, PIPE_T, PIPE_R, Methane(CH4_pressure, CH4_T0), False)
    Tank_LN2 = Vessel(TANK_L, TANK_T, TANK_R, Nitrogen(14.7, LN2_T0), True)
    Pipe_LN2 = Vessel(PIPE_L, PIPE_T, PIPE_R, Nitrogen(14.7, LN2_T0), False)
    Tank_Air = Vessel(TANK_L, TANK_T, TANK_R, Nitrogen(14.7, LN2_T0+1), True)
    Pipe_Air = Vessel(PIPE_L, PIPE_T, PIPE_R, Nitrogen(14.7, LN2_T0+1), False)
    Late_Pipe = Vessel(50, PIPE_T, PIPE_R, Nitrogen(14.7, env_temp+1), False)

    Tank_ins = Insulation(Tank_LOx, 1, 11.97)
    Pipe_ins = Insulation(Pipe_LOx, 1, 25)
    Late_ins = Insulation(Late_Pipe, 1, 25)

    t, temp_tank_LOx = timestep_sim(LOx_T0, Tank_ins.tr, Tank_ins.hc + Tank_LOx.hc, dt, t_end)
    t, temp_pipe_LOx = timestep_sim(LOx_T0, Pipe_ins.tr, Pipe_ins.hc + Pipe_LOx.hc, dt, t_end)
    t, temp_tank_CH4 = timestep_sim(CH4_T0, Tank_ins.tr, Tank_ins.hc + Tank_CH4.hc, dt, t_end)
    t, temp_pipe_CH4 = timestep_sim(CH4_T0, Pipe_ins.tr, Pipe_ins.hc + Pipe_CH4.hc, dt, t_end)
    t, temp_tank_Air = timestep_sim(LN2_T0, Tank_ins.tr, Tank_ins.hc + Tank_Air.hc, dt, t_end)
    t, temp_pipe_Air = timestep_sim(LN2_T0, Pipe_ins.tr, Pipe_ins.hc + Pipe_Air.hc, dt, t_end)

    plt.figure(figsize=(6,4), dpi=400)
    plt.plot(t, temp_tank_LOx, 'b-')
    plt.plot(t, temp_tank_CH4, 'r-')
    plt.plot(t, temp_pipe_LOx, 'b-')
    plt.plot(t, temp_pipe_CH4, 'r-')
    plt.plot(t, temp_tank_Air, 'k-')
    plt.plot(t, temp_pipe_Air, 'k-')

    print("Open LN2 boil rate in tank = ", ((env_temp - LN2_T0) / Tank_ins.tr)/(Nitrogen.Hv) * 3600, "kg/hr")
    print("Open LOx boil rate in tank = ", ((env_temp - LOx_T0) / Tank_ins.tr)/(Oxygen.Hv) * 3600, "kg/hr")
    print("Open CH4 boil rate in tank = ", ((env_temp - CH4_T0) / Tank_ins.tr)/(Methane.Hv) * 3600, "kg/hr")
    print("Open LN2 boil rate in pipe = ", ((env_temp - LN2_T0) / Pipe_ins.tr)/(Nitrogen.Hv) * 3600, "kg/hr")
    print("Open LOx boil rate in pipe = ", ((env_temp - LOx_T0) / Pipe_ins.tr)/(Oxygen.Hv) * 3600, "kg/hr")
    print("Open CH4 boil rate in pipe = ", ((env_temp - CH4_T0) / Pipe_ins.tr)/(Methane.Hv) * 3600, "kg/hr")
    print("Max CH4 boiloff in line = ", (env_temp - CH4_T0)*(Late_Pipe.hc+Late_ins.hc) / Methane.Hv, "kg")

    plt.legend(["Tank LOx", "Tank CH4", "Pipe LOx", "Pipe CH4", "Tank Air", "Pipe Air"])
    plt.show()

