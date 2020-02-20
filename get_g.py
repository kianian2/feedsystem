# RPL @ UCSB 
# Mitchell Aslo
# 02/17/2020
# Find gravitational constant 

from math import *

def get_g(latitude,altitude):
    '''
    Inputs:
        latitude: location on Earth in [degrees]
        altitude: height above sea level in meters [m]
        
    Returns:
        gravitational constant, g [m/s^2]    
        
    All values referenced from NASA paper & confirmed with multiple sources
    https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20060028164.pdf
    
    FAR SITE: 
        latitude = 35.3474 ± 0.0003 [degrees]
        altitude = 628 ± 1 [m]
        g = 9.795694 ± 0.000003 [m/s^2]
        
    '''
    g_s_e = 9.7803253359;   # surface gravity at the equator [m/s^2]
    e2 = 0.00669437999014;  # eccentricity of the ellipse squared
    
    k = 0.00193185265241;   # given by ((b*g_s_p)/(a*g_s_e))-1 where a & b are
                            # semi-major & semi-minor axis of ellipse of Earth
                            # g_s_p is surface gravity at the pole
    
    g_0_top = (1+k*(sin(radians(latitude)))**2);        # top of fraction
    g_0_bot = (1-e2*(sin(radians(latitude)))**2)**0.5;  # bottom of fraction
    
    g_latitude = g_s_e*g_0_top/g_0_bot;      # gravitational constant [m/s^2]
    
    g_altitude = (-3.086*(10**(-6)))*altitude;  # altitude correction [m/s^2]
    
    g = g_latitude+g_altitude;              # final value for g [m/s^2]
    
    return g