
import numpy as np
import itertools
from matlab import *

def CylNuT(U,D,mat,Tf):
    ReD = mat.reynolds(U,D)
    Pr  = mat.prandlt()
    k = mat.get_thermal_conductivity()
    if np.min(ReD*Pr) < 0.2:
        print('warn : CylNuT: ReD*Pr < 0.2')
    NuD = 0.3+0.62*ReD**0.5*Pr**(1/3)*(1+(ReD/282000)**0.625)**0.8/(1+(0.4/Pr)**(2/3))**0.25
    h   = NuD*k/D  
    return h,NuD,ReD                                               



def PlateNuT(U,L,ReCrit,mat,Tf):
    ReL = mat.reynolds(U,D)
    Pr  = mat.prandlt()
    k = mat.get_thermal_conductivity()               
    def NuLam(ReL,Pr):
        return 0.664*ReL**0.5*Pr**(1/3)    
    def NuTurb(ReL,Pr): 
        return 0.0370*ReL**0.8*Pr**(1/3)    
    NuL = MixNu('T',NuLam,NuTurb,ReCrit,ReL,Pr,0) 
    h = NuL*kf/L
    return h, NuL, ReL


def MixNu(flag,NuLam,NuTurb,Rc,R,Pr,n):
    Nu=np.zeros(size(R))
    j=np.where(R < Rc);            # find laminar cases
    if isempty(j[0]):
        Prj=Pick(Pr,j);                                           
        Nu[j] = NuLam(R[j],Prj)
    j=find(R >= Rc);           # find mixed turbulent cases
    if not isempty(j[0]):
        Prj=Pick(Pr,j);                                           
        if flag=='T':
            Nu[j]=NuTurb(R[j],Prj)+(NuLam(Rc,Prj)-NuTurb(Rc,Prj))*(Rc/R[j])**n;        
    elif flag=='H':
        Nu[j]=1/(1/NuTurb(R[j],Prj)+(1/NuLam(Rc,Prj)-1/NuTurb(Rc,Prj))*(Rc/R[j])**n); 
    else:
        print('Unknown flag, ''T'' or ''H'' required');
