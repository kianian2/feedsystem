import numpy as np
import pandas as pd
from scipy import interpolate
import glob
import requests
import os
    
DIR = os.path.dirname(os.path.realpath(__file__))

# def get_prop(fs,id):
#     Ttot = []
#     Ptot = []
#     proptot = []
#     for f in fs:
#         table = np.genfromtxt(f, delimiter='\t')
#         T = table[:,0][1:]
#         P = table[:,1][1:]
#         prop = table[:,id][1:]
#         Ttot = np.append(Ttot,T)
#         Ptot = np.append(Ptot,P)
#         proptot = np.append(proptot,prop)
#     return Ttot,Ptot,proptot

# def make_table(fs,id):
#     for f in fs:
#         table = np.genfromtxt(f, delimiter='\t')
#         prop = table[:,id][1:]
#         Ttot = np.append(Ttot,T)
#         Ptot = np.append(Ptot,P)
#         proptot = np.append(proptot,prop)
#     return Ttot,Ptot,proptot

class PropTable:
    keys = {'T':0,'P':1,'rho':2,'specvol':3,'U':4,
    'h':5,'s':6,'Cv':7,'Cp':8,'c':9,'JT':10,'mu':11,'k':12,
    'phase':13}
    def __init__(self,f,P1,P2,Pstep,T1,T2,Tstep):
        self.bigtable = np.genfromtxt(f)
        self.P = self.bigtable[:,1]
        self.T = self.bigtable[:,0]
        self.P1 = P1; self.P2 = P2; self.Pstep = Pstep
        self.T1 = T1; self.T2 = T2; self.Tstep = Tstep
    def get(self,T,P,prop):
        id = self.keys[prop]
        loc = ((self.P>=P)&(self.P<(P+self.Pstep)))&\
            ((self.T>=T)&(self.T<(T+self.Tstep)))
        prop = self.bigtable[:,id]
        return prop[loc][0]


class Material:
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T
    def get_density(self):
        return self.ptable.get(self.T,self.P,'rho')
    def get_viscosity(self):
        return self.ptable.get(self.T,self.P,'mu')*1e-6
    def get_internal_energy(self):
        return self.ptable.get(self.T,self.P,'U')/1000
    def get_enthalpy(self):
        return self.ptable.get(self.T,self.P,'h')/1000
    def get_entropy(self):
        return self.ptable.get(self.T,self.P,'h')*1000
    def get_Cv(self):
        return self.ptable.get(self.T,self.P,'Cv')*1000
    def get_Cp(self):
        return self.ptable.get(self.T,self.P,'Cp')*1000
    def get_speed_of_sound(self):
        return self.ptable.get(self.T,self.P,'c')
    def get_thermal_conductivity(self):
        return self.ptable.get(self.T,self.P,'k')
    def get_phase(self):
        phase =  self.ptable.get(self.T,self.P,'phase')
        if phase==0:
            return "vapor"
        if phase==1:
            return "liquid"
        if phase==3:
            return "supercritical"
        else:
            print("error: unrecognized phase")

    def reynolds(self,v,L):
        return self.density*v*L/self.visc

    def set_temp(self,newT):
        self.T = newT
    def set_pressure(self,newP):
        self.P = newP


class Methane(Material):
    ptable = PropTable(os.path.join(DIR,"ch4.csv"),10,750,10,0,400,1)
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T
 
class Helium(Material):
    ptable = PropTable(os.path.join(DIR,"He.csv"),5,1300,5,80,500,1)
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T

    