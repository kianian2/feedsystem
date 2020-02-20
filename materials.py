import numpy as np
import pandas as pd
from scipy import interpolate
import glob
import requests
import os
    
DIR = os.path.dirname(os.path.realpath(__file__))

""" 
Object oriented program for getting thermophysical properties 
of different materials ripped from the NIST database
Author: Nolan McCarthy
Date: 
"""

"""NOTE:
Prof. Ted Bennett is a moron and fucked up his thermal expansion
coefficients, so... there's that"""

class PropTable:
    conv1 = 1e-6
    conv2 = 1000
    keys = {'T':0,'P':1,'rho':2,'specvol':3,'U':4,
    'h':5,'s':6,'Cv':7,'Cp':8,'c':9,'JT':10,'mu':11,'k':12,
    'phase':13,'den':2}
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
    def get_derive(self,T,P,prop):
        T1 = T; T2 = T+ self.Tstep
        id = self.keys[prop]
        loc1 = ((self.P>=P)&(self.P<(P+self.Pstep)))&\
            ((self.T>=T)&(self.T<(T+self.Tstep)))
        
        loc2 = ((self.P>=P)&(self.P<(P+self.Pstep)))&\
            ((self.T>=T2)&(self.T<(T2+self.Tstep)))
        prop = self.bigtable[:,id]
        p1 = prop[loc1][0]; p2 = prop[loc2][0]
        dp = (p2-p1)/(T2-T1)
        return dp


class PropTableTed:
    conv1 = 1
    conv2 = 2
    '''I had to write this because Ted Bennet sucks'''
    keys = {'T':0,'k':1,'rho':2,'Cp':3,'Cv':4,'mu':5,'expan':6,'den':2}
    def __init__(self,file):
        f = open(file,'r')
        lines = f.readlines()
        bigtable = np.zeros((len(lines)-2,7))
        floatv = np.vectorize(float)
        for i in range(2,len(lines)):
            line = lines[i].lstrip().rstrip('\n')
            #print(line.split())
            bigtable[i-2] = floatv(line.split())
        self.bigtable = bigtable
    def get(self,T,P,prop):
        id = self.keys[prop]
        Ts = self.bigtable[:,0]
        loc = np.argmin(np.abs(Ts - T))
        prop0 = self.bigtable[:,id][loc]
        T0 = self.bigtable[:,0][loc]
        if T > T0:
            T1 = self.bigtable[:,0][loc-1]
            prop1 = self.bigtable[:,id][loc-1]
            addendum = (T-T0)*((prop1 - prop0)/(T1 - T0))
            return prop0 + addendum
        else:
            T1 = self.bigtable[:,0][loc-1]
            prop1 = self.bigtable[:,id][loc-1]
            addendum = (T-T0)*((prop1 - prop0)/(T1 - T0))
            return prop0 + addendum





class Material:
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T
    def get_density(self):
        return self.ptable.get(self.T,self.P,'rho')
    def get_viscosity(self):
        return self.ptable.get(self.T,self.P,'mu')*self.ptable.conv1
    def get_internal_energy(self):
        return self.ptable.get(self.T,self.P,'U')*self.ptable.conv2
    def get_enthalpy(self):
        return self.ptable.get(self.T,self.P,'h')*self.ptable.conv2
    def get_entropy(self):
        return self.ptable.get(self.T,self.P,'h')*self.ptable.conv2
    def get_Cv(self):
        return self.ptable.get(self.T,self.P,'Cv')/self.ptable.conv2
    def get_Cp(self):
        return self.ptable.get(self.T,self.P,'Cp')/self.ptable.conv2
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
        return self.get_density()*v*L/self.get_viscosity()

    def prandlt(self):
        mu = self.get_viscosity()
        k = self.get_thermal_conductivity()
        rho = self.get_density()
        Cp = self.get_Cp()
        Pr = (mu/rho)/(k/(Cp*rho))
        return Pr

    def set_temp(self,newT):
        self.T = newT
    def set_pressure(self,newP):
        self.P = newP


class Oxygen(Material):
    ptable = PropTable(os.path.join(DIR,"Ox.csv"),10,1000,10,0,1200,1)
    Hv = 3.4 / 16.0 * 1000 * 1000 # kJ/mol / g/mol * g/kg * J/kJ = J/kg
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T
    def get_expan(self,T,P):
        drho = self.ptable.get_derive(T,P,'rho')
        expan = drho/rho
        return expan

class Methane(Material):
    ptable = PropTable(os.path.join(DIR,"ch4.csv"),10,750,10,0,400,1)
    Hv = 8.5 / 16.04 * 1000 * 1000 # kJ/mol / g/mol * g/kg * J/kJ= J/kg
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T
    def get_expan(self,T,P):
        drho = self.ptable.get_derive(T,P,'rho')
        expan = drho/rho
        return expan
 
class Helium(Material):
    ptable = PropTable(os.path.join(DIR,"He.csv"),5,1300,5,80,500,1)
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T
    def get_expan(self,T,P):
        drho = self.ptable.get_derive(T,P,'rho')
        expan = drho/rho
        return expan
    
class Air(Material):
    ptable = PropTableTed(os.path.join(DIR,"Air.dat"))
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P # unnecessary assumes 1 atm
        self.T = T
    def get_expan(self):
        return self.ptable.get(self.T,self.P,'expan')

class Nitrogen(Material):
    ptable = PropTable(os.path.join(DIR,"N2.csv"),10,1000,10,0,1200,1)
    def __init__(self,P,T):
        '''Pressure (psig), Temperature (K)'''
        self.P = P
        self.T = T
    def get_expan(self,T,P):
        drho = self.ptable.get_derive(T,P,'rho')
        expan = drho/rho
        return expan