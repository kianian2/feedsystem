
def CylNuT(U,D,mat,Tf):
    ReD = mat.reynolds(U,D)
    Pr  = mat.prandlt()
    if np.min(ReD*Pr) < 0.2:
        print('warn : CylNuT: ReD*Pr < 0.2')
    NuD = 0.3+0.62*ReD**0.5*Pr**(1/3)*(1+(ReD/282000)**0.625)**0.8/(1+(0.4/Pr)**(2/3))**0.25
    h   = NuD*kf/D  
    return h,NuD,ReD                                               
