import math 
import Modulo1

def Tw(Q, visc, Hfg , Tens , Rho , cpjuice , k , Tebll ):  
    tp1 = 0.0
    tp2 = 0.0
    tp3 = 0.0
    tp4 = 0.0
    
    alfa = 1
    Csf = 0.00413
    try:
        tp1 = Q / (visc * Hfg * 1000)
        #tp2 = Sqr(Tens / (9.81 * (Rho - 0.521956)))
        tp2 = (Tens / (9.81 * (Rho - 0.521956)))**0.5
        tp3 = (cpjuice * visc * 1000 / k) ** alfa
        tp4 = Hfg / cpjuice
        Tw = Csf * ((tp1 * tp2) ** (1 / 3)) * tp3 * tp4 + Tebll
    except:
        Tw = 0.1
    return Tw

def twg(espesor , flux , twe ):
    k = 21.5
    try:
        twg = (espesor / k) * flux + twe
    except:
        twg = 0.1
    return twg

def Tadiabatica(Exceso , EfReaccion , Hum_bz , hum_air ):
    Hf_bz = 0.0
    Hf_CO2 = 0.0
    Hf_CO = 0.0
    Hf_H2O_l = 0.0
    Hf_H2O_g = 0.0
    mH2O = 0.0
    mBz_seca = 0.0
    mBz_h = 0.0
    MM_Bz = 0.0
    Tad = 0.0
    Tad2 = 0.0
    Moles_CO_Salida = 0.0
    Moles_CO2_Salida = 0.0
    Moles_N2_Req = 0.0
    Moles_O2_Salida = 0.0
    Moles_H2O_Salida = 0.0
    yco2 = 0.0
    yco = 0.0
    yo2 = 0.0
    yh2o = 0.0
    yn2 = 0.0
    Error = 0.0
    temporal = 0.0
    
    Hf_bz = -116.94
    Hf_CO2 = -393.5
    Hf_CO = -110.5
    Hf_H2O_g = -241.8
    Hf_H2O_l = -285.8
    MM_Bz = 23.21
    
    mBz_h = 1000
    mH2O = mBz_h * Hum_bz
    mBz_seca = mBz_h - mH2O
    
    Moles_Bz = (mBz_seca/MM_Bz)
    Moles_O2_Req_CO2 = EfReaccion*Moles_Bz*0.96613405
    Moles_O2_Req_CO = (1-EfReaccion)*Moles_Bz*0.46613405
    Moles_O2_Req_ideal = Moles_Bz*0.96613405
    Moles_O2_reales = Exceso*Moles_O2_Req_ideal
    Moles_H2O_producidos = Moles_Bz*0.561628615
    Moles_N2_Req = (Moles_O2_reales*0.79)/0.21
    
    Moles_aire = Moles_N2_Req + Moles_O2_reales
    Moles_h2o_air = Moles_aire * (hum_air * (Modulo1.MasaMolecular(0, 0, 0.79, 0.21, 0) / Modulo1.MMH2O_KG_KMOL()))
    
    
    Moles_H2O = (mH2O/Modulo1.MMH2O_KG_KMOL()) + Moles_h2o_air
    
    Moles_H2O_Salida = Moles_H2O_producidos + Moles_H2O
    Moles_CO2_Salida = Moles_Bz * EfReaccion
    Moles_CO_Salida = Moles_Bz * (1 - EfReaccion)
    Moles_O2_Salida = Moles_O2_reales - Moles_O2_Req_CO2 - Moles_O2_Req_CO
    
    Moles_salida_totales = Moles_N2_Req + Moles_H2O_Salida + Moles_CO2_Salida + Moles_CO_Salida + Moles_O2_Salida
    
    yco = Moles_CO_Salida / Moles_salida_totales
    yco2 = Moles_CO2_Salida / Moles_salida_totales
    yo2 = Moles_O2_Salida / Moles_salida_totales
    yn2 = Moles_N2_Req / Moles_salida_totales
    yh2o = Moles_H2O_Salida / Moles_salida_totales
    Tad = 2000
    DH2 = (Moles_Bz * Hf_bz) + ((Moles_H2O - Moles_h2o_air) * Hf_H2O_l) + (Moles_h2o_air * Hf_H2O_g) - (Moles_CO2_Salida * Hf_CO2) - (Moles_CO_Salida * Hf_CO) - (Moles_H2O_Salida * Hf_H2O_g)
    Error = 10000000
    conta=0
    while Error > 0.00000001 and conta<20:
        DH3 = Modulo1.DH_KJKmol(25, Tad, Moles_CO_Salida/1000, Moles_CO2_Salida/1000, Moles_N2_Req/1000, Moles_O2_Salida/1000, Moles_H2O_Salida/1000)
        Cpp = Modulo1.Cp(Tad, yco, yco2, yn2, yo2, yh2o) * (Moles_salida_totales * Modulo1.MasaMolecular(yco, yco2, yn2, yo2, yh2o)/1000)
        temporal = (DH3 - DH2) / Cpp
        Tad2 = Tad - temporal
        Error = abs(Tad2 - Tad)
        Tad = Tad2 
        conta=conta+1
    return Tad





def Tcalculada(Qgas , m_GAS , yco , yco2 , yn2 , yo2 , yh2o ):

    Tprueba = 0.0
    Tprueba2 = 0.0
    Moles_gases = 0.0
    temporal  = 0.0
    Error = 0.0
    Qtemporal = 0.0
    
    Error = 100000
    
    Moles_gases = m_GAS / Modulo1.MasaMolecular(yco, yco2, yn2, yo2, yh2o) #'kmol/h
    
    Tprueba = 1000
    
    conta=0
    while Error > 0.00000001 and conta<20:
        Qtemporal = ((Modulo1.DH_KJKmol(25, Tprueba, yco, yco2, yn2, yo2, yh2o) * Moles_gases) / 3600)
        DH = Qtemporal - Qgas
        Cpp = Modulo1.Cp(Tprueba, yco, yco2, yn2, yo2, yh2o) * m_GAS / 3600
        temporal = DH / Cpp
        Tprueba2 = Tprueba - temporal
        Error = abs(Tprueba2 - Tprueba)
        Tprueba = Tprueba2
        conta=conta+1
    Tcalculada = Tprueba
    return Tcalculada

def XbrixCl(m_jc , Xjc , alfa , Q , Xch , P , Tin ):

    m_c = 0.0
    
    Vcl = 0.0
    Hcl = 0.0
    Tcl = 0.0
    hc = 0.0
    Q1 = 0.0
    h_jc = 0.0
    Error = 0.0
    temporal = 0.0
    temporal2 = 0.0
    Xt1 = 0.0
    Xt2 = 0.0
    Q22 = 0.0
    Q33 = 0.0
    Der = 0.0
    B = 0.0
    Qsensible = 0.0
    
    Xt1 = Xjc
    Error = 10000
    Qsensible = CalorCl(m_jc, Xjc, alfa, Xch, P, Tin, Xjc)
    conta=0
    if Q * 3600 < Qsensible:
        Xt1 = Xjc
    else:
    
        while Error > 0.00000001 and conta<30:
            Q1 = CalorCl(m_jc, Xjc, alfa, Xch, P, Tin, Xt1) - Q * 3600 #' f(x)
            Q22 = CalorCl(m_jc, Xjc, alfa, Xch, P, Tin, Xt1 + 0.000000001)
            Q33 = CalorCl(m_jc, Xjc, alfa, Xch, P, Tin, Xt1)
            
            Der = (Q22 - Q33) / 0.000000001
            
            B = Q1 - Der * Xt1
            
            Xt2 = -B / Der

            Error = abs(Xt2 - Xt1)
            Xt1 = Xt2
            conta=conta+1
    XbrixCl = Xt1
    return XbrixCl

