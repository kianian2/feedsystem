import numpy as np
import pandas as pd
from scipy import interpolate
import glob

def get_prop(fs,id):
    Ttot = []
    Ptot = []
    proptot = []
    for f in fs:
        table = np.genfromtxt(f, delimiter='\t')
        T = table[:,0][1:]
        P = table[:,1][1:]
        prop = table[:,id][1:]
        Ttot = np.append(Ttot,T)
        Ptot = np.append(Ptot,P)
        proptot = np.append(proptot,prop)
    fprop = interpolate.interp2d(Ttot, Ptot, proptot, kind='nearest')
    return fprop


class Material:
    def reynolds(self,v,L):
        return self.rho*self.visc*v/L
    def get_density(self):
        return self.fdens(self.T,self.P)[0]
    def get_viscosity(self):
        return self.fvisc(self.T,self.P)[0]

class Methane(Material):
    fdens = get_prop(glob.glob("./ch4_*"),2)
    fvisc = get_prop(glob.glob("./ch4_*"),11)
    def __init__(self,P,T):
        self.P = P
        self.T = T
        self.density = self.get_density()
        self.viscosity = self.get_viscosity()


    