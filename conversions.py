# RPL @ UCSB
# Mitchell Aslo
# 02/17/2020
# File with unit conversion constants

# All information and 
# All numerical values (not divisions) are exact numbers from 
# https://www.nist.gov/pml/weights-and-measures/publications/nist-handbooks/other-nist-handbooks/other-nist-handbooks-2-3


# Lengths

in2m = 0.0254;      # [in] to [m]
m2in = 1/in2m;      # [m] to [in]

ft2m = 0.3048;      # [ft] to [m]
m2ft = 1/ft2m;      # [m] to [ft]

# Volumes

gal2lit = 3.785411784;  # gallons [gal] to liters [L]
lit2gal = 1/gal2lit;    # liters [L] to gallons [gal]

lit2cubm = 0.001;       # liters [L] to cubic meters [m^3]
cubm2lit = 1000;        # cubic meters [m^3] to liters [L]

gal2cubm = gal2lit*lit2cubm;    # gallons [gal] to cubic meters [m^3]
cubm2gal = 1/gal2cubm;          # cubic meters [m^3] to gallons [gal]

gal2cubin = 231;         # gallons [gal] to cubic inches [in^3]
cubin2gal = 1/gal2cubin; # cubic inches [in^3] to gallons [gal]

cubft2cubin = 1728;             # cubic feet [ft^3] to cubic inches [in^3]
cubin2cubft = 1/cubft2cubin;    # cubic inches [in^3] to cubic feet [ft^3]

gal2cubft = gal2cubin*cubin2cubft;  # gallons [gal] to cubic feet[ft^3]
cubft2gal = 1/gal2cubft;            # cubic feet[ft^3] to gallons [gal]

cubft2cubm = 0.028316846592;    # cubic feet [ft^3] to cubic meters [m^3]
cubm2cubft = 1/cubft2cubm;      # cubic meters [m^3] to cubic feet [ft^3]

# Mass (also known as a MESS)

lb2kg = 0.45359237;     # pounds [lbs] to kilograms [kg]
kg2lb = 1/lb2kg;        # kilograms [kg] to pounds [lbs]

# Pressure (not exact number)

psi2pa = 6894.757;  # pounds per square inch (psi) [lbf/in^2] to pascals [Pa]
pa2psi = 1/psi2pa;  # pascals [Pa] to psi [lbf/in^2]


def get_C(value,unit):
    '''
    Inputs:
        value: temperature value you are in
        unit: unit of temp value, 'F', 'K', or 'R'
        
    Output:
        Temperature Value in Celsius [C]
    '''
    
    if unit == 'K':
        C = value-273.15;
    if unit == 'F':
        C = (value-32)/1.8;
    if unit == 'R':
        C = (value-459.67-32)/1.8;
    return C

def get_F(value,unit):
    '''
    Inputs:
        value: temperature value you are in
        unit: unit of temp value, 'C', 'K', or 'R'
        
    Output:
        Temperature Value in Fahrenheit [F]
    '''
    
    if unit == 'K':
        F = ((value-273.15)*1.8)+32;
    if unit == 'C':
        F = (value*1.8)+32;
    if unit == 'R':
        F = value-459.67;
    return F

def get_K(value,unit):
    '''
    Inputs:
        value: temperature value you are in
        unit: unit of temp value, 'F', 'C', or 'R'
        
    Output:
        Temperature Value in Kelvin [K]
    '''
    
    if unit == 'F':
        K = (value+459.67)/1.8;
    if unit == 'C':
        K = value+273.15;
    if unit == 'R':
        K = value/1.8;
    return K

def get_R(value,unit):
    '''
    Inputs:
        value: temperature value you are in
        unit: unit of temp value, 'F', 'C', or 'K'
        
    Output:
        Temperature Value in Rankine [R]
    '''
    
    if unit == 'F':
        R = value+459.67;
    if unit == 'C':
        R = (value*1.8)+32+459.67;
    if unit == 'K':
        R = value*1.8;
    return R
