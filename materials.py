import numpy as np
import pandas as pd
from scipy import interpolate
import glob
import requests
    

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
    #fprop = interpolate.interp2d(Ttot, Ptot, proptot, kind='linear')
    return Ttot,Ptot,proptot

class PropTable:
    def __init__(self,files,id):
        self.Ts,self.Ps,self.prop = get_prop(files,id)
    def get(self,T,P):
        loc = ((self.P>=500)&(P<510))&((T>=120)&(T<121))


class Material:
    def reynolds(self,v,L):
        return self.density*v*L/self.visc
    def get_density(self):
        return self.fdens(self.T,self.P)[0]
    def get_viscosity(self):
        return self.fvisc(self.T,self.P)[0]

class Methane(Material):
    #fdens = get_prop(glob.glob("./C74828/*"),2)
    #fvisc = get_prop(glob.glob("./C74828/*"),11)
    def __init__(self,P,T):
        self.P = P
        self.T = T
        self.density = self.get_density()
        self.visc = self.get_viscosity()


    