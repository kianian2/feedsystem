# RPL @ UCSB
# Mitchell Aslo
# 02/17/2020
# Determine Temperature of Helium after Pressurizing

from conversions import *
from materials import *

def get_TF_Helium(Pi,Pin,PF,Ti,Tin):
    
    ui = Material.get_internal_energy(Helium(Pi,Ti))
    hin = Material.get_enthalpy(Helium(Pin,Tin))
    
    TF = (PF*Ti/Pi)*(((((PF/Pi)-1)*(ui/hin))+1)**(-1))

    return TF