def CalorCl(m_jc , Xjc , alfa , Xch , P , Tin , Xc ):

    m_c = 0.0
    
    Vcl = 0.0
    Hcl = 0.0
    Tcl = 0.0
    hc = 0.0
    Q1 = 0.0
    h_jc = 0.0
    qT = 0.0
       
        
    m_c = m_jc * (Xjc - alfa * Xch) / Xc
    Vcl = m_jc * (1 - alfa) - m_c
    Tcl = Tjugo(P, Xc)
    Hcl = Hvapor(Tcl)
    hc = hjugo(Tcl, Xc)
    h_jc = hjugo(Tin, Xjc)
    h_ch = hjugo(Tcl, Xch)
    qT = -m_jc * (h_jc - alfa * h_ch) + Vcl * Hcl + m_c * hc
    CalorCl = qT
    return CalorCl

def CalorCl_sensible(m_jc , Xjc , alfa , P , Tamb , Tj ):


    m_c = 0.0
    
    Vcl = 0.0
    Hcl = 0.0
    Tcl = 0.0
    hc = 0.0
    Q1 = 0.0
    h_jc = 0.0
    qT = 0.0
    Xc = 0.0
    Xch = 0.0
       
    Xc = Xjc
    Xch = Xjc
        
    m_c = m_jc * (Xjc - alfa * Xch) / Xc
    Vcl = 0.0
    Tcl = Tj
    Hcl = Hvapor(Tj)
    hc = hjugo(Tcl, Xc)
    h_jc = hjugo(Tamb, Xjc)
    h_ch = hjugo(Tcl, Xch)
    #qT = -1.0*m_jc * (h_jc - alfa * h_ch) + Vcl * Hcl + m_c * hc
    qT=-1.0*m_jc*(h_jc-alfa)#*h_ch)
    CalorCl_sensible = qT
    return CalorCl_sensible

def Tfinal_jugo(Xjc , P , Tamb , mjc , Q , alfa ):

    Qsensible = 0.0
    Xt = 0.0
    Ttemp = 0.0
    Qtemp = 0.0
    Error = 0.0
    Ts = 0.0
    Q_Ts = 0.0
    Q_Tss = 0.0
    Der = 0.0
    B = 0.0
    
    Qsensible = CalorCl(mjc, Xjc, alfa, Xjc, P, Tamb, Xjc)
    
    if Q * 3600 < Qsensible:
    
    
        Error = 10000
        Ts = 25
        while Error > 0.00000001:
        
        
            Q_Ts = CalorCl_sensible(mjc, Xjc, alfa, P, Tamb, Ts) - Q * 3600
            Q_Tss = CalorCl_sensible(mjc, Xjc, alfa, P, Tamb, Ts + 0.00000001) - Q * 3600
            Der = (Q_Tss - Q_Ts) / 0.00000001
            B = Q_Ts - Der * Ts
            Tss = -B / Der
            Error = abs(Tss - Ts)
            Ts = Tss    
    #' calcular la temperatura    
        Ttemp = Ts
    
    else:
        Qtemp = Q * 3600
        Xt = XbrixCl(mjc, Xjc, alfa, Q, Xjc, P, Tamb)
        
        Ttemp = Tjugo(P, Xt)
          
    Tfinal_jugo = Ttemp
    return Tfinal_jugo

def hjugo(T, Brix):
    A = 3.288
    B = 0.03
    c = 0.226
    Tr = 25
    hjugo = A * (T - Tr) - B * Brix * (T - Tr) + c * (T * (math.log(T) - 1) - Tr * (math.log(Tr) - 1))
    return hjugo

def Hvapor(T):
    Tr = 25
    Hvapor = 1.601 * T - 4.216 * Tr + 2512.94
    return Hvapor

def hagua(T):
    Tr = 25
    hagua = 4.216 * (T - Tr)
    return hagua

def Tantoine(P):
    AA = 5.11564
    BB = 1687.537
    CC = 230.17
    Tantoine = (BB / (AA - (math.log(P) / math.log(10)))) - CC
    return Tantoine

def delta_Tjugo(X):
    try:
        delta_Tjugo = 0.2209 * math.exp(0.0557 * X)
    except:
        delta_Tjugo = 20
    return delta_Tjugo

def Tjugo(P, X):
    Tjugo = Tantoine(P) + delta_Tjugo(X)
    return Tjugo