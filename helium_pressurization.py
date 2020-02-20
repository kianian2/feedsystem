#helium pressurization

from materials import Helium

def compute_He_T_rise(mat,T0):
    He = Helium(600,600)

    V_He = 0.01 # m^3
    E_He = V_He*He.get_density()*He.get_Cv()*(He.T - mat.T0)
    V_Tank = 0.015
    E_LOx = V_Tank*mat.rho*mat.cp
    return E_LOx/E_He