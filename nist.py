import requests
import os
import numpy as np

#A program for mass downloading NIST thermophysical properties

def get_props_nist(P,T1,T2,Tstep,CAS):
    '''
    P (psi)
    The rest: SI
    '''
    url = "https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID="+CAS+ "&Type=IsoBar&Digits=5&P=" + str(int(P)) + "&THigh=" +str(int(T2)) + "&TLow=" +str(int(T1)) + "&TInc=" +str(int(Tstep)) + "&RefState=DEF&TUnit=K&PUnit=psia&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm"

    r = requests.get(url)
    text = r.text.replace('liquid','1')
    text = text.replace('vapor','0')
    text = text.replace('supercritical','2')
    f = open('./%s/%s_%.5d.csv'%(CAS,CAS,P),'w')
    f.write(text)
    f.close()

def get_all_data(CAS,P1,P2,Pstep,T1,T2,Tstep):
    if not os.path.isdir(CAS):
        os.mkdir(CAS)
    for P in range(P1,P2+Pstep,Pstep):
        get_props_nist(P,T1,T2,Tstep,CAS)

def make_big_table(CAS,P1,P2,Pstep,T1,T2,Tstep):
    table = None
    for P in range(P1,P2+Pstep,Pstep):
        if P == P1:
            table = np.genfromtxt('./%s/%s_%.5d.csv'%(CAS,CAS,P), delimiter='\t')[1:]
        else:
            newtable = np.genfromtxt('./%s/%s_%.5d.csv'%(CAS,CAS,P), delimiter='\t')[1:]
            table = np.append(table,newtable,axis=0)
    return table

def make_file(fname, CAS,P1,P2,Pstep,T1,T2,Tstep):
    get_all_data(CAS,P1,P2,Pstep,T1,T2,Tstep)
    table = make_big_table(CAS,P1,P2,Pstep,T1,T2,Tstep)
    np.savetxt(fname,table)