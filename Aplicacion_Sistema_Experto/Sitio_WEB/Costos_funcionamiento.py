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
#Definición de las variables globales
global Capacidad_hornilla
global Molino_seleccionado
global Horas_trabajo_al_dia

###Rutinas para generar el pdf del costo
#Layout del informe
def Fondo(canvas):
    #Dibujar logo y membrete de AGROSAVIA
#    canvas.drawImage('static/Iconos/Agrosavia.jpg', 420, 720, width=150, height=40)
#    canvas.drawImage('static/Iconos/Membrete.png' , 0, 0, width=650, height=240)
#    canvas.drawImage('static/Iconos/Membrete2.png', 0, 650, width=150, height=150)  
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
    
#Función para generar la parte escrita del informe
def Generar_reporte_financiero(D1, D2, D3, D4, D5, D6):
    #Genera la vista previa
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf01/A6_informe.pdf", pagesize=letter)
    canvas = Fondo(canvas)
    #Hoja=1
    for k in range(3):
        canvas.setFont('Helvetica-Bold', 12)
        """----------->>>>>>> Publicar Calculos por etapa<<<<<<<<<<<------------"""
        #Publicar calculos de la hornilla
        if(k==0):
            Diccionario=D1
            puntero_v=640
            puntero_h=50
        elif(k==1):
            Diccionario=D2
            puntero_v=640
            puntero_h=50
        elif(k==2):
            Diccionario=D3
        Etiquetas=list(dict.keys(Diccionario))
        for i in Etiquetas:
            canvas.setFont('Helvetica-Bold', 11)
            canvas.drawString(puntero_h, puntero_v, i)
            #Función para dibujar los valores de la Tabla    
            Valores=Diccionario[i]
            puntero_h=puntero_h+300
            for j, vector in enumerate(Valores):
                Texto=str(vector)
                if(i=='Nombre'):
                    canvas.setFont('Helvetica-Bold', 9)
                elif((i=='Valor total de la hornilla') 
                        or (i=='Valor total del recuperador de calor') 
                        or (i=='Total de gastos operativos')):
                    canvas.setFillColorRGB(0,0,0)
                    canvas.setFont('Helvetica-Bold', 9)
                    if(j>1):
                        try:
                            Texto=Formato_Moneda(float(Texto), "$", 2)
                        except:
                            print('Error '+Texto)
                else:
                    canvas.setFont('Helvetica', 9)
                    if(j>0):
                        try:
                            Texto=Formato_Moneda(float(Texto), "$", 2)
                        except:
                            print('Error '+Texto)
                        
                canvas.drawString(puntero_h, puntero_v, Texto) 
                puntero_h=puntero_h+80
            puntero_v=puntero_v-15
            puntero_h=50
            if(puntero_v<=30):
                canvas.showPage()
                puntero_v=640
        if(k==0):
            canvas.setFillColorRGB(0,0,0)
            canvas.setFont('Helvetica-Bold', 14)
            canvas.drawString(190,680,'--->>>COSTO DE LA HORNILLA<<<---')
            canvas.setFont('Helvetica-Oblique', 10)
            canvas.drawString(puntero_h, puntero_v-10, "Nota: El acero usado en la construcción de la hornilla es inoxidable 304.") 
            canvas.showPage()
            canvas=Fondo(canvas)
            puntero_v=640
            canvas.setFillColorRGB(0,0,0)
            canvas.setFont('Helvetica-Bold', 14)
            canvas.drawString(140,680,'--->>>COSTO DEL RECUPERADOR DE CALOR<<<---')
        elif(k==1):
            canvas.setFillColorRGB(0,0,0)
            canvas.setFont('Helvetica-Oblique', 10)
            puntero_v=puntero_v-10
            canvas.drawString(puntero_h, puntero_v, "Nota: El acero usado en la construcción del recuperador de calor es inoxidable 304.")
            canvas.setFont('Helvetica-Bold', 14)
            puntero_v=puntero_v-40
            canvas.drawString(202, puntero_v,'--->>>GASTOS OPERATIVOS<<<---')  
            puntero_v=puntero_v-40
            
    canvas.setFillColorRGB(0,0,0)       
    canvas.setFont('Helvetica-Bold', 14)
    puntero_v=puntero_v-40
    canvas.drawString(200, puntero_v,'--->>>CONSOLIDADO PARCIAL<<<---')  
    puntero_v=puntero_v-40
    Diccionario=D4
    Etiquetas=list(dict.keys(Diccionario))
    for i in Etiquetas:
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(puntero_h, puntero_v, i)
        #Función para dibujar los valores de la Tabla    
        Valores=Diccionario[i]
        puntero_h=puntero_h+425
        Texto=str(Valores)
        if(i=='Descripción'):
            canvas.setFont('Helvetica-Bold', 11)
        elif((i=='Valor total de la construcción con recuperador de calor') 
                or (i=='Valor total de la construcción sin recuperador de calor')):
            canvas.setFillColorRGB(0,0,0)
            canvas.setFont('Helvetica-Bold', 9)
            Texto=Formato_Moneda(float(Texto), "$", 2)
        else:
            canvas.setFont('Helvetica', 9)
            Texto=Formato_Moneda(float(Texto), "$", 2)
        canvas.drawString(puntero_h, puntero_v, Texto) 
        canvas.setFillColorRGB(0,0,0)
        puntero_v=puntero_v-15
        puntero_h=50
        if(puntero_v<=30):
            canvas.showPage()
            puntero_v=640
            
    canvas.showPage()
    canvas=Fondo(canvas)
    canvas.setFillColorRGB(0,0,0)       
    canvas.setFont('Helvetica-Bold', 14)
    puntero_v=680
    canvas.drawString(80, puntero_v,'--->>>COSTO DE FUNCIONAMIENTO DE LA HORNILLA POR KG<<<---')  
    puntero_v=640
    Diccionario=D5
    Etiquetas=list(dict.keys(Diccionario))
    for i in Etiquetas:
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(puntero_h, puntero_v, i)
        #Función para dibujar los valores de la Tabla    
        Valores=Diccionario[i]
        puntero_h=puntero_h+400
        for j, vector in enumerate(Valores):
            Texto=str(vector)
            if((i=='¿El diseño incorpora recuperador de calor?') or (i=='Capacidad de la hornilla [kg/h]')):
                canvas.setFont('Helvetica-Bold', 11)
            elif(i=='Valor total del kg de caña'):
                canvas.setFillColorRGB(0,0,0)
                canvas.setFont('Helvetica-Bold', 9)
                Texto=Formato_Moneda(float(Texto), "$", 2)
            else:
                canvas.setFont('Helvetica', 9)
                Texto=Formato_Moneda(float(Texto), "$", 2)
            canvas.drawString(puntero_h, puntero_v, Texto) 
            puntero_h=puntero_h+80
        puntero_v=puntero_v-15
        puntero_h=50
        if(puntero_v<=30):
            canvas.showPage()
            puntero_v=640
    canvas.setFillColorRGB(0,0,0)
    canvas.setFont('Helvetica-Oblique', 10)
    puntero_v=puntero_v-10
    canvas.drawString(puntero_h, puntero_v, "Nota: Cuando el diseño de la hornilla incorpora recuperador de calor se estima un aumento de la capacidad de la")
    puntero_v=puntero_v-10
    canvas.drawString(puntero_h, puntero_v, "hornilla hasta de un 40%.")
    canvas.setFont('Helvetica-Bold', 14)
    puntero_v=puntero_v-40
    canvas.drawString(180, puntero_v,'--->>>GASTOS DE FINANCIACIÓN<<<---')  
    puntero_v=puntero_v-40 

    Diccionario=D6
    Etiquetas=list(dict.keys(Diccionario))
    for numero_i, i in enumerate (Etiquetas, start=0):
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(puntero_h, puntero_v, i)
        #Función para dibujar los valores de la Tabla    
        Valores=Diccionario[i]
        puntero_h=puntero_h+350
        for j, vector in enumerate(Valores):
            Texto=str(vector)
            if(i=='¿El diseño incorpora recuperador de calor?'):
                canvas.setFont('Helvetica-Bold', 9)
            elif(i=='Ingresos anuales aproximados ($)'):
                canvas.setFillColorRGB(0,0,0)
                canvas.setFont('Helvetica-Bold', 9)          
            else:
                canvas.setFont('Helvetica', 9)
            if(numero_i<4 or (numero_i>6 and numero_i<9)):
                canvas.drawString(puntero_h, puntero_v, Texto) 
            else:
                try:
                    canvas.drawString(puntero_h, puntero_v, Formato_Moneda(float(Texto), "$", 2)) 
                except:
                    print(Texto)
            puntero_h=puntero_h+80
        puntero_v=puntero_v-15
        puntero_h=50
        if(puntero_v<=30):
            canvas.showPage()
            puntero_v=640
            
    canvas.showPage()
    canvas=Fondo(canvas)
    canvas.drawImage('static/Graficas/Depreciacion.png', 40, 480, width=280, height=200)
    canvas.drawImage('static/Graficas/Flujo_Caja_1.png', 330, 480, width=280, height=200)
    canvas.drawImage('static/Graficas/RI_Meses.png', 40, 190, width=280, height=200)
    canvas.drawImage('static/Graficas/RI_Anos.png', 330, 190, width=280, height=200)                         
    canvas.save()
    
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
    Archivo_Temporal=xlrd.open_workbook('static/Temp/Temp2.xlsx')
    libro = Archivo_Temporal.sheet_by_index(0)
    Tipo_de_Pailas=[]
    Cantidad_pailas=[]
    for i in range(len(libro.row(1))):
        Tipo_de_Pailas.append(libro.row(1)[i].value)
        Cantidad_pailas.append(libro.row(2)[i].value)
    Tipo_de_Pailas=Tipo_de_Pailas[1:]
    Cantidad_pailas=Cantidad_pailas[1:]
    """>>>>>>>>>>>>-----------IMPORTAR MOLINOS-------------<<<<<<<<<<<<<<<"""
    Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
    Diesel=Molino['Diesel'].values
    Electrico=Molino['Electrico'].values
    Valor_M=Molino['Precio'].values      
    """>>>>>>>>>>>>-----------COSTOS DEL PROYECTO-------------<<<<<<<<<<<<"""
    """>>>>>>>>>>>>----------Costos de la hornilla-------------<<<<<<<<<<<<"""
    Valor_Hornilla=[]
    Total_pailas=sum(Cantidad_pailas)
    Hornilla=pd.read_excel('static/Costos/Hornilla.xlsx')   
    #>>>>>>>>>Pailas<<<<<<<<<#
    Pailas_disponibles_1=['plana', 'plana SA', 'pirotubular circular','pirotubular circular SA',
                        'semiesférica', 'semicilindrica', 'semicilindrica SA', 'cuadrada', 'cuadrada SA',
                        'acanalada', 'acanalada SA']
    Pailas_disponibles_2=['Paila plana', 'Paila plana sin aletas', 'Paila pirotubular circular', 
                          'Paila pirotubular circular sin aletas', 'Paila semiesférica', 'Paila semicilindrica', 
                          'Paila semicilindrica sin aletas', 'Paila pirotubular cuadrada', 'Paila pirotubular cuadrada sin aletas', 
                          'Paila acanalada con canales cuadrados','Paila acanalada con canales cuadrados y sin aletas']
    Etiquetas_Hornilla=['Nombre']
    #Crear un vector con la cantidad de pailas
    for pun_i in range(len(Pailas_disponibles_1)):
        if(Cantidad_pailas[pun_i]>0):
            a=float(Hornilla[Pailas_disponibles_1[pun_i]].values)
            a=a*((0.004*Capacidad_hornilla)+0.2)
            Valor_Hornilla.append([Cantidad_pailas[pun_i], a, a*Cantidad_pailas[pun_i]])  
            Etiquetas_Hornilla.append(Pailas_disponibles_2[pun_i])
    
    #Revisar cantidad de valvulas
    #>>>>>>>>>>Otros accesorios de la hornilla<<<<<<<<<<<<<#
    Accesorios_disponibles=['Prelimpiador 1', 'Prelimpiador 2', 'Válvula de la chimenea', 'Ladrillos refractarios', 'Pegante bulto', 'Tubo acero inxidable de 3 pulgadas',
                        'Codos sanitarios de 3 pulgadas','Válvula de bola de 3 pulgadas', 'Férula sanitaria de 3 pulgadas',
                        'Abrazadera sanitaria de 3 pulgadas', 'Empaque de silicona de 3 pulgadas (alta temperatura)',
                        'Sección de parrilla', 'Marco de la puerta','Paila melotera', 'Valor aproximado del molino',
                        'Valor total de la hornilla']
    #vector de accesorios
    for pun_i in range(len(Accesorios_disponibles)):
        Etiquetas_Hornilla.append(Accesorios_disponibles[pun_i])    
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
    #Falta la tuberia del jugo crudo a la hornilla "Quitar accesolrios"
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
    D_Hornilla=dict(zip(Etiquetas_Hornilla,Valor_Hornilla))  

    """>>>>>>>>>>>>----------Costos recuperador de calor------------<<<<<<<<<<<<"""
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
    """>>>>>>>>>>>>----------Costos operativos-------------<<<<<<<<<<<<"""
    #Construcción
    Operativos=pd.read_excel('static/Costos/Operativos.xlsx')
    Valor_Operativo=[]
    c=float(Operativos['Ingeniero'].values)
    Valor_Operativo.append([1, c, c*6])
    c=float(Operativos['Maestro de obra'].values)
    Valor_Operativo.append([2, c, c*12])
    c=float(Operativos['Obrero'].values)	
    Cantidad=math.ceil(Total_pailas/4)
    Valor_Operativo.append([Cantidad, c, Cantidad*c*6])
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>Total gastos operativos
    total_operativos=estimar_total(Valor_Operativo)
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
    Valor_Operativo.append([' ',' ',total_operativos])
    Valor_Operativo.insert(0,['Cantidad', 'Valor Mes', 'Valor 3 Meses'])    
    Etiquetas_Operativos=['Nombre', 'Profesional titulado', 'Maestro de obra', 'Obrero', 
                          'Total de gastos operativos']
    D_Operativo=dict(zip(Etiquetas_Operativos,Valor_Operativo))  

    """>>>>>>>>>>>>>>-------------TOTALES PROYECTO--------------<<<<<<<<<<<<<<<"""
    Costo_imprevistos=math.ceil(0.02*total_hornilla)
    Consolidado_totales_1=[total_hornilla, total_recuperador, total_operativos, Costo_imprevistos]#, float(Operativos['Movilidad'])]
    Total_proyecto=sum(Consolidado_totales_1)
    """>>>>>>>>>>>>>>>>>>>>>Codificar rotulo del informe<<<<<<<<<<<<<<<<"""
    Consolidado_totales_1.append(Total_proyecto)
    Consolidado_totales_1.append(Total_proyecto-total_recuperador)
    Consolidado_totales_1.insert(0,'Valor aproximado')    
    Etiquetas_Totales=['Descripción',
                       'Valor total de la construcción de la hornilla',
                       'Valor total de la construcción del recuperador de calor', 
                       'Valor total del gasto operativo durante la construcción', 
                       'Seguro contra gastos imprevistos (2% del total de la construcción de la hornilla)',
                       #'Movilidad',
                       'Valor total de la construcción con recuperador de calor',
                       'Valor total de la construcción sin recuperador de calor',
                        ]
    D_Consolidado=dict(zip(Etiquetas_Totales,Consolidado_totales_1))    
    L_etiquetas_aux_excel1=[Etiquetas_Totales,Consolidado_totales_1]
    mem_capacidad=Capacidad_hornilla
    lista_produccion_1=[]
    lista_produccion_2=[]
    for k in range(2):    
        """>>>>-----------------COSTOS DE LA PRODUCCIÓN-------------------------<<<"""
        if(k==0):
            Capacidad_hornilla=mem_capacidad
        elif (k==1):
            Capacidad_hornilla=mem_capacidad+25

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
        # >>>>>>>>>> Materia Prima	
        #Multiplico por 1000 para pasar de KG/h a litros
        Relacion=(Toneladas_cana_a_moler/numero_moliendas)/(Capacidad_hornilla*1000)
    
        Costo_kg_cana=math.ceil(Valor_Cana*Relacion)
        #Otros insumos Cera, Empaques, Clarificante			
        Costo_kg_otros=math.ceil(Precio_otros_dia/Produ_diaria)
        #Costo personal			
        Numero_Operarios=Total_pailas-2
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
    L_etiquetas_aux_excel2=[Etiquetas_produccion,lista1]
    
    """>>>>>>>>>>>>>>>>>>>>----------------COSTO FINANCIERO---------------------<<<<<<<<<"""
    mem_capacidad=Capacidad_hornilla
    mem_total_proyecto=Total_proyecto
    lista_financiero_1=[]
    lista_financiero_2=[]   
    lista_Depreciacion1=[]
    lista_Depreciacion2=[]      
    for k in range(2):
        if(k==0):
            Total_proyecto=mem_total_proyecto-total_recuperador
            Capacidad_hornilla=mem_capacidad+25
        elif (k==1):
            Total_proyecto=mem_total_proyecto
            Capacidad_hornilla=mem_capacidad
            
        Interes=float(Operativos['Tasa interes'].values)
        t_anos=float(Operativos['Anos depreciacion'].values)
        Costo_financiero=(Total_proyecto*(1+Interes)**t_anos)-Total_proyecto
        """>>>>>>>>>>>>-------------GANACIAS DE LA PANELA-----------<<<<<<<<<<<<<<<<<<<<<<<"""
        Valor_panela=float(Operativos['Costo panela por kg'].values)
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
            lista_financiero_2=[' ', ' ', ' ', ' ', 
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
    
#    Memoria_Temp=lista_financiero_2[10]
#    lista_financiero_2[10]=lista_financiero_1[10]
#    lista_financiero_1[10]=Memoria_Temp 
        
    lista1=[]
    for i in range(len(lista_financiero_1)):
        lista1.append([lista_financiero_1[i], lista_financiero_2[i]])
    D_Financiero=dict(zip(Etiquetas_financiacion,lista1)) 
    
    L_etiquetas_aux_excel3=[Etiquetas_financiacion,lista1]
    L_etiquetas_aux_excel=[L_etiquetas_aux_excel1,L_etiquetas_aux_excel2,L_etiquetas_aux_excel3]
    #Exportar para ver en el formulario html
    df = pd.DataFrame(L_etiquetas_aux_excel)
    df.to_excel('static/Graficas/Temp6.xlsx')    
    
    ###########>>>>>>>>>>>>>>>>>>>>>>Graficar Depreciación<<<<<<<<<<<<<<<<<<<<<################
    Fig_1,a = plt.subplots(frameon=False)
    l1,=a.plot(range(len(lista_Depreciacion2)),np.array(lista_Depreciacion2)/1000000, linewidth=4)
    l2,=a.plot(range(len(lista_Depreciacion1)),np.array(lista_Depreciacion1)/1000000, linewidth=4)
    a.grid(color='k', linestyle='--', linewidth=1)
    a.set_ylabel('Valor (X $1.000.000)', fontsize=18)
    a.set_xlabel('Vida útil de la hornilla (Años)', fontsize=18)
    a.set_title('Depreciación del equipo', fontsize=20)
    a.legend([l1, l2],["Con recuperador", "Sin recuperador"])  
    for item in [Fig_1,a]:
           item.patch.set_visible(False)
    FigureCanvasAgg(Fig_1).print_png('static/Graficas/Depreciacion.png')       
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
        l2 =b.barh(range(len(lista_flujo_2)),np.array(lista_flujo_2)/(1000000),edgecolor='black',hatch="o")
    else:
        lim_max=m2
        l2 =b.barh(range(len(lista_flujo_2)),np.array(lista_flujo_2)/(1000000),edgecolor='black',hatch="o")
        l1 =b.barh(range(len(lista_flujo_1)),np.array(lista_flujo_1)/(1000000),edgecolor='black',hatch="/")
    if(m3<m4):
        lim_min=m3
    else:
        lim_min=m4        

    b.set_xlim([lim_min-10,lim_max+10])
    b.grid(color='k', linestyle='--', linewidth=1)
    #plt.setp(b.get_xticklabels(), fontsize=18, rotation=45)
   # plt.setp(b.get_yticklabels(), fontsize=18)
    b.set_ylabel('Tiempo (Años)', fontsize=22)
    b.set_xlabel('Costo * ($1.000.000)', fontsize=22)
    b.set_title('Flujo de caja aproximado', fontsize=20)
    #b.legend([l1, l2],["Burner with head recovery", "Simple burner"], fontsize=14)
    b.legend([l1, l2],["Con recuperador", "Sin recuperador"], fontsize=14)
    for item in [Fig_2,b]:
           item.patch.set_visible(False)    
    FigureCanvasAgg(Fig_2).print_png('static/Graficas/Flujo_Caja_1.png') 
#    #Con recuperador
#    Fig_2a,c = plt.subplots(frameon=False)
#    c.barh(range(len(lista_flujo_2)),np.array(lista_flujo_2)/1000000)
#    c.set_xlim([lim_min-10,lim_max+10])
#    c.grid(color='k', linestyle='--', linewidth=1)
#    c.set_ylabel('Años [Vida útil de la hornilla]')
#    c.set_xlabel('Valor en pesos (X1000000)')
#    c.set_title('Flujo de caja aproximado de la hornilla con recuperador')
#    for item in [Fig_2a,c]:
#           item.patch.set_visible(False)
#    FigureCanvasAgg(Fig_2a).print_png('static/Graficas/Flujo_Caja_2.jpg') 
    ############################################################################################
    """>>>>>>------RETORNO A LA INVERSION----<<<<"""
    Retorno_inversion1=[]  
    Retorno_inversion2=[] 
    for k in range(2):
        if(k==0):
            Valor_panela=float(Operativos['Costo panela por kg'].values)
            Costo_produccion=lista_costo_produccion_1
            flujo_caja=lista_flujo_1
            Produccion_anual_kg=lista_financiero_1[8]
        elif (k==1):
            Valor_panela=float(Operativos['Costo panela por kg'].values)
            Costo_produccion=lista_costo_produccion_2
            flujo_caja=lista_flujo_2
            Produccion_anual_kg=lista_financiero_2[8]
            
        Retorno_inversion=[]    
        for i in Costo_produccion:
            Ingreso_esperado=Valor_panela*Produccion_anual_kg
            Ganancia_Acumulada=(Ingreso_esperado-i)/20
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
    l2,=d.plot(lista_valor_panela2,Anos2, linewidth=4)
    d.grid(color='k', linestyle='--', linewidth=1)
    d.set_ylabel('Time (years)', fontsize=20)
    d.set_xlabel('NCS value (USD)', fontsize=20)    
#    plt.setp(d.get_xticklabels(), fontsize=16, rotation=45)
#    plt.setp(d.get_yticklabels(), fontsize=16)
    d.set_ylabel('Funcionamiento (Años)', fontsize=18)
    d.set_xlabel('Valor de la panela (COP)', fontsize=18)
    d.set_title('Tiempo de retorno a la inversión', fontsize=20)
    d.legend([l1, l2],["Con recuperador", "Sin recuperador"], fontsize=14)
    for item in [Fig_3,d]:
           item.patch.set_visible(False)
    FigureCanvasAgg(Fig_3).print_png('static/Graficas/RI_Anos.png') 
    ############################################################################################
    ###########>>>>>>>>>>>>>>>>>Graficar Retorno a la inversión<<<<<<<<<<<<<<<<<################
    Fig_4,e = plt.subplots(frameon=False)
    l1,=e.plot(lista_valor_panela1,Meses1, linewidth=4)
    l2,=e.plot(lista_valor_panela2,Meses2, linewidth=4)   
    e.grid(color='k', linestyle='--', linewidth=1)
    e.set_ylabel('Funcionamiento de la hornilla (meses)', fontsize=18)
    e.set_xlabel('Valor de la panela (COP)', fontsize=18)
    e.set_title('Tiempo de retorno a la inversión', fontsize=20)
    e.legend([l1, l2],["Con recuperador", "Sin recuperador"])
    for item in [Fig_4,e]:
           item.patch.set_visible(False)
    with open('static/Graficas/RI_Meses.png', 'wb') as f:
        FigureCanvasAgg(Fig_4).print_png(f)     
    plt.close(Fig_1)
    plt.close(Fig_2)
#    plt.close(Fig_2a)
    plt.close(Fig_3)
    plt.close(Fig_4)
    del(Fig_1)
    del(Fig_2)
 #   del(Fig_2a)
    del(Fig_3)
    del(Fig_4)
#    #Exportar a excel
#    df = pd.DataFrame(range(len(lista_Depreciacion1)),np.array(lista_Depreciacion1)/1000000)
#    df.to_excel('Depre_con_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    df = pd.DataFrame(range(len(lista_Depreciacion2)),np.array(lista_Depreciacion2)/1000000)
#    df.to_excel('Depre_sin_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    df = pd.DataFrame(range(len(lista_flujo_1)),np.array(lista_flujo_1)/1000000)
#    df.to_excel('Flujo_con_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    df = pd.DataFrame(range(len(lista_flujo_2)),np.array(lista_flujo_2)/1000000)
#    df.to_excel('Flujo_sin_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    
#    df = pd.DataFrame(range(len(lista_flujo_1)),np.array(lista_flujo_1)/1000000)
#    df.to_excel('Flujo_con_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    df = pd.DataFrame(range(len(lista_flujo_2)),np.array(lista_flujo_2)/1000000)
#    df.to_excel('Flujo_sin_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    df = pd.DataFrame([lista_valor_panela1,Anos1])
#    df.to_excel('Anos_valor_1_con_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    df = pd.DataFrame([lista_valor_panela2,Anos2])
#    df.to_excel('Anos_valor_2_sin_r.xlsx')
#    #>>>>>>>>>>>---------------<<<<<<<<<<<<<<<<<<< 
#    df = pd.DataFrame([lista_valor_panela1,Meses1])
#    df.to_excel('Meses_valor_1_con_r.xlsx')
#    #>>>>>>>>>>>>>>------------><<<<<<<<<<<<<<<<
#    df = pd.DataFrame([lista_valor_panela2,Meses2])
#    df.to_excel('Meses_valor_2_sin_r.xlsx')
#    #>>>>>>>>>>>---------------<<<<<<<<<<<<<<<<<<<    
    
    sleep(1)
    Generar_reporte_financiero(D_Hornilla, D_Recuperador, D_Operativo, D_Consolidado, D_Produccion, D_Financiero) 
    ############################################################################################
#print(Retorno_inversion)
#    Marca=Molino['Marca'].values
#    Modelo=Molino['Modelo'].values
#    Kilos=Molino['kghora'].values
#    Diesel=Molino['Diesel'].values
#    Electrico=Molino['Electrico'].values
#    Valor=Molino['Valor'].values
#    Seleccionado=[]
#    