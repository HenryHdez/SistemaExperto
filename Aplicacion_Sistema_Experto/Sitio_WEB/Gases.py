# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:52:53 2020

@author: hahernandez
"""
import math
import numpy as np
import pandas as pd
import Diseno_inicial
import Pailas
import Costos_funcionamiento
import Modulo1
import Modulo2
import Modulo21
import Modulo4

def diccionarios_sis(D1,D2):
    global Diccionario_Entr
    global Diccionario_Pailas
    Diccionario_Entr=D1
    Diccionario_Pailas=D2
    
def Calcular_parrillas(Area_Calculada,Capacidad_Hornilla,i,Calor_suministrado,Tipo_ladrillo,Temperatura_ambiente,Temperatura_Flama_Ad):
    """>>>----------Algoritmo para el calculo de las parrillas-----------<<<<<<<<<"""
    Ancho_seccion=0.155	
    Longitudes=[0.75, 1, 1.25, 1.5]
    if(Capacidad_Hornilla<40):
        Longitud_Seccion=0.5
    else:
        Longitud_Seccion=Longitudes[i]        
    Temp=math.ceil(Area_Calculada/(Ancho_seccion*Longitud_Seccion))
    
    if (Temp>7):
        Temp2=math.ceil(Temp/2)
    else:
        Temp2=Temp
        
    if (Temp<7):
        Temp3=1
    else:
        Temp3=math.ceil(Temp/Temp2)  
        
    Temp4=Temp2*Ancho_seccion
    if(Temp4<0.62):
        Temp4=5
    
    Numero_secciones_An1=Temp
    Numero_secciones_An2=Temp2  
    Numero_secciones_Lon=Temp3
    Secciones_totales=Temp2*Temp3
    Ancho_parrilla=Temp4
    Area_Calculada=Longitud_Seccion*Temp3*Temp4
    
    if(Capacidad_Hornilla<40):
        Area_Calculada=(Longitud_Seccion*Numero_secciones_Lon)*(Ancho_seccion*Numero_secciones_An2)  

    #>>>>>>-------------Aqui se pone la geometría de la camara para hallar el vólumen
    Volumen_Calculado=Calor_suministrado/450 #Tener presente
    Ancho_camara=Ancho_parrilla+0.3
    Longitud_Camara=(Longitud_Seccion*Numero_secciones_Lon)+0.3
    Altura_camara=Volumen_Calculado/(Ancho_camara*Longitud_Camara)
    
    #Más larga que ancha
    if(Longitud_Camara<Ancho_camara):
        Ancho_camara=Longitud_Camara
        Longitud_Camara=Ancho_camara
    
    #Calculo de la pared con respecto a los ladrillos
    Area_Cam=2*((Ancho_camara*Longitud_Camara)+(Ancho_camara*Altura_camara)+(Longitud_Camara*Altura_camara))
    Coef_Conduct_Termica=0
    if(Tipo_ladrillo=='Refractario'):
        Coef_Conduct_Termica=0.29
    else:
        if(Tipo_ladrillo=='Semirefractario'):
            Coef_Conduct_Termica=0.45
        else:
            Coef_Conduct_Termica=0.9
    Esp_Camara=0.12
    Aux=-264.44+(1.03*Temperatura_Flama_Ad)
    Q_Perd_Camara=(Coef_Conduct_Termica*Area_Cam)*((Aux-Temperatura_ambiente)/Esp_Camara)
    
    Costos_funcionamiento.cantidad_parr(Secciones_totales)
    Pailas.Dimensiones_parrilla(Ancho_seccion*1000, Longitud_Seccion*1000, Secciones_totales, Ancho_camara*1000, Longitud_Camara*1000, Altura_camara*1000)
    return Q_Perd_Camara

#Función para calcular las propiedades de los gases           
def Propiedades(Calor_transferido, AF, PF, AL):
    #Valores iniciales
    global Diccionario_Entr
    global Diccionario_Pailas
    
    Datos_simulacion=[]
    
    Q_Cedido=Q_Cedido_gas(Calor_transferido)
    Masa_Bagazo=float(Diccionario_Entr['Bagazo suministrado'])
    Cantidad_Pailas=int(Diccionario_Pailas['Etapas'])   
    Humedad_bagazo=float(Diccionario_Entr['Humedad del bagazo'])
    Exceso_aire=float(Diccionario_Entr['Exceso de aire'])
    Temperatura_ambiente=(float(Diccionario_Entr['CSS panela'])*100.0)+273.0
    Eficiencia_Combustion=0.95 #Lo esperado en la combustión    
    Humedad_aire=0.001
    #Composición del bagazo en %
    Carbono=0.470
    Hidrogeno=0.065
    Oxigeno=0.440
    Escorias=0.025
    Masa_Bagazo_Seco=float(Diccionario_Entr['Bagazo seco'])#Masa_Bagazo*(1-(Humedad_bagazo))
    #Masa molar    
    C=12.011
    H2=2.016
    CO2=44.010
    CO=28.010
    H2O=18.015
    O2=31.999
    N2=28.013
    #Masa molar (Entrada)
    C_bagazo=Masa_Bagazo_Seco*Carbono/C
    H2_bagazo=Masa_Bagazo_Seco*Hidrogeno/H2
    O2_bagazo=Masa_Bagazo_Seco*Oxigeno/O2
    H2O_bagazo=Humedad_bagazo*Masa_Bagazo/H2O
    O2_req=(C_bagazo+(H2_bagazo/2))-O2_bagazo
    O2_sum=O2_req*Exceso_aire
    N2_sum=O2_sum*3.76
    H2O_aire=(((N2_sum*N2)+(O2_sum*O2))*Humedad_aire)/H2O
       
    #Masa molar(Salida)
    CO2_producidos=Eficiencia_Combustion*C_bagazo*1000.0
    CO_producidos=(C_bagazo*1000)-CO2_producidos
    H2O_producidos=H2_bagazo*1000.0
    H2O_Totales=H2O_producidos+((H2O_aire+H2O_bagazo)*1000.0)
    O2_producidos=((O2_sum-O2_req)*1000.0)+(CO_producidos/2)
    N2_producidos=N2_sum*1000.0

    Gases_Totales        = CO2_producidos+CO_producidos+H2O_Totales+O2_producidos+N2_producidos
    Temperatura_llama    = 1180.0 + 273.15
    masa_Gases_Total     = (CO2_producidos*CO2)+(CO_producidos*CO)+(H2O_Totales*H2O)+(O2_producidos*O2)+(N2_producidos*N2)
    Potencia_Inicial_Gas = float(Diccionario_Entr['Calor suministrado'])
    
    CO2_producidos_2=CO2*CO2_producidos/1000.0
    CO_producidos_2=CO*CO_producidos/1000.0    
    H2O_Totales_2=(H2O*H2O_Totales)/1000.0
    O2_producidos_2=(O2*O2_producidos)/1000.0
    N2_producidos_2=(N2*N2_producidos)/1000.0
    Gas_Total=CO2_producidos_2+CO_producidos_2+H2O_Totales_2+O2_producidos_2+N2_producidos_2
    Flujo_Masico=Gas_Total/3600.0    
    CO2_producidos_3=CO2_producidos/Gases_Totales
    CO_producidos_3=CO_producidos/Gases_Totales
    H2O_Totales_3=H2O_Totales/Gases_Totales
    O2_producidos_3=O2_producidos/Gases_Totales
    N2_producidos_3=N2_producidos/Gases_Totales
    Gas_Total_2=CO2_producidos_3+CO_producidos_3+H2O_Totales_3+O2_producidos_3+N2_producidos_3  
    
    Presion=float(Diccionario_Entr['Presión atmosférica'])/760.0
    Temperatura_Flama_Ad=Modulo2.Tadiabatica(Exceso_aire,Eficiencia_Combustion,Humedad_bagazo,Humedad_aire)
    Velocidad_I=(Flujo_Masico/Modulo1.Densidad_kgm3(CO_producidos_3,CO2_producidos_3,N2_producidos_3,O2_producidos_3,H2O_Totales_3,Presion*101.325,Temperatura_Flama_Ad))/0.32
   
    Energia_inicial_Gas=Modulo1.DH_KJKmol(25,Temperatura_Flama_Ad,CO_producidos/1000,CO2_producidos/1000,N2_producidos/1000,O2_producidos/1000,H2O_Totales/1000)/3600
    Perdida_total=Energia_inicial_Gas*0.14

    Datos_simulacion.append(Q_Cedido)
    Datos_simulacion.append(Calor_transferido)
    Datos_simulacion.append(Masa_Bagazo)
    Datos_simulacion.append(CO2_producidos_2)
    Datos_simulacion.append(CO_producidos_2)
    Datos_simulacion.append(H2O_Totales_2)
    Datos_simulacion.append(O2_producidos_2)
    Datos_simulacion.append(N2_producidos_2)
    Datos_simulacion.append(Gas_Total)
    Datos_simulacion.append(Flujo_Masico)
    Datos_simulacion.append(Velocidad_I)
    Datos_simulacion.append(CO2_producidos_3)
    Datos_simulacion.append(CO_producidos_3)
    Datos_simulacion.append(H2O_Totales_3)
    Datos_simulacion.append(O2_producidos_3)
    Datos_simulacion.append(N2_producidos_3)
    Datos_simulacion.append(Gas_Total_2)
    Datos_simulacion.append(Temperatura_Flama_Ad)
    Datos_simulacion.append(Energia_inicial_Gas)

    Tipo_ladrillo=0
    Q_perdido_cam = Calcular_parrillas(float(Diccionario_Entr['Área de la parrilla']),
                                       float(Diccionario_Entr['Capacidad estimada de la hornilla']),
                                       Tipo_ladrillo,
                                       float(Diccionario_Entr['Calor suministrado']),
                                       'Refractario',
                                       float(Diccionario_Entr['Temperatura del ambiente']),
                                       Temperatura_Flama_Ad)
    
    '''>>>>>>>>---------------Calculo de los gases----------------<<<<<<<<<<<<'''
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>Este arreglo inicia por la ultima paila<<<<<<<<<<<<<<<<<<<<<<<
    Gas_Paila=[]
    Gases_Consolidado=[] 
    Temp1=0
    Temp2=0
    for i in range(Cantidad_Pailas):
        if(i==0):
            Temp1=Energia_inicial_Gas-(Q_perdido_cam/1000)
        else:
            Temp1=Temp2
        Gas_Paila.append(Temp1)                                     #Calor antes de la paila
        aux=Temp1-(0.25*Perdida_total)-Calor_transferido[i]
        Gas_Paila.append(aux)        
        mem1= abs(Modulo2.Tcalculada(Temp1,                                 #Temperatura antes de la paila
                             Gas_Total,
                             CO_producidos_3,
                             CO2_producidos_3,
                             N2_producidos_3,
                             O2_producidos_3,
                             H2O_Totales_3))                        #Calor despues de la paila
        Gas_Paila.append(mem1)
        mem2= abs(Modulo2.Tcalculada(aux,                                   #Temperatura despues de la paila
                             Gas_Total,
                             CO_producidos_3,
                             CO2_producidos_3,
                             N2_producidos_3,
                             O2_producidos_3,
                             H2O_Totales_3))
        Gas_Paila.append(mem2)
        Promedio_mem=(mem1+mem2)/2                                  #Temperatura bajo la paila
        Gas_Paila.append(Promedio_mem)
        Gas_Paila.append(0)                                         #Perdidas (Falta modelo)
        Gas_Paila.append(0.25*Perdida_total)                        #Perdida 14%
        Gases_Consolidado.append(Gas_Paila)                         #Consolidado
        Gas_Paila=[]
        Temp2=aux        
    
    Gases_Consolidado_t=np.transpose(np.around(Gases_Consolidado,3))
    
    '''>>>>>>>>---------------Estimar el calor por convección y radiación----------------<<<<<<<<<<<<'''
    Temperarura_Gases=Gases_Consolidado_t[4]  
    C_Boltzman=0.0000000567
    Emisividad_Fondo_paila=0.4 
    Emisividad_Ducto=0.96
    Factor_forma_Pared=0.4
    Factor_Forma_Piso=0.2
    
    Area_Paredes_radiantes= np.ones(Cantidad_Pailas)     #Faltan ecuaciones
    Area_Piso_radiante    = np.ones(Cantidad_Pailas)     #Faltan ecuaciones
    Area_Flujo            = AF                
    Area_Lisa             = AL
    Perimetro             = PF
    
    Temperatura_Superficie=Q_Cedido[15]                    #Lista del arreglo Q_cedido
    Emisividad_gases=np.ones(Cantidad_Pailas)*0.2 #Revisar nomograma
    Q_Total_estimado=[]
    for i in range(Cantidad_Pailas):
    #'''>>>>>>>>---------------Calor por convección----------------<<<<<<<<<<<<'''
        aux=Modulo1.Cp(Temperarura_Gases[i],                                                                                #Calor Especifico a Presión Cte           
               CO_producidos_3,
               CO2_producidos_3,
               N2_producidos_3,
               O2_producidos_3,
               H2O_Totales_3)
        aux2=Modulo1.Densidad_kgm3(CO_producidos_3,                                                                         #Densidad
                           CO2_producidos_3,
                           N2_producidos_3,
                           O2_producidos_3,
                           H2O_Totales_3,
                           Presion*101.325,
                           Temperarura_Gases[i])
        visc_dina =0.0000175+(0.0000000335*Temperarura_Gases[i])                                                    #Viscosidad dinámica
        Coef_teri =(0.0229+(0.0000647*Temperarura_Gases[i]))/1000                                                   #Coeficiente conductividad térmica
        vel_gase1 =(masa_Gases_Total/(3600*1000))/(aux2*Area_Flujo[i])                                              #Velocidad del gas
        visc_sup1 =0.0000175+(0.0000000335*Temperatura_Superficie[i])                                               #Viscocidad dinamica superficial
        visc_cine =visc_dina/aux2                                                                                   #Viscocidad cinematica
        n_plant   =visc_dina*aux/Coef_teri                                                                          #N° Prandlt
        Diametro_h=4*Area_Flujo[i]/Perimetro[i]                                                                     #Diametro hidraulico
        try:
            n_reynol=(aux2*vel_gase1*Diametro_h)/visc_dina                                                            #Numero de Reynolds
            Nu1=((0.664*n_reynol)**(1/2))*(n_plant**(1/3))                                                              #No. Nusselt  Nre<1e5
            Nu2=(0.037*(n_reynol**0.8)*n_plant)/(1+(2.443*(n_reynol**-0.1))*((n_plant**0.67)-1))                        #No. Nusselt  Nre>5e5
            Nu3=((Nu1**2)+(Nu2**2))**(0.5)                                                                              #No. Nusselt  1e5< Nre <5e5
            Nu4=((0.4*(n_reynol**0.5))+0.06*(n_reynol**(2/3)))*((n_plant**0.4)*((visc_dina/visc_sup1)**(1/4)))          #No. Nusselt P.S.E
            Nu5=(2.36*((0.027*(n_reynol**0.8))*(n_plant**(1/3))*(visc_dina/visc_sup1)**(1/4)))-13.6                     #No. Nusselt Pirotubular Re<2,3e3
        except:
            n_reynol=2000
            Nu1=0.01
            Nu2=0.01
            Nu3=((Nu1**2)+(Nu2**2))**(0.5) 
            Nu4=0.01
            Nu5=0.01
        Coef_conv=Coef_teri*Nu4/Diametro_h                                                                          #Coeficiente de convección corregido
        Calor_conv=Area_Lisa[i]*Coef_conv*(Temperarura_Gases[i]-Temperatura_Superficie[i])                          #Calor por convección
        T_pared=abs(-264.44+(1.03*Temperarura_Gases[i]))+273                                                        #Temperatura de la pared
        T_piso=abs(-87.31+(0.79*Temperarura_Gases[i]))+273                                                          #Temperatura del piso
        '''>>>>>>>>---------------Calor por radiación----------------<<<<<<<<<<<<'''
        Temp_Fon=Temperatura_Superficie[i]+273.15                                                                   #Temperatura del fondo de la paila    
        Q_Paredes=2*(C_Boltzman*(T_pared**4-Temp_Fon**4)/((1-Emisividad_Fondo_paila)/(Area_Lisa[i]*Emisividad_Fondo_paila)+1/(Area_Lisa[i]*Factor_forma_Pared)+(1-Emisividad_Ducto)/(Area_Paredes_radiantes[i]/Emisividad_Ducto)))/1000
        Q_Piso=((C_Boltzman*((T_piso**4)-(Temp_Fon**4)))/((1-Emisividad_Fondo_paila)/(Area_Lisa[i]*Emisividad_Fondo_paila)+1/(Area_Lisa[i]*Factor_Forma_Piso)+(1-Emisividad_Ducto)/(Area_Piso_radiante[i]/Emisividad_Ducto)))/1000
        Q_Gas=C_Boltzman*Area_Lisa[i]*Emisividad_Fondo_paila*Emisividad_gases[i]*((Temperarura_Gases[i]+273.15)**4-(Temp_Fon**4))
        Q_Gas=(Q_Gas/(1-(1-Emisividad_Fondo_paila)*(1-Emisividad_gases[i])))/1000
        Q_Total_paila=Q_Paredes+Q_Piso+Q_Gas
        Q_Total_paila=saturador(Q_Total_paila,1300,0)
        Q_Total_estimado.append(Q_Total_paila+Calor_conv)


    
    df1 = pd.DataFrame(Datos_simulacion)
    df1.to_excel('static/Reporte1.xlsx')
    
    return Q_Total_estimado

def saturador (valor_i,maximo,minimo):
    if(valor_i<minimo):
        return minimo
    elif(valor_i>maximo):
        return maximo
    else:
        return valor_i
'''>>>>>>>>>>>>Concentrancion y Propiedades del jugo según calor cedido por el gas<<<<<<<<<'''
def Q_Cedido_gas(Calor_estimado):
    global Diccionario_Entr
    global Diccionario_Pailas
    Cantidad_Pailas=int(Diccionario_Pailas['Etapas']) 
    Area_lisa=np.random.random(Cantidad_Pailas)*2 #[0.614,0.99,1.8,2.176,2.9,5]
    Espesor_lamina=np.random.random(Cantidad_Pailas)*0.01 #[0.019,0.016,0.016,0.013,0.013,0.013]
    #Calor_estimado=[47.135,59.740,78.743,64.603,57.385,62.503,47.135,59.740,78.743,64.603,57.385,62.503]
#    La matriz tiene la siguiente disposición 
#    Lista_Contenido[0]=Calor Transferido desde el gas 
#    Lista_Contenido[1]=Concentracion de Solidos Inicial
#    Lista_Contenido[2]=Concentracion de Solidos Final
#    Lista_Contenido[3]=Concentracion de Solidos Promedio
#    Lista_Contenido[4]=Masa Jugo Entrada
#    Lista_Contenido[5]=Temperatura jugo
#    Lista_Contenido[6]=Viscosidad del Jugo
#    Lista_Contenido[7]=Tension Superficial
#    Lista_Contenido[8]=Densidad
#    Lista_Contenido[9]=Calor Especifico  jugo
#    Lista_Contenido[10]=Entalpia de Vaporización
#    Lista_Contenido[11]=Conductividad del jugo
#    Lista_Contenido[12]=Area Interior Paila
#    Lista_Contenido[13]=flux Calor Paila
#    Lista_Contenido[14]=T Pared L Jugo
#    Lista_Contenido[15]=T Pared L Gas
    Etapas=int(Diccionario_Pailas['Etapas']) 
    Lista_Contenido=np.zeros((16, Etapas))
    """Calculo de la hornilla por etapas"""   
    CSS_Cana=float(Diccionario_Entr['CSS del jugo de Caña'])
#    print(Diccionario_Entr['Temperatura del ambiente'])
    Temp_amb=float(Diccionario_Entr['Temperatura del ambiente'])
    Presion =float(Diccionario_Entr['Presión atmosférica'])/760.0
    Tension_superficial=0.05546
    Lista_Contenido[0]=Calor_estimado
    Lista_Contenido[12]=Area_lisa  
    
    for i in range(Etapas-1,-1,-1):
        if(i==Etapas-1):
            Lista_Contenido[1][i]=CSS_Cana 
            Lista_Contenido[4][i]=float(Diccionario_Entr['Jugo pre-limpiador'])
        else:
            Lista_Contenido[1][i]=Lista_Contenido[2][i+1]
            Masa_Jugo_Aux=(Lista_Contenido[4][i+1]*Lista_Contenido[1][i+1]/Lista_Contenido[2][i+1])
            if(i==Etapas-2):
                Lista_Contenido[4][i]=Masa_Jugo_Aux-(0.04*Masa_Jugo_Aux)
            else:
                Lista_Contenido[4][i]=Masa_Jugo_Aux    
                
        Lista_Contenido[2][i]=Modulo2.XbrixCl(Lista_Contenido[4][i], 
                                      Lista_Contenido[1][i], 0, 
                                      Lista_Contenido[0][i], 
                                      CSS_Cana,
                                      Presion,
                                      Temp_amb)
        Lista_Contenido[2][i]=saturador(Lista_Contenido[2][i],100,0) #Reparación en caso de que el CSS se dispare
        Lista_Contenido[3][i]=(Lista_Contenido[2][i]+Lista_Contenido[1][i])/2           
        Lista_Contenido[5][i]=Modulo2.Tjugo(Presion,Lista_Contenido[3][i]) 
        Temp_amb=Lista_Contenido[5][i]
        Lista_Contenido[6][i]=(math.exp(-11.229+(3257.5/(Lista_Contenido[5][i]+273.15))+(0.07572*Lista_Contenido[3][i])))/1000                
        Lista_Contenido[7][i]=Tension_superficial
        Lista_Contenido[8][i]=(1043+4.854*Lista_Contenido[3][i])-(1.07*Lista_Contenido[5][i])   
        Lista_Contenido[9][i]=4.18*(1-(0.006*Lista_Contenido[3][i]))                                       
        Lista_Contenido[10][i]=2492.9-(2.0523*Lista_Contenido[5][i])-(0.0030752*Lista_Contenido[5][i]**2)  
        Lista_Contenido[11][i]=(0.3815-0.0051*Lista_Contenido[3][i])+(0.001866*Lista_Contenido[5][i]) 
        Lista_Contenido[13][i]=1000*(Lista_Contenido[0][i]/Lista_Contenido[12][i])     
        Lista_Contenido[14][i]=Modulo2.Tw(Lista_Contenido[13][i],
                                  Lista_Contenido[6][i],
                                  Lista_Contenido[10][i],
                                  Lista_Contenido[7][i],
                                  Lista_Contenido[8][i],
                                  Lista_Contenido[9][i],
                                  Lista_Contenido[11][i],
                                  Lista_Contenido[5][i])       
        Lista_Contenido[15][i]=Modulo2.twg(Espesor_lamina[i], Lista_Contenido[13][i], Lista_Contenido[14][i])
    return Lista_Contenido
    
def Optimizacion(Diccionario_1, Diccionario_2, L_temp):
    global Diccionario_Entr
    global Diccionario_Pailas
    Diccionario_Entr=Diccionario_1
    Diccionario_Pailas=Diccionario_2
    #Parámetros del algoritmo de optimización
    Iteracion_actual = 0
    Taza_cambio=0.1
#    Error_actual     = 100
    #Individuos de la población inicial
    #Diccionario = Diseno_inicial.datos_entrada(Diccionario_Entr,0,0)
    #Condiciones iniciales
    Calor_0=Diccionario_Pailas['Calor Nece Calc por Etapa [kW]']
    Factor_bagazo_nuevo=Diccionario_Entr['Factor de consumo de bagazo']
    Diccionario = Diseno_inicial.datos_entrada(Diccionario_Entr,1,Factor_bagazo_nuevo)
    Efec=Diccionario['Eficiencia de la hornilla']
    Factor_original=Factor_bagazo_nuevo
    Flag=True
    while (Iteracion_actual<=100):
        Diccionario = Diseno_inicial.datos_entrada(Diccionario_Entr,Iteracion_actual,Factor_bagazo_nuevo)
        Efec=Diccionario['Eficiencia de la hornilla']
        Calor_1=np.around(Propiedades(Calor_0, L_temp[0], L_temp[1], L_temp[2]),3)
        
        for x in np.nditer(Calor_1):
            if(x<=0 or np.isnan(x)):
                Flag=False
                break
            else:
                Flag=True
       
        a11 = np.array(Calor_1, dtype = np.float)
        a11 [np.isnan(a11)] = 0.1
        Calor_1=a11

        #Calculo del error usando la magnitud del vector
        Calor_0 = np.array(Calor_0)
        Calor_1 = np.array(Calor_1) 

        x0=np.linalg.norm(Calor_0)
        x1=np.linalg.norm(Calor_1)
        Error=(x1-x0)/x0
        #Error_actual=abs(Error)
               
        if(Efec<40 and Flag==True):
            Calor_0=Calor_1
            Factor_original=Factor_bagazo_nuevo
        else:
            if(Error<0):
                Factor_bagazo_nuevo=Factor_bagazo_nuevo-(Taza_cambio*np.random.random(1))
            else:
                Factor_bagazo_nuevo=Factor_bagazo_nuevo+(Taza_cambio*np.random.random(1))
            Factor_bagazo_nuevo=float(saturador(Factor_bagazo_nuevo,10,1))        
            
        Iteracion_actual=Iteracion_actual+1
        
#        print('Factor Consumo bagazo='+str(Diccionario['Factor de consumo de bagazo']))
#        print('Area parrilla='+str(Diccionario['Área de la parrilla']))
#        print('Eficiencia de la hornilla='+str(Diccionario_1['Eficiencia de la hornilla']))
#        print('Factor original='+str(Factor_original))
#        print('Q=' + str(Calor_1))
#        print('Q0=' + str(Calor_0))
#        print('Error='+str(Error))
#        print('Iteracion='+str(Iteracion_actual))
    
    Diccionario = Diseno_inicial.datos_entrada(Diccionario_Entr,Iteracion_actual,Factor_original)
#    Efec=Diccionario['Eficiencia de la hornilla']
#    print(Factor_original)
#    print('Area parrilla='+str(Diccionario['Área de la parrilla']))
#    print(Efec)
#    print(Propiedades(Calor_0, L_temp[0], L_temp[1], L_temp[2]))
#    print('Fin algoritmo')
        
#Optimizacion(Diccionario, Diccionario_2)