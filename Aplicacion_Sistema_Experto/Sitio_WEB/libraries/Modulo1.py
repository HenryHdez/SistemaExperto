import math 
from libraries import Modulo2

ACO2 = 0
ACO  = 0
AN2  = 0
AH2O = 0
AO2  = 0
A_prom=[]
i=0.0
H=0.0

Tin=0.0
Tout=0.0
yco2=0.0
yco=0.0
yn2=0.0
yh2o=0.0
yo2=0.0
R=0.0
Tprueba=0.0
Error=0.0
contador=0

def MMO2_KG_KMOL():
    #As Double
    c = 12.0107
    O = 15.999
    H = 1.00794
    N = 14.0067
    
    CO = c + O
    CO2 = c + 2 * O
    N2 = 2 * N
    O2 = 2 * O
    MMO2_KG_KMOL = O2
    return MMO2_KG_KMOL

def MMCO2_KG_KMOL():
    #As Double
    c = 12.0107
    O = 15.999
    H = 1.00794
    N = 14.0067
    
    CO = c + O
    CO2 = c + 2 * O
    N2 = 2 * N
    O2 = 2 * O
    MMCO2_KG_KMOL = CO2
    return MMCO2_KG_KMOL

def MMN2_KG_KMOL():
    #As Double
    c = 12.0107
    O = 15.999
    H = 1.00794
    N = 14.0067
    
    CO = c + O
    CO2 = c + 2 * O
    N2 = 2 * N
    O2 = 2 * O
    MMN2_KG_KMOL = N2
    return MMN2_KG_KMOL

def MMCO_KG_KMOL():
    #As Double
    c = 12.0107
    O = 15.999
    H = 1.00794
    N = 14.0067
    
    CO = c + O
    CO2 = c + 2 * O
    N2 = 2 * N
    O2 = 2 * O
    MMCO_KG_KMOL = CO
    return MMCO_KG_KMOL

def MMH2O_KG_KMOL():
    #As Double
    c = 12.0107
    O = 15.999
    H = 1.00794
    N = 14.0067
    
    CO = c + O
    CO2 = c + 2 * O
    N2 = 2 * N
    O2 = 2 * O
    H2O = 2 * H + O
    MMH2O_KG_KMOL = H2O
    return MMH2O_KG_KMOL

def MasaMolecular(yco, yco2 , yn2 , yo2 , yh2o ):
    #As Double
    c = 12.0107
    O = 15.999
    H = 1.00794
    N = 14.0067
    
    CO = c + O
    CO2 = c + 2 * O
    N2 = 2 * N
    O2 = 2 * O
    H2O = 2 * H + O
    MasaMolecular = yco * CO + yco2 * CO2 + yn2 * N2 + yo2 * O2 + yh2o * H2O 
    return MasaMolecular
 
def Ho(T , yco , yco2 , yn2 , yo2 , yh2o ):
    #As Double    
    if (T + 273.15 > 1000):
        CO2 = [4.63659493, 0.00274131991, -0.000000995828531, 1.60373011E-10, -9.16103468E-15, -1696.827307, -1.93534855]
        CO  = [3.04848583, 0.00135172818, -0.000000485794075, 7.88536486E-11, -4.69807489E-15, -972.4894446, 6.0170979]
        O2  = [3.66096083, 0.000656365523, -0.000000141149485, 2.06797658E-11, -1.29913248E-15, -1215.97725, 3.41536184]
        N2  = [2.95257626, 0.00139690057, -0.000000492631691, 7.86010367E-11, -4.60755321E-15, -923.948645, 5.87189252]
        H2O = [2.67703787, 0.00297318329, -0.00000077376969, 9.44336689E-11, -4.26900959E-15, -801.0769913, 6.88255571]
    else:
        
        CO2 = [2.35677352, 0.00898459677, -0.000007123556269, 2.45919022E-09, -1.43699548E-13, -1043.865014, 9.90105222]
        CO  = [3.57953347, -0.00061035368, 0.00000101681433, 9.07005884E-10, -9.04424499E-13, -1050.458397, 3.50840928]
        O2  = [3.782456636, -0.00299673415, 0.000009847302, -9.68129508E-09, 3.24372836E-12, -1063.94356, 3.65767573]
        N2  = [3.53100528, -0.000123660987, -0.000000502999437, 2.43530612E-09, -1.40881235E-12, -1046.97628, 2.96747468]
        H2O = [4.19864056, -0.0020364341, 0.00000652040211, -5.48797062E-09, 1.77197817E-12, -1208.90995, -0.849032208]
    
    A_prom=[]
    for i in range(0,6):
        A_prom.append((CO2[i] * yco2) + (CO[i] * yco) + (O2[i] * yo2) + (N2[i] * yn2) + (H2O[i] * yh2o))
        aPRUEBA = A_prom[i]
    H = 0.0
    for i in range(0,4):
        H = H + ((A_prom[i]*((T+273.15)**(i + 1)))/(i + 1))
    Ho = H + A_prom[5]
    return Ho
    
def Cp(T , yco , yco2 , yn2 , yo2 , yh2o ):
    #As Double
    
    R = 8.314472 #'J/mol ªC  -  KJ/Kmol ªC
    
    MM = MasaMolecular(yco, yco2, yn2, yo2, yh2o)
    
    if (T + 273.15 > 1000):
    
        CO2 = [4.63659493, 0.00274131991, -0.000000995828531, 1.60373011E-10, -9.16103468E-15, -1696.827307, -1.93534855]
        CO  = [3.04848583, 0.00135172818, -0.000000485794075, 7.88536486E-11, -4.69807489E-15, -972.4894446, 6.0170979]
        O2  = [3.66096083, 0.000656365523, -0.000000141149485, 2.06797658E-11, -1.29913248E-15, -1215.97725, 3.41536184]
        N2  = [2.95257626, 0.00139690057, -0.000000492631691, 7.86010367E-11, -4.60755321E-15, -923.948645, 5.87189252]
        H2O = [2.67703787, 0.00297318329, -0.00000077376969, 9.44336689E-11, -4.26900959E-15, -801.0769913, 6.88255571]
    else:
    
        CO2 = [2.35677352, 0.00898459677, -0.000007123556269, 2.45919022E-09, -1.43699548E-13, -1043.865014, 9.90105222]
        CO  = [3.57953347, -0.00061035368, 0.00000101681433, 9.07005884E-10, -9.04424499E-13, -1050.458397, 3.50840928]
        O2  = [3.782456636, -0.00299673415, 0.000009847302, -9.68129508E-09, 3.24372836E-12, -1063.94356, 3.65767573]
        N2  = [3.53100528, -0.000123660987, -0.000000502999437, 2.43530612E-09, -1.40881235E-12, -1046.97628, 2.96747468]
        H2O = [4.19864056, -0.0020364341, 0.00000652040211, -5.48797062E-09, 1.77197817E-12, -1208.90995, -0.849032208]
    
    A_prom=[]
    for i in range(0,6):
        A_prom.append(CO2[i] * yco2 + CO[i] * yco + O2[i] * yo2 + N2[i] * yn2 + H2O[i] * yh2o)
        aPRUEBA = A_prom[i]
    
    Cpp = 0
    for i in range(0,4):
        Cpp = Cpp + (A_prom[i] * (((T + 273.15) ** (i))))

    Cp = Cpp * R / MM
    return Cp
    
def DH_KJKmol(Tin , Tout , yco , yco2 , yn2 , yo2 , yh2o ):
    #As Double
    R = 8.314472
    DH_KJKmol = (Ho(Tout, yco, yco2, yn2, yo2, yh2o) - Ho(Tin, yco, yco2, yn2, yo2, yh2o)) * R
    return DH_KJKmol
 
def DH_KJKg(Tin , Tout , yco , yco2 , yn2 , yo2 , yh2o ):
    #As Double
    R = 8.314472
    MM = MasaMolecular(yco, yco2, yn2, yo2, yh2o)
    DH_KJKg = DH_KJKmol(Tin, Tout, yco, yco2, yn2, yo2, yh2o) / MM
    return DH_KJKmol

def Densidad_kgm3(yco , yco2 , yn2 , yo2 , yh2o , P , T ):
    #As Double
    MM = MasaMolecular(yco, yco2, yn2, yo2, yh2o)
    R = 8.314472
    Densidad_kgm3 = P * MM / (R * (T + 273.15))
    return Densidad_kgm3