# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:38:48 2020

@author: hahernandez
"""
import math
import pandas as pd
"""----->>>>Selección del molino<<<<----"""
def Seleccionar_Molino(Kilos_Hora):
    Molino=pd.read_excel('static/Catalogos/Molinos.xlsx')
    Marca=Molino['Marca'].values
    Modelo=Molino['Modelo'].values
    Kilos=Molino['kghora'].values
    Diesel=Molino['Diesel'].values
    Electrico=Molino['Electrico'].values
    Valor=Molino['Valor'].values
    Enlaces=Molino['Link'].values
    Seleccionado=[]
    M1=[]
    M2=[]        
    K1=[]
    D1=[]    
    E1=[]
    G1=[]
    V1=[]
    aux=0
    for i in range (len(Kilos)):
        if((Kilos[i]<Kilos_Hora)and(i<(len(Kilos)-1))):
            aux=Kilos[i]
        else:
            aux=Kilos[i]
            for j in range(len(Kilos)):
                if(aux==Kilos[j]):
                    Seleccionado.append(j)
            break 
    for i in Seleccionado:
        M1.append(Marca[i])
        M2.append(Modelo[i])        
        K1.append(Kilos[i])
        D1.append(Diesel[i])    
        E1.append(Electrico[i])
        G1.append(Enlaces[i])
        V1.append(Valor[i])  
        
    datos={'Marca'      :M1,
           'Modelo'     :M2,
           'kg/hora'    :K1,
           'Diesel'     :D1,
           'Electrico'  :E1,
           'Link'       :G1,
           'Precio'     :V1
            }
    df = pd.DataFrame(datos, columns = ['Marca', 'Modelo', 'kg/hora', 'Diesel', 'Electrico','Link', 'Precio'])
    df.to_excel('static/Temp/Temp.xlsx')
    return sum(E1)/len(E1)
    
def datos_entrada(Diccionario,iteracion,Valor_Algoritmo):
    """Estos datos se toman directamente del archivo HTML"""
    #Crecimiento del área sembrada en los proximos 5 años		
    #Area de Caña Sembrada Propia			
    #Area de Caña Sembrada Para Calculo			
    #Periodo vegetatio			
    #Caña por Hectarea Esperada			
    #CSS de la Caña			
    #Jornada de Trabajo			
    #Dias de Trabajo			
    #Horas al Dia		
    #CSS Panela	
    #Altura del Sitio	
    
    """Nota: los valores de estas variables son supuestos (Estas son otras variables de entrada)"""
    Porcentaje_extraccion=0.6       #60%
    Bagazillo_Prelimpiador=0.02 #2%
    Cachaza=0.04 #4%    
    CSS_Jugo_Clarificado=float(Diccionario['Grados Brix de la caña (promedio)'])+5
    CSS_Jugo_Posevaporacion=float(Diccionario['Grados Brix de la caña (promedio)'])+58
    Tipo_de_camara='Ward'
    Humedad_bagazo=0.3#15%			
    Exceso_Aire=1.8 #lamda	
    Extraccion=0.6#60%
    Porcentaje_Fibra=0.14#14%
    Temperatura_Ambiente=25#°C			
    Altura_sitio=float(Diccionario['Altura media sobre el nivel del mar'].replace(" m", ""))
    """Fin de los datos supuestos entrada"""
    
    """Calculo de la capacidad del molino"""		
    #Área de caña sembrada para el calculo
    Crecimiento=float(Diccionario['Crecimiento aproximado del área sembrada'])
    Crecimiento=Crecimiento+float(Diccionario['Área caña sembrada'])
    Area_cana_calculo=(Crecimiento+float(Diccionario['Área caña sembrada']))/2
    Cana_esperada_hectarea=float(Diccionario['Caña esperada por hectárea'])
    P_vegetativo=float(Diccionario['Periodo vegetativo'])
    #Caña molida al mes = Area sembrada de caña para calculo*Caña esperada por hectarea/Periodo vegetativo
    Cana_molida_mes=(Area_cana_calculo*Cana_esperada_hectarea)/P_vegetativo
    # Area cosechada al mes = Caña esperada por hectarea/Caña molida al mes
    Area_Cosechada_mes=Cana_molida_mes/Cana_esperada_hectarea
    #Caña molida a la semana = Caña molida al mes/numero de moliendas
    Cana_molida_semana=Cana_molida_mes/float(Diccionario['Número de moliendas'])
    #Caña molida por hora = Caña molida a la semana/Dias de trabajo*Horas al dia
    Cana_molida_hora=Cana_molida_semana/(float(Diccionario['Días de trabajo a la semana'])*float(Diccionario['Horas de trabajo al día']))
    #Jugo Crudo=Caña molida por hora*porcentaje de extraccion
    Jugo_Crudo=Cana_molida_hora*Porcentaje_extraccion
    #Jugo Clarificado=Jugo_Crudo-((Jugo_Crudo*Bagacillo en Prelimpiador+((Jugo_Crudo-(Jugo_Crudo*Bagacillo en Prelimpiador))*(Cachaza))
    Jugo_Clarificado=Jugo_Crudo-((Jugo_Crudo*Bagazillo_Prelimpiador+((Jugo_Crudo-(Jugo_Crudo*Bagazillo_Prelimpiador))*(Cachaza))))
    #Masa de panela=((Jugo_Clarificado*CSS de la caña))/CCS de la panela)*1000
    CSS_Cana=float(Diccionario['Grados Brix de la caña (promedio)']) *0.6
    CSS_Panela=float(Diccionario['Grados Brix de la panela (promedio)'])
    Masa_panela = (Jugo_Clarificado*CSS_Cana/CSS_Panela)*1000
    #Capacidad del molino=constante*caña molida hora*1000
    Capacidad_molino=Cana_molida_hora*1.3*1000
    #Capacidad de la hornilla=Masa de panela
    Capacidad_Hornilla=Masa_panela
    
    """Calculos para la masa"""
    Masa_Jugo_Clarificado=(CSS_Panela*Capacidad_Hornilla)/CSS_Cana
    Masa_Jugo_Prelimpiador=Masa_Jugo_Clarificado/(1-Cachaza)
    Masa_Cachaza=Masa_Jugo_Prelimpiador*Cachaza
    Masa_Jugo=Masa_Jugo_Prelimpiador/(1-Bagazillo_Prelimpiador)
    Masa_Bagazillo= Masa_Jugo*Bagazillo_Prelimpiador 
    Masa_Cana=Masa_Jugo/Extraccion
    
    Masa_Agua_Evaporar=Masa_Jugo_Prelimpiador-Capacidad_Hornilla
    Masa_A_clarificacion=Masa_Jugo_Prelimpiador
    Masa_A_Evaporacion=Masa_Jugo_Clarificado
    Masa_A_Concentracion=(CSS_Jugo_Clarificado*Masa_A_Evaporacion)/CSS_Jugo_Posevaporacion
    Masa_Bag_Humedo=Masa_Cana-Masa_Jugo
    Humedad_inicial_bagazo=((Masa_Jugo-Masa_Jugo*(Extraccion+Porcentaje_Fibra))-(Masa_Jugo-Masa_Jugo*(Extraccion+Porcentaje_Fibra))*(CSS_Cana/100))/(Masa_Jugo*(1-Extraccion))			
    Masa_Bag_Seco=Masa_Bag_Humedo*((1-Humedad_inicial_bagazo)/(1-Humedad_bagazo))
    if(iteracion==0):
        Factor_consumo_bagazo=Masa_Bag_Seco/Capacidad_Hornilla
    else:
        Factor_consumo_bagazo=Valor_Algoritmo
    Masa_Bag_Suministrado=Capacidad_Hornilla*Factor_consumo_bagazo
    Presion_atmosferica=760.0*math.exp(-0.0001158*Altura_sitio)
    Temperatura_Ebullicion_Agua=-227.03 + (3816.44/(18.3036 - math.log(7.5*(Presion_atmosferica*(133.3224/1000)))))
    
    """Calculos de las propiedades de los jugos"""
    #NOTA: Esta es una caracteristica (T33) es propia del molino (Tomarla del catálogo).
    T33=Seleccionar_Molino(Capacidad_molino) 
    #>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
    Inicial_Clf=997.39+(4.46*CSS_Cana)   
    Inicial_Eva=997.39+(4.46*CSS_Jugo_Clarificado)
    Inicial_Con=997.39+(4.46*CSS_Jugo_Posevaporacion)
    Ebullicion_Clarificacion=Temperatura_Ebullicion_Agua + 0.2209*math.exp(0.0557*CSS_Jugo_Clarificado)	
    Ebullicion_Evaporacion=Temperatura_Ebullicion_Agua + 0.2209*math.exp(0.0557*CSS_Jugo_Posevaporacion)
    Ebullicion_Concentracion=Temperatura_Ebullicion_Agua + 0.2209*math.exp(0.0557*T33)	
    Entalpia_Clarificacion=2492.9-2.0523*((Temperatura_Ebullicion_Agua+Ebullicion_Clarificacion)/2)-0.0030752*((Temperatura_Ebullicion_Agua+Ebullicion_Clarificacion)/2)**2
    Entalpia_Evaporacion=2492.9-2.0523*((Ebullicion_Clarificacion+Ebullicion_Evaporacion)/2)-0.0030752*((Ebullicion_Clarificacion+Ebullicion_Evaporacion)/2)**2
    Entalpia_Concentracion=2492.9-2.0523*((Ebullicion_Evaporacion+Ebullicion_Concentracion)/2)-0.0030752*((Ebullicion_Evaporacion+Ebullicion_Concentracion)/2)**2
    Q_Especifico_Inicial=4.18*(1-0.006*CSS_Cana)
    Q_Especifico_Clarificado=4.18*(1-0.006*CSS_Jugo_Clarificado)	
    Q_Especifico_Eva=4.18*(1-0.006*CSS_Jugo_Posevaporacion)	
    Poder_Calorifico_bagazo=17.85-20.35*Humedad_bagazo
    Calor_Suministrado=(Capacidad_Hornilla*Factor_consumo_bagazo)*Poder_Calorifico_bagazo/3.6	
    Area_de_Parrilla=Calor_Suministrado/1000	    

    """Calculos de calor requerido por etapa"""   
    Q_Etapa_Clarificacion=((Masa_A_clarificacion*Q_Especifico_Inicial*(Ebullicion_Clarificacion-Temperatura_Ambiente))+((Masa_A_clarificacion-Masa_A_Evaporacion)*Entalpia_Clarificacion))/3600   
    Q_Etapa_Evaporacion=(Masa_A_Evaporacion*Q_Especifico_Clarificado*(Ebullicion_Evaporacion-Ebullicion_Clarificacion)+(Masa_A_Evaporacion-Masa_A_Concentracion)*Entalpia_Evaporacion)/3600
    Q_Etapa_Concentracion=(Masa_A_Concentracion*Q_Especifico_Eva*(Ebullicion_Concentracion-Ebullicion_Evaporacion)+(Masa_A_Concentracion-Capacidad_Hornilla)*Entalpia_Concentracion)/3600
    Total_Etapa=Q_Etapa_Clarificacion+Q_Etapa_Evaporacion+Q_Etapa_Concentracion
    Total_Etapa_F_L=(Masa_Jugo*(Ebullicion_Concentracion-Temperatura_Ambiente)*Q_Especifico_Inicial+Masa_Agua_Evaporar*((Entalpia_Clarificacion+Entalpia_Concentracion)/2))/3600
    """>>>>>>>>>>>>>>>>Eficiencia<<<<<<<<<<<<<<<<<<<<<<<"""
    Eficiencia=(Total_Etapa/Calor_Suministrado)*100
    """Ampliación del diccionario"""
    Etiquetas=['DATOS DE ENTRADA',
               'Capacidad estimada de la hornilla',			
               'Factor de consumo de bagazo',	
               'Eficiencia de la hornilla',					
               'Bagacillo del pre-limpiador',		
               'Cachaza',			
               'CSS del jugo de Caña',			
               'CSS del jugo clarificado',			
               'CSS del jugo pos-evaporación',		
               'CSS panela',			
               'Tipo de cámara',			
               'Humedad del bagazo',		
               'Exceso de aire',			
               'Extracción',			
               'Porcentaje de Fibra',					
               'Temperatura del ambiente',			
               'Humedad inicial bagazo',			
               'Presión atmosférica',			
               'Temperatura de ebullición del agua',
               'CAPACIDAD MOLINO',
               'Caña molida al mes',	
               'Área cosechada al mes',		
               'Caña molida a la semana',		
               'Caña molida por Hora',		
               'Jugo crudo',		
               'Jugo clarificado',		
               'Masa de panela',		
               'Capacidad del Molino',		
               'DATOS DE LA MASA',
               'Caña',
               'Jugo',
               'Bagacillo',	
               'Jugo pre-limpiador',	
               'Cachaza',	
               'Jugo clarificado',	
               'Agua a evaporar',	
               'A clarificación',	
               'A evaporación',
               'A concentración',	
               'Bagazo suministrado',	
               'Bagazo húmedo',	
               'Bagazo seco',	
               'PROPIEDADES DE LOS JUGOS',
               'Densidad',
               'Inicial de clarificación',
               'Inicial de evaporación',
               'Inicial de concentración',
               'Temperatura ebullición (Clarificación)',
               'Temperatura ebullición (Evaporación)',
               'Temperatura ebullición (Concentración)',
               'Entalpia de evaporización (Clarificación)',
               'Entalpia de evaporización (Evaporación)',
               'Entalpia de evaporización (Concentración)',
               'Calor especifico jugo',			
               'Inicial',
               'Clarificado',
               'Eva',
               'Otros datos',
               'Poder calorífico bagazo',
               'Calor suministrado',
               'Área de la parrilla',
               'CALOR REQUERIDO POR ETAPA',
               'Clarificación [KW]',
               'Evaporación [KW]',
               'Concentración',
               'Total [KW]',
               'Total(F.L.) [KW]'
               ]
    
    Valores=['DATOS DE ENTRADA',
             math.ceil(Capacidad_Hornilla),
             round(Factor_consumo_bagazo,3),
             round(Eficiencia,3),
             round(Bagazillo_Prelimpiador,3),
             round(Cachaza,3),
             round(CSS_Cana,3),
             round(CSS_Jugo_Clarificado,3),
             round(CSS_Jugo_Posevaporacion,3),
             round(CSS_Panela,3),
             Tipo_de_camara,
             round(Humedad_bagazo,3),
             round(Exceso_Aire,3),
             round(Extraccion,3),
             round(Porcentaje_Fibra,3),
             round(Temperatura_Ambiente,3),
             round(Humedad_inicial_bagazo,3),
             round(Presion_atmosferica,3),
             round(Temperatura_Ebullicion_Agua,3),
             'CAPACIDAD MOLINO',
             round(Cana_molida_mes,3),
             round(Area_Cosechada_mes,3),
             round(Cana_molida_semana,3),
             round(Cana_molida_hora,3),
             round(Jugo_Crudo,3),
             round(Jugo_Clarificado,3),
             round(Masa_panela,3),
             round(Capacidad_molino,3),
             'DATOS DE LA MASA',
             round(Masa_Cana,3),
             round(Masa_Jugo,3),
             round(Masa_Bagazillo,3),
             round(Masa_Jugo_Prelimpiador,3),
             round(Masa_Cachaza,3),
             round(Masa_Jugo_Clarificado,3),
             round(Masa_Agua_Evaporar,3),
             round(Masa_A_clarificacion,3),
             round(Masa_A_Evaporacion,3),
             round(Masa_A_Concentracion,3),
             round(Masa_Bag_Suministrado,3),
             round(Masa_Bag_Humedo,3),
             round(Masa_Bag_Seco,3),
             'PROPIEDADES DE LOS JUGOS',
             'Densidad',
             round(Inicial_Clf,3),
             round(Inicial_Eva,3),
             round(Inicial_Con,3),
             round(Ebullicion_Clarificacion,3),
             round(Ebullicion_Evaporacion,3),
             round(Ebullicion_Concentracion,3),
             round(Entalpia_Clarificacion,3),
             round(Entalpia_Evaporacion,3),
             round(Entalpia_Concentracion,3),
             'Calor especifico jugo',
             round(Q_Especifico_Inicial,3),
             round(Q_Especifico_Clarificado,3),
             round(Q_Especifico_Eva,3),
             'Otros datos',
             round(Poder_Calorifico_bagazo,3),
             round(Calor_Suministrado,3),
             round(Area_de_Parrilla,3),
             'CALOR REQUERIDO POR ETAPA',
             round(Q_Etapa_Clarificacion,3),
             round(Q_Etapa_Evaporacion,3),
             round(Q_Etapa_Concentracion,3),
             round(Total_Etapa,3),
             round(Total_Etapa_F_L,3)
            ]
    
    Dict_aux=dict(zip(Etiquetas,Valores))
    Diccionario.update(Dict_aux)
    return Diccionario

def Calculo_por_etapas(Diccionario):
    """Calculo de la hornilla por etapas"""   
    Lista_Contenido=[]
    Lista_columnas=[]
    #Etapas es un supuesto de cuantas pailas debe tener la hornilla
    Cana_esperada_hectarea=float(Diccionario['Caña esperada por hectárea'])
    Etapas=10#int(round(Cana_esperada_hectarea/10,0))
    #Saturador "minimo son dos etapas"
    if (Etapas>2):
        Factor_Division=Etapas-2
    else:
        Factor_Division=2   
        Etapas=2
    #Caracteristicas de las celdas de cada columna (Lista_columnas)
    #Fila 0 concentración de solidos inicial
    #Fila 1 Concentración de solidos final
    #Fila 2 Concentración promedio
    #Fila 3 Masa de jugo de entrada
    #Fila 4 Calor Especifico P Cte jugo
    #Fila 5 Densidad del Jugo
    #Fila 6 Volumen de jugo kg
    #Fila 7 Volumen de jugo en L
    #Fila 8 Temperatura de Entrada
    #Fila 9 Temperatura de Salida
    #Fila 10 Entalpia de Vaporización
    #Fila 11 Masa de Agua a Evaporar
    #Fila 12 Calor Nece Calc por Etapa
    for i in range(13):
        for j in range (Etapas):
            Lista_columnas.append(float(i+j))
        Lista_Contenido.append(Lista_columnas)
        Lista_columnas=[]
        
    Lista_Contenido[0][0]=float(Diccionario['CSS del jugo pos-evaporación'])         #Concentracion_solidos_inicial (CSS02)
    Lista_Contenido[1][0]=float(Diccionario['CSS panela'])                          #Concentracion_solidos_final   (CSSF1)
    Lista_Contenido[0][Etapas-1]=float(Diccionario['CSS del jugo de Caña'])         #Concentracion_solidos_inicial (CSS01)
    Lista_Contenido[1][Etapas-1]=float(Diccionario['CSS del jugo clarificado'])     #Concentracion_solidos_final   (CSSF1)
    
    if(Etapas>2):
        ite=0
        for i in range(Etapas-2,0,-1):
            Lista_Contenido[0][i]=Lista_Contenido[1][i+1]
            if(ite==0):
                Lista_Contenido[1][i]=((Lista_Contenido[0][0]-Lista_Contenido[0][i])/Factor_Division)+Lista_Contenido[0][i]
                ite=ite+1
            else:
                Lista_Contenido[1][i]=((Lista_Contenido[0][0]-Lista_Contenido[0][Etapas-2])/Factor_Division)+Lista_Contenido[0][i]
    
    
    for i in range(Etapas-1,-1,-1):
        #Concentración promedio=(Concentracion_solidos_inicial+Concentracion_solidos_final)/2
        Lista_Contenido[2][i]=(Lista_Contenido[0][i]+Lista_Contenido[1][i])/2
        if(i==Etapas-1):
            #Masa de jugo de entrada
            Lista_Contenido[3][i]=float(Diccionario['A clarificación'])
        else:
            #Masa de jugo de entrada=(Masa de jugo etapa anterior*CCS inicial etapa anterior)/CCS Final etapa anterior
            Lista_Contenido[3][i]=Lista_Contenido[3][i+1]*Lista_Contenido[0][i+1]/Lista_Contenido[1][i+1]    
        #Calor_Especifico_P_Cte_jugo=4.18*(1-(0.006*Concetracion_promedio))
        Lista_Contenido[4][i]=4.18*(1-(0.006*Lista_Contenido[2][i]))
        #Densidad_del_Jugo=997.39+(4.46*Concetracion_promedio)
        Lista_Contenido[5][i]=997.39+(4.46*Lista_Contenido[2][i])
        #Volumen_jugo=Masa_jugo_de_entrada/Densidad_del_Jugo
        Lista_Contenido[6][i]=Lista_Contenido[3][i]/Lista_Contenido[5][i]
        #Volumen_jugo_L=Volumen_jugo*1000
        Lista_Contenido[7][i]=Lista_Contenido[6][i]*1000.0
        if(i==Etapas-1):
            #Temperatura_Entrada=Temperatura ambiente
            Lista_Contenido[8][i]=float(Diccionario['Temperatura del ambiente'])        
        else:
            #Temperatura_Entrada=Temperatura_ebullición_agua+0.2209*math.exp(0.0557*Concentracion_solidos_inicial)
            Lista_Contenido[8][i]=Lista_Contenido[9][i+1]   
        #Temperatura_Salida=G37+0.2209*math.exp(0.0557*Concentracion_solidos_final)
        Lista_Contenido[9][i]=float(Diccionario['Temperatura de ebullición del agua'])+0.2209*math.exp(0.0557*Lista_Contenido[1][i])    
        #Entalpia_Vaporizacion=(2492.9-(2.0523*Temperatura_Entrada))-(0.0030752*(Temperatura_Entrada**2))
        Lista_Contenido[10][i]=(2492.9-(2.0523*Lista_Contenido[8][i]))-(0.0030752*(Lista_Contenido[8][i]**2))
        #Masa_Agua_Evaporar=Masa_jugo_de_entrada-(Masa_jugo_de_entrada*Concentracion_solidos_inicial/Concentracion_solidos_final)
        Lista_Contenido[11][i]=Lista_Contenido[3][i]-(Lista_Contenido[3][i]*Lista_Contenido[0][i]/Lista_Contenido[1][i])
        #Calor_por_Etapa=(Masa_jugo_de_entrada*Calor_Especifico_P_Cte_jugo*(Temperatura_Salida-Temperatura_Entrada)+Masa_Agua_Evaporar*Entalpia_Vaporizacion)/3600
        Lista_Contenido[12][i]=(Lista_Contenido[3][i]*Lista_Contenido[4][i]*(Lista_Contenido[9][i]-Lista_Contenido[8][i])+Lista_Contenido[11][i]*Lista_Contenido[10][i])/3600.0
        
    #Fijar decimales en 3
    for j in range (13):
        for i in range (Etapas):
            Lista_Contenido[j][i]=round(Lista_Contenido[j][i],3)
    Etiquetas=[
               'Concentracion de Solidos Inicial [ºBrix]',
               'Concentracion de Solidos Final [ºBrix]',
               'Concentracion de Solidos Promedio [ºBrix]',
               'Masa de Jugo Entrada [Kg]',
               'Calor Especifico P Cte jugo [KJ/Kg °C]',
               'Densidad del Jugo [kg/m3]',
               'Volumen de jugo [m^3/kg]',
               'Volumen de jugo [L]',
               'Temperatura de Entrada [ºC]',
               'Temperatura de Salida [ºC]',
               'Entalpia de Vaporización [KJ/kg]',
               'Masa de Agua a Evaporar [Kg]',
               'Calor Nece Calc por Etapa [KW]']
    Dict_aux=dict(zip(Etiquetas,Lista_Contenido))    
    Dict_aux_2=dict(zip(['Etapas'],[Etapas]))  
    Dict_aux.update(Dict_aux_2)
    return Dict_aux