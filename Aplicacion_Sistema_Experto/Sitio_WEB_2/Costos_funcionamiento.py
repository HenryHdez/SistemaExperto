# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:08:42 2020

@author: hahernandez
"""
"""----------->>>>>Librerias para crear la ambientación del grafico de costo<<<<<<<------"""
from matplotlib.backends.backend_agg import FigureCanvasAgg
from time import sleep
import xlrd
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Proyeccion_economica 
#Definición de las variables globales
global Capacidad_hornilla
global Molino_seleccionado
global Horas_trabajo_al_dia

###Rutinas para generar el pdf del costo
#Layout del informe
def Fondo(canvas):
    #Dibujar logo y membrete de AGROSAVIA 
    canvas.drawImage('static/Iconos/Hoja.jpg', 0, 0, width=612, height=795)
    canvas.setLineWidth(.3)
    return canvas

#Cambiar formato a miles
def Formato_Moneda(num, simbolo, n_decimales):
    n_decimales = abs(n_decimales) #abs asegura que los dec. sean positivos.
    num = round(num, n_decimales) #Redondear a los decimales indicados
    num, dec = str(num).split(".") #Se divide el numero en cadenas y convierte en String
    dec += "0" * (n_decimales - len(dec)) #Concatenar ceros a la cadena
    num = num[::-1] #Inversion del vector para agregar comas
    l = [num[pos:pos+3][::-1] for pos in range(0,50,3) if (num[pos:pos+3])] #Separador de miles
    l.reverse() #Invierte nuevamente
    num = str.join(",", l) #unir string por comas
    try: #eliminar parte negativa
        if num[0:2] == "-,":
            num = "-%s" % num[2:]
    except IndexError:
        pass
    #si no se especifican decimales, se retorna un numero entero.
    if not n_decimales:
        return "%s %s" % (simbolo, num)
    return "%s %s.%s" % (simbolo, num, dec)
      
def Variables(Capacidad, Horas, semana, moliendas, Cana_estimada, cana_hora):
    global Capacidad_hornilla
    global Horas_trabajo_al_dia
    global Dias_trabajo_semana
    global Toneladas_cana_a_moler
    global numero_moliendas
    global Cana_molida_hora
    Capacidad_hornilla=Capacidad
    Horas_trabajo_al_dia=Horas
    Dias_trabajo_semana=semana
    Toneladas_cana_a_moler=Cana_estimada
    numero_moliendas=moliendas
    Cana_molida_hora=cana_hora
    
def estimar_total(vector):
    acumulado=[]
    for i in vector:
        acumulado.append(i[2])
    return sum(acumulado)

def cantidad_parr(canti):
    global parrillas
    parrillas=canti
    
def costos():
    global Capacidad_hornilla
    global Horas_trabajo_al_dia
    global Dias_trabajo_semana
    global Toneladas_cana_a_moler
    global numero_moliendas
    global parrillas
    global Cana_molida_hora

    #Inicio calculo de costos de la hornilla
    Archivo_Temporal=xlrd.open_workbook('static/Temp/Temp2.xlsx')
    libro = Archivo_Temporal.sheet_by_index(0)
    Tipo_de_Pailas=[]
    Cantidad_pailas=[]    
    Tipo_de_Pailas_rec=[]
    Cantidad_pailas_rec=[] 
    
    for i in range(len(libro.row(1))):
        Tipo_de_Pailas.append(libro.row(1)[i].value)
        Cantidad_pailas.append(libro.row(2)[i].value)
        Tipo_de_Pailas_rec.append(libro.row(3)[i].value)
        Cantidad_pailas_rec.append(libro.row(4)[i].value)
    Tipo_de_Pailas=Tipo_de_Pailas[1:]
    Cantidad_pailas=Cantidad_pailas[1:]
    Tipo_de_Pailas_rec=Tipo_de_Pailas_rec[1:]
    Cantidad_pailas_rec=Cantidad_pailas_rec[1:]    
    
    """>>>>>>>>>>>>-----------IMPORTAR MOLINOS-------------<<<<<<<<<<<<<<<"""
    Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
    Diesel=Molino['Diesel'].values
    Electrico=Molino['Electrico'].values
    Valor_M=Molino['Precio'].values 
    #>>>>>>>>>Definición de las pailas<<<<<<<<<#
    Hornilla=pd.read_excel('static/Costos/Hornilla.xlsx')   
    Pailas_disponibles_1=['plana', 'plana SA', 'pirotubular circular','pirotubular circular SA',
                        'semiesférica', 'semicilindrica', 'semicilindrica SA', 'cuadrada', 'cuadrada SA',
                        'acanalada', 'acanalada SA']
    Pailas_disponibles_2=['Paila plana', 'Paila plana sin aletas', 'Paila pirotubular circular', 
                          'Paila pirotubular circular sin aletas', 'Paila semiesférica', 'Paila semicilindrica', 
                          'Paila semicilindrica sin aletas', 'Paila pirotubular cuadrada', 'Paila pirotubular cuadrada sin aletas', 
                          'Paila acanalada con canales cuadrados','Paila acanalada con canales cuadrados y sin aletas']    
    #Establecimiento de factores para el calculo de elementos
    if(Cana_molida_hora<0.8):
        Cantidad_1=1
        Cantidad_2=0
    elif(Cana_molida_hora>0.8 and Cana_molida_hora<1.6):
        Cantidad_1=1
        Cantidad_2=1
    elif(Cana_molida_hora>1.6 and Cana_molida_hora<2.0):
        Cantidad_1=1
        Cantidad_2=2
    elif(Cana_molida_hora>2.0):
        Cantidad_1=2
        Cantidad_2=2    
    D_Hornilla_1={}
    D_Hornilla_2={}
    Mem_total_Hornilla_1=0
    Mem_total_Hornilla_2=0
    for k in range(2):
        """>>>>>>>>>>>>-----------COSTOS DEL PROYECTO-------------<<<<<<<<<<<<"""
        """>>>>>>>>>>>>----------Costos de la hornilla-------------<<<<<<<<<<<<"""
        Valor_Hornilla=[]
        Etiquetas_Hornilla=['Nombre']
        if(k==0):
            Total_pailas=sum(Cantidad_pailas)
            Cant_pail_aux=Cantidad_pailas
        elif(k==1):
            Total_pailas=sum(Cantidad_pailas_rec)
            Cant_pail_aux=Cantidad_pailas_rec
                    
        #Crear un vector con la cantidad de pailas
        for pun_i in range(len(Pailas_disponibles_1)):
            if(Cant_pail_aux[pun_i]>0):
                a=float(Hornilla[Pailas_disponibles_1[pun_i]].values)
                a=a*((0.004*Capacidad_hornilla)+0.2)
                Valor_Hornilla.append([Cant_pail_aux[pun_i], a, a*Cant_pail_aux[pun_i]])  
                Etiquetas_Hornilla.append(Pailas_disponibles_2[pun_i])
        
        #Revisar cantidad de valvulas
        #>>>>>>>>>>Otros accesorios de la hornilla<<<<<<<<<<<<<#
        Accesorios_disponibles=['Prelimpiador 1', 'Prelimpiador 2', 'Válvula de la chimenea', 'Ladrillos refractarios', 'Pegante bulto', 'Tubo acero inxidable de 3 pulgadas',
                            'Codos sanitarios de 3 pulgadas','Válvula de bola de 3 pulgadas', 'Férula sanitaria de 3 pulgadas',
                            'Abrazadera sanitaria de 3 pulgadas', 'Empaque de silicona de 3 pulgadas',
                            'Sección de parrilla', 'Marco de la puerta','Paila melotera', 'Valor aproximado del molino',
                            'Valor total de la hornilla']
        #vector de accesorios
        for pun_i in range(len(Accesorios_disponibles)):
            Etiquetas_Hornilla.append(Accesorios_disponibles[pun_i])    
        
        a=float(Hornilla['Prelimpiador'].values)
        Valor_Hornilla.append([Cantidad_1, a, a*Cantidad_1])
        a=float(Hornilla['Prelimpiador'].values)
        Valor_Hornilla.append([Cantidad_2, a, a*Cantidad_2])
        a=float(Hornilla['Válvula de la chimenea'].values)
        Cantidad=1
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Ladrillos refractarios'].values)
        Cantidad=1200*Total_pailas
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Pegante bulto'].values)
        Cantidad=6*Total_pailas
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Tubo sanitario'].values)
        Cantidad=math.ceil((0.017142857*Capacidad_hornilla)+2.714285714)
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Codos sanitarios'].values)
        Cantidad=math.ceil((0.017142857*Capacidad_hornilla)+0.714285714)
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Válvula de bola'].values)
        Cantidad=math.ceil((0.017142857*Capacidad_hornilla)+2.714285714)
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['férula sanitaria'].values)
        Cantidad=math.ceil(0.9*Total_pailas)
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Abrazadera sanitaria'].values)
        Cantidad=math.ceil(0.9*Total_pailas)
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Empaque de silicona'].values)
        Cantidad=math.ceil(0.9*Total_pailas)
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=float(Hornilla['Sección de parrilla'].values)	
        Cantidad=math.ceil(parrillas) #Traerlo
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        #Cambiarlo poner marco de puerta
        #Falta la tuberia del jugo crudo a la hornilla "Quitar accesorios"
        #Valvula de la chimenea $1000000
        #Quitar movilidad
        #por kilo arregla y verficar precio Fedepanela
        a=float(Hornilla['Marco de la puerta'].values)	
        Cantidad=math.ceil(Total_pailas/20)
        Valor_Hornilla.append([Cantidad, a, a*Cantidad])
        a=round(float(Hornilla['Paila melotera'].values)*Capacidad_hornilla/250)
        Valor_Hornilla.append([1, a, a*1])
    #    a=float(Hornilla['Accesorios paila melotera'].values)	
    #    Valor_Hornilla.append([1, a, a*1])    
        Valor_molino=math.ceil(sum(Valor_M)/len(Valor_M))
        Valor_Hornilla.append([1,Valor_molino,1*Valor_molino])
    #    a=float(Hornilla['Base molino'].values)	
    #    Valor_base_mol=math.ceil(a)
    #    Valor_Hornilla.append([1,Valor_base_mol,1*Valor_base_mol])
        #>>>>>>>>>>>>>>>>>>>>>>>>>total gastos de la hornilla
        total_hornilla=math.ceil(estimar_total(Valor_Hornilla))
        Valor_Hornilla.append([' ',' ',total_hornilla])
        """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
        Valor_Hornilla.insert(0,['Cantidad', 'Valor unitario', 'Valor Total'])
        if(k==0):
            Mem_total_Hornilla_1=total_hornilla
            D_Hornilla_1=dict(zip(Etiquetas_Hornilla,Valor_Hornilla)) 
        elif(k==1):
            Mem_total_Hornilla_2=total_hornilla
            D_Hornilla_2=dict(zip(Etiquetas_Hornilla,Valor_Hornilla)) 
        
    """>>>>>>>>>>>>----------COSTOS DEL RECUPERADOR DE CALOR------------<<<<<<<<<<<<"""
    Recuperador=pd.read_excel('static/Costos/Recuperador.xlsx')
    Valor_Recuperador=[]
    b=float(Recuperador['Recuperador exterior'].values)
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Recuperador interior'].values)	
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Serpentín semi-cilíndrico'].values)	
    Cantidad=Cantidad*2
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Serpentín plano'].values)
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Tubería y accesorios'].values)	
    Cantidad=math.ceil(Total_pailas/30)
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Ladrillo para las chimeneas'].values)	
    Cantidad=math.ceil(Total_pailas/30)*1000
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Pegante'].values)	
    Cantidad=math.ceil(Total_pailas/30)*8
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Sección metálica para las chimeneas'].values)
    Cantidad=math.ceil(Total_pailas/30)*4
    Valor_Recuperador.append([Cantidad, b, b*Cantidad])
    b=float(Recuperador['Bomba'].values)
    Valor_Recuperador.append([1, b, b*1])    
    b=float(Recuperador['Instrumentacion y control'].values)
    Valor_Recuperador.append([1, b, b*1])   
    #>>>>>>>>>>>>>>>>>>>>>>>>total gastos de recuperador
    total_recuperador=estimar_total(Valor_Recuperador) 
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
    Valor_Recuperador.append([' ',' ',total_recuperador])
    Valor_Recuperador.insert(0,['Cantidad', 'Valor unitario', 'Valor Total'])    
    Etiquetas_Recuperador=['Nombre',
                        'Recuperador exterior', 'Recuperador interior', 'Serpentín semicilíndrico', 'Serpentín plano',
                        'Tubería y accesorios', 'Ladrillo para la chimenea', 'Pegante','Sección metálica para la chimenea',
                        'Bomba','Instrumentación y control', 'Valor total del recuperador de calor']
    D_Recuperador=dict(zip(Etiquetas_Recuperador,Valor_Recuperador))    

    """>>>>>>>>>>>>----------COSTOS OPERATIVOS-------------<<<<<<<<<<<<"""
    #Construcción
    Operativos=pd.read_excel('static/Costos/Operativos.xlsx')
    D_Operativo_1={}
    D_Operativo_2={}
    D_Consolidado_1={}
    D_Consolidado_2={}
    
    for k in range(2):
        Valor_Operativo=[]
        if(k==0):
            Total_pailas=sum(Cantidad_pailas)
            c=float(Operativos['Ingeniero'].values)
            Valor_Operativo.append([1, c, c*6])
            c=float(Operativos['Maestro de obra'].values)*2
            Valor_Operativo.append([1, c, c*6])
            c=float(Operativos['Obrero'].values)	
            Cantidad=math.ceil(Total_pailas/2)
            Valor_Operativo.append([Cantidad, c, Cantidad*c*6])
        elif(k==1):
            Total_pailas=sum(Cantidad_pailas_rec)
            c=float(Operativos['Ingeniero'].values)*1.5
            Valor_Operativo.append([1, c, c*6])
            c=float(Operativos['Maestro de obra'].values)*2.5
            Valor_Operativo.append([1, c, c*6])
            c=float(Operativos['Obrero'].values)	
            Cantidad=math.ceil(Total_pailas/2)+1
            Valor_Operativo.append([Cantidad, c, Cantidad*c*6])            

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>Total gastos operativos
        total_operativos=estimar_total(Valor_Operativo)
        """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
        Valor_Operativo.append([' ',' ',total_operativos])
        Valor_Operativo.insert(0,['Cantidad', 'Valor Mes', 'Proyección (6 meses)'])    
        Etiquetas_Operativos=['Nombre', 'Estudio de ingeniería', 'Acopañamiento del constructor', 'Auxiliares de obra', 
                              'Total de gastos operativos']
        if(k==0):
            D_Operativo_1=dict(zip(Etiquetas_Operativos,Valor_Operativo))  
            """>>>>>>>>>>>>>>-------------TOTALES PROYECTO--------------<<<<<<<<<<<<<<<"""
            Costo_imprevistos=math.ceil(0.02*Mem_total_Hornilla_1)
            Consolidado_totales_1=[Mem_total_Hornilla_1, total_operativos, Costo_imprevistos]    
        elif(k==1):
            D_Operativo_2=dict(zip(Etiquetas_Operativos,Valor_Operativo))      
            """>>>>>>>>>>>>>>-------------TOTALES PROYECTO--------------<<<<<<<<<<<<<<<"""
            Costo_imprevistos=math.ceil(0.02*Mem_total_Hornilla_2)
            Consolidado_totales_2=[Mem_total_Hornilla_2+total_recuperador, total_operativos, Costo_imprevistos]    

    """>>>>>>>>>>>>>>>>>>>>>Codificar rótulo del informe sin recuperador<<<<<<<<<<<<<<<<"""
    Total_proyecto_1=sum(Consolidado_totales_1)
    Consolidado_totales_1.append(Total_proyecto_1)
    Consolidado_totales_1.insert(0,'Valor aproximado')    
    Etiquetas_Totales=['Descripción',
                       'Valor total de la construcción de la hornilla',
                       'Valor total del gasto operativo durante la construcción', 
                       'Seguro contra gastos imprevistos (2% del total)',
                       'Valor total de la obra civil'
                        ]
    D_Consolidado_1=dict(zip(Etiquetas_Totales,Consolidado_totales_1)) 
    
    """>>>>>>>>>>>>>>>>>>>>>Codificar rótulo del informe con recuperador<<<<<<<<<<<<<<<<"""    
    Total_proyecto_2=sum(Consolidado_totales_2)
    Consolidado_totales_2.append(Total_proyecto_2)
    Consolidado_totales_2.insert(0,'Valor aproximado')   
    Etiquetas_Totales=['Descripción',
                       'Valor total de la construcción con recuperador de calor',
                       'Valor total del gasto operativo durante la construcción', 
                       'Seguro contra gastos imprevistos (2% del total)',
                       'Valor total de la obra civil'
                        ]
    D_Consolidado_2=dict(zip(Etiquetas_Totales,Consolidado_totales_2)) 
    
    """>>>>-----------------COSTOS DE LA PRODUCCIÓN-------------------------<<<"""        
    lista_produccion_1=[]
    lista_produccion_2=[]
        
    for k in range(2):        
        #Variables
        Valor_Cana=float(Operativos['Tonelada de Caña'].values)	
        Galon_diesel=float(Operativos['Galon diesel'].values)		
        P_KWh=float(Operativos['Precio kWh'].values)	
        Mtto=float(Operativos['Mantenimiento'].values)
        Valor_operario=float(Operativos['Operarios'].values)
        Precio_otros_dia=float(Operativos['Valor otros'].values)
        Produ_diaria=Horas_trabajo_al_dia*Capacidad_hornilla
        #>>>>>>>>>>>>>>>>>>>>>Calculos de los Molinos<<<<<<<<<<<<<<<<<<
        #Calculos del molino con motores eléctricos     
        Potencia_e=sum(Electrico)/len(Electrico)
        Eficiencia=0.875		
        PA=((Potencia_e*0.75)/Eficiencia)
        Consumo=PA*Horas_trabajo_al_dia
        Precio_KWh=P_KWh
        Consumo_Motor=Precio_KWh*Consumo
        Costo_kg_Motor=math.ceil(Consumo_Motor/Produ_diaria)
        #Calculos del molino con motores eléctricos de combustion Diesel		
        Potencia_d=sum(Diesel)/len(Diesel)
        Eficiencia=30	
        Consumo=((Potencia_d)/Eficiencia)*Horas_trabajo_al_dia
        Precio_Galon_Diesel=Galon_diesel
        Consumo_Diesel =	Precio_Galon_Diesel*Consumo 
        Costo_kg_Diesel=math.ceil(Consumo_Diesel/Produ_diaria)
        #Potencia disipada por el controlador y la bomba del evaporador   
        Activaciones=Horas_trabajo_al_dia*0.1
        Watts=3000 #Consumo aproximado de la bomba y el controlador
        Consumo=Watts*Activaciones
        Precio_KWh=P_KWh
        Consumo_Controlador=Precio_KWh*Consumo
        Total_Control=math.ceil(Consumo_Controlador/Produ_diaria)
        
        if(k==0):
            Costo_kg_control=0
        elif(k==1):
            Costo_kg_control=math.ceil(Total_Control/Produ_diaria)
            
        # >>>>>>>>>>>>>>>>>>>> Materia Prima<<<<<<<<<<<<<<<<<<<<<<<<<<	
        #Multiplico por 1000 para pasar de KG/h a litros
        Relacion=(Toneladas_cana_a_moler/numero_moliendas)/(Capacidad_hornilla*1000)
    
        Costo_kg_cana=math.ceil(Valor_Cana*Relacion)
        #Otros insumos Cera, Empaques, Clarificante			
        Costo_kg_otros=math.ceil(Precio_otros_dia/Produ_diaria)
        #Costo personal			
        if(k==0):
            Numero_Operarios=Total_pailas-2
        elif(k==1):
            Numero_Operarios=Total_pailas-3
        Valor_Contrato=Valor_operario*Numero_Operarios
        Costo_kg_Contrato=math.ceil(Valor_Contrato/Produ_diaria)			
        #Costo Mantenimiento			
        
        Costo_kg_Mtto=math.ceil(Mtto/(Produ_diaria*Dias_trabajo_semana*4*12))
        """>>>>>>>>>>>>>>-------------TOTALES PRODUCCION--------------<<<<<<<<<<<<<<<"""
        Consolidado_totales_2=[Costo_kg_Motor, Costo_kg_control, Costo_kg_cana, Costo_kg_otros, Costo_kg_Mtto, Costo_kg_Contrato]
        Costo_total_kg=sum(Consolidado_totales_2)
        if(k==0):
            lista_produccion_1=Consolidado_totales_2
            lista_produccion_1.append(Costo_total_kg)
            lista_produccion_1.insert(0,Capacidad_hornilla)
            lista_produccion_1.insert(0,'NO')
        elif (k==1):
            lista_produccion_2=Consolidado_totales_2
            lista_produccion_2.append(Costo_total_kg)
            lista_produccion_2.insert(0,Capacidad_hornilla)
            lista_produccion_2.insert(0,'SI')
    
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""  
    Etiquetas_produccion=['¿El diseño incorpora recuperador de calor?',
                          'Capacidad de la hornilla [kg/h]',
                          'Costo de funcionamiento del molino por kg (Motor eléctrico)', 
                          'Costo de funcionamiento del controlador por kg',
                          'Costo del kg de caña',
                          'Costo de los insumos para la producción (Cera-Empaques-Clarificante)',
                          'Costo del mantenimiento de la hornilla por kg',
                          'Costo de los operarios por kg',
                          'Valor total del kg de caña'
                          ]
    lista1=[]
    for i in range(len(lista_produccion_1)):
        lista1.append([lista_produccion_1[i], lista_produccion_2[i]])
    D_Produccion=dict(zip(Etiquetas_produccion,lista1))    
       
    """>>>>>>>>>>>>>>>>>>>>----------------COSTO FINANCIERO---------------------<<<<<<<<<"""
    mem_total_proyecto=0
    lista_financiero_1=[]
    lista_financiero_2=[]   
    lista_Depreciacion1=[]
    lista_Depreciacion2=[]     
        
    for k in range(2):
        if(k==0):
            Total_proyecto=Total_proyecto_1
            Valor_panela=float(Operativos['Costo panela por kg'].values)*1.2
        elif (k==1):
            Total_proyecto=Total_proyecto_2
            Valor_panela=float(Operativos['Costo panela por kg'].values)
            
        Interes=float(Operativos['Tasa interes'].values)
        t_anos=float(Operativos['Anos depreciacion'].values)
        Costo_financiero=(Total_proyecto*(1+Interes)**t_anos)-Total_proyecto
        """>>>>>>>>>>>>-------------GANACIAS DE LA PANELA-----------<<<<<<<<<<<<<<<<<<<<<<<"""
        
        Produccion_mensual_kg=Capacidad_hornilla*Horas_trabajo_al_dia*Dias_trabajo_semana*numero_moliendas
        Produccion_anual_kg=Produccion_mensual_kg*12
        Ingreso_anual=Valor_panela*Produccion_anual_kg
        """>>>>>>>>>>>>>>>>>>>>--------------------DEPRECIACION---------------<<<<<<<<<<<<<<<<<"""
        Valor_Inicial=Total_proyecto
        Vida_util_anos_horn=int(Operativos['vida util hornilla'].values)
        Valor_Salvamento=Total_proyecto*0.05
        Depreciacion_anual=math.ceil((Valor_Inicial-Valor_Salvamento)/Vida_util_anos_horn)
        Depreciacion=[]
        Depreciacion.append(round(Valor_Inicial,3))
        for ano in range(1,Vida_util_anos_horn):
            Depreciacion.append(round(Depreciacion[ano-1]-Depreciacion_anual,3))
        if(k==0):
            lista_financiero_1=[Vida_util_anos_horn, 
                                Interes, 
                                t_anos, 
                                Valor_panela, 
                                math.ceil(Costo_financiero), 
                                round(Depreciacion_anual,0), 
                                round(Produccion_mensual_kg,0),  
                                round(Produccion_anual_kg,0),  
                                round(Valor_Salvamento,0),  
                                round(Ingreso_anual,0)]
            lista_Depreciacion1=Depreciacion
            lista_financiero_1.insert(0,'SI')
        elif (k==1):
            lista_financiero_2=[' ', ' ', ' ', Valor_panela, 
                                math.ceil(Costo_financiero), Depreciacion_anual, Produccion_mensual_kg, 
                                Produccion_anual_kg, Valor_Salvamento, Ingreso_anual]
            lista_Depreciacion2=Depreciacion
            lista_financiero_2.insert(0,'NO')
                
        """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""  
        Etiquetas_financiacion=['¿El diseño incorpora recuperador de calor?',
                              'Vida útil estimada de la hornilla (años)',
                              'Tasa de interés de la financiación',
                              'Tiempo mínimo para recuperar la inversión (años)', 
                              'Valor de la panela para el cálculo ', 
                              'Costo financiero',
                              'Depreciación anual',
                              'Producción mensual (kg)',
                              'Producción anual en (kg)',
                              'Valor de salvamento (5% del total del costo de la hornilla)',
                              'Ingreso anual aproximado'                          
                              ]
    
    Memoria_Temp=lista_financiero_1[5]
    lista_financiero_1[5]=lista_financiero_2[5]
    lista_financiero_2[5]=Memoria_Temp    

    Memoria_Temp=lista_financiero_1[6]
    lista_financiero_1[6]=lista_financiero_2[6]
    lista_financiero_2[6]=Memoria_Temp  

    Memoria_Temp=lista_financiero_1[9]
    lista_financiero_1[9]=lista_financiero_2[9]
    lista_financiero_2[9]=Memoria_Temp 
            
    lista1=[]
    for i in range(len(lista_financiero_1)):
        lista1.append([lista_financiero_1[i], lista_financiero_2[i]])
    D_Financiero=dict(zip(Etiquetas_financiacion,lista1))  
    
    Bandera=0
    if(Capacidad_hornilla<=150):
        Bandera=0
    else:
        Bandera=1
    ###########>>>>>>>>>>>>>>>>>>>>>>Graficar Depreciación<<<<<<<<<<<<<<<<<<<<<################
    Fig_1,a = plt.subplots(frameon=False)
    l1,=a.plot(range(len(lista_Depreciacion2)),np.array(lista_Depreciacion2)/1000000, linewidth=4)
    if(Bandera==0):
        l2,=a.plot(range(len(lista_Depreciacion1)),np.array(lista_Depreciacion1)/1000000, linewidth=4)
    a.grid(color='k', linestyle='--', linewidth=1)
    a.set_ylabel('Valor (X $1.000.000)', fontsize=18)
    a.set_xlabel('Vida útil de la hornilla (Años)', fontsize=18)
    a.set_title('Depreciación del equipo', fontsize=20)
    if(Bandera==0):
        a.legend([l1, l2],["Con recuperador", "Sin recuperador"])  
    for item in [Fig_1,a]:
           item.patch.set_visible(False)
    FigureCanvasAgg(Fig_1).print_png('static/Latex/Graficas/Depreciacion.png')       
    ############################################################################################
        
    """>>>>>>>>>>>>>>>>>>>>--------------------FLUJO DE CAJA---------------<<<<<<<<<<<<<<<<<"""
    mem_total_proyecto=Total_proyecto  
    lista_costo_produccion_1=[]  
    lista_costo_produccion_2=[] 
    lista_flujo_1=[]  
    lista_flujo_2=[] 
    #Ruido del flujo de caja
    Ruido=(lista_financiero_2[10]/4)*np.random.rand(Vida_util_anos_horn)
    mem_ruido=0
    for k in range(2):
        if(k==0):
            Total_proyecto=mem_total_proyecto-total_recuperador
            Costo_financiero=lista_financiero_1[5]
            Depreciacion_anual=lista_financiero_1[6]
            Produccion_anual_kg=lista_financiero_1[8]
            Valor_Salvamento=lista_financiero_1[9]
            Ingreso_anual=lista_financiero_1[10]   
            Costo_total_kg=lista_produccion_1[8]
            mem_ruido=Ingreso_anual
        elif (k==1):
            Total_proyecto=mem_total_proyecto
            Costo_financiero=lista_financiero_2[5]
            Depreciacion_anual=lista_financiero_2[6]
            Produccion_anual_kg=lista_financiero_2[8]
            Valor_Salvamento=lista_financiero_2[9]
            Ingreso_anual=lista_financiero_2[10]   
            Costo_total_kg=lista_produccion_2[8]
            mem_ruido=Ingreso_anual
        #Depreciación Anual, Mtto, Ingresos, Flujo de caja
        Estado_caja=[0, 0, 0, Valor_Salvamento-(Total_proyecto+Costo_financiero)]
        Lista_caja=[]
        Lista_caja.append(Estado_caja)
        flujo_caja=[]
        flujo_caja.append(Estado_caja[3])
        Costo_produccion=[]
        for ano in range(1,Vida_util_anos_horn):
            Estado_caja=[Depreciacion_anual, 
                         Produccion_anual_kg*Costo_total_kg, 
                         Ingreso_anual, 
                         Ingreso_anual-(Depreciacion_anual+(Produccion_anual_kg*Costo_total_kg))]
            Ingreso_anual=mem_ruido-Ruido[ano]
            Lista_caja.append(Estado_caja)
            Costo_produccion.append(Estado_caja[1])
            flujo_caja.append(Estado_caja[3])
        if(k==0):
            lista_costo_produccion_1=Costo_produccion   
            lista_flujo_1=flujo_caja 
        elif (k==1):
            lista_costo_produccion_2=Costo_produccion   
            lista_flujo_2=flujo_caja 
    
    ###########>>>>>>>>>>>>>>>>>>>>>>Graficar flujo de caja<<<<<<<<<<<<<<<<<<<<<################
    #Sin recuperador
    Fig_2,b = plt.subplots(frameon=False)#, figsize=(8,10))
    m1=max(np.array(lista_flujo_1)/(1000000))
    m2=max(np.array(lista_flujo_2)/(1000000))
    m3=min(np.array(lista_flujo_1)/(1000000))
    m4=min(np.array(lista_flujo_2)/(1000000))   
    lim_max=0
    lim_min=0
    if(m1>m2):
        lim_max=m1
        l1 =b.barh(range(len(lista_flujo_1)),np.array(lista_flujo_1)/(1000000),edgecolor='black',hatch="/")
        if(Bandera==0):
            l2 =b.barh(range(len(lista_flujo_2)),np.array(lista_flujo_2)/(1000000),edgecolor='black',hatch="o")
    else:
        lim_max=m2
        if(Bandera==0):
            l2 =b.barh(range(len(lista_flujo_2)),np.array(lista_flujo_2)/(1000000),edgecolor='black',hatch="o")
        l1 =b.barh(range(len(lista_flujo_1)),np.array(lista_flujo_1)/(1000000),edgecolor='black',hatch="/")
    if(m3<m4):
        lim_min=m3
    else:
        lim_min=m4        

    b.set_xlim([lim_min-10,lim_max+10])
    b.grid(color='k', linestyle='--', linewidth=1)
    b.set_ylabel('Tiempo (Años)', fontsize=22)
    b.set_xlabel('Costo * ($1.000.000)', fontsize=22)
    b.set_title('Flujo de caja aproximado', fontsize=20)
    if(Bandera==0):
        b.legend([l1, l2],["Con recuperador", "Sin recuperador"], fontsize=14)
    for item in [Fig_2,b]:
           item.patch.set_visible(False)    
    FigureCanvasAgg(Fig_2).print_png('static/Latex/Graficas/Flujo_Caja_1.png') 

    """>>>>>>------RETORNO A LA INVERSION----<<<<"""
    Retorno_inversion1=[]  
    Retorno_inversion2=[] 
    
    for k in range(2):
        if(k==0):
            Costo_produccion=lista_costo_produccion_1
            flujo_caja=lista_flujo_1
            Produccion_anual_kg=lista_financiero_1[8]
            Valor_panela=float(Operativos['Costo panela por kg'].values)
        elif (k==1):
            Costo_produccion=lista_costo_produccion_2
            flujo_caja=lista_flujo_2
            Produccion_anual_kg=lista_financiero_2[8]
            Valor_panela=float(Operativos['Costo panela por kg'].values)
            
        Retorno_inversion=[]    
        for i in Costo_produccion:
            Ingreso_esperado=Valor_panela*Produccion_anual_kg
            Ganancia_Acumulada=(Ingreso_esperado-i)/100
            Valor_Proyecto=round(flujo_caja[0],3)
            if(Ganancia_Acumulada==0):
                Ganancia_Acumulada=0.1
            Tiempo_anos=round(-Valor_Proyecto/Ganancia_Acumulada,3)
            Estado_retorno=[Valor_panela, 
                            i, 
                            Ingreso_esperado,
                            Ganancia_Acumulada,  
                            Valor_Proyecto, 
                            Tiempo_anos, 
                            Tiempo_anos*12]
            Valor_panela=Valor_panela+75#+random.uniform(-500, 500)
            Retorno_inversion.append(Estado_retorno)
        if(k==0):
            Retorno_inversion1=Retorno_inversion
        elif (k==1):
            Retorno_inversion2=Retorno_inversion
    MA=np.array(Retorno_inversion1)
    lista_valor_panela1=MA[:,0]
    Anos1=MA[:,5]
    Meses1=MA[:,6]
    
    MB=np.array(Retorno_inversion2)
    lista_valor_panela2=MB[:,0]
    Anos2=MB[:,5]
    Meses2=MB[:,6]
    ###########>>>>>>>>>>>>>>>>>Graficar Retorno a la inversión<<<<<<<<<<<<<<<<<################
    Fig_3,d = plt.subplots(frameon=False)#, figsize=(8,10))
    l1,=d.plot(lista_valor_panela1,Anos1, linewidth=4)
    if(Bandera==0):
        l2,=d.plot(lista_valor_panela2,Anos2, linewidth=4)
    d.grid(color='k', linestyle='--', linewidth=1)
    d.set_ylabel('Time (years)', fontsize=20)
    d.set_xlabel('NCS value (USD)', fontsize=20)    
    d.set_ylabel('Funcionamiento (Años)', fontsize=18)
    d.set_xlabel('Valor de la panela (COP)', fontsize=18)
    d.set_title('Tiempo de retorno a la inversión', fontsize=20)
    if(Bandera==0):
        d.legend([l1, l2],["Con recuperador", "Sin recuperador"], fontsize=14)
    for item in [Fig_3,d]:
           item.patch.set_visible(False)
    FigureCanvasAgg(Fig_3).print_png('static/Latex/Graficas/RI_Anos.png') 
    ############################################################################################
    ###########>>>>>>>>>>>>>>>>>Graficar Retorno a la inversión<<<<<<<<<<<<<<<<<################
    Fig_4,e = plt.subplots(frameon=False)
    l1,=e.plot(lista_valor_panela1,Meses1, linewidth=4)
    if(Bandera==0):
        l2,=e.plot(lista_valor_panela2,Meses2, linewidth=4)   
    e.grid(color='k', linestyle='--', linewidth=1)
    e.set_ylabel('Funcionamiento de la hornilla (meses)', fontsize=18)
    e.set_xlabel('Valor de la panela (COP)', fontsize=18)
    e.set_title('Tiempo de retorno a la inversión', fontsize=20)
    if(Bandera==0):
        e.legend([l1, l2],["Con recuperador", "Sin recuperador"])
    for item in [Fig_4,e]:
           item.patch.set_visible(False)
    with open('static/Latex/Graficas/RI_Meses.png', 'wb') as f:
        FigureCanvasAgg(Fig_4).print_png(f)     
            
    plt.close(Fig_1)
    plt.close(Fig_2)
    plt.close(Fig_3)
    plt.close(Fig_4)
    del(Fig_1)
    del(Fig_2)
    del(Fig_3)
    del(Fig_4) 
    
    sleep(1)
    Proyeccion_economica.Documento_Latex.portada('SIN')
    Proyeccion_economica.Documento_Latex.Horn_sin(D_Hornilla_1, D_Operativo_1, D_Consolidado_1, D_Produccion, D_Financiero)
    Proyeccion_economica.Documento_Latex.generar_pdf('A6_informe1', 'pdf01/')
    Proyeccion_economica.Documento_Latex.portada('CON')
    Proyeccion_economica.Documento_Latex.Horn_con(D_Hornilla_2, D_Recuperador, D_Operativo_2, D_Consolidado_2, D_Produccion, D_Financiero)
    Proyeccion_economica.Documento_Latex.generar_pdf('A6_informe2', 'pdf03/')
    
    return [Total_proyecto_1, Total_proyecto_2]
    ############################################################################################