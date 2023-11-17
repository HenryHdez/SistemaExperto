# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 11:59:11 2022

@author: Camila Rodriguez
"""
# PESOS MOLECULARES DE LOS SIGUIENTES COMPUESTOS:(C,H,O,N,CO2,CO,O2,N2,H2O,NO,NO2,CH4,N2_air,O2_air,air) kg⁄kmol
def MW_func():
    C=12.0110
    H=1.0079
    O=15.9994
    N=14.0067
    CO2=C+O
    CO= C+(O*2)
    O2 = O*2
    N2 = N*2
    H2O= H*2+O
    NO = N+O
    NO2= N+O*2
    CH4= C+H*4
    N2air=0.79
    O2air=0.21
    air=N2air*N2+O2air*O2
    N2O2mol=N2air/O2air
    
    return[C,H,O,N,CO,CO2,O2,N2,H2O,NO,NO2,CH4,N2air,O2air,air,N2O2mol]


