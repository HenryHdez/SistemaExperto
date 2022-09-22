import MW   
import H
import S
import XSteamPython as stm  #Propiedades del vapor
import math as m  
import pandas as pd  #Procesamiento de datos
import numpy as N    #Procesamiento numérico

def EvaluacionPar(Nom_Arch):
    """1.2.IMPORTAR ARCHIVO DE EXCEL"""
    
    # el archivo excel en este codigo se importa la hoja 1 que contiene los datos de entrada para extraer
    Data1 = pd.read_excel(Nom_Arch, sheet_name="dat")
    
    # En este codigo se importa la hoja 2 que contiene los datos de los °BRIX
    Data2 = pd.read_excel(Nom_Arch, sheet_name="Brix")
    
    # En este codigo se importa la hoja 2 que contiene los datos de las especies definidas
    Data3= pd.read_excel(Nom_Arch,sheet_name="fg_conc")
    
    # En este codigo se importa la hoja 2 que contiene los datos de las especies definidas
    Data4= pd.read_excel(Nom_Arch,sheet_name="fg_temp")
    
    """1.3. SE IMPORTA LOS DATOS DE ENTRADA DEL ARCHIVO EXCEL Y DEFINICION DE VARIABLES"""
    
    """SECCIÓN 2"""###########################################################################
    """1.3.1. Datos de masa (Utilizados en el jugo de caña  en los balances (punto 2)"""
    # Los datos se importaron de la hoja 1 que llamamos a esa variable Data 1, despues extraemos el valor de cada
    # variable que en la hoja 1 en  la casilla que se llama (Value), y ubicamos la posición de la fila en que esta
    # la variable.
    
    m_cs = Data1['Value'][2]  # Masa de caña (kg/h)
    m_cb = Data1['Value'][3]  # Masa de Bagazo de caña (Kg/h)
    m_ci = Data1['Value'][5]  # Masa de impurezas (Kg/h)
    m_ncs = Data1['Value'][7]  # Masa de panela (kg/h)
    m_ch = Data1['Value'][8]  # Masa de cachaza (kg/h)
    
    
    """1.3.2. Datos de formación de matrices en la ecuación de balances de masa y Agua evaporada (Punto 2.4)"""
    # Los siguientes datos se definen primero para crear las matrices y utilizarlas en el ciclo for para
    # resolver la ecuación y obtener los resultados de masa de jugo y agua evaporada.
    
    # Vector  de los Brix In: Primero se ubica la hoja 2 Y extraemos la columna de los °BrixIn
    bxi = N.array(Data2['BrixIn'])
    # Vector de los  Brix Out:Primero se ubica la hoja 2 Y extraemos la columna de los °BrixOut
    bxo = N.array(Data2['BrixOut'])
    # Esta Matriz establece la cantidad de casillas que contiene la columna ques es igual a 11, los valores en los °Brix
    sz = (N.size(bxi))
    # mat es la Matriz de ceros para el Balance de Masa en los  °Brix que esta matriz tiene (11,2)
    # 11 filas y 2 columnas.
    mat = N.zeros((sz, 2))
    # Definimos mat y ubicamos la posición [sz-1,0] que eso seria en la posicion [11-1,0], osea
    # se encuentra en la posicion [10,0] enla matriz que seria igual a m_ncs a la masa de panela
    # equivalente a 100.
    mat[sz-1, 0] = m_ncs
    # Definimos s2 como (sz-1) que seria (11-1=10), que por lo tanto s2 equivale a 10
    s2 = sz-1
    
    
    """1.3.3 Datos de Propiedades físicas y térmicas del jugo (punto 2.5.1)"""
    
    
    # Delta de Temperatura en grados Brix, se halla primero para hallar la temperatura de saturación (°c),
    # Se agrega Numpy (N) para convertirlo de lista a serie
    DeltaT_ebull = []
    
    DeltaT_ebull = (0.2209*N.exp(0.0557*bxo))+273.15
    
    # Presión atmosferica (mmHG)
    Patm = Data1['Value'][21]
    
    # Temperatura de saturación de algua para hallar la temperatura de ebullición. (°C)
    Tsat_a = ((3830/(23.19-m.log(Patm)))-228.32)+273.15
    
    Tebull = (Tsat_a+DeltaT_ebull)+273.15  # Temperatura de Ebullicion (°K)
    
    """1.3.3.Datos de balance de energia y exergia (punto 2.6)"""
    Ti = Data2['TIn(°C)']  # Vector  de la temperatura in: Primero se ubica la hoja 2 Y extraemos la columna de los TIn(°C)
    # Vector  de la temperatura out: Primero se ubica la hoja 2 Y extraemos la columna de los TOut(°C)
    To = Data2['TOut(°C)']
    # Presión atmosferica (mmHG): primero se ubica en la hoja 1 vamos a la Columna (Value) en la
    # posicion de la fila 21 del datframe
    Patm = Data1['Value'][21]
    # Presión de vapor (mmHG) primero se ubica en la hoja 1 vamos a la Columna (Value) en la
    # posicion de la fila 22del dataframe
    Pvap = Data1['Value'][22]
    
    # Vector de la funciónde los pesos moleculares
    [MWC, MWH, MWO, MWN, MWCO2, MWCO, MWO2,MWN2,  MWH2O, MWNO, MWNO2, MWCH4, MWN2air, MWO2air, MWair, N2O2mol]=MW.MW_func()
    
    # Flujo de masa de vapor: primero se ubica en la hoja 1 y vamos la columna (Value)
    # posición de la fila 24 de datframe (Kg/h)
    MV = Data1['Value'][24]
    # Presión de vapor en la caldera: primero se ubica en la hoja 1 y vamos la columna (Value)
    # posición de la fila 25 de datframe (Kpa)
    Pv = Data1['Value'][25]
    # Presión de condensado: primero se ubica en la hoja 1 y vamos la columna (Value)
    # posición de la fila 26 de datframe (Kpa)
    Pcond = Data1['Value'][26]
    # Presión de vapor en el evaporador: primero se ubica en la hoja 1 y vamos la columna (Value)
    # posición de la fila 27 de datframe (Kpa)
    Pve = Data1['Value'][27]
    
    
    """1.3.4. Exergí­as quí­micas estandar kJ/kmol"""
    e_CO2 = 19.48*1000
    e_CO = 274.71*1000
    e_O2=3.97*1000
    e_N2=0.72*1000
    e_NO=88.9*1000
    e_NO2=55.6*1000
    e_CH4=836.51*1000
    e_H2Ol = 0.9*1000
    e_H2Og = 9.5*1000
    """1.3.5.Presiones parciales estandar (bar)en el ambiente T = 298.15 K, PÂ° = 1.013 25 bar"""
    P_CO2 = 0.000294
    P_H2Og = 0.0088
    P_N2 = 0.7583
    P_O2 = 0.2040
    """1.3.5 Calculos de combustión"""
    
    # Fracción de Masa de humedad en el bagazo de caña (Kg H20/ kg Cb)
    Xmw_cb = Data1['Value'][11]
    # Fracción de Masa de C en el bagazo de caña (Kg C/ kg Cb)
    Xme_cbC = Data1['Value'][12]
    # Fracción de Masa de H en el bagazo de caña (Kg H/ kg Cb)
    Xme_cbH = Data1['Value'][13]
    # Fracción de Masa de O en el bagazo de caña (Kg O/ kg Cb)
    Xme_cbO = Data1['Value'][14]
    # Fracción de Masa de N en el bagazo de caña (Kg N/ kg Cb)
    Xme_cbN = Data1['Value'][15]
    # Fracción de Masa de SZ en el bagazo de caña (Kg CZ/ kg Cb)
    Xme_cbCZ = Data1['Value'][16]
    
    
    Xme_cb=N.c_[Xme_cbC,Xme_cbH,Xme_cbO,Xme_cbN]
     
    #Flujo másico de bagazo e caña en bas humeda (Kg/h)
    mcb_wb=Data1['Value'][10]
    
    """SECCIÓN 4"""#--------------------------------------------------------------
    """1.3.5. Definición de especies en el balance de combustión"""
    #Rx: P[CHON] + Q[O2+3.76N2] = R[CO2] + S[CO] + T[O2] + U[N2] + V[H2Of] + W[NO] + X[NO2] + Z[CH4]
    
    
    #Vector  de   cada una de las especies: Primero se ubica la hoja 3 Y extraemos la columna donde esta ubicada cada una de ellas.
    global fgc_CO2
    fgc_CO2= N.array(Data3['R(CO2)'])
    fgc_CO= N.array(Data3['S(CO)'])
    fgc_O2= N.array(Data3['T(O2)'])
    fgc_N2= N.array(Data3['U(N2)'])
    fgc_NO= N.array(Data3['W(NO)'])
    fgc_NO2= N.array(Data3['X(NO2)'])
    fgc_CH4= N.array(Data3['Z(CH4)'])
    
    
    # Esta Matriz establece la cantidad de casillas que contiene la columna ques es igual a 60, los valores en las concentraciones de
    #cada especie
    sz1=N.size(fgc_CO2)
    """
    #Definición de Variables del Balance del flujo del gas"""
        
    MWgas=N.zeros((sz1,1))
    g_molgas=N.zeros((sz1,7))
    g_ggas=N.zeros((sz1,7))
    g_kggas=N.zeros((sz1,7))
    mol_kggas=N.zeros((sz1,7))
    mol_kgbm=N.zeros((sz1,7))
    kggas_h=N.zeros((sz1,7))
    kmol_h=N.zeros((sz1,7))
    Mgas=N.zeros((sz1,1))
    Relacion=N.zeros((sz1,1))
    fbc=N.zeros((sz1,2))
    YHgas=N.zeros((sz1,1))
    RelacionH=N.zeros((sz1,1))
    YH2Ogas=N.zeros((sz1,1))
    mH2O=N.zeros((sz1,1))
    YOair=N.zeros((sz1,1))
    Ctdair=N.zeros((sz1,1))
    molair=N.zeros((sz1,1))
    Mair=N.zeros((sz1,1))
    YN2gas=N.zeros((sz1,1))
        
       
    """1.3.7. Definición de las  temperaturas  en el flujo del gas """
    
    #Vector  de   cada una de las temperaturas: Primero se ubica la hoja 4 Y extraemos la columna donde esta ubicada cada una de ellas.
    
    global T_1
    T1=N.array(Data4['T1(°K)'])
    T2= N.array(Data4['T2(°K)'])
    T3= N.array(Data4['T3(°K)'])
    T4= N.array(Data4['T4(°K)'])
    T5= N.array(Data4['T5(°K)'])
    T6=N.array(Data4['T6(°K)'])
    Tref=298.15
    
    
    T=[T1, T2, T3, T4, T5, T6] #Temperatura
    
    
    
    """SECCIÓN 5"""#--------------------------------------------------------------
    
    """1.3.8 Definición  de variables Balance de Energia del flujo del gas"""
    
    
    
    
    """2. CALCULOS EN EL JUGO DE CAÑA """ ##################################################################################
    
    """2.1 Balance de masa en el molino """
    m_sj1 = m_cs-m_cb  # Masa de jugo sucio (Kg/h)
    ext = (m_sj1/m_cs)*100  # Extracción (%)
    
    """2.2 Balanace de masa en el Pre-limpiador """
    m_sj2 = m_sj1-m_ci  # Masa de jugo prelimpio (Kg/h)
    imp = (m_ci/m_sj1)*100  # Impurezas (%)
    
    """2.3 Balance de masa en la hornilla """
    m_sj3 = m_sj2-m_ch  # Masa de jugo limpio (Kg/h)
    chz = (m_ch/m_sj2)*100  # Cachaza (%)
    
    
    """2.4 Ecuación de balanace de masa en el procesos y de agua Evaporada """
    # Ciclo For:
    # Primero de finimos el rango (range) en que el ciclo for va a correr en este caso esta en el (s2+1)
    # que equivalaria (10+1=11) osea nos va correr desde i que corre desde la posicion 0 hasta 11 que definimos
    # el rango.
    # El if se utiliza para ejecutar un bloque de código si, y solo si, se cumple una determinada condición.
    # Por tanto, if es usado para la toma de decisiones.en esta caso la condición del if es (i>0)
    # i desde la posicion 0,1,2,3...etc es mayor que 0.
    
    # 1.Ecuación Balance de masa para jugo: traemos la variable mat que esta se ubicaria en la
    # matriz en la posicion [s2-i,0] osea la matriz va correr en [10-i(i puede correr en la
    # posición 0,1,2,3,4...),0] ejemplo: (5-0=5,0) seria en la posición (10,0) es igual a masa de panela
    # osea mat  en la posición [(s2+1)-i,0], que seria [(5+1)-i,0] , [(10)-i(0.1.2.3.4..),0],
    # ejemplo [(11)-1 =10,0] despues se multiplica por la variable establecida de los grados brix de salida (bxo)
    # que está en la posición [(s2+1)-i] , seria igual a[(6+1)-i(0,1,2,3,4..)] , dividdido en los grados brix
    # de entrada (bxi) que se encuentra en la misma posicion de los brix de salida [(6+1)-i(0,1,2,3,4..)]
    # 2. Ecuación Balance de Agua Evaporada:  traemos la variable mat que esta se ubicaria en la
    # matriz en la posicion [(s2+1)-i,1], esta matriz va correr en la posición ((10+1=11)-i(0,1,2,3,4..),1)
    # ejemplo: (11-0=11,1) cuando corre esta formula arrojara el resultadp de agua evaporada en la posición (11,1),
    # es igual a mat[s2-i,0] que es la ecuación del balance de masa para jugo, menos la masa de jugo de la
    # posicion anterior, osea es mat [(s2+1)-i,0], en la posición [(10+1)-i,0],[(11)-i(0,1,2,3...),0].
    
    for i in range(s2+1):
        if(i > 0):
            # Ecuacion Balance de masa para jugo
            mat[s2-i, 0] = mat[(s2+1)-i, 0]*(bxo[(s2+1)-i]/bxi[(s2+1)-i])
            # Ecuacón Balance de Agua Evaporada
            mat[(s2+1)-i, 1] = mat[s2-i, 0]-mat[(s2+1)-i, 0]
    
    
    """2.5 Propiedades fisicas , termicas y balance de masa """
    
    
    """ 2.5.1 Propiedades físicas y térmicas del jugo"""
    rho = 1043+4.854*bxo-1.07*Tebull  # Densidad del jugo (kg/m3)
    visc = 0.047/Tebull  # Viscocidad dinamica sj (Pa. s)
    cp = 4187*(1-0.006*bxo)/1000  # Calor especifico sj (kJ/kg K)
    lam = 2492.9-2.0523*bxo-0.0030752*bxo**2 # Calor latente de vaporización (kJ/kg)
    k = 0.3815-0.0051*bxo+0.0001866*Tebull  # Conductividad termica (W/mK)
    
    
    """2.6. Balances de energía y exergía """
    
    
    # Para hallar la presión parcial de agua (ppw), se requiere hallar primero  la humedad absoluta del aire.
    # Humedad absoluta del aire (Kmol de agua/ kmol de aire seco)
    HA_air = (((0.662*Pvap)/(Patm-Pvap))*MWair)/MWH2O
    
    """2.6.1 Exergias """
    ex_Sac = (5969.28/342.3)*1000  # Exergia de la sacarosa KJ/Kg
    # Exergia especifica  fisica de Agua evaporada (KJ/kg)
    Ef_ae = (stm.hV_T(100)-stm.hV_T(25))-25*(stm.sV_T(100)-stm.sV_T(25))
    ppw = ((HA_air*MWair)/MWH2O)*Patm*0.0013322  # Presión parcial de agua (bar)
    # Exergia quimica especifica de agua evaporada (KJ/Kmol)
    eq_ae = (8.3144*298.15*m.log(1/ppw))/MWH2O
    
    """2.6.2 Caldera"""
    mcond = MV  # Flujo de masa de vapor (Kg/h)
    
    """2.6.3 Exergia vapor en caldera"""
    ef_v = (stm.hV_p(Pv)-stm.hV_T(25))-25*(stm.sV_p(Pv)-stm.sV_T(25))
    E_v = (MV*ef_v)/3600  # Exergia de vapor en la caldera (KJ/kg)
    
    """2.6.4 Exergia de vapor en el evaporador"""
    ef_ve = (stm.hV_p(Pve)-stm.hV_T(25))-25*(stm.sV_p(Pve)-stm.sV_T(25))
    E_ve = (MV*ef_ve)/3600  # Exergia de vapor en el evaporador (KJ/kg)
    
    """2.6.5. Exergia de condensado"""
    Tcond = stm.Tsat_p(Pcond)
    ef_cond = (stm.hV_T(Tcond)-stm.hV_T(25))-25*(stm.sV_T(Tcond)-stm.sV_T(25))
    E_cond = (mcond*ef_cond)/3600  # Exergia de condensado (KJ/kg)
    
    """2.7 ENERGIA """
    
    # Se define la Calor específico (Cp) y Lambda (Lam) para calcular el calor sensibe y el calor latente
    
    Qs = mat[:, 0]*cp*(To-Ti)/3600  # Calor sensible (KW)
    Ql = (mat[:, 1]*lam)/3600  # Calor latente (KW)
    Qt = Qs+Ql  # Calor total o potencia termica (KW)
    
    """2.7.1 Exergias Quimicas"""
    
    # Flujo Exergetico quimico especifica del jugo kJ/Kg
    exq_sj = mat[:, 0]*(((1-bxo/100)*eq_ae)+((bxo/100)*ex_Sac))
    exq_asj = eq_ae*e_H2Ol  # flujo exergetico quimico de agua en el jugo KJ/Kg
    
    exq_asj1=mat[:,1]*eq_ae*e_H2Ol
    
    """2.7.2 Flujos exergeticos"""
    
    ex_sj = mat[:, 0]*(exq_sj+exq_asj)/3600  # Flujo exergetico  del jugo sj(kW)
    ex_va = (mat[:, 1]*(Ef_ae+eq_ae))/3600  # Flujo exergetico vapor de agua (Kw)
    
    mt_w = mat[:, 1]  # Masa total de agua evaporada (Kg/h)
    qu = Qt  # Calor total transferido (KW)
    E_ae = (mt_w*(Ef_ae+eq_ae))/3600  # Flujo exergetico de agua evaporada
    
    
    """ SECCIÓN 3: CALCULOS DE COMBUSTIÓN""" ##############################################################################
    
    """ 3.1. Fracción de ceniza libre de masa seca y humedad (daf) """
    
    
    """ 3.1 Analisis proximo"""
    War_Humedad=40.57 #Fracción de humedad (%)
    Wdb_Mvolatil=81.96 #Fraccion de Materia volátil  en base seca (%)
    Wdb_Cfijo=14.79 #Fracción de Carbon activado en base seca (%)
    Wdb_Ceniza=3.25 #Fracción de Ceniza en base seca (%)
    
    War_Mvolatil=Wdb_Mvolatil*(1-(War_Humedad/100)) #Fracción de Materia Volatil Humeda (%)
    War_Cfijo=Wdb_Cfijo*(1-(War_Humedad/100)) #Fraccion de Carbon fijo Humedo (%) 
    War_Ceniza=Wdb_Ceniza*(1-(War_Humedad/100)) #Fracción de Ceniza (%)
    
    Wdaf_Mvolatil=Wdb_Mvolatil*(1+(War_Ceniza/100)) #Fracción de Materia volátil libre de ceniza (%)
    Wdaf_Cfijo=Wdb_Cfijo*(1+(Wdb_Ceniza/100)) #Fracción de Carbon fijo libre de ceniza (%)
    
    
    
    """ 3.2. Fracción de ceniza libre de masa seca y humedad por compuesto"""
    "Calculo de Fracciones  del analisis proximo"
    WC_daf=53 #Fracción de Carbono libre de ceniza (%)
    WH_daf=4.7 #Fracción de Hidrogeno  libre de ceniza (%) 
    WO_daf=41.9 #Fracción de Oxigeno libre de ceniza (%)
    WN_daf=0.4 #Fracción de Nitrogeno libre de ceniza (%)
    
    WC_db=WC_daf*(1-(MWC/100)) #Fracción de Carbono en base seca (%)
    WH_db=WH_daf*(1-(MWH/100)) #Fracción de Hidrogno en base seca (%)
    WO_db=WO_daf*(1-(MWO/100)) #Fracción de Oxigeno en base seca (%)
    WN_db=WN_daf*(1-(MWN/100)) #Fracción de Nitrogeno en base seca (%)
    Wash_db=Wdb_Ceniza #Fracción de Ceniza en base seca (%)
    Wh20_db=War_Humedad
    
    WC_wb=WC_daf*(1-(War_Humedad/100)) #Fracción de Carbono en base humeda (%)
    WH_wb=WH_daf*(1-(War_Humedad/100)) #Fracción de Hidrogeno en base humeda (%)
    WO_wb=WO_daf*(1-(War_Humedad/100)) #Fracción de Oxigeno en base humeda (%)
    WN_wb=WN_daf*(1-(War_Humedad/100)) #Fracción de nitrogeno en base humeda (%)
    
    """3.3. Masa del combustible solido """
    "Calculo de masas del analisis proximo"
    mbiwb_Humedad=War_Humedad*10 #Masa del combustible en base humeda (g/kg)
    mbiwb_Mvolatil=War_Mvolatil*10 #Masa de materia volátil en base humeda (g/kg)
    mbiwb_Cfijo=War_Cfijo*10 #Masa de Carbono en base humeda (g/Kg)
    mbiwb_Ceniza=War_Ceniza*10 #Masa de Ceniza en base humeda (g/kg)
    
    mbidb_Mvolatil=Wdb_Mvolatil*10 #Masa de Materia volátil en base seca (g/kg)
    mbidb_Cfijo=Wdb_Cfijo*10 #Masa de carbon fijo en base seca (g/kg) 
    mbidb_Ceniza=Wdb_Ceniza*10 #Masa de Ceniza en base seca (g/kg)
    
    mbidaf_Mvolatil=Wdaf_Mvolatil*10 #Masa de materia volátil en base seca libre de ceniza (g/kg)
    mbidaf_Cfijo=Wdaf_Cfijo*10 #Masa de carbon fijo en base seca libre de ceniza (g/kg)
    
    mbiHumedad_wb=mbiwb_Humedad/1000 #Masa del combustible en base humeda (kg/kg)
    mbiMvolatil_wb=mbiwb_Mvolatil/1000 #Masa de materia volátil en base humeda (kg/kg)
    mbiCfijo_wb=mbiwb_Cfijo/1000 #Masa de Carbono en base humeda (kg/Kg)
    mbiCeniza_wb=mbiwb_Ceniza/1000 #Masa de Ceniza en base seca (kg/kg)
    
    mbiMvolatil_db=mbidb_Mvolatil/1000 #Masa de Materia volátil en base seca (kg/kg)
    mbiCfijo_db=mbidb_Cfijo/1000 #Masa de carbon fijo en base seca (kg/kg) 
    mbiCeniza_db=mbidb_Ceniza/1000 #Masa de Ceniza en base seca (kg/kg)
    
    mbiMvolatil_daf=mbidaf_Mvolatil/1000 #Masa de materia volátil en base seca libre de ceniza (kg/kg)
    mbiCfijo_daf=mbidaf_Cfijo/1000 #Masa de carbon fijo en base seca libre de ceniza (kg/kg)
    
    """3.4. Calculo de Fracciones de cada uno de los componentes"""
    
    
    WwbC=WC_daf*(1-(War_Humedad/100)) #Fracción de Carbono en base humeda (%)
    WwbH=WH_daf*(1-(War_Humedad/100)) #Fracción de Hidrogeno en base humeda (%)
    WwbO=WO_daf*(1-(War_Humedad/100)) #Fracción de Oxigeno en base humeda  (%)
    WwbN=WN_daf*(1-(War_Humedad/100)) #Fracción de Nitrogeno en base humeda (%)
    
    WdbC=WC_daf*(1-(Wdb_Ceniza/100)) #Fracción de Carbono en base seca  (%)
    WdbH=WH_daf*(1-(Wdb_Ceniza/100)) #Fracción de Hidrogeno en base seca  (%)
    WdbO=WO_daf*(1-(Wdb_Ceniza/100)) #Fracción de Oxigeno en base seca  (%)
    WdbN=WN_daf*(1-(Wdb_Ceniza/100)) #Fracción de Nitrogeno en base seca  (%)
    
    WdbCenizas=Wdb_Ceniza #Fracción de cenizas (%)
    WC_daf=53 #Fracción de Carbon en base seca libre de ceniza (%)
    WH_daf=4.7 #Fracción de Hidrogeno en base seca  libre de ceniza (%) 
    WO_daf=41.9 #Fracción de Oxigeno en base seca libre de ceniza (%)
    WN_daf=0.4 #Fracción de Nitrogeno en base seca libre de ceniza (%)
    
    
    """3.5. La masa de combustible en relación  con cada una de las bases"""
    
    mbiwb_C=WwbC*10 #Masa de Carbono  en base humeda (g/kg)
    mbiwb_H=WwbH*10 #Masa de Hidrogno en base humeda (g/kg)
    mbiwb_O=WwbO*10 #Masa de Oxigeno en base humeda (g/kg)
    mbiwb_N=WwbN*10 #Masa de Nitrogeno en base hueda (g/kg)
    
    mbidb_C=WdbC*10 #Masa de Carbono en base seca (g/kg)
    mbidb_H=WdbH*10 #Masa de Hidrogeno en base seca (g/kg)
    mbidb_O=WdbO*10 #Masa de Oxigeno en base seca (g/kg)
    mbidb_N=WdbN*10 #Masa de Nitrogeno en base seca (g/kg)
    mbidb_Ceniza= WdbCenizas*10 #Masa de Ceniza en base seca (g/kg)
    
    mbidaf_C=WC_daf*10 #Masa de Carbono en base seca libre de ceniza (g/kg) 
    mbidaf_H=WH_daf*10 #Masa de Hidrogeo en base seca libre de ceniza (g/kg)
    mbidaf_O=WO_daf*10 #Masa de Oxigeno en base seca libre de ceniza (g/kg)
    mbidaf_N=WN_daf*10 #Masa de Nitrogeno en base seca libre de ceiza (g/kg)
    
    mbiC_wb=mbiwb_C/1000 #Masa de Carbono  en base humeda (kg/kg)
    mbiH_wb=mbiwb_H/1000 #Masa de Hidrogno en base humeda (kg/kg)
    mbiO_wb=mbiwb_O/1000 #Masa de Oxigeno en base humeda (kg/kg)
    mbiN_wb=mbiwb_N/1000 #Masa de Nitrogeno en base hueda (kg/kg)
    
    mbiC_db=mbidb_C/1000 #Masa de Carbono en base seca (kg/kg)
    mbiH_db=mbidb_H/1000 #Masa de Hidrogeno en base seca (kg/kg)
    mbiO_db=mbidb_O/1000 #Masa de Oxigeno en base seca (kg/kg)
    mbiN_db=mbidb_N/1000 #Masa de Nitrogeno en base seca (kg/kg)
    mbiCeniza_db=mbidb_Ceniza/1000 #Masa de Ceniza en base seca (kg/kg)
    
    mbiC_daf=mbidaf_C/1000 #Masa de Carbono en base seca libre de ceniza (kg/kg)
    mbiH_daf=mbidaf_H/1000 #Masa de Hidrogeo en base seca libre de ceniza (kg/kg)
    mbiO_daf=mbidaf_O/1000 #Masa de Oxigeno en base seca libre de ceniza (kg/kg)
    mbiN_daf=mbidaf_N/1000 #Masa de Nitrogeno en base seca libre de ceiza (kg/kg)
    
    """3.6. La masa de combustible en relación con las moles de  cada una de las bases """
    niwb_C=WwbC/MWC*10 #Moles de Carbon en base humeda (mol/kg)
    niwb_H=WwbH/MWH*10 #Moles de Hidrogeno en base humeda (mol/kg)
    niwb_O=WwbO/MWO*10 #Moles de Oxigeno en base humeda (mol/kg)
    niwb_N=WwbN/MWN*10 #Moles de Nitrogeno e base humeda (mol/kg)
    niwb_h20=Wh20_db/MWH2O*10
    
    nidb_C=WdbC/MWC*10 #Moles de Carbon en base seca (mol/kg)
    nidb_H=WdbH/MWH*10 #Moles de Hidrogeno en base seca (mol/kg)
    nidb_O=WdbO/MWO*10 #Moles de Oxigeno en base seca (mol/kg)
    nidb_N=WdbN/MWN*10 #Moles de Nitrogeno en base seca (mol/kg)
    
    nidaf_C=WC_daf/MWC*10 #Moles de Carbon en base seca libre de ceniza (mol/kg)
    nidaf_H=WH_daf/MWH*10 #Moles de Hidrogeno en base seca libre de ceniza (mol/kg)
    nidaf_O=WO_daf/MWO*10 #Moles de Oxigeno en bas seca libre de ceniza (mol/kg)
    nidaf_N=WN_daf/MWN*10 #Moles de Oxigeno en bas seca libre de ceniza (mol/kg)
    
    """3.7. Las concentraciones de combustible en relación con las moles de  cada una de las bases """
    YCwb=mbiwb_C/MWC #Concentracion de Carbono en base humeda (mol/kgbm)
    YHwb=mbiwb_H/MWH #Concentracion de Hidrogeno en base humeda (mol/kgbm)
    YOwb=mbiwb_O/MWO #Concentracion de Oxigeno en base humeda (mol/kgbm)
    YNwb=mbiwb_N/MWN #Concentracion de Nitrogeno en base humeda (mol/kgbm)
    
    YCdb=mbidb_C/MWC #Concentracion de Carbono en base seca (mol/kgbm)
    YHdb=mbidb_H/MWH #Concentracion de Hidrogeno en base seca(mol/kgbm)
    YOdb=mbidb_O/MWO #Concentracion de Oxigeno en base seca (mol/kgbm)
    YNdb=mbidb_N/MWN #Concentracion de Nitrogeno en base seca (mol/kgbm)
    
    YCdaf=mbidaf_C/MWC #Concentracion de Carbono en base seca libre de ceniza (mol/kgbm)
    YHdaf=mbidaf_H/MWH #Concentracion de Hidrogeno en base seca libre de ceniza (mol/kgbm)
    YOdaf=mbidaf_O/MWO #Concentracion de Oxigeno en base seca libre de ceniza (mol/kgbm)
    YNdaf=mbidaf_N/MWN #Concentracion de Nitrogeno en base seca libre de ceniza (mol/kgbm)
    
    """3.7 Datos del combustible y del aire  """
    """3.7.1 Datos del combustible"""
    mcb_db=mcb_wb*(1-Xmw_cb) #Flujo másico de bagazo de caña en base seca (kg/h)
    nw_cb=(mcb_wb-mcb_db)/MWH2O #Flujo molar del agua en el bagazo de caña (Kmol/h)
    mcb_daf=mcb_db*(1-Wdb_Ceniza/100) #Flujo másico de bagazo de caña en base seca  LIBRE DE CENIZA(kg/h)
    
    """3.7.2 Datos del aire"""
    nO2=MWO2air*2 #Moles de O2 (molo2/molaire)
    nN2=MWN2air*2 #mOLES DE N2 (moln2/molaire)
    nO2air=nO2/MWair #Moles de O2 en el aire (mol/kgaire)
    nN2air=nN2/MWair #Moles de N2 en el aire (mol/kgaire)
    mO2air=nO2*MWO/MWair #Masa de O2 en el aire (gO2/gaire)
    mN2air=nN2*MWN/MWair  #Masa de N2 en el aire (gN2/gaire)
    nAlpha=N2O2mol #Alpha  (mol N2/mol O2)
    mAlpha=(nAlpha*(MWN*2))/(MWO*2) #Aplha  (kg N2/kg O2)
     
    """3.8  Energia y exergia """
    LHV=17799.3- 20305.95*Xmw_cb- 2035.98*0.025 #Valor Calorifico neto (KJ/kg)
    Qs_cb =( LHV*mcb_wb)/3600                       #Potencia termica de entrada (kW)
    
    phi_d = (1.0438 + 0.1882*(Xme_cbH/Xme_cbC) - 0.2509*(1+ 0.7256*(Xme_cbH/Xme_cbC)) + 0.0383*(Xme_cbN/Xme_cbC)/(1-0.3035*(Xme_cbO/Xme_cbC)));
    #For water substance at TÂ° = 298.15K, hfg = 2442 kJ/kg
    e_bs = (LHV + Xmw_cb*2442)*phi_d;   #Exergia especifica bagazo seco kJ/kg
    E_bs =( mcb_wb*e_bs)/3600;            #Flujo de Exergi­a Bagazo de Caña
    
    
    """SECCIÓN 4:Balanace de masa de los gases de Cobustión""" ############################################################
    
    #Conversiones de Unidades
    for i in range (sz1):
        MWgas[i,0]=fgc_CO2[i]*MWCO2+fgc_CO[i]*MWCO+fgc_O2[i]*MWO2+fgc_N2[i]*MWN2+fgc_NO[i]*MWNO+fgc_NO2[i]*MWNO2+fgc_CH4[i]*MWCH4 #Peso molecular del gas (g/mol)
        
    for i in range (sz1):
        g_molgas[i,0]=fgc_CO2[i]*MWCO2 #Flujo molar del CO2 (g/molgas)
        g_molgas[i,1]=fgc_CO[i]*MWCO #Flujo molar del CO (g/molgas)
        g_molgas[i,2]=fgc_O2[i]*MWO2 #Flujo molar del O2 (g/molgas)
        g_molgas[i,3]=fgc_N2[i]*MWN2 #Flujo molar del N2 (g/molgas)
        g_molgas[i,4]=fgc_NO[i]*MWNO #Flujo molar del NO (g/molgas)
        g_molgas[i,5]=fgc_NO2[i]*MWNO2 #Flujo molar del NO2 (g/molgas)
        g_molgas[i,6]=fgc_CH4[i]*MWCH4 #Flujo molar del CH4 (g/molgas)
        
    for i in range (sz1):
        g_ggas[i,0]= fgc_CO2[i]*MWCO2/MWgas[i,0] #Flujo masico CO2 (g/gas)
        g_ggas[i,1]= fgc_CO[i]*MWCO/MWgas[i,0] #Flujo masico CO (g/gas)
        g_ggas[i,2]= fgc_O2[i]*MWO2/MWgas[i,0] #Flujo masico O2 (g/gas)
        g_ggas[i,3]= fgc_N2[i]*MWN2/MWgas[i,0] #Flujo masico N2 (g/gas)
        g_ggas[i,4]= fgc_NO[i]*MWNO/MWgas[i,0] #Flujo masico NO (g/gas)
        g_ggas[i,5]= fgc_NO2[i]*MWNO2/MWgas[i,0] #Flujo masico NO2 (g/gas)
        g_ggas[i,6]= fgc_CH4[i]*MWCH4/MWgas[i,0] #Flujo masico CH4 (g/gas)
        
    for i in range (sz1):
        g_kggas[i,0]= g_ggas[i,0]*1000 #Flujo masico CO2 (g/kgas)
        g_kggas[i,1]= g_ggas[i,1]*1000 #Flujo masico CO (g/kgas)
        g_kggas[i,2]= g_ggas[i,2]*1000 #Flujo masico O2 (g/kgas)
        g_kggas[i,3]= g_ggas[i,3]*1000 #Flujo masico N2 (g/kgas)
        g_kggas[i,4]= g_ggas[i,4]*1000 #Flujo masico NO (g/kgas)
        g_kggas[i,5]= g_ggas[i,5]*1000 #Flujo masico NO2 (g/kgas)
        g_kggas[i,6]= g_ggas[i,6]*1000 #Flujo masico CH4 (g/kgas)
        
    for i in range (sz1):
        mol_kggas[i,0]=g_kggas[i,0]/MWCO2 #Flujo molar de CO2 (mol/kggas)
        mol_kggas[i,1]=g_kggas[i,1]/MWCO #Flujo molar de CO (mol/kggas)
        mol_kggas[i,2]=g_kggas[i,2]/MWO2 #Flujo molar de O2 (mol/kggas)
        mol_kggas[i,3]=g_kggas[i,3]/MWN2 #Flujo molar de N2 (mol/kggas)
        mol_kggas[i,4]=g_kggas[i,4]/MWNO #Flujo molar de NO (mol/kggas)
        mol_kggas[i,5]=g_kggas[i,5]/MWNO2 #Flujo molar de NO2 (mol/kggas)
        mol_kggas[i,6]=g_kggas[i,6]/MWNO2 #Flujo molar de CH4 (mol/kggas)
    
    for i in range (sz1):
        fbc[i,0]=fgc_CO2[i]*MWC/MWgas[i,0] #Fraccion molar de CO2 de C (mol/mol)
        fbc[i,1]=fgc_CO[i]*MWC/MWgas[i,0] #Fraccion molar de CO2 de C (mol/mol)
        
    """4.1. Balance de Masa de los gases de Combustión"""#------------------------
    
    """4.1.1 Balance de Carbono """
    
    for i in range (sz1):
        Mgas[i,0]=(mcb_daf*mbiC_daf)/(fbc[i,0]+fbc[i,1]) #Flujo masico del gas en daf  (kg/h)#Balance de Carbono
        
        
    for i in range (sz1):
        Relacion[i,0]=Mgas[i,0]/mcb_daf #Balance de Carbono.
    
    for i in range (sz1):
        mol_kgbm[i,0]=( mol_kggas[i,0]*MWCO2)*1000*(Relacion[i,0]/1000)/MWCO2 #Flujo másico de CO2 (mol/kgbm)
        mol_kgbm[i,1]=( mol_kggas[i,1]*MWCO)*1000*(Relacion[i,0]/1000)/MWCO #Flujo másico de CO (mol/kgbm)
        mol_kgbm[i,2]=( mol_kggas[i,2]*MWO2)*1000*(Relacion[i,0]/1000)/MWO2 #Flujo másico de O2 (mol/kgbm)
        mol_kgbm[i,3]=( mol_kggas[i,3]*MWN2)*1000*(Relacion[i,0]/1000)/MWN2 #Flujo másico de N2 (mol/kgbm)
        mol_kgbm[i,4]=( mol_kggas[i,4]*MWNO)*1000*(Relacion[i,0]/1000)/MWNO #Flujo másico de NO (mol/kgbm)
        mol_kgbm[i,5]=( mol_kggas[i,5]*MWNO2)*1000*(Relacion[i,0]/1000)/MWNO2 #Flujo másico de NO2 (mol/kgbm)
        mol_kgbm[i,6]=( mol_kggas[i,6]*MWCH4)*1000*(Relacion[i,0]/1000)/MWCH4 #Flujo másico de CH4 (mol/kgbm)
        
    for i in range (sz1):
        kggas_h[i,0]= (mol_kgbm[i,0]*mcb_daf*MWCO2)/1000 #Flujo másico de CO2 (kg/h) 
        kggas_h[i,1]= (mol_kgbm[i,1]*mcb_daf*MWCO)/1000 #Flujo másico de CO (kg/h) 
        kggas_h[i,2]= (mol_kgbm[i,2]*mcb_daf*MWO2)/1000 #Flujo másico de O2 (kg/h) 
        kggas_h[i,3]= (mol_kgbm[i,3]*mcb_daf*MWN2)/1000 #Flujo másico de N2 (kg/h) 
        kggas_h[i,4]= (mol_kgbm[i,4]*mcb_daf*MWNO)/1000 #Flujo másico de NO (kg/h) 
        kggas_h[i,5]= (mol_kgbm[i,5]*mcb_daf*MWNO2)/1000 #Flujo másico de NO2 (kg/h) 
        kggas_h[i,6]= (mol_kgbm[i,6]*mcb_daf*MWCH4)/1000 #Flujo másico de CH4 (kg/h) 
    
    for i in range (sz1):
        kmol_h[i,0]=  kggas_h[i,0]/MWgas[i,0] #Flujo molar CO2 (kmol/h)
        kmol_h[i,1]=  kggas_h[i,1]/MWgas[i,0] #Flujo molar CO (kmol/h)
        kmol_h[i,2]=  kggas_h[i,2]/MWgas[i,0] #Flujo molar O2 (kmol/h)
        kmol_h[i,3]=  kggas_h[i,3]/MWgas[i,0] #Flujo molar N2 (kmol/h)
        kmol_h[i,4]=  kggas_h[i,4]/MWgas[i,0] #Flujo molar NO (kmol/h)
        kmol_h[i,5]=  kggas_h[i,5]/MWgas[i,0] #Flujo molar NO2 (kmol/h)
        kmol_h[i,6]=  kggas_h[i,6]/MWgas[i,0] #Flujo molar CH4 (kmol/h)
        
        
        
    """4.1.2 Balance de Hidrogeno  """
    for i in range (sz1):
        YHgas[i,0]=(mcb_daf*YHdaf)/ Mgas[i,0] #Fracción de Hidrógeno del gas mol/kggas
    for i in range (sz1):
        RelacionH[i,0]=  YHgas[i,0]*Relacion[i,0] #Relación de Hidrógeno molH/kgbm
    for i in range (sz1):
        YH2Ogas[i,0]=  RelacionH[i,0]/2 #Fracción de Agua en el gas mol/kgbm 
    for i in range (sz1):
        mH2O[i,0]=(mcb_daf* YH2Ogas[i,0]*MWH2O)/1000 #Masa de Agua kg/h
                    
    """4.1.3 Balance de Oxigeno"""
    
    for i in range (sz1):
        YOair[i,0]=((((2*mol_kgbm[i,0])+mol_kgbm[i,1]+(2*mol_kgbm[i,2])+(2*mol_kgbm[i,5]))+YH2Ogas[i,0])-YOdaf)/2 #Fracción de Oxigeno en el gas mol/kgbm              
    for i in range (sz1):
        Ctdair[i,0]=YOair[i,0]+nAlpha*YOair[i,0] #Cantidad de aire mol/kgbm
    for i in range (sz1):
        molair[i,0]= Ctdair[i,0]*mcb_daf #Moles de Aire mol/h
    for i in range (sz1):
        Mair[i,0]=(molair[i,0]*MWair)/1000 #Masa de Aire kg/h
               
                    
    """4.1.3 Balance de Nitrogeno"""
    for i in range (sz1):
        YN2gas[i,0]=(YNdaf+YOair[i,0]*2*nAlpha-(2*mol_kgbm[i,0]))/2 #Fracción de Nitrogeno en el gas mol/kgbm
                    
    
    """SECCIÓN 5:Balance de Energia del flujo del gas """ #################################################################
    
    SZ_T=N.size(T1)
    Tsat=170
    
    Tref=25+273.15
    Rmol=8.3144
    
    #Matrices
    
    coef_fgdb=N.zeros((sz1,8)) #Coeficientes de cada especie #molsp/molgas en base seca
    coef_fgwb=N.zeros((sz1,8)) #Coeficientes de cada especie #molsp/molgas en base humeda
    n_spdb=N.zeros((sz1,8)) #Flujo molar de la especie en base  seca kmol/h
    n_spwb=N.zeros((sz1,8)) #Flujo molar de la especie en base  humeda kmol/h
    n_fgdb=N.zeros((sz1,1)) #Flujo molar del gas en base seca kmol/h
    n_fgwb=N.zeros((sz1,8)) #Flujo molar del gas en base humeda kmol/h
    nair=N.zeros((sz1,1)) #Flujo molar del aire en base humeda kmol/h
    nH2Oa=N.zeros((sz1,1)) #Flujo molar del agua kmol/h
    
    
    for i in range (sz1):
        n_fgdb[i,0]= Mgas[i,0]/MWgas[i,0] #Flujo molar del gas en base seca kmol/h
    for i in range (sz1):
        n_spdb[i,0]= n_fgdb[i,0]*fgc_CO2[i] #Flujo molar de CO2 kmol/h
        n_spdb[i,1]=n_fgdb[i,0]*fgc_CO[i] #Flujo molar de CO kmol/h
        n_spdb[i,2]=n_fgdb[i,0]*fgc_O2[i] #Flujo molar de O2 kmol/h
        n_spdb[i,3]=n_fgdb[i,0]*fgc_N2[i] #Flujo molar de N2 kmol/h
        n_spdb[i,4]=n_fgdb[i,0]*fgc_NO[i] #Flujo molar de NO kmol/h
        n_spdb[i,5]=n_fgdb[i,0]*fgc_NO2[i] #Flujo molar de NO2 kmol/h
        n_spdb[i,6]=n_fgdb[i,0]*fgc_CH4[i] #Flujo molar de CH4 kmol/h
        n_spdb[i,7]= YH2Ogas[i,0]*mcb_daf/1000 #Flujo molar de H2O formada kmol/h
    
        
    for i in range (sz1):
        coef_fgdb[i,0]= n_spdb[i,0]/n_fgdb[i,0] #Coeficientes molares de CO2 molCO2/molgas
        coef_fgdb[i,1]= n_spdb[i,1]/n_fgdb[i,0]  #Coeficientes molares de CO molCO/molgas
        coef_fgdb[i,2]= n_spdb[i,2]/n_fgdb[i,0]  #Coeficientes molares de O2 molO2/molgas
        coef_fgdb[i,3]= n_spdb[i,3]/n_fgdb[i,0]  #Coeficientes molares de N2 molN2/molgas
        coef_fgdb[i,4]= n_spdb[i,4]/n_fgdb[i,0]  #Coeficientes molares de NO molNO/molgas
        coef_fgdb[i,5]= n_spdb[i,5]/n_fgdb[i,0]  #Coeficientes molares de NO2 molNO2/molgas
        coef_fgdb[i,6]= n_spdb[i,6]/n_fgdb[i,0]  #Coeficientes molares de CH4 molCH4/molgas
        coef_fgdb[i,7]= n_spdb[i,7]/n_fgdb[i,0]  #Coeficientes molares de H2O molH2O/molgas
        
    for i in range (sz1):
        nair[i,0]=molair[i,0]/1000
        
    WA_air=(((0.622*Pvap)/(Patm-Pvap))*MWair)/MWH2O #Humedad absoluta del aire (kmolH2O/kmol aire seco)
    nw_cb=(mcb_wb-mcb_db)/MWH2O
    
    for i in range (sz1):
        nH2Oa[i,0]= nair[i,0]*WA_air #Agua para el aire (kmol/h)
        
    for i in range (sz1):
        n_spwb[i,0]= n_spdb[i,0] #Flujo molar de CO2 kmol/h
        n_spwb[i,1]= n_spdb[i,1] #Flujo molar de CO kmol/h
        n_spwb[i,2]= n_spdb[i,2] #Flujo molar de O2 kmol/h
        n_spwb[i,3]= n_spdb[i,3] #Flujo molar de N2 kmol/h
        n_spwb[i,4]= n_spdb[i,4] #Flujo molar de NO kmol/h
        n_spwb[i,5]= n_spdb[i,5] #Flujo molar de NO2 kmol/h
        n_spwb[i,6]= n_spdb[i,6]  #Flujo molar de CH4 kmol/h
        n_spwb[i,7]= n_spdb[i,7]+nH2Oa[i,0]+nw_cb  #Flujo molar de H2O formada kmol/h
        
    
    
    for i in range (sz1):
        n_fgwb[i,0]=  n_spwb[i,0]+n_spwb[i,1]+n_spwb[i,2]+n_spwb[i,3]+n_spwb[i,4]+n_spwb[i,5]+n_spwb[i,6]
    
    for i in range (sz1):
        coef_fgwb[i,0]= n_spwb[i,0]/n_fgwb[i,0] #Coeficientes molares de CO2 molCO2/molgas
        coef_fgwb[i,1]= n_spwb[i,1]/n_fgwb[i,0]  #Coeficientes molares de CO molCO/molgas
        coef_fgwb[i,2]= n_spwb[i,2]/n_fgwb[i,0]  #Coeficientes molares de O2 molO2/molgas
        coef_fgwb[i,3]= n_spwb[i,3]/n_fgwb[i,0]  #Coeficientes molares de N2 molN2/molgas
        coef_fgwb[i,4]= n_spwb[i,4]/n_fgwb[i,0]  #Coeficientes molares de NO molNO/molgas
        coef_fgwb[i,5]= n_spwb[i,5]/n_fgwb[i,0]  #Coeficientes molares de NO2 molNO2/molgas
        coef_fgwb[i,6]= n_spwb[i,6]/n_fgwb[i,0]  #Coeficientes molares de CH4 molCH4/molgas
        coef_fgwb[i,7]= n_spwb[i,7]/n_fgwb[i,0]  #Coeficientes molares de H2O molH2O/molgas
        
        
    """5.1 Exergias quimicas"""
    
    eqSP=N.zeros((sz1,8))
    
    for i in range (sz1):
        eqSP[i,0]=((coef_fgwb[i,0]*e_CO2)+Rmol*Tref*coef_fgwb[i,0]*(m.log(coef_fgwb[i,0]))) #Exergia Quimica CO2 KJ/kmol
        eqSP[i,1]=((coef_fgwb[i,1]*e_CO)+Rmol*Tref*coef_fgwb[i,1]*(m.log(coef_fgwb[i,1]))) #Exergia Quimica CO KJ/kmol
        eqSP[i,2]=((coef_fgwb[i,2]*e_O2)+Rmol*Tref*coef_fgwb[i,2]*(m.log(coef_fgwb[i,2]))) #Exergia Quimica O2 KJ/kmol
        eqSP[i,3]=((coef_fgwb[i,3]*e_N2)+Rmol*Tref*coef_fgwb[i,3]*(m.log(coef_fgwb[i,3]))) #Exergia Quimica N2 KJ/kmol
        eqSP[i,4]=((coef_fgwb[i,4]*e_NO)+Rmol*Tref*coef_fgwb[i,4]*((coef_fgwb[i,4]))) #Exergia Quimica NO KJ/kmol
        eqSP[i,5]=((coef_fgwb[i,5]*e_NO2)+Rmol*Tref*coef_fgwb[i,5]*((coef_fgwb[i,5]))) #Exergia Quimica NO2 KJ/kmol
        eqSP[i,6]=((coef_fgwb[i,6]*e_CH4)+Rmol*Tref*coef_fgwb[i,6]*((coef_fgwb[i,6]))) #Exergia Quimica CH4 KJ/kmol
        eqSP[i,7]=((coef_fgwb[i,7]*e_H2Og)+Rmol*Tref*coef_fgwb[i,7]*(m.log(coef_fgwb[i,7]))) #Exergia Quimica H2O KJ/kmol
        
    
    eq_fg= eqSP[:,0]+eqSP[:,1]+eqSP[:,2]+eqSP[:,3]+eqSP[:,4]+eqSP[:,5]+eqSP[:,6]+eqSP[:,7]
    
    # [SCO2, SCO, SO2, SN2, SNO, SNO2, SCH4, SH2O]=S.Ssp_fun(T)
    
    
    "POTENCIA DE CADA ESPECIE KJ/kmol"
    
    
    T = N.c_[T1, T2, T3, T4, T5, T6]
    Tref=N.ones((60,6))*298.15
    
    [S1]=S.Ssp_fun(T) #Entropia en funcion de las temmperaturas
    [S2]=S.Ssp_fun(Tref) #Entropia en funcion de las temmperatura de referencia
    
    [H1]=H.Hsp_fun(T) #Entropia en funcion de las temmperaturas
    [H2]=H.Hsp_fun(Tref)
    
    Hco2=H1[0,:,:]-H2[0,:,:] #Entalpia de CO2 (kj/mol)
    Hco=H1[1,:,:]-H2[1,:,:] #Entalpia de CO (kj/mol)
    Ho2=H1[2,:,:]-H2[2,:,:] #Entalpia de O2 (kj/mol)
    Hn2=H1[3,:,:]-H2[3,:,:] #Entalpia de N2 (kj/mol)
    Hno=H1[4,:,:]-H2[4,:,:] #Entalpia de NO (kj/mol)
    Hno2=H1[5,:,:]-H2[5,:,:] #Entalpia de NO2 (kj/mol)
    Hch4=H1[6,:,:]-H2[6,:,:]#Entalpia de CH4 (kj/mol)
    Hh2o=H1[7,:,:]-H2[7,:,:] #Entalpia de H2O (kj/mol)
    
    Sco2=S1[0,:,:]-S2[0,:,:] #Entropia de CO2 (J/ K° mol)
    Sco=S1[1,:,:]-S2[1,:,:] #Entropia de CO (J/ K° mol)
    So2=S1[2,:,:]-S2[2,:,:] #Entropia de CO2 (J/ K° mol)
    Sn2=S1[3,:,:]-S2[3,:,:] #Entropia de N2 (J/ K° mol)
    Sno=S1[4,:,:]-S2[4,:,:] #Entropia de NO (J/ K° mol)
    Sno2=S1[5,:,:]-S2[5,:,:] #Entropia de NO2 (J/ K° mol)
    Sch4=S1[6,:,:]-S2[6,:,:] #Entropia de CH4 (J/ K° mol)
    Sh2o=S1[7,:,:]-S2[7,:,:] #Entropia de H2O (J/ K° mol)
    
    QCO2=(n_fgwb[i:,0]*coef_fgwb[i:,0]*Hco2)/3600 #Potencia térmica de CO2 (KJ/kmol)
    QCO=(n_fgwb[i:,0]*coef_fgwb[i:,1]*Hco)/3600 #Potencia térmica de CO (KJ/kmol)
    QO2=(n_fgwb[i:,0]*coef_fgwb[i:,2]*Ho2)/3600 #Potencia térmica de O2 (KJ/kmol)
    QN2=(n_fgwb[i:,0]*coef_fgwb[i:,3]*Hn2)/3600 #Potencia térmica de N2 (KJ/kmol)
    QNO=(n_fgwb[i:,0]*coef_fgwb[i:,4]*Hno)/3600 #Potencia térmica de NO (KJ/kmol)
    QNO2=(n_fgwb[i:,0]*coef_fgwb[i:,5]*Hno2)/3600 #Potencia térmica de NO2 (KJ/kmol)
    QCH4=(n_fgwb[i:,0]*coef_fgwb[i:,6]*Hch4)/3600 #Potencia térmica de CH4 (KJ/kmol)
    QH2O=(n_fgwb[i:,0]*coef_fgwb[i:,7]*Hh2o)/3600 #Potencia térmica de H2O  (KJ/kmol)
    Qfg=QCO2+QCO+QO2+QN2+QNO+QNO2+QCH4 #Potencia térmica del gas (KJ/kmol))
    
    
    
        
    """ExergÃ­a FÃ­sica especifica para mezcla de gases kJ/kmolK"""
    
    cphCO2=Hco2/(T-Tref) #Capacidad calorifica de entalpia del CO2 (kJ/kmol K°)
    cphCO=Hco/(T-Tref) #Capacidad calorifica de entalpia del CO (kJ/kmol K°)
    cphO2=Ho2/(T-Tref) #Capacidad calorifica de entalpia del O2 (kJ/kmol K°)
    cphN2=Hn2/(T-Tref) #Capacidad calorifica de entalpia del N2 (kJ/kmol K°)
    cphNO=Hno/(T-Tref) #Capacidad calorifica de entalpia del NO (kJ/kmol K°)
    cphNO2=Hno2/(T-Tref) #Capacidad calorifica de entalpia del NO2 (kJ/kmol K°)
    cphCH4=Hch4/(T-Tref) #Capacidad calorifica de entalpia deL CH4 (kJ/kmol K°)
    cphH2O=Hh2o/(T-Tref) #Capacidad calorifica de entalpia del H2O (kJ/kmol K°)
    
    
    cpsCO2=Sco2/N.log(T/Tref) #Capacidad calorifica de entropia del CO2 (kJ/kmol K°)
    cpsCO=Sco/N.log(T/Tref) #Capacidad calorifica de entropia del CO (kJ/kmol K°)
    cpsO2=So2/N.log(T/Tref) #Capacidad calorifica de entropia del O2 (kJ/kmol K°)
    cpsN2=Sn2/N.log(T/Tref) #Capacidad calorifica de entropia del N2 (kJ/kmol K°)
    cpsNO=Sno/N.log(T/Tref) #Capacidad calorifica de entropia del NO (kJ/kmol K°)
    cpsNO2=Sno2/N.log(T/Tref) #Capacidad calorifica de entropia del NO2 (kJ/kmol K°)
    cpsCH4=Sch4/N.log(T/Tref) #Capacidad calorifica de entropia del CH4 (kJ/kmol K°)
    cpsH2O=Sh2o/N.log(T/Tref) #Capacidad calorifica de entropia del H2O (kJ/kmol K°)
    
    efCO2=coef_fgwb[i,0]*((cphCO2*(T-Tref)-Tref*cpsCO2*N.log(T/Tref))) #Exergia  especifica fisica del CO2 (kJ/kg)
    efCO=coef_fgwb[i,1]*(cphCO*(T-Tref)-Tref*cpsCO*N.log(T/Tref)) #Exergia  especifica fisica del CO (kJ/kg)
    efO2=coef_fgwb[i,2]*(cphO2*(T-Tref)-Tref*cpsO2*N.log(T/Tref)) #Exergia  especifica fisica del O2 (kJ/kg)
    efN2=coef_fgwb[i,3]*(cphN2*(T-Tref)-Tref*cpsN2*N.log(T/Tref)) #Exergia  especifica fisica del N2 (kJ/kg)
    efNO=coef_fgwb[i,4]*(cphNO*(T-Tref)-Tref*cpsNO*N.log(T/Tref)) #Exergia  especifica fisica del NO (kJ/kg)
    efNO2=coef_fgwb[i,5]*(cphNO2*(T-Tref)-Tref*cpsNO2*N.log(T/Tref)) #Exergia  especifica fisica del NO2(kJ/kg)
    efCH4=coef_fgwb[i,6]*(cphCH4*(T-Tref)-Tref*cpsCH4*N.log(T/Tref)) #Exergia  especifica fisica del CH4 (kJ/kg)
    efH2O=coef_fgwb[i,7]*(cphH2O*(T-Tref)-Tref*cpsH2O*N.log(T/Tref)) #Exergia  especifica fisica del H2O (kJ/kg)
    
    
    
    """6.estadisticas"""
    #Balance de Exergia
    M_efCO2=(efCO2.mean(axis=0)) #Media de exergia especifica fisica del CO2 (kJ/kg)
    M_efCO=(efCO.mean(axis=0)) #Media de exergia especifica fisica del CO (kJ/kg)
    M_efO2=(efO2.mean(axis=0)) #Media de exergia especifica fisica del O2 (kJ/kg)
    M_efN2=(efN2.mean(axis=0)) #Media de exergia especifica fisica del N2 (kJ/kg)
    M_efNO=(efCO2.mean(axis=0)) #Media de exergia especifica fisica del NO (kJ/kg)
    M_efNO2=(efNO2.mean(axis=0)) #Media de exergia especifica fisica del NO2 (kJ/kg)
    M_efCH4=(efCH4.mean(axis=0)) #Media de exergia especifica fisica del CH4 (kJ/kg)
    M_efH2O=(efH2O.mean(axis=0)) #Media de exergia especifica fisica del H2O (kJ/kg)
    M_eqSP=(eqSP.mean(axis=0)) #Media de exergia especifica quimica de la especie  (kJ/kg)
    M_eqfg=(eq_fg.mean(axis=0)) #Media de exergia especifica quimica del gas  (kJ/kg)
    
    
    
    
    
    #Desviación estandar
    
    sd_efCO2=(efCO2.std(axis=0)) #desviación estandar de exergia especifica fisica del CO2 (kJ/kg)
    sd_efCO=(efCO.std(axis=0)) #desviación estandar de exergia especifica fisica del CO (kJ/kg)
    sd_efO2=(efO2.std(axis=0)) #desviación estandar de exergia especifica fisica del O2 (kJ/kg)
    sd_efN2=(efN2.std(axis=0)) #desviación estandar de exergia especifica fisica del N2 (kJ/kg)
    sd_efNO=(efCO2.std(axis=0))#desviación estandar de exergia especifica fisica del NO (kJ/kg)
    sd_efNO2=(efNO2.std(axis=0)) #desviación estandar de exergia especifica fisica del NO2 (kJ/kg)
    sd_efCH4=(efCH4.std(axis=0)) #desviación estandar de exergia especifica fisica del CH4 (kJ/kg)
    sd_efH2O=(efH2O.std(axis=0)) #desviación estandar de exergia especifica fisica del H2O (kJ/kg)
    sd_eqSP=(eqSP.std(axis=0)) #desviación estandar de exergia especifica quimica de la especie (kJ/kg)
    
    sdQCO2=(QCO2.std(axis=0)) #desviacion estandar  de potencia CO2 (KJ/kmol)
    sdQCO=(QCO.std(axis=0)) #desviacion estandar  de potencia CO (KJ/kmol)
    sdQO2=(QO2.std(axis=0)) #desviacion estandar  de potencia O2 (KJ/kmol)
    sdQN2=(QN2.std(axis=0)) #desviacion estandar  de potencia N2 (KJ/kmol)
    sdQNO=(QNO.std(axis=0)) #desviacion estandar  de potencia NO (KJ/kmol)
    sdQNO2=(QNO2.std(axis=0)) #desviacion estandar  de potencia NO2 (KJ/kmol)
    sdQCH4=(QCH4.std(axis=0)) #desviacion estandar  de potencia CH4 (KJ/kmol)
    sdQH2O=(QH2O.std(axis=0)) #desviacion estandar  de potencia H2O (KJ/kmol)
    sdeqSP=(eqSP.std(axis=0)) #desviacion de exergia especifica quimica de la especie (KJ/kg)
    #Balance masa del gas
    sd_Mgas=(Mgas.std(axis=0)) #desviacion de masa de gas (Kg/h)
    sd_MWgas=(MWgas.std(axis=0)) #desviacion estandar del peso molecular del gas (g /mol)
    sd_nfg=(n_fgdb.std(axis=0)) #desviacion estandar Flujo molar del gas en base seca (kmol/h)
    #Propiedades termicas del gas
    sd_fgT=(T.std(axis=0)) #Desviación estandar de Temperaturas (°k)
    sd_Qfg=(Qfg.std(axis=0)) #Desviacion estandar de potencia del gas (kJ/kmol)
    #Balance de masa por combustión de especie:
    sd_Cfgdb=(coef_fgdb.std(axis=0)) #Desviación estandar de coeficientes del gas en base seca  (mol/mol)  
    sd_Cfgwb=(coef_fgwb.std(axis=0)) #Desviación estandar de coeficientes del gas en base seca  (mol/mol)  
    #Aire:
    sd_molair=(molair.std(axis=0)) #Desviación estandar moles de aire (mol/h)
    M_molair=(molair.mean(axis=0))#Media moles de aire (mol/h)
    M_Mair=(Mair.mean(axis=0)) #Media de masa de aire estanda moles de aire (kg/h)
    
    sd_Mair=(Mair.std(axis=0)) #Desviación estanda masa de aire (kg/h)
    
    
    #Balance de masa
    
    #Gas de Combustión
    
    M_Mgas=(Mgas.mean(axis=0)) #Media de Masa de gas (kg/h)
    M_MWgas=(MWgas.mean(axis=0)) #Media del peso molecular del gas (g/mol)
    M_YHgas=(YHgas.mean(axis=0))#Media de fraccion de hidrogeno en el gas -(mol /kg gas)
    sd_Mgas=(Mgas.std(axis=0)) #Desviación estandar de Masa de gas (kg/h)
    sd_MWgas=(MWgas.std(axis=0)) #Desviacion estandar del peso molecular del gas (g/mol)
    sd_YHgas=(YHgas.std(axis=0))#Desviación estandar fraccion de hidrogeno en el gas -(mol /kg gas)
    
    
    
    M_frmdb=(n_spdb.mean(axis=0)) #Media flujo molar delgas en base seca (kmol/h)
    M_frmwb=(n_spwb.mean(axis=0)) #Media Flujo molar delgas en base humeda (kmol/h)
    M_fml=(kmol_h.mean(axis=0)) #Media del flujo molar (kmol/h)
    M_fms=(kggas_h.mean(axis=0)) #Media del flujo másico (kggas/h)
    
    sd_frmdb=(n_spdb.std(axis=0)) #Desviación estandar Flujo molar delgas en base seca (kmol/h)
    sd_frmwb=(n_spwb.std(axis=0)) #Desviación estandar Flujo molar delgas en base humeda (kmol/h)
    sd_fml=(kmol_h.std(axis=0)) #Desviacion estandar flujo molar (kmol/h)
    sd_fms=(kggas_h.std(axis=0)) #Desviacion estandar flujo másico (kggas/h)
    
    
    #Balance de masa por especie
    MQCO2=(QCO2.mean(axis=0)) #Media de potencia de CO2 (KJ/kmol)
    MQCO=(QCO.mean(axis=0)) #Media de potencia de CO (KJ/kmol)
    MQO2=(QO2.mean(axis=0)) #Media de potencia de O2 (KJ/kmol)
    MQN2=(QN2.mean(axis=0)) #Media de potencia de N2 (KJ/kmol)
    MQNO=(QNO.mean(axis=0)) #Media de potencia de NO (KJ/kmol)
    MQNO2=(QNO2.mean(axis=0)) #Media de potencia de NO2 (KJ/kmol)
    MQCH4=(QCH4.mean(axis=0)) #Media de potencia de CH4 (KJ/kmol)
    MQH2O=(QH2O.mean(axis=0)) #Media de potencia de H2O (KJ/kmol)
    
    
    
    #Balance de energia en el gas
    MT1=(T1.mean(axis=0)) #Media de temperaturas
    MT2=(T2.mean(axis=0))
    MT3=(T3.mean(axis=0))
    MT4=(T4.mean(axis=0))
    MT5=(T5.mean(axis=0))
    MT6=(T6.mean(axis=0))
    sdT1=(T1.std(axis=0)) #Desviacion estandar de temperaturas 
    sdT2=(T2.std(axis=0))
    sdT3=(T3.std(axis=0))
    sdT4=(T4.std(axis=0))
    sdT5=(T5.std(axis=0))
    sdT6=(T6.std(axis=0))
    
    Q1=QCO2[:,0]+QCO[:,0]+QO2[:,0]+QN2[:,0]+QNO[:,0]+QNO2[:,0]+QCH4[:,0] #POTENCIA DEL GAS EN LAS DIFERENTES TEMPERATURAS
    Q2=QCO2[:,1]+QCO[:,1]+QO2[:,1]+QN2[:,1]+QNO[:,1]+QNO2[:,1]+QCH4[:,1]
    Q3=QCO2[:,2]+QCO[:,2]+QO2[:,2]+QN2[:,2]+QNO[:,2]+QNO2[:,2]+QCH4[:,2]
    Q4=QCO2[:,3]+QCO[:,3]+QO2[:,3]+QN2[:,3]+QNO[:,3]+QNO2[:,3]+QCH4[:,3]
    Q5=QCO2[:,4]+QCO[:,4]+QO2[:,4]+QN2[:,4]+QNO[:,4]+QNO2[:,4]+QCH4[:,4]
    Q6=QCO2[:,5]+QCO[:,5]+QO2[:,5]+QN2[:,5]+QNO[:,5]+QNO2[:,5]+QCH4[:,5]
    
    
    
    MQ1=(Q1.mean(axis=0)) #Media de potencia del gas  en diferentes temperaturas
    MQ2=(Q2.mean(axis=0))
    MQ3=(Q3.mean(axis=0))
    MQ4=(Q4.mean(axis=0))
    MQ5=(Q5.mean(axis=0))
    MQ6=(Q6.mean(axis=0))
    sdQ1=(Q1.std(axis=0))#Desviación estandar de potencia del gas  en diferentes temperaturas
    sdQ2=(Q2.std(axis=0))
    sdQ3=(Q3.std(axis=0))
    sdQ4=(Q4.std(axis=0))
    sdQ5=(Q5.std(axis=0))
    sdQ6=(Q6.std(axis=0))
    
    #Balance de Exergia
    
    Mex_sac=ex_Sac #Media de exergia de la sacarosa
    MEf_ae=Ef_ae #Media Exergia especifica  fisica de Agua evaporada (KJ/kg)
    Meq_ae=eq_ae #Media de Exergia quimica especifica de agua evaporada (KJ/Kmol)
    Mexq_asj=exq_asj #Media de flujo exergetico quimico de agua en el jugo KJ/Kg
    Mexq_sj=(exq_sj.mean(axis=0)) # Flujo Exergetico quimico especifica del jugo kJ/Kg
    Me_bs=e_bs  #Media Exergia especifica bagazo seco kJ/kg
    ME_bs=E_bs # Media Flujo de Exergi­a Bagazo de Caña
    
    ">>>>>>>>>>---------Hoja 1------------<<<<<<<<<<<<<"
        
    Etiquetas=['MASS BALANCE SUGARCANE JUICE', 'Variable',
               'Caña de Azucar', 'Bagazo de caña en el molino',
               'Jugo en el molino', 'Impurezas en el prelimpiador', 'Jugo Pre-limpio', 'Cachaza', 'Jugo limpio', 
               'NCS', 'Flujo másico total de agua evaporada', 'Extracción en el molino', 'Impurezas en el jugo Pre-limpio',
               'Cachaza']
    Unidades=['--', 'Unidad', 
              '(kg/h)', '(kg/h)', '(kg/h)', '(kg/h)', '(kg/h)', '(kg/h)', '(kg/h)', '(kg/h)', '(kg/h)', '(%)', '(%)', '(%)']
    Valores=['--', 'Valor', 
             m_cs, m_cb, ' ', m_ci,' ' , m_ch,' ', m_ncs,' ', ext, imp, chz]
    
    df1 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':Unidades,
                        'Col 3':Valores})
    
    Etiquetas=['BALANCE DE MASA Y ENERGIA MEDIANTE INTERCAMBIADOR', 'Intercambiador',
               'Jugo', 'Clarificadora', 'Evap1', 'Evap2', 'Evap3', 'Evap4', 'Evap5', 'Evap6', 'Evap7', 'Evap8', 'Concentradora']
    col1=list(mat[:,0])
    col1.insert(0, 'Jugo másico de jugo(kg/h)')
    col1.insert(0, '--')
    col2=list(mat[:,1])
    col2.insert(0, 'Agua Evaporada (kg/h)')
    col2.insert(0, '--')
    col3=list(Qs)
    col3.insert(0, 'Calor sensible (kW)')
    col3.insert(0, '--')
    col4=list(Ql)
    col4.insert(0, 'Calor latente(kW)')
    col4.insert(0, '--')
    col5=list(Qt)
    col5.insert(0, 'Calor latente(kW)')
    col5.insert(0, '--')
    
    df2 = pd.DataFrame({'Col 1': Etiquetas ,
                       'Col 2': col1 ,
                       'Col 3': col2,
                       'Col 4': col3,
                       'Col 5': col4,
                       'Col 6': col5
                       })
    
    Etiquetas=['BALANCE DE EXERGIA POR INTERCAMBIADOR', 'Intercambiador',
               'Jugo', 'Clarificadora', 'Evap1', 'Evap2', 'Evap3', 'Evap4', 'Evap5', 'Evap6', 'Evap7', 'Evap8', 'Concentradora']
    col1=list(exq_asj1)
    col1.insert(0, 'Exergia quimica especifica H2O(l)(kJ/kg)')
    col1.insert(0, '--')
    col2=list(exq_sj)
    col2.insert(0, 'Exergia fisica especifica Sj(kJ/kg)')
    col2.insert(0, '--')
    col3=list(ex_sj)
    col3.insert(0, 'Flujo exergetico Sj(kW)')
    col3.insert(0, '--')
    col4=list(ex_va)
    col4.insert(0, 'Flujo exergetico H2O(g)(kW)')
    col4.insert(0, '--')
    
    df3 = pd.DataFrame({'Col 1': Etiquetas ,
                       'Col 2': col1 ,
                       'Col 3': col2,
                       'Col 4': col3,
                       'Col 5': col4
                       })
    
    Hoja1 = pd.concat([df1, df2, df3])
    
    ">>>>>>>>>>---------Hoja 2------------<<<<<<<<<<<<<"
    
    Etiquetas=['Variable', 'Flujo másico de bagazo de caña en wb', 'Flujo másico de bagazo de caña en db',
               'Flujo másico de bagazo de caña en daf', 'Contenido de humedad', 'Valor calorifico neto', 
               'Potencia termica de entrada', 'Exergia especifica', 'Flujo exergetico']
    Unidades=['Unidad','(kg/h)','(kg/h)','(kg/h)','(% w)','(kJ/kg)','(kW)','(kJ/kg)','(kW)']
    Valores=['Valor', mcb_wb, mcb_db, mcb_daf, Xmw_cb, LHV, Qs_cb, e_bs, E_bs]
    
    Hoja2 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':Unidades,
                        'Col 3':Valores})
    Hoja2.to_excel('static/Salida.xlsx')
    
    ">>>>>>>>>>---------Hoja 3------------<<<<<<<<<<<<<"
    Etiquetas=['RESULTADOS: AIRE', 'Variable', 'Humedad absoluta del aire', 'Flujo molar estequiometrico del aire',
               'Flujo molar del aire', 'Flujo masico del aire real']
    Unidades=['--','Unidad','kmol H2O/kg air seco','(g/molaire)','(kmol/h)','(kg/h)']
    col1=['--','Mean',WA_air,M_Mair,M_molair,M_Mair]#Verificar Var
    col2=['--','sd','--','--',sd_molair,sd_Mair]#Verificar Var
    df1 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':Unidades,
                        'Col 3':col1,
                        'Col 4':col2})
    
    Etiquetas=['RESULTADO: GAS DE COMBUSTIÓN', 'Flujo masico del gas en daf', 'Peso molecular del gas de combustión (daf)', 'Flujo molar de los gases de combustión']
    Unidades=['--','(kg/h)','(kg/kmol)','(kmol/kgas)']
    col1=['--',M_Mgas,0,0] #Verificar Var
    df2 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':Unidades,
                        'Col 3':col1})
    
    Etiquetas=['Mass Balance', 'Variable', 'mol fraction daf (mol/mol)', 'molar flow in daf (kmol/h)', 'mass flow in daf (kg/h)', 'Emission Index (kg sp/kg NCS)']
    col1=['--','Mean CO2', M_frmdb[0], M_fml[0], M_fms[0], 0]
    col2=['--','Mean CO', M_frmdb[1], M_fml[1], M_fms[1], 0]
    col3=['--','Mean O2', M_frmdb[2], M_fml[2], M_fms[2], 0]
    col4=['--','Mean N2', M_frmdb[3], M_fml[3], M_fms[3], 0]
    col5=['--','Mean NO', M_frmdb[4], M_fml[4], M_fms[4], 0]
    col6=['--','Mean NO2', M_frmdb[5], M_fml[5], M_fms[5], 0]
    col7=['--','Mean CH4', M_frmdb[6], M_fml[6], M_fms[6], 0]
    col8=['--','Mean H2O', M_frmdb[6], M_fml[6], M_fms[6], 0]
    col9=['--','Sd CO2', sd_frmdb[0], sd_fml[0], sd_fms[0], 0]
    col10=['--','Sd CO2', sd_frmdb[1], sd_fml[1], sd_fms[1], 0]
    col11=['--','Sd CO', sd_frmdb[2], sd_fml[2], sd_fms[2], 0]
    col12=['--','Sd O2', sd_frmdb[3], sd_fml[3], sd_fms[3], 0]
    col13=['--','Sd N2', sd_frmdb[4], sd_fml[4], sd_fms[4], 0]
    col14=['--','Sd NO', sd_frmdb[5], sd_fml[5], sd_fms[5], 0]
    col15=['--','Sd NO2', sd_frmdb[6], sd_fml[6], sd_fms[6], 0]
    col16=['--','Sd CH4', sd_frmdb[6], sd_fml[6], sd_fms[6], 0]
    
    df3 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':col1,
                        'Col 3':col2,
                        'Col 4':col3,
                        'Col 5':col4,
                        'Col 6':col5,
                        'Col 7':col6,
                        'Col 8':col7,
                        'Col 9':col8,
                        'Col 10':col9,
                        'Col 11':col10,
                        'Col 12':col11,
                        'Col 13':col12,
                        'Col 14':col13,
                        'Col 15':col14,
                        'Col 16':col15,
                        'Col 17':col16
                        })
    
    Etiquetas=['ENERGY BALANCE IN DAF', 'Especie', 'CO2', 'CO', 'O2', 'N2', 'NO', 'NO2', 'CH4', 'H2O']
    
    ind=0
    col1=['--', 'Mean (kW)(1)', MQCO2[ind], MQCO[ind], MQO2[ind], MQN2[ind], MQNO[ind], MQNO2[ind], MQCH4[ind], MQH2O[ind]]
    ind=1
    col2=['--', 'Mean (kW)(2)', MQCO2[ind], MQCO[ind], MQO2[ind], MQN2[ind], MQNO[ind], MQNO2[ind], MQCH4[ind], MQH2O[ind]]
    ind=2
    col3=['--', 'Mean (kW)(3)', MQCO2[ind], MQCO[ind], MQO2[ind], MQN2[ind], MQNO[ind], MQNO2[ind], MQCH4[ind], MQH2O[ind]]
    ind=3
    col4=['--', 'Mean (kW)(4)', MQCO2[ind], MQCO[ind], MQO2[ind], MQN2[ind], MQNO[ind], MQNO2[ind], MQCH4[ind], MQH2O[ind]]
    ind=4
    col5=['--', 'Mean (kW)(5)', MQCO2[ind], MQCO[ind], MQO2[ind], MQN2[ind], MQNO[ind], MQNO2[ind], MQCH4[ind], MQH2O[ind]]
    ind=5
    col6=['--', 'Mean (kW)(6)', MQCO2[ind], MQCO[ind], MQO2[ind], MQN2[ind], MQNO[ind], MQNO2[ind], MQCH4[ind], MQH2O[ind]]
    ind=0
    col7=['--', 'Sd(1)', sdQCO2[ind], sdQCO[ind], sdQO2[ind], sdQN2[ind], sdQNO[ind], sdQNO2[ind], sdQCH4[ind], sdQH2O[ind]]
    ind=1
    col8=['--', 'Sd(2)', sdQCO2[ind], sdQCO[ind], sdQO2[ind], sdQN2[ind], sdQNO[ind], sdQNO2[ind], sdQCH4[ind], sdQH2O[ind]]
    ind=2
    col9=['--', 'Sd(3)', sdQCO2[ind], sdQCO[ind], sdQO2[ind], sdQN2[ind], sdQNO[ind], sdQNO2[ind], sdQCH4[ind], sdQH2O[ind]]
    ind=3
    col10=['--', 'Sd(4)', sdQCO2[ind], sdQCO[ind], sdQO2[ind], sdQN2[ind], sdQNO[ind], sdQNO2[ind], sdQCH4[ind], sdQH2O[ind]]
    ind=4
    col11=['--', 'Sd(5)', sdQCO2[ind], sdQCO[ind], sdQO2[ind], sdQN2[ind], sdQNO[ind], sdQNO2[ind], sdQCH4[ind], sdQH2O[ind]]
    ind=5
    col12=['--', 'Sd(6)', sdQCO2[ind], sdQCO[ind], sdQO2[ind], sdQN2[ind], sdQNO[ind], sdQNO2[ind], sdQCH4[ind], sdQH2O[ind]]
    df4 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':col1,
                        'Col 3':col2,
                        'Col 4':col3,
                        'Col 5':col4,
                        'Col 6':col5,
                        'Col 7':col6,
                        'Col 8':col7,
                        'Col 9':col8,
                        'Col 10':col9,
                        'Col 11':col10,
                        'Col 12':col11,
                        'Col 13':col12
                        })
    
    Etiquetas=['ENERGY BALANCE IN FLUE GAS','Flue Gas','Temperatura (°C)','Potencia termica en  daf(kW)']
    col1=['--','Mean(1)', MT1, MQ1]
    col2=['--','Mean(2)', MT2, MQ2]
    col3=['--','Mean(3)', MT3, MQ3]
    col4=['--','Mean(4)', MT4, MQ4]
    col5=['--','Mean(5)', MT5, MQ5]
    col6=['--','Mean(6)', MT6, MQ6]
    col7=['--','sd(1)', sdT1, sdQ1]
    col8=['--','sd(2)', sdT2, sdQ2]
    col9=['--','sd(3)', sdT3, sdQ3]
    col10=['--','sd(4)', sdT4, sdQ4]
    col11=['--','sd(5)', sdT5, sdQ5]
    col12=['--','sd(6)', sdT6, sdQ6]
    df5 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':col1,
                        'Col 3':col2,
                        'Col 4':col3,
                        'Col 5':col4,
                        'Col 6':col5,
                        'Col 7':col6,
                        'Col 8':col7,
                        'Col 9':col8,
                        'Col 10':col9,
                        'Col 11':col10,
                        'Col 12':col11,
                        'Col 13':col12
                        })
    Hoja3 = pd.concat([df1, df2, df3, df4, df5])
    
    ">>>>>>>>>>---------Hoja 4------------<<<<<<<<<<<<<"
    Etiquetas=['RESULTS: EXERGY SUGARCANE JUICE', 'Variable','Exergia quimica especifica de la sacarosa','Exergia fisica especifica de agua evaporada',
               'Exergia quimica especifica de agua evaporada0','Exergy Flow Evaporated Water','Exergy Flow NCS',
               'RESULTS: EXERGY CANE BAGASSE', 'Exergía específica del bagazo seco', 'Flujo de exergía Bagazo de caña',
               'RESULTS: CHEMICAL EXERGY FLUE GAS', 'Specific Chemical Exergy Flue Gas',
               'EXERGY BALANCE IN COMBUSTION CHAMBER','Exergy Flow Cane Bagasse','Flow Exergy FlueGas','Flow exergy destroyed','Exergy Condensed','Exergy Steam',
               'EXERGY BALANCE IN EVAPORATION','Flow Exergy Flue Gas Inlet','Exergy Flow SJ','Flow Exergy Flue Gas Outlet','Exergy Flow Evaporated Water',
               'Exergy Flow NCS','Flow exergy destroyed','Exergy Steam']
    Unidades=['--','Unidad','(kJ/kg)','(kJ/kg)','(kJ/kg)','kW','kW',
              '--','(kJ/kg)','(kW)',
              '--', '(kJ/kmol)',
              '--','(kW)','(kW)','(kW)','(kW)','(kW)',
              '--','(kW)','kW','(kW)','(kW)','(kW)','(kW)','(kW)']
    Medias=['--','MeanValor',Mex_sac,Mex_sac,Meq_ae,Mexq_asj,Mexq_sj,
              '--',0,0,
              '--', 0,
              '--',0,0,0,0,0,
              '--',0,0,0,0,0,0,0]
    
    sd=['--','sd',0,0,0,0,0,
              '--',0,0,
              '--', 0,
              '--',0,0,0,0,0,
              '--',0,0,0,0,0,0,0]
    
    Hoja4 = pd.DataFrame({'Col 1':Etiquetas,
                        'Col 2':Unidades,
                        'Col 3':Medias,
                        'Col 4':sd})
    
    with pd.ExcelWriter('static/Salida.xlsx') as writer:  
        Hoja1.to_excel(writer, sheet_name='Jugo')
        Hoja2.to_excel(writer, sheet_name='Gas')
        Hoja3.to_excel(writer, sheet_name='Gas de combustion')
        Hoja4.to_excel(writer, sheet_name='Exergia')
