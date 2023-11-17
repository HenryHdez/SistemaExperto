#''Dim matriz As Variant
#''Dim Vsolucion As Variant
#''Dim MatrizInv As Variant
#''Dim Vresultado As Variant
import numpy as np
import Modulo2
Xjc = 0.0
Xch = 0.0
hjc = 0.0
Hvcl = 0.0
alfa = 0.0
mc = 0.0
Xc = 0.0
hc = 0.0
hch = 0.0
matrix = []

def Qconcentracion(Xp, Tp, Xmiel, Tmiel, mmiel):
    Qconcentracion = resolver_concentracion(Xp, Tp, Xmiel, Tmiel, mmiel, 1)
    return Qconcentracion

def Qevaporacion(Xmiel, Tmiel, Xc, Tc, mc):
    Qevaporacion = resolver_evaporacion(Xmiel, Tmiel, Xc, Tc, mc, 1)
    return Qevaporacion

def Masa_miel(Xmiel, Tmiel, Xc, Tc, mc):
    Masa_miel = resolver_evaporacion(Xmiel, Tmiel, Xc, Tc, mc, 2)
    return Masa_miel

def Masa_vapor_evaporacion(Xmiel, Tmiel, Xc, Tc, mc):
    Masa_vapor_evaporacion = resolver_evaporacion(Xmiel, Tmiel, Xc, Tc, mc, 3)
    return Masa_vapor_evaporacion

def Qclarificacion(Xjc, Xch, alfa, mc, Xc, Tjc, Tc):
    Qclarificacion = resolver_clarificacion(Xjc, Xch, alfa, mc, Xc, Tjc, Tc, 1)
    return Qclarificacion

def Masa_jugo_crudo(Xjc, Xch, alfa, mc, Xc, Tjc, Tc):
    Masa_jugo_crudo = resolver_clarificacion(Xjc, Xch, alfa, mc, Xc, Tjc, Tc, 2)
    return Masa_jugo_crudo

def Masa_vapor_clarificacion(Xjc, Xch, alfa, mc, Xc, Tjc, Tc):
    Masa_vapor_clarificacion = resolver_clarificacion(Xjc, Xch, alfa, mc, Xc, Tjc, Tc, 3)
    return Masa_vapor_clarificacion

def Masa_cachaza(Xjc, Xch, alfa, mc, Xc, Tjc, Tc):
    Masa_cachaza = resolver_clarificacion(Xjc, Xch, alfa, mc, Xc, Tjc, Tc, 4)
    return Masa_cachaza

def resolver_clarificacion(Xjc, Xch, alfa, mc, Xc, Tjc, Tc, X):
    hjc = 0.0
    Hvcl = 0.0
    hc = 0.0
    hch = 0.0
    
    A=np.zeros((4,5))
    hjc = Modulo2.hjugo(Tjc, Xjc)
    Hvcl = Modulo2.Hvapor(Tc)
    hc = Modulo2.hjugo(Tc, Xc)
    A[0, 0] = 0
    A[0, 1] = 1
    A[0, 2] = -1
    A[0, 3] = -1
    A[0, 4] = mc
    
    A[1, 0] = 0
    A[1, 1] = Xjc
    A[1, 2] = 0
    A[1, 3] = -Xch
    A[1, 4] = mc * Xc
    
    A[2, 0] = 1
    A[2, 1] = hjc
    A[2, 2] = -Hvcl
    A[2, 3] = -hch
    A[2, 4] = mc * hc
    
    A[3, 0] = 0
    A[3, 1] = -alfa
    A[3, 2] = 0
    A[3, 3] = 1
    A[3, 4] = 0
    resolver_clarificacion = GaussJ(A, X)
    return resolver_clarificacion

def resolver_evaporacion(Xmiel, Tmiel, Xc, Tc, mc, X):
    a=0
    hmiel = 0.0
    He = 0.0
    hc = 0.0
    
    A=np.zeros((3,4))
    hmiel = Modulo2.hjugo(Tmiel, Xmiel)
    He = Modulo2.Hvapor((Tmiel + Tc) / 2)
    hc = Modulo2.hjugo(Tc, Xc)   
    
    A[0, 0] = 0
    A[0, 1] = 1
    A[0, 2] = 1
    A[0, 3] = mc
    
    A[1, 0] = 0
    A[1, 1] = Xmiel
    A[1, 2] = 0
    A[1, 3] = mc * Xc
    
    A[2, 0] = -1
    A[2, 1] = hmiel
    A[2, 2] = He
    A[2, 3] = mc * hc
    
    resolver_evaporacion = GaussJ(A, X)
    return resolver_evaporacion

def resolver_concentracion(Xp, Tp, Xmiel, Tmiel, mmiel, X):
    x=0
    hmiel = 0.0
    hc = 0.0
    hp = 0.0
    A=np.zeros((3,4))
        
    hmiel = Modulo2.hjugo(Tmiel, Xmiel)
    
    hc = Modulo2.Hvapor((Tmiel + Tp) / 2)
    
    hp = Modulo2.hjugo(Tp, Xp)
    
    A[0, 0] = 0
    A[0, 1] = 1
    A[0, 2] = 1
    A[0, 3] = mmiel
    
    A[1, 0] = 0
    A[1, 1] = Xp
    A[1, 2] = 0
    A[1, 3] = mmiel * Xmiel
    
    A[2, 0] = -1
    A[2, 1] = hp
    A[2, 2] = hc
    A[2, 3] = mmiel * hmiel
    
    resolver_concentracion = GaussJ(A, X)
    return resolver_concentracion

def GaussJ(matrix, X):
    #Dim A As Variant
    #'prueba = matrix(1, 5)
    #N = UBound(matrix, 1) ' filas
    #m = UBound(matrix, 2) ' columnas
    A=matrix
    aux=np.shape(matrix)
    N=aux[0] #Filas
    m=aux[1] #Columnas
    
    if (m == N + 1):
        for i in range(0,N):
            if A[i, i] == 0:
                j = 1
                while j <= N:
                    if j != i:
                        if A[j, i] != 0:
                            for k in range(0,m):
                                A[i, k] = (A[j, k] + A[i, k]) / A[j, i]
                            j = 5
                        else:
                            j = j + 1
                    else:
                        j = j + 1
        
        for i in range(0,N):
            temporal = A[i, i]
            for j in range(0,m):
                A[i, j] = A[i, j] / temporal
        
        for i in range(0,N):
            for j in range(0,N):
                if i != j:
                    if A[j, i] != 0:
                        factor = -(A[j, i] / A[i, i])
                        for k in range(0,m):
                            A[j, k] = factor * A[i, k] + A[j, k]
                            
        for i in range(0,N):
            temporal = A[i, i]
            for j in range(0,m):
                A[i, j] = A[i, j] / temporal     
        
        if X <= N:
            GaussJ = A[X, m-1]
        else:
            GaussJ = False
    
    else:
        GaussJ = False
    
    return GaussJ