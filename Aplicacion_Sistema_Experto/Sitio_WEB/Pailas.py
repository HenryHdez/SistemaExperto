# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:53:50 2020

@author: hahernandez
"""
#Librerías de construcción propia
from Costos_funcionamiento import Fondo
#Librerás para la generación de contenido
import math
import numpy
import random
import time
import os
import pandas as pd
import shutil
global Cantidad_pailas
global Lista_de_pailas
#Cantidad_pailas[0] es plana
#Cantidad_pailas[1] es plana sin aletas
#Cantidad_pailas[2] es pirotubular circular
#Cantidad_pailas[3] es pirotubular circular SA
#Cantidad_pailas[4] es semiesférica
#Cantidad_pailas[5] es semicilindrica
#Cantidad_pailas[6] es semicilindrica SA
#Cantidad_pailas[7] es cuadrada
#Cantidad_pailas[8] es cuadrada SA
#Cantidad_pailas[9] es acanalada
#Cantidad_pailas[10] es acanalada SA
Cantidad_pailas=[0,0,0,0,0,0,0,0,0,0,0]
Lista_de_pailas=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
"Librería para realizar los calculos de la geometría de las pailas de una hornilla"

"""--->>>Generar informe en pdf<<<<---"""
#Función para unir el informe generado en varias funciones
def Unir_Informe(nombre, ruta_carp, borrar_F):
    from PyPDF2 import PdfFileMerger, PdfFileReader
    from shutil import rmtree
    listaPdfs = os.listdir(ruta_carp)
    listaPdfs=sorted(listaPdfs)
    merger = PdfFileMerger()
    if(borrar_F!=2 and borrar_F!=3):
        for file in listaPdfs:
            merger.append(PdfFileReader(ruta_carp+file))
        merger.write('static/'+nombre+'.pdf')
    else:
        caracter=' '
        if(borrar_F==2):
            caracter='A'
        elif(borrar_F==3):
            caracter='B'
        for file in listaPdfs:
            if(file[0]==caracter):
                merger.append(PdfFileReader(ruta_carp+file))
        merger.write('static/'+nombre+'.pdf')
    """Borrar datos cargados temporalmente"""
    if(borrar_F==1):
        try:
            rmtree('static/Temp')
            rmtree('static/pdf01')
            rmtree('static/pdf02')
            os.mkdir('static/Temp')
            os.mkdir('static/pdf01')
            os.mkdir('static/pdf02')
        except:
            print('Sistema ocupado')
    
#Función para generar las portadas
def Generar_portada():
    #Espacio de trabajo disponible desde 20 hasta 650
    from reportlab.lib.pagesizes import letter
    #Sección 2
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf01/B0_portada.pdf", pagesize=letter)
    Fondo(canvas)
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,435,'                         SECCIÓN 2:     ') 
    canvas.drawString(20,400,'              DIAGRAMAS MECÁNICOS   ') 
    canvas.showPage() #Salto de página    
    canvas.save()
    #Sección 3
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf02/C0_portada.pdf", pagesize=letter)
    Fondo(canvas)
    canvas.drawImage('static/Iconos/Fondo_otros.png', 50, 220, width=500, height=350)
    canvas.setFont('Helvetica-Bold', 30)
    canvas.drawString(20,390,'                         SECCIÓN 1:     ') 
    canvas.drawString(20,355,'  INFORMACIÓN TÉCNICA DETALLADA   ') 
    canvas.showPage() #Salto de página    
    canvas.save()
    
#Función para generar la parte escrita del informe
def Generar_reporte(D1,D2):
    """----------->>>>>>> Publicar Calculos por etapa<<<<<<<<<<<------------"""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    canvas = canvas.Canvas("static/pdf02/C2_informe.pdf", pagesize=letter)
    #Estructura para imprimir los calculos por Etapa
    Fondo(canvas)
    puntero_v=450
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(200,700,'--->>>PARÁMETROS DE DISEÑO<<<---')  
    Etiquetas=list(dict.keys(D2))
    Etiquetas.insert(0,'Orden de las pailas según el flujo del gas')
    for i in range(len(Etiquetas)-1):
        canvas.saveState()
        canvas.translate(puntero_v, 680)
        canvas.rotate(-90)
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(0, 0, str(Etiquetas[i]))
        puntero_v=puntero_v-25
        canvas.restoreState()     
    #Función para dibujar los valores de la Tabla    
    Valores=list(dict.values(D2))
    puntero_h=400
    for i in range(int(D2['Etapas'])): #Etapas
        puntero_v=450
        canvas.saveState()
        canvas.translate(puntero_v, puntero_h)
        canvas.rotate(-90)
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(0, 0, str(int(D2['Etapas'])-i)) #orden segun el flujo
        puntero_v=puntero_v-25
        canvas.restoreState()
        for j in range(13):#Literales de la tabla
            canvas.saveState()
            canvas.translate(puntero_v, puntero_h)
            canvas.rotate(-90)
            canvas.drawString(0, 0, str(Valores[j][i]))
            puntero_v=puntero_v-25
            canvas.restoreState()
        if(puntero_h<200):
            puntero_h=700
            canvas.showPage()
            Fondo(canvas)
            canvas.setFont('Helvetica-Bold', 12)
        else:
            puntero_h=puntero_h-80
    #Gruardas informe en pdf
    Generar_portada()
    canvas.save()
    Unir_Informe('Informe_WEB', 'static/pdf01/', 2)
    Unir_Informe('Planos_WEB', 'static/pdf01/', 3)
    Unir_Informe('Calculos_WEB', 'static/pdf02/', 0)
    Unir_Informe('Informe', 'static/pdf01/', 1)
    
def Dimensiones_parrilla(Ancho_seccion, Longitud_Seccion, Secciones_totales, Ancho_camara, Longitud_Camara, Altura_camara):
    global Dimensiones_Camara
    Dimensiones_Camara=[]
    Dimensiones_Camara.append(Ancho_seccion)
    Dimensiones_Camara.append(Longitud_Seccion)
    Dimensiones_Camara.append(Secciones_totales)
    Dimensiones_Camara.append(Ancho_camara)
    Dimensiones_Camara.append(Longitud_Camara)
    Dimensiones_Camara.append(Altura_camara)

def Fijar_pailas(canvas, Espacio, Desplazamiento1, UP, Factor, Etapas, Vector_Entrada, Tipo_Hornilla, itera, Diccionario):
    #Fijar plano
    mem_desp=0
    Desplazamiento=Desplazamiento1
    if(itera==0):
        if(Tipo_Hornilla=='cámara Ward' or Tipo_Hornilla=='cámara plana'):
            canvas.drawImage('static/Vistas/Planta/Arquitectonico.jpg', 0, 0, width=970, height=628)
        else:
            canvas.drawImage('static/Vistas/Planta/Arquitectonico3.jpg', 0, 0, width=970, height=628)  
    elif(itera==1):
        if(Tipo_Hornilla=='cámara Ward' or Tipo_Hornilla=='cámara plana'):
            canvas.drawImage('static/Vistas/Planta/Arquitectonico1a.jpg', 0, 0, width=970, height=628)
        else:
            canvas.drawImage('static/Vistas/Planta/Arquitectonico3a.jpg', 0, 0, width=970, height=628)  
        canvas=Dibujar_Cotas_arquitectonico1(canvas, Diccionario)
        canvas=Dibujar_Cotas_arquitectonico2(canvas, Diccionario)
    elif(itera==2):
        if(Tipo_Hornilla=='cámara Ward' or Tipo_Hornilla=='cámara plana'):
            canvas.drawImage('static/Vistas/Planta/Arquitectonico1b.jpg', 0, 0, width=970, height=628)
        else:
            canvas.drawImage('static/Vistas/Planta/Arquitectonico3b.jpg', 0, 0, width=970, height=628) 
    #Fija pailas    
    if(Tipo_Hornilla=='cámara Ward' or Tipo_Hornilla=='cámara plana'):
        for i in range (Etapas):
            if(itera==2):
                canvas.setFont('Helvetica-Bold', 10)
                canvas.drawString(Desplazamiento+12, UP-25, 'Paila: '+str(i+1))                              
                if(i==2):
                    canvas.drawString(Desplazamiento-5, UP+65, 'Concentradora')
                elif(i==3 and Etapas>6):
                    canvas.drawString(Desplazamiento-5, UP+65, 'Concentradora')    
                elif(i==Etapas-1):
                    canvas.drawString(Desplazamiento+90, UP-25, 'Paila: Melotera') 
                    canvas.drawString(Desplazamiento-5, UP+65, 'Recibidora')
                elif(i==Etapas-2):
                    canvas.drawString(Desplazamiento-5, UP+65, 'Clarificadora')
                else:
                    canvas.drawString(Desplazamiento-5, UP+65, 'Evaporadora')
                    
            if Vector_Entrada[i][0]==1:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Plana_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Plana_sin_aletas.png'
            elif Vector_Entrada[i][0]==2: 
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_circular_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_circular_sin_aletas.png'
            elif Vector_Entrada[i][0]==3:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dsemiesferica_superior.png'
                Nombre_Paila='static/Vistas/Superior/'+'Semiesferica.png' 
            elif Vector_Entrada[i][0]==4:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dsemicilindrica_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Semicilindrica_con_aletas.png'
                else:
                   Nombre_Paila='static/Vistas/Superior/'+'Semicilindrica_sin_aletas.png'
            elif Vector_Entrada[i][0]==5:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_cuadrada_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_cuadrada_sin_aletas.png'
            elif Vector_Entrada[i][0]==6:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Cuadrada_acanalada_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Cuadrada_acanalada_sin_aletas.png' 
            canvas.drawImage(Nombre_Paila, Desplazamiento, UP, width=Espacio*0.19, height=Espacio*0.19)  
            canvas=Dibujar_Rotulo(canvas, 'Representación de la hornilla', 'Pictórico')
            Desplazamiento=Desplazamiento+Espacio-Factor
            canvas.drawImage('static/Vistas/Superior/'+'Plana_sin_aletas.png', Desplazamiento, UP, width=Espacio*0.19, height=Espacio*0.19)  
    else:
        #Doble
        for i in range (Etapas):
            if(i==0):
                mem_desp=Desplazamiento
            if(itera==2):
                canvas.setFont('Helvetica-Bold', 10)
                if(i!=2):
                    canvas.drawString(Desplazamiento+12, UP-25, 'Paila: '+str(i+1))                              
                if(i==2):
                    canvas.drawString(mem_desp-30, UP+135, 'Paila: '+str(i+1)) 
                    canvas.drawString(mem_desp+5, UP+135, '-Concentradora')
                elif(i==3 and Etapas>6):
                    canvas.drawString(Desplazamiento-5, UP+65, 'Concentradora')    
                elif(i==Etapas-1):
                    canvas.drawString(Desplazamiento+135, UP-25, 'Paila: Melotera') 
                    canvas.drawString(Desplazamiento-5, UP+65, 'Recibidora')
                elif(i==Etapas-2):
                    canvas.drawString(Desplazamiento-5, UP+65, 'Clarificadora')
                else:
                    canvas.drawString(Desplazamiento-5, UP+65, 'Evaporadora')
                    
            if Vector_Entrada[i][0]==1:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Plana_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Plana_sin_aletas.png'
            elif Vector_Entrada[i][0]==2: 
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_circular_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_circular_sin_aletas.png'
            elif Vector_Entrada[i][0]==3:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dsemiesferica_superior.png'
                Nombre_Paila='static/Vistas/Superior/'+'Semiesferica.png' 
            elif Vector_Entrada[i][0]==4:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dsemicilindrica_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Semicilindrica_con_aletas.png'
                else:
                   Nombre_Paila='static/Vistas/Superior/'+'Semicilindrica_sin_aletas.png'
            elif Vector_Entrada[i][0]==5:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_cuadrada_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Pirotubular_cuadrada_sin_aletas.png'
            elif Vector_Entrada[i][0]==6:
                #Nombre_ducto='static/Vistas/Ductos/'+'Dplana_superior.png'
                if Vector_Entrada[i][1]==True:
                    Nombre_Paila='static/Vistas/Superior/'+'Cuadrada_acanalada_con_aletas.png'
                else:
                    Nombre_Paila='static/Vistas/Superior/'+'Cuadrada_acanalada_sin_aletas.png' 
            
            if(i==2):
                if(itera<=1):
                    des_pos=25
                else:
                    des_pos=80
                canvas.drawImage(Nombre_Paila, mem_desp, UP+des_pos, width=Espacio*0.19, height=Espacio*0.19) 
            else:
                canvas.drawImage(Nombre_Paila, Desplazamiento, UP, width=Espacio*0.19, height=Espacio*0.19) 
                canvas=Dibujar_Rotulo(canvas, 'Representación de la hornilla', 'Pictórico')
                Desplazamiento=Desplazamiento+Espacio-Factor
                canvas.drawImage('static/Vistas/Superior/'+'Plana_sin_aletas.png', Desplazamiento, UP, width=Espacio*0.19, height=Espacio*0.19)
            
    if(itera<=1):
        canvas.showPage()
    return canvas
    
def Dibujar_planta(Vector_Entrada, Tipo_Hornilla, Etapas, Nombres_Ubicaciones, Capacidad_hornilla, Altura_UP, Ancho_UP, Lista_Falcas, Diccionario):
    global Dimensiones_Pailas
    global Dimensiones_Camara
#    print(Dimensiones_Pailas)
#    print(Vector_Entrada)
#    print(Tipo_Hornilla)
#    print(Etapas)
    for inter in range(2):      
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        if(inter==0):
            canvas = canvas.Canvas("static/B1_Etapa_Planta_WEB.pdf", pagesize=letter)
            canvas.setPageSize((970,628))
            if(Tipo_Hornilla=='cámara Ward' or Tipo_Hornilla=='cámara plana'):
                if(Etapas==5):
                    canvas=Fijar_pailas(canvas, 130, 240, 362, 80, Etapas, Vector_Entrada, Tipo_Hornilla, 0, Diccionario)
                    canvas=Fijar_pailas(canvas, 110, 265, 368, 63, Etapas, Vector_Entrada, Tipo_Hornilla, 1, Diccionario)
                    canvas=Fijar_pailas(canvas, 260, 180, 296, 150, Etapas, Vector_Entrada, Tipo_Hornilla, 2, Diccionario)
                if(Etapas==6):
                    canvas=Fijar_pailas(canvas, 100, 260, 364, 60, Etapas, Vector_Entrada, Tipo_Hornilla, 0, Diccionario)
                    canvas=Fijar_pailas(canvas, 80, 280, 370, 43, Etapas, Vector_Entrada, Tipo_Hornilla, 1, Diccionario)
                    canvas=Fijar_pailas(canvas, 230, 150, 300, 135, Etapas, Vector_Entrada, Tipo_Hornilla, 2, Diccionario)
                if(Etapas==7):
                    canvas=Fijar_pailas(canvas, 80, 250, 366, 45, Etapas, Vector_Entrada, Tipo_Hornilla, 0, Diccionario)
                    canvas=Fijar_pailas(canvas, 60, 300, 372, 33, Etapas, Vector_Entrada, Tipo_Hornilla, 1, Diccionario)
                    canvas=Fijar_pailas(canvas, 200, 140, 304, 110, Etapas, Vector_Entrada, Tipo_Hornilla, 2, Diccionario)
            else:
                if(Etapas==5):
                    canvas=Fijar_pailas(canvas, 130, 275, 358, 80, Etapas, Vector_Entrada, Tipo_Hornilla, 0, Diccionario)
                    canvas=Fijar_pailas(canvas, 110, 275, 358, 60, Etapas, Vector_Entrada, Tipo_Hornilla, 1, Diccionario)
                    canvas=Fijar_pailas(canvas, 260, 125, 275, 100, Etapas, Vector_Entrada, Tipo_Hornilla, 2, Diccionario)
                if(Etapas==6):
                    canvas=Fijar_pailas(canvas, 100, 280, 361, 55, Etapas, Vector_Entrada, Tipo_Hornilla, 0, Diccionario)
                    canvas=Fijar_pailas(canvas, 80, 280, 361, 35, Etapas, Vector_Entrada, Tipo_Hornilla, 1, Diccionario)
                    canvas=Fijar_pailas(canvas, 230, 140, 275, 105, Etapas, Vector_Entrada, Tipo_Hornilla, 2, Diccionario)
            
            canvas.showPage()        
            if(Tipo_Hornilla=='cámara plana'):    
                canvas.drawImage('static/Vistas/Camaras/Plana2_cotas.png', 0, 0,  width=970, height=628)  
                canvas=Dibujar_Cotas_Camara(canvas,'Cámara hornilla', Dimensiones_Pailas[0][4], Dimensiones_Pailas[0][3], 3)
                canvas.showPage()
                canvas.drawImage('static/Vistas/Chimeneas/Chimenea1_cotas.png', 0, 0,  width=970, height=628)
                canvas=Dibujar_Cotas_Chimenea(canvas,'Chimenea hornilla', Capacidad_hornilla, Altura_UP)
                canvas.showPage()
                canvas.drawImage('static/Vistas/Chimeneas/Valvula_1.png', 0, 0,  width=970, height=628)   
                Dibujar_Cotas_Valvula_1(canvas,'Válvula de tiro para la chimenea', Capacidad_hornilla, Ancho_UP)               
            elif(Tipo_Hornilla=='doble cámara'):
                canvas.drawImage('static/Vistas/Camaras/Doble_cotas.png', 0, 0,  width=970, height=628)  
                canvas=Dibujar_Cotas_Camara(canvas,'Cámara hornilla', Dimensiones_Pailas[0][4], Dimensiones_Pailas[0][3], 1)
                canvas.showPage()
                canvas.drawImage('static/Vistas/Chimeneas/Chimenea1_cotas.png', 0, 0,  width=970, height=628)
                canvas=Dibujar_Cotas_Chimenea(canvas,'Chimenea hornilla', Capacidad_hornilla, Altura_UP)
                canvas.showPage()
                canvas.drawImage('static/Vistas/Chimeneas/Valvula_1.png', 0, 0,  width=970, height=628)   
                Dibujar_Cotas_Valvula_1(canvas,'Válvula de tiro para la chimenea', Capacidad_hornilla, Ancho_UP) 
            elif(Tipo_Hornilla=='cámara Ward'):
                canvas.drawImage('static/Vistas/Camaras/Cimpa_cotas.png', 0, 0,  width=970, height=628)
                canvas=Dibujar_Cotas_Camara(canvas,'Cámara hornilla', Dimensiones_Pailas[0][4], Dimensiones_Pailas[0][3], 2)
                canvas.showPage()
                canvas.drawImage('static/Vistas/Chimeneas/Chimenea1_cotas.png', 0, 0,  width=970, height=628)
                canvas=Dibujar_Cotas_Chimenea(canvas,'Chimenea hornilla', Capacidad_hornilla, Altura_UP)
                canvas.showPage()
                canvas.drawImage('static/Vistas/Chimeneas/Valvula_1.png', 0, 0,  width=970, height=628)   
                Dibujar_Cotas_Valvula_1(canvas,'Válvula de tiro para la chimenea', Capacidad_hornilla, Ancho_UP) 
            canvas.save()

            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            canvas = canvas.Canvas("static/B3_Etapa_Planta_WEB.pdf", pagesize=letter)
            canvas.setPageSize((970,628))
            canvas.drawImage('static/Vistas/Otros/Formato.png', 0, 0, width=970, height=628)
            Altura=0.0
            Grados_inc=0.06
            Memoria=0.0
            for i in range(Etapas):    
                Grados_inc=float(math.atan(Grados_inc))
                Falca_actual=float(Lista_Falcas[i]*1000)
                Longitud=1300.0+Memoria+(Falca_actual/2)
                Memoria=Memoria+Falca_actual+50
                Altura=Dimensiones_Camara[5]-(Longitud*Grados_inc)
                if(i>0):
                    canvas.showPage()
                if Vector_Entrada[i][0]==1:
                    canvas=Dibujar_Cotas(canvas,1,Dimensiones_Pailas[i], Nombres_Ubicaciones[i], Altura, Grados_inc, i)
                    ruta_ladrillos='static/Vistas/Ductos/Dplana_ladrillos.png'
                    ruta_ladrillos_2='static/Vistas/Ductos/Dplana_ladrillos_2.png'
                    ruta_ladrillos_3='static/Vistas/Ductos/Dplana_ladrillos_3.png'
                elif Vector_Entrada[i][0]==2: 
                    canvas=Dibujar_Cotas(canvas,1,Dimensiones_Pailas[i], Nombres_Ubicaciones[i], Altura, Grados_inc, i)
                    ruta_ladrillos='static/Vistas/Ductos/Dplana_ladrillos.png'
                    ruta_ladrillos_2='static/Vistas/Ductos/Dplana_ladrillos_2.png'
                    ruta_ladrillos_3='static/Vistas/Ductos/Dplana_ladrillos_3.png'
                elif Vector_Entrada[i][0]==3:
                    canvas=Dibujar_Cotas(canvas,3,Dimensiones_Pailas[i], Nombres_Ubicaciones[i], Altura, Grados_inc, i)
                    ruta_ladrillos='static/Vistas/Ductos/Dsemiesferica_ladrillos.png' 
                    ruta_ladrillos_2='static/Vistas/Ductos/Dsemiesferica_ladrillos_2.png'
                    ruta_ladrillos_3='static/Vistas/Ductos/Dsemiesferica_ladrillos_3.png'
                elif Vector_Entrada[i][0]==4:
                    canvas=Dibujar_Cotas(canvas,2,Dimensiones_Pailas[i], Nombres_Ubicaciones[i], Altura, Grados_inc, i)
                    ruta_ladrillos='static/Vistas/Ductos/Dsemicilindrica_ladrillos.png' 
                    ruta_ladrillos_2='static/Vistas/Ductos/Dsemicilindrica_ladrillos_2.png'
                elif Vector_Entrada[i][0]==5:
                    canvas=Dibujar_Cotas(canvas,1,Dimensiones_Pailas[i], Nombres_Ubicaciones[i], Altura, Grados_inc, i)
                    ruta_ladrillos='static/Vistas/Ductos/Dplana_ladrillos.png'
                    ruta_ladrillos_2='static/Vistas/Ductos/Dplana_ladrillos_2.png'
                    ruta_ladrillos_3='static/Vistas/Ductos/Dplana_ladrillos_3.png'
                elif Vector_Entrada[i][0]==6:
                    canvas=Dibujar_Cotas(canvas,1,Dimensiones_Pailas[i], Nombres_Ubicaciones[i], Altura, Grados_inc, i)
                    ruta_ladrillos='static/Vistas/Ductos/Dplana_ladrillos.png'
                    ruta_ladrillos_2='static/Vistas/Ductos/Dplana_ladrillos_2.png'
                    ruta_ladrillos_3='static/Vistas/Ductos/Dplana_ladrillos_3.png' 
                canvas.showPage()
                canvas.drawImage(ruta_ladrillos, 0, 0,  width=970, height=628) 
                canvas=Dibujar_Rotulo(canvas, Nombres_Ubicaciones[i], 'Ubicación de los ladrillos')                
                canvas.showPage()
                canvas.drawImage(ruta_ladrillos_2, 0, 0,  width=970, height=628) 
                canvas=Dibujar_Rotulo(canvas, Nombres_Ubicaciones[i], 'Ubicación de los ladrillos')
                if(Vector_Entrada[i][0]!=4):
                    canvas.showPage()
                    canvas.drawImage(ruta_ladrillos_3, 0, 0,  width=970, height=628) 
                    canvas=Dibujar_Rotulo(canvas, Nombres_Ubicaciones[i], 'Ubicación de los ladrillos')
            canvas.save()

        if(inter==1):
            canvas = canvas.Canvas("static/B4_Etapa_Planta_WEB.pdf", pagesize=letter)
            canvas.setPageSize((970,628))
            canvas.drawImage('static/Vistas/Otros/Formato.png', 0, 0, width=970, height=628)  
            canvas.setFont('Helvetica-Bold', 48)
            canvas.drawString(30, 320, 'A continuación se presenta una hornilla')
            canvas.drawString(30, 220, 'con recuperador')
            canvas=Dibujar_Rotulo(canvas, 'Aviso', 'Aviso')
            canvas.showPage()
            canvas.drawImage('static/Vistas/Chimeneas/Recuperador.png', 0, 0,  width=970, height=628)  
            canvas.save()

    shutil.copy("static/B1_Etapa_Planta_WEB.pdf","static/pdf01/B1_Etapa_Planta_WEB.pdf")
    shutil.copy("static/B3_Etapa_Planta_WEB.pdf","static/pdf01/B3_Etapa_Planta_WEB.pdf")
    shutil.copy("static/B4_Etapa_Planta_WEB.pdf","static/pdf01/B4_Etapa_Planta_WEB.pdf")

def Dibujar_Rotulo(canvas, Nombre_Usuario, Nombre_Paila):
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(720, 71, Nombre_Usuario)   
    canvas.drawString(720, 62, Nombre_Paila)  
    canvas.drawString(720, 52, 'APLICACIÓN')
    canvas.drawString(720, 43, 'APLICACIÓN') 
    canvas.drawString(720, 34, 'AGROSAVIA') 
    canvas.drawString(720, 25, 'AGROSAVIA') 
    canvas.setFont('Helvetica-Bold', 5)
    tiempo = time.asctime(time.localtime(time.time()))
    canvas.drawString(720,16,str(tiempo))
    return canvas

def Dibujar_Cotas_arquitectonico1(canvas, Diccionario):
    global Dimensiones_Camara
    global DIV
    global Aplano
    Conv=['A','B','C','D','E','F','G','H']
    Valores_Dim=[]
    Aplano=Dimensiones_Camara[3]+float(Diccionario['Ancho de la bagacera (mm)'])+float(Diccionario['Ancho de la zona de bodega (mm)'])+3000
    P_Q=float(Diccionario['Largo del cañetero (mm)'])+float(Diccionario['Largo de la bagacera (mm)'])
    RESTO=P_Q-float(Diccionario['Largo de la zona de moldeo (mm)'])-float(Diccionario['Largo de la zona de empaque (mm)'])-float(Diccionario['Largo de la zona de bodega (mm)'])-1500
    DIV=round(RESTO/7)
    Valores_Dim.append(round(Aplano)) #A                 
    Valores_Dim.append(DIV) #B 
    Valores_Dim.append(DIV) #C 
    Valores_Dim.append(1500) #D 
    Valores_Dim.append(round(float(Diccionario['Largo de la zona de moldeo (mm)']))) #E 
    Valores_Dim.append(round(float(Diccionario['Largo de la zona de empaque (mm)']))) #F 
    Valores_Dim.append(round(float(Diccionario['Largo de la zona de bodega (mm)']))) #G 
    Valores_Dim.append(DIV) #H   
    x_i=50
    y_i=120
    vv=155
    #Dimensiones de las cotas
    canvas.setLineWidth(0.5)
    canvas.line(x_i,y_i,x_i+245,y_i)
    for i in range(len(Valores_Dim)):
        Puntero=(y_i-8)-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(x_i+60, Puntero-1, Conv[i])
        canvas.setFont('Helvetica', 9)
        try:
            canvas.drawString(x_i+170, Puntero-1, str(round(Valores_Dim[i],3)))
        except:
            canvas.drawString(x_i+vv, Puntero-1, str(Valores_Dim[i]))            
        canvas.line(x_i,Puntero-2,x_i+245,Puntero-2)      
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(x_i+95, y_i+2, 'CONVENCIONES') 
    canvas.line(x_i,y_i,x_i,Puntero-2)
    canvas.line(x_i+125,y_i,x_i+125,Puntero-2)
    canvas.line(x_i+245,y_i,x_i+245,Puntero-2)         
    return canvas

def Dibujar_Cotas_arquitectonico2(canvas, Diccionario):
    global DIV
    global Aplano
    Bplano = Aplano-float(Diccionario['Ancho del cañetero (mm)'])-float(Diccionario['Ancho de la zona de bodega (mm)'])
    Conv=['I','J','K','L','M','N','O','P','Q']
    Valores_Dim=[]
    Valores_Dim.append(DIV) #I 
    Valores_Dim.append(DIV) #J
    Valores_Dim.append(DIV) #K
    Valores_Dim.append(DIV) #L
    Valores_Dim.append(round(Bplano)) #M
    Valores_Dim.append(round(float(Diccionario['Ancho de la zona de bodega (mm)']))) #N
    Valores_Dim.append(round(float(Diccionario['Ancho del cañetero (mm)']))) #O
    Valores_Dim.append(round(float(Diccionario['Largo del cañetero (mm)']))) #P
    Valores_Dim.append(round(float(Diccionario['Largo de la bagacera (mm)']))) #Q    
    x_i=350
    y_i=120
    vv=155
    #Dimensiones de las cotas
    canvas.setLineWidth(0.5)
    canvas.line(x_i,y_i,x_i+245,y_i)
    for i in range(len(Valores_Dim)):
        Puntero=(y_i-8)-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(x_i+60, Puntero-1, Conv[i])
        canvas.setFont('Helvetica', 9)
        try:
            canvas.drawString(x_i+170, Puntero-1, str(round(Valores_Dim[i],3)))
        except:
            canvas.drawString(x_i+vv, Puntero-1, str(Valores_Dim[i]))            
        canvas.line(x_i,Puntero-2,x_i+245,Puntero-2)      
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(x_i+95, y_i+2, 'CONVENCIONES') 
    canvas.line(x_i,y_i,x_i,Puntero-2)
    canvas.line(x_i+125,y_i,x_i+125,Puntero-2)
    canvas.line(x_i+245,y_i,x_i+245,Puntero-2)        
    return canvas

def Dibujar_Cotas_Valvula_1(canvas,Nombre_Usuario, Capacidad_hornilla, Ancho_UP):
    Conv=['A','B','C','D','E','F']
    Valores_Dim=[]
    #A 800
    #B Ancho + 200
    #C 300
    Valores_Dim.append(800)                 
    Valores_Dim.append(round(Ancho_UP)+200)
    Valores_Dim.append(300)
    x_i=675
    y_i=200
    vv=155
    #Dimensiones de las cotas
    canvas.setLineWidth(0.5)
    canvas.line(x_i,y_i,x_i+245,y_i)
    for i in range(len(Valores_Dim)):
        Puntero=(y_i-8)-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(x_i+60, Puntero-1, Conv[i])
        canvas.setFont('Helvetica', 9)
        try:
            canvas.drawString(x_i+170, Puntero-1, str(round(Valores_Dim[i],3)))
        except:
            canvas.drawString(x_i+vv, Puntero-1, str(Valores_Dim[i]))            
        canvas.line(x_i,Puntero-2,x_i+245,Puntero-2)      
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(x_i+95, y_i+2, 'CONVENCIONES') 
    canvas.line(x_i,y_i,x_i,Puntero-2)
    canvas.line(x_i+125,y_i,x_i+125,Puntero-2)
    canvas.line(x_i+245,y_i,x_i+245,Puntero-2)        
    canvas=Dibujar_Rotulo(canvas, Nombre_Usuario, 'Válvula de tiro')  
    return canvas

def Dibujar_Cotas_Chimenea(canvas,Nombre_Usuario, Capacidad_hornilla, Altura_UP):
    Conv=['A','B','C','D','E','F','G']
    Valores_Dim=[]
    #A es la sección de corte
    #B Tapa
    #C Interior
    #D exterior 
    Valores_Dim.append("Sección de corte") #A                 
    Tiro=math.floor(Capacidad_hornilla/10)
    if(Tiro<=0):
        Tiro=1
    Valores_Dim.append(Tiro*1000)          #B                                        
    Valores_Dim.append(800)                #C                                     
    Valores_Dim.append(900)                #D
    Valores_Dim.append(round(Altura_UP))
    Valores_Dim.append(1100)
    Valores_Dim.append(1000)
    x_i=675
    y_i=200
    vv=155
    #Dimensiones de las cotas
    canvas.setLineWidth(0.5)
    canvas.line(x_i,y_i,x_i+245,y_i)
    for i in range(len(Valores_Dim)):
        Puntero=(y_i-8)-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(x_i+60, Puntero-1, Conv[i])
        canvas.setFont('Helvetica', 9)
        try:
            canvas.drawString(x_i+170, Puntero-1, str(round(Valores_Dim[i],3)))
        except:
            canvas.drawString(x_i+vv, Puntero-1, str(Valores_Dim[i]))            
        canvas.line(x_i,Puntero-2,x_i+245,Puntero-2)      
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(x_i+95, y_i+2, 'CONVENCIONES') 
    canvas.line(x_i,y_i,x_i,Puntero-2)
    canvas.line(x_i+125,y_i,x_i+125,Puntero-2)
    canvas.line(x_i+245,y_i,x_i+245,Puntero-2)        
    canvas=Dibujar_Rotulo(canvas, Nombre_Usuario, 'Dimensiones de la chimenea')  
    return canvas

def Dibujar_Cotas_Camara(canvas,Nombre_Usuario, Longitud_paila_1, Ancho_paila_1, Cam_Sel):
    global Dimensiones_Camara
    # 0 Ancho_seccion
    # 1 Longitud_Seccion
    # 2 Secciones_totales
    # 3 Ancho_camara
    # 4 Longitud_Camara
    # 5 Altura_camara
    Conv=['Secciones de parrilla','A','B','C','D','E','G','F','H','I','J','K','L','M','N','O','P','Q','R','S']
    Valores_Dim=[]
#    if(Cam_Sel==0): #Plana 1
#        Valores_Dim.append(Dimensiones_Camara[2]) 
#        Valores_Dim.append("Sección de corte")                                     #A
#        Valores_Dim.append(800)                                                    #B Tamaño de puerta
#        Valores_Dim.append(Dimensiones_Camara[3])                                  #C Distancia primer paila
#        Valores_Dim.append(abs((Dimensiones_Camara[1]*2)-((Longitud_paila_1)/2)))  #D 
#        Valores_Dim.append(Dimensiones_Camara[5])                                  #E 
#        Valores_Dim.append(abs((Dimensiones_Camara[5]/2)-100))                     #F Verificar con las dimensiones de los ladrillos        
#        Valores_Dim.append(abs((Dimensiones_Camara[5]/2)-100))                     #G Verificar con las dimensiones de los ladrillos
#        Valores_Dim.append((Dimensiones_Camara[5]/2))                              #H Verificar con las dimensiones de los ladrillos
#        Valores_Dim.append(Dimensiones_Camara[3]/2)                                #I Verificar con las dimensiones de los ladrillos
#        Valores_Dim.append(Dimensiones_Camara[0])                                  #J
#        Valores_Dim.append(Dimensiones_Camara[1]*2)                                #K
#        Valores_Dim.append(Dimensiones_Camara[4])                                  #L        
#        Valores_Dim.append(Dimensiones_Camara[4]-Dimensiones_Camara[1])            #M   
    if(Cam_Sel==1): #Plana doble
        Valores_Dim.append(Dimensiones_Camara[2]) 
        Valores_Dim.append(400)                                                        #A
        Valores_Dim.append(400)                                                        #B 
        Valores_Dim.append("Sección de corte")                                         #C
        Valores_Dim.append(round(Dimensiones_Camara[5])+1800)                          #D 
        Valores_Dim.append(800)                                                        #E 
        Valores_Dim.append(round(Dimensiones_Camara[5])+1800)                          #F         
        Valores_Dim.append(1800)                                                       #G
        L_n=round(abs((Dimensiones_Camara[4]/2)+(Longitud_paila_1)/2))
        if(L_n<1300):
            L_n=1300
        Valores_Dim.append(L_n)                                                        #H
        Valores_Dim.append(round(abs(Dimensiones_Camara[4]+(Longitud_paila_1)/2)))     #I 
        Valores_Dim.append(round(abs(Dimensiones_Camara[4]+(Longitud_paila_1)/2)+10))  #J
        Valores_Dim.append(Dimensiones_Camara[4])                                      #K
        Valores_Dim.append((Longitud_paila_1/2)+100)                                   #L        
        Valores_Dim.append(abs(Dimensiones_Camara[3]-((Longitud_paila_1)/2)-100))      #M
        Valores_Dim.append(round(Dimensiones_Camara[3])+500)                           #N
        Valores_Dim.append(Dimensiones_Camara[0])                                      #O
        Valores_Dim.append(Dimensiones_Camara[3])                                      #P        
        Valores_Dim.append(Dimensiones_Camara[1])                                      #Q
        Valores_Dim.append(Dimensiones_Camara[3])                                      #R     
        Valores_Dim.append(Dimensiones_Camara[1]+10)                                   #S   
    elif(Cam_Sel==2): #Ward cimpa pequeña
        Valores_Dim.append(Dimensiones_Camara[2]) 
        Valores_Dim.append(round(Dimensiones_Camara[5]))                                  #A
        Valores_Dim.append(1800)                                                          #B 
        Valores_Dim.append(1500+round(abs((Dimensiones_Camara[4])+(Longitud_paila_1)/2))) #C
        Valores_Dim.append(round(Dimensiones_Camara[0]))                                  #D 
        Valores_Dim.append("Sección de corte")                                            #E 
        Valores_Dim.append(round(Dimensiones_Camara[1]))                                  #F       
        Valores_Dim.append(round(Dimensiones_Camara[3]))                                  #G
        Valores_Dim.append(1500+round(abs((Dimensiones_Camara[4])+(Longitud_paila_1)/2))) #H
        Valores_Dim.append(1500)                                                          #I
    elif(Cam_Sel==3): #Plana 2
        Valores_Dim.append(round(Dimensiones_Camara[2])) 
        Valores_Dim.append(400)                                                             #A
        Valores_Dim.append("Sección de corte")                                              #B
        Valores_Dim.append(round(Dimensiones_Camara[5]))                                    #C
        Valores_Dim.append(1500)                                                            #D 
        L_n=round(abs((Dimensiones_Camara[4]/2)+(Longitud_paila_1)/2))
        if(L_n<1300):
            L_n=1300
        Valores_Dim.append(L_n)                                                             #E 
        Valores_Dim.append(1800)                                                            #G        
        Valores_Dim.append(round(Dimensiones_Camara[5])+100)                                #F
        Valores_Dim.append(round(abs((Dimensiones_Camara[4]/2)+(Longitud_paila_1)/2)+1500)) #H
        Valores_Dim.append(round(Dimensiones_Camara[3]+480))                                #I
        Valores_Dim.append(1500+(L_n-round(Dimensiones_Camara[1])))                         #J
        Valores_Dim.append(round(Dimensiones_Camara[1]))                                    #K
        Valores_Dim.append(round(Dimensiones_Camara[4]-Dimensiones_Camara[1]))              #L        
        Valores_Dim.append(round(Dimensiones_Camara[3]))                                    #M
    elif(Cam_Sel==4): #Ward cimpa
        Valores_Dim.append(Dimensiones_Camara[2]) 
        L_n=round(abs((Dimensiones_Camara[4]/2)+(Longitud_paila_1)/2))
        if(L_n<1300):
            L_n=1300
        Valores_Dim.append(L_n)                                                             #A 
        Valores_Dim.append(round(L_n+(Longitud_paila_1/2)))                                 #B
        Valores_Dim.append(400)                                                             #C
        Valores_Dim.append("Sección de corte")                                              #D 
        Valores_Dim.append(round(1800+Dimensiones_Camara[5]))                               #E 
        Valores_Dim.append(1800)                                                            #F       
        Valores_Dim.append(round(1800+Dimensiones_Camara[5]))                               #G
        Valores_Dim.append(1800)                                                            #H
        Valores_Dim.append(round(Dimensiones_Camara[1]))                                    #I
        Valores_Dim.append(1500+L_n)                                                        #J
        Valores_Dim.append(round(1500+Dimensiones_Camara[4]))                               #K
        Valores_Dim.append(round(Dimensiones_Camara[0]))                                    #L        
        Valores_Dim.append(round(Dimensiones_Camara[0])+120)                                #M
        Valores_Dim.append(round(Dimensiones_Camara[3]))                                    #N
    #Dimensiones de las cotas
    canvas.setLineWidth(0.5)
    x_i=675
    y_i=300
    canvas.line(x_i,y_i,x_i+245,y_i)
    for i in range(len(Valores_Dim)):
        Puntero=(y_i-8)-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        if(i<1):
            canvas.drawString(x_i+20, Puntero-1, Conv[i])
        else:
            canvas.drawString(x_i+60, Puntero-1, Conv[i])
        canvas.setFont('Helvetica', 9)
        try:
            canvas.drawString(x_i+170, Puntero-1, str(round(Valores_Dim[i],3)))
        except:
            canvas.drawString(x_i+155, Puntero-1, str(Valores_Dim[i]))            
        canvas.line(x_i,Puntero-2,x_i+245,Puntero-2)      
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(x_i+95, y_i+2, 'CONVENCIONES') 
    canvas.line(x_i,y_i,x_i,Puntero-2)
    canvas.line(x_i+125,y_i,x_i+125,Puntero-2)
    canvas.line(x_i+245,y_i,x_i+245,Puntero-2)        
    canvas=Dibujar_Rotulo(canvas, Nombre_Usuario, 'Dimensiones de la camára y la parrilla')  
    return canvas
        
def Dibujar_Cotas(canvas,sel_Plano,Dimensiones, Nombre_Usuario, Altura, Grados_inc, conta): 
    global Altura_snm
    if(conta<3):
        y_ducto=(Altura_snm*0.02)-16   
        if(Altura_snm<800):
            y_ducto=0
        if(Altura_snm>1800):
            y_ducto=20
    else:
        y_ducto=(Altura_snm*-0.02)+16   
        if(Altura_snm<800):
            y_ducto=0
        if(Altura_snm>1800):
            y_ducto=-20

    Conv=['A','B','Z','C','D','E','F','G','H','I','J','K','L','M','N']
    Valores_Dim=[]
    a=0
    if(sel_Plano==1):        
        ruta_cotas='static/Vistas/Ductos/Dplana_cotas.png'
        Valores_Dim.append(Dimensiones[4])                              #A
        Valores_Dim.append(Dimensiones[4]+120)                          #B 
        Valores_Dim.append(abs(round(Altura-Dimensiones[1]+y_ducto)))   #Z
        Valores_Dim.append(Dimensiones[2])                              #C
        Valores_Dim.append(Dimensiones[2]+480)                          #D 
        Valores_Dim.append(Dimensiones[3])                              #E 
        Valores_Dim.append(round(Altura+y_ducto))                       #F       
        Valores_Dim.append(round(Altura+480+y_ducto))                   #G 
        Valores_Dim.append(Dimensiones[2]+120)                          #H 
        Valores_Dim.append(Dimensiones[2]+480)                          #I  
        Valores_Dim.append(Grados_inc*100)                              #Inc
    elif(sel_Plano==2):
        ruta_cotas='static/Vistas/Ductos/Dsemicilindrica_cotas.png'
        Valores_Dim.append(Dimensiones[17])                             #A
        Valores_Dim.append(Dimensiones[4])                              #B 
        Valores_Dim.append(abs(round(Altura-Dimensiones[1]+y_ducto)))   #Z
        Valores_Dim.append(Dimensiones[4]+120)                          #C
        Valores_Dim.append(Dimensiones[2])                              #D 
        Valores_Dim.append(Dimensiones[2]+480)                          #E 
        Valores_Dim.append(round(Altura+120+y_ducto))                   #F       
        Valores_Dim.append(round(Altura+y_ducto))                       #G 
        Valores_Dim.append(Dimensiones[3])                              #H 
        Valores_Dim.append(Grados_inc*100)                              #Inc
    elif(sel_Plano==3):
        ruta_cotas='static/Vistas/Ductos/Dsemiesferica_cotas.png'
        a=2
        Valores_Dim.append(abs(round(Altura-Dimensiones[1]+y_ducto)))   #Z
        Valores_Dim.append(Dimensiones[2])                              #C
        Valores_Dim.append(120)                                         #D 
        Valores_Dim.append(round(Altura+y_ducto))                       #E 
        Valores_Dim.append(round(Altura+120+y_ducto))                   #F         
        Valores_Dim.append(Dimensiones[2]-60)                           #G 
        Valores_Dim.append(Dimensiones[2]+100)                          #H 
        Valores_Dim.append(Dimensiones[2]+480)                          #I 
        Valores_Dim.append(Dimensiones[2]-70)                           #J 
        Valores_Dim.append(Dimensiones[2])                              #K 
        Valores_Dim.append(Dimensiones[2]+480)                          #L  
        Valores_Dim.append(120)                                         #M
        Valores_Dim.append(120)                                         #N
        Valores_Dim.append(Grados_inc*100)                              #Inc
    canvas.drawImage(ruta_cotas, 0, 0,  width=970, height=628)
    #Dimensiones de las cotas
    canvas.setLineWidth(0.5)
    x_i=675
    y_i=250
    canvas.line(x_i,y_i,x_i+245,y_i)
    for i in range(len(Valores_Dim)):
        Puntero=(y_i-8)-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        if(i<len(Valores_Dim)-1):
            canvas.drawString(x_i+60, Puntero-1, Conv[i+a])
        else:
            canvas.drawString(x_i+13, Puntero-1, 'Inclinación en grados')
        canvas.setFont('Helvetica', 9)
        canvas.drawString(x_i+170, Puntero-1, str(round(Valores_Dim[i],3)))
        canvas.line(x_i,Puntero-2,x_i+245,Puntero-2)      
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(x_i+95, y_i+2, 'CONVENCIONES') 
    canvas.line(x_i,y_i,x_i,Puntero-2)
    canvas.line(x_i+125,y_i,x_i+125,Puntero-2)
    canvas.line(x_i+245,y_i,x_i+245,Puntero-2)        
    canvas=Dibujar_Rotulo(canvas, Nombre_Usuario, 'Dimensiones de la sección de ducto')  
    return canvas

#Funcion para dibujar planos acotados
def Crear_plano_pdf(directorio_imagen, Nombre_archivo, Nombre_Usuario, Nombre_Paila, Valores_plano, valores_eliminar, Sel_Canal):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    if(Sel_Canal==1):
        Canal_T='Separación entre canales'
        Altura_T='Altura Canal'
        N_T='Número de canales'
    else:
        Altura_T='Altura aletas'
        Canal_T='Separación entre aletas'
        N_T='Número de aletas'
    Etiquetas=['Altura de la falca',        #A
               'Altura del fondo',          #B
               'Ancho del fondo',           #C
               'Ancho de la falca',         #D 
               'Longitud de la falca',      #E
               'Longitud del doblez',       #F  
               'Angulo',                    #G 
               Altura_T,                    #H 
               Canal_T,                     #I 
               N_T,                         #J
               'Altura del casco',          #K
               'Ancho del casco',           #L
               'Cantidad de tubos',         #M 
               'Diametro del tubo',         #N
               'Lado del tubo',             #O
               'Ancho del canal',           #P
               'Cantidad de canales',       #Q
               'Longitud del fondo']        #R
    Conv=['A','B','C','D','E','G','I','F','H','J','K','L','M','N','O','P','Q','R']
    for i in range(len(valores_eliminar)-1,-1,-1):
        Valores_plano.pop(valores_eliminar[i])
        Etiquetas.pop(valores_eliminar[i])
        Conv.pop(valores_eliminar[i])
    canvas = canvas.Canvas(Nombre_archivo+".pdf", pagesize=letter)
    canvas.setPageSize((970,628))
    canvas.drawImage(directorio_imagen, 0, 0, width=970, height=628)
    #Dimensiones
    canvas.setLineWidth(0.5)
    canvas.line(705,224,950,224)
    for i in range(len(Etiquetas)):
        Puntero=216-(i*9)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(707, Puntero, Etiquetas[i])
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(845, Puntero, Conv[i])
        canvas.setFont('Helvetica', 9)
        canvas.drawString(900, Puntero, str(round(Valores_plano[i],3)))
        canvas.line(705,Puntero-2,950,Puntero-2)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(800, 226, 'CONVENCIONES') 
    canvas.line(705,224,705,Puntero-2)
    canvas.line(830,224,830,Puntero-2)
    canvas.line(870,224,870,Puntero-2)
    canvas.line(950,224,950,Puntero-2)
    #Rotulo
    Dibujar_Rotulo(canvas, Nombre_Usuario, Nombre_Paila)
    canvas.showPage() #Salto de página  
    canvas.setPageSize((970,628))
    canvas.drawImage(directorio_imagen.replace(".png","_vistas.png"), 0, 0, width=970, height=628)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(720, 71, Nombre_Usuario)   
    canvas.drawString(720, 62, Nombre_Paila)  
    canvas.drawString(720, 52, 'APLICACIÓN')
    canvas.drawString(720, 43, 'APLICACIÓN') 
    canvas.drawString(720, 34, 'AGROSAVIA') 
    canvas.drawString(720, 25, 'AGROSAVIA') 
    canvas.setFont('Helvetica-Bold', 5)
    tiempo = time.asctime(time.localtime(time.time()))
    canvas.drawString(720,16,str(tiempo))
    canvas.save()

"""--->>>Está función convierte en milimetros las dimensiones y envia los 
parámetros de salida a la función para exportar a pdf<<<<----"""   
    #Hfn        Altura de fondo
    #Hfa o hfl  Altura falca
    #hal        Altura aletas
    #An o A     Ancho de paila
    #Hc         Altura de casco
    #H          Altura total     
def Dibujar_plano(Nombre_Sitio,Nombre_archivo,Tipo_paila,H_fl,H_fn,Ancho,L,Ho,Hc,N_Aletas,h_Aletas,Angulo,nT,dT,lT,lC,Cantidad_canales,Activar_Aletas):
    global Cantidad_pailas
    global Lista_de_pailas
    global Dimensiones_Pailas
    global An_g
    global Lo_g
    #Convertir medidas en milimetros
    A=H_fl*1000                                             #0
    A=A+1
    B=H_fn*1000                                             #1
    C=Ancho*1000                                            #2
    G=L*1000                                                #3
    D=2*(math.sin((math.pi/2)-Angulo)*H_fl)+Ancho           #5
    D=D*1000                                            
    I=(180*Angulo)/math.pi                                  #6
    F=h_Aletas*1000                                         #7
    H=0.07*1000                                             #8- 0.07 es la separación entre aletas
    J=N_Aletas                                              #9
    K=Hc*1000                                               #10
    if Tipo_paila==4:
        E=(L*1000)+(2*K)+100                                #4
    else:
        E=(L*1000)+100
    R=(L*1000)                                              #17
    L=H_fn*1000                                             #11 ACDIK
    M=nT                                                    #12
    N=dT*1000                                               #13
    O=lT*1000                                               #14
    P=lC*1000                                               #15
    Q=Cantidad_canales                                      #16
    An_g = C
    Lo_g = E
    Valores_plano=[round(A),round(B),round(C),round(D),round(E),50,round(I),round(F),round(H),round(J),round(K),round(L),round(M),round(N),round(O),round(P),round(Q),round(R)]
    Dimensiones_Pailas.append([round(A),round(B),round(C),round(D),round(E),50,round(I),round(F),round(H),round(J),round(K),round(L),round(M),round(N),round(O),round(P),round(Q),round(R)])
    if Tipo_paila==1:
        if Activar_Aletas==True:
            Cantidad_pailas[0]=Cantidad_pailas[0]+1
            Lista_de_pailas[0]='Plana'
            Crear_plano_pdf('static/Pailas/Plana_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila plana con aletas', Valores_plano, [10,11,12,13,14,15,16,17],0)
        else:
            if(Nombre_Sitio!="Paila Melotera"):
                Cantidad_pailas[1]=Cantidad_pailas[1]+1
            Lista_de_pailas[1]='Plana SA'
            Crear_plano_pdf('static/Pailas/Plana_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila plana sin aletas', Valores_plano, [7,8,9,10,11,12,13,14,15,16,17],0)
    elif Tipo_paila==2: 
        if Activar_Aletas==True:
            Cantidad_pailas[2]=Cantidad_pailas[2]+1
            Lista_de_pailas[2]='Pirotubular'
            Crear_plano_pdf('static/Pailas/Pirotubular_circular_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular circular con aletas', Valores_plano, [10,11,14,15,16,17],0)
        else:
            Cantidad_pailas[3]=Cantidad_pailas[3]+1
            Lista_de_pailas[3]='Pirotubular SA'
            Crear_plano_pdf('static/Pailas/Pirotubular_circular_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular circular sin aletas', Valores_plano, [7,8,9,10,11,14,15,16,17],0)
    
    elif Tipo_paila==3:
        Cantidad_pailas[4]=Cantidad_pailas[4]+1
        Lista_de_pailas[4]='Semiesferica'
        Crear_plano_pdf('static/Pailas/Semiesferica.png', Nombre_archivo,
                        Nombre_Sitio, 'Diagrama de una paila semiesférica', Valores_plano, [4,7,8,9,10,11,12,13,14,15,16,17],0)   
        
    elif Tipo_paila==4:
        if Activar_Aletas==True:
            Cantidad_pailas[5]=Cantidad_pailas[5]+1
            Lista_de_pailas[5]='Semicilindria'
            Crear_plano_pdf('static/Pailas/Semicilindrica_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila semicilindrica con aletas', Valores_plano, [1,12,13,14,15,16],0)
        else:
            Cantidad_pailas[6]=Cantidad_pailas[6]+1
            Lista_de_pailas[6]='Semicilindrica SA'
            Crear_plano_pdf('static/Pailas/Semicilindrica_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila semicilindrica sin aletas', Valores_plano, [1,7,8,9,12,13,14,15,16],0)

    elif Tipo_paila==5:
        if Activar_Aletas==True:
            Cantidad_pailas[7]=Cantidad_pailas[7]+1
            Lista_de_pailas[7]='Pirotubular cuadrada'
            Crear_plano_pdf('static/Pailas/Pirotubular_cuadrada_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular cuadrada con aletas', Valores_plano, [10,11,13,15,16,17],0)
        else:
            Cantidad_pailas[8]=Cantidad_pailas[8]+1
            Lista_de_pailas[8]='Pirotubular cuadrada SA'
            Crear_plano_pdf('static/Pailas/Pirotubular_cuadrada_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila pirotubular cuadrada sin aletas', Valores_plano, [7,8,9,10,11,13,15,16,17],0)    

    elif Tipo_paila==6:
        if Activar_Aletas==True:
            Cantidad_pailas[9]=Cantidad_pailas[9]+1
            Lista_de_pailas[9]='Cuadrada acanalada'
            #Valores_plano[1]=Valores_plano[7]
            Crear_plano_pdf('static/Pailas/Cuadrada_acanalada_con_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila cuadrada acanalada con aletas', Valores_plano, [1,10,11,12,13,14,17],1)
        else:
            Cantidad_pailas[10]=Cantidad_pailas[10]+1
            Lista_de_pailas[10]='Cuadrada acanalada SA'
            #Valores_plano[1]=Valores_plano[7]
            Crear_plano_pdf('static/Pailas/Cuadrada_acanalada_sin_aletas.png', Nombre_archivo,
                            Nombre_Sitio, 'Diagrama de una paila cuadrada acanalada sin aletas', Valores_plano, [1,7,8,9,10,11,12,13,14,17],1)     


"""**************************************************************************"""
"""--->>>Este grupo de funciones estima las dimensiones de la geometria de la paila<<<----"""
def Cantidad_Aletas(A,B_Aletas):
    #El numero de aletas es un parámetro que varia en función del 
    #ancho de la paila.Lla separación minima entre ellas es de 7cm
    if(B_Aletas==True):
        Separacion_Aletas=0.07
        return round(A/Separacion_Aletas,0), Separacion_Aletas	
    else:
        return 0, 0
    
#Orden de las variables de salida
#Volumen_Total, Ang, N_Aletas_Canal ó N_Aletas, h_Aletas, Seperacion_Aletas, dT, nT, lT, N_Canales
                
def Semiesferica(H_fn,A,H_fl):   
    #Hfn        Altura de fondo
    #Hfa o hfl  Altura falca
    #hal        Altura aletas
    #An o A     Ancho de paila
    #Hc         Altura de casco
    #H          Altura total  
    #K es altura de fondo
    #G longitud doblez
    #D es ancho de falca
    #Alto de  Casco <= (Ancho del fondo/2)
    if(A>=H_fn/2):
        A=H_fn/2
    R=(((A/2)**2)+(H_fn**2))/(2*H_fn)	
    Ang=68*math.pi/180
    VTJ=(math.pi*(H_fn**2)*(3*R-H_fn))/3
    A1=math.pi*((A/2)**2)
    x=A+2*(H_fl/math.tan(Ang))
    A2=x**2
    VFA=(H_fl*(A1+A2+math.sqrt(A1*A2)))/3
    Volumen_Total=VFA+VTJ	
    return [Volumen_Total, Ang, 0, 0, 0, 0, 0, 0, 0, 0]

def Semicilindrica(H,Hc,A,L,Hfa,B_Aletas):
    N_Aletas_Canal, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.1
    Ang=68*math.pi/180
    #Oculto en la base
    R=(((A/2)**2)+(H**2))/(2*H)
    d=R-A
    Teta=2*math.asin((A/2)/R)
    s=Teta*R
    Asccil=((R**2)*(Teta)/2)-((R**2)*math.sin(Teta)/2)
    Vcil=Asccil*L
    Acil=s*L
    Rca=((R**2)+(Hc**2))/(2*Hc)
    Vsc=(math.pi*(Hc**2)*(3*Rca-Hc)/3)
    Vca=(H/(R*2))*Vsc
    Asc=2*math.pi*Rca*Hc
    Aca=Asc*(H/(R*2))
    x1=A+(2*(Hfa/math.tan(Ang)))
    x2=(L+2*Hc)+(2*(Hfa/math.tan(Ang)))
    A1=x1*x2
    R1=(((A/2)**2)+(Hc**2))/(2*Hc)
    Teta1=2*math.asin((A/2)/R1)
    Ax=((R1**2)*Teta1/2)-((R1**2)*math.sin(Teta1)/2)
    A2=(A*L)+(2*Ax)
    V=(Hfa*(A1+A2+math.sqrt(A1*A2)))/3
    #No oculto en la base
    Arco=Acil+(2*Aca)
    VTJ=Vcil+(2*Vca)
    VFA=V
    Volumen_Total=VTJ+VFA
    return [Volumen_Total, Ang, N_Aletas_Canal, h_Aletas, Separacion_Aletas, 0, 0, 0, 0, 0]
       
def Plana(H_fl,H_fn,A,L,B_Aletas): 
    N_Aletas, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.1
    Ang=68*math.pi/180
    Area=(A*L)+(2*A*H_fn)+(2*H_fn*L)	
    Volumen_Fon=(H_fn*A*L)	
    Volumen_Total=(A*H_fn*L)+(A+H_fl/math.tan(Ang))*H_fl*L
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(2*h_Aletas*L*N_Aletas)+Area
    return [Volumen_Total, Ang, N_Aletas, h_Aletas, Separacion_Aletas, 0, 0, 0, 0, 0]
	
def Pirotubular_Circular(H_fl,H_fn,A,L,B_Aletas):
    N_Aletas, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.1
    Ang=68*math.pi/180
    dT=H_fn/3
    nT=round((A+dT)/(dT*2))
    Volumen_Fon=((H_fn*A)-(((math.pi/4)*(dT**2))*nT))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=((((H_fn)*(A))-(2*((math.pi/4)*dT**2)*nT))+(2*(H_fn*L)+(A*L)))+(math.pi*dT*L*nT)+(2*(L*h_Aletas)+(2*(h_Aletas))*N_Aletas)
    return [Volumen_Total, Ang, N_Aletas, h_Aletas, Separacion_Aletas, dT, nT, 0, 0, 0]

def Pirotubular_Cuadrada(H_fl,H_fn,A,L,B_Aletas): 
    N_Aletas, Separacion_Aletas=Cantidad_Aletas(A,B_Aletas)
    h_Aletas=0.1
    Ang=68*math.pi/180
    lT=H_fl/2
    nT=round((A+lT)/(lT*2))
    Area=(A*L+2*L*H_fn+2*A*H_fn)-2*nT*(lT**2)
    Volumen_Fon=((A*H_fn)-(nT*(lT**2)))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(h_Aletas*L*N_Aletas*2)+Area
    return [Volumen_Total, Ang, N_Aletas, h_Aletas, Separacion_Aletas, 0, nT, lT, 0, 0]
    
def Acanalada_Cuadrada(H_fl,H_fn,A,L,B_Aletas):
    lC=H_fn/3
    N_Aletas_Canal, Separacion_Aletas=Cantidad_Aletas(lC,B_Aletas)
    h_Aletas=0.1
    Ang=68*math.pi/180
    N_Canales=round((A+lC)/(lC*2))
    Area=(A*L+2*L*H_fn+2*A*H_fn)-2*(N_Canales-1)*(lC**2)
    Volumen_Fon=((A*(H_fn-lC))+N_Canales*(lC**2))*L
    Volumen_Total=Volumen_Fon+(L*H_fl*(A+H_fl/math.tan(Ang)))
    """Otros parámetros"""
    Porcentaje_Llenado=Volumen_Fon/Volumen_Total
    Area_TCC=(h_Aletas*L*N_Aletas_Canal*N_Canales*2)+Area
    return [Volumen_Total, Ang, N_Aletas_Canal, h_Aletas, Separacion_Aletas, 0, 0, 0, N_Canales, lC]

"""--->>>-------------------------------------------------------------<<<----"""
"""**************************************************************************"""

"""--->>>Está función mide el valor de aptitud del individuo (Paila)<<<---"""
def Valor_Aptitud(Vol_objetivo,Tipo_paila,H_fl,H_fn,A,L,H,Hc,Activar_Aletas):
    #Semiesferica(H_fn,A,H_fl)
    #Semicilindrica(H,Hc,A,L,Hfa,B_Aletas)
    #Plana(H_fl,H_fn,A,L,B_Aletas)
    #Pirotubular_Circular(H_fl,H_fn,A,L,B_Aletas)
    #Pirotubular_Cuadrada(H_fl,H_fn,A,L,B_Aletas)
    #Acanalada_Cuadrada(H_fl,H_fn,A,L,lC,B_Aletas)
    f=100.0
    if Tipo_paila==1:
        lista_par=Plana(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==2:
        lista_par=Pirotubular_Circular(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==3:
        lista_par=Semiesferica(H_fn,A,H_fl)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==4:
        lista_par=Semicilindrica(H,Hc,A,L,H_fl,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0
    elif Tipo_paila==5:
        lista_par=Pirotubular_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0    
    elif Tipo_paila==6:
        lista_par=Acanalada_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        f=abs(Vol_objetivo-lista_par[0])
        f=(f/Vol_objetivo)*100.0 
    return [f, lista_par[0:10]]

"""--->>>>Está funcion esta oculta pero retorna el margen de error del algoritmo
por consola<<<----"""
def Comprobar_diseno(Vol,i,Tipo_paila,H_fl,H_fn,A,L,H,Hc,Activar_Aletas):
    print("Etapa: "+str(i+1))
    print("Capacidad en m^3/kg esperada: "+str(Vol))
    if Tipo_paila==1:
        lista_par=Plana(H_fl,H_fn,A,L,Activar_Aletas)
        print("Capacidad en m^3/kg estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Plana con aletas")
        else:
            print("Tipo seleccionado: Plana sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))
    elif Tipo_paila==2:
        lista_par=Pirotubular_Circular(H_fl,H_fn,A,L,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Pirotubular circular con aletas")
        else:
            print("Tipo seleccionado: Pirotubular circular sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))
    elif Tipo_paila==3:
        lista_par=Semiesferica(H_fn,A,H_fl)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        print("Tipo seleccionado: Semiesferica")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
    elif Tipo_paila==4:
        lista_par=Semicilindrica(H,Hc,A,L,H_fl,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Semicilindrica con aletas")
        else:
            print("Tipo seleccionado: Semicilindrica sin aletas")
        print("H_fl: "+str(H_fl))
        print("Hc: "+str(Hc))
        print("A: "+str(A))
        print("L: "+str(L)) 
        print("H: "+str(H))
    elif Tipo_paila==5:  
        lista_par=Pirotubular_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Pirotubular cuadrada con aletas")
        else:
            print("Tipo seleccionado: Pirotubular cuadrada sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))        
    elif Tipo_paila==6:
        lista_par=Acanalada_Cuadrada(H_fl,H_fn,A,L,Activar_Aletas)
        print("Cantidad en Litros estimada: "+str(lista_par[0]))
        if(Activar_Aletas==True):
            print("Tipo seleccionado: Acanalada cuadrada con aletas")
        else:
            print("Tipo seleccionado: Acanalada cuadrada sin aletas")
        print("H_fl: "+str(H_fl))
        print("H_fn: "+str(H_fn))
        print("A: "+str(A))
        print("L: "+str(L))

"""--------->>>>limitador de los valores asignados a las dimensiones<<------"""
def comprobar_individuo(Lim_inf,Lim_sup,valor_actual):
    if(valor_actual>=Lim_sup):
        return Lim_sup
    elif (valor_actual<=Lim_inf):
        return Lim_inf
    else:
        return valor_actual

"""--------->>>Función que optimiza las dimensiones de la paila a partir de los,
pesos<<-------------""" 
#Dimensiones de la lamina 4*10 pies o 1.21*3.04 metros (Restricción del sistema)
def Mostrar_pailas(Vol_aux, Etapas, Sitio, T_Hornilla, Cap_hornilla, altura_media, Diccionario):
    global Cantidad_pailas
    global Lista_de_pailas
    global Dimensiones_Pailas
    global An_g
    global Lo_g
    global Altura_snm
    Altura_snm=altura_media
    Pailas_Planta=[] 
    Nombres_Ubi=[]
    Dimensiones_Pailas=[]
    Tipo_paila=[[],[]]
    Lista_Falcas=[]
    Lista=[]
    Lista2=[]
#    Tipo_paila[0].append(1)
#    Tipo_paila[0].append(2)
#    Tipo_paila[0].append(3)
#    Tipo_paila[0].append(4)
#    Tipo_paila[0].append(5)
#    Tipo_paila[0].append(6)
#    Tipo_paila[1].append(True)
#    Tipo_paila[1].append(True)
#    Tipo_paila[1].append(True)
#    Tipo_paila[1].append(True)
#    Tipo_paila[1].append(True)
#    Tipo_paila[1].append(True)
#    Tipo_paila[0].append(1)
#    Tipo_paila[0].append(2)
#    Tipo_paila[0].append(3)
#    Tipo_paila[0].append(4)
#    Tipo_paila[0].append(5)
#    Tipo_paila[0].append(6)
#    Tipo_paila[1].append(False)
#    Tipo_paila[1].append(False)
#    Tipo_paila[1].append(False)
#    Tipo_paila[1].append(False)
#    Tipo_paila[1].append(False)
#    Tipo_paila[1].append(False)
    for i in range(Etapas):
        #<100 litros semiesferica   0.1
        #>100 <200 semicilindrica   0.1     0.2
        #>200 de otras              0.2
        if(i<Etapas-3):            
            Tipo_paila[0].append(3)
            Tipo_paila[1].append(False)
        elif(float(Vol_aux[i])<=0.15):
            Tipo_paila[0].append(3)
            Tipo_paila[1].append(False)            
        elif(float(Vol_aux[i])>0.15 and float(Vol_aux[i])<=0.3):            
            Tipo_paila[0].append(4)
            Tipo_paila[1].append(random.choice([True,False]))
        else:
            Paila_seleccionada=random.choice([1,2,5,6])
            Tipo_paila[0].append(Paila_seleccionada)
            Tipo_paila[1].append(random.choice([True,False]))  
#        print(Tipo_paila[0])
#        print(float(Vol_aux[i]))
                   
    """---->>>>Algoritmo de optimización (Ascenso a la colina)<<<<----"""
    for i in range(Etapas-1,-1,-1):
        f_1=10000000
        iteraciones=0
        #Vol_aux[i]=float(Vol_aux[i])
        Volumen=float(Vol_aux[i])
        
        #Recuerde H_fl o Hfa es lo mismo
        #Asignación de valores iniciales (variables de entrada)
        #H_fl 300 y 600 todas
        #A 800 y 1200 Semiesferica
        #A 1000 y 1600 semicilidrica
        #A 1200 y 2400
        #L=A*1.5
        #Las mas grandes 1 m de ancho minimo
        
        #H_fn semiesferica y semicilindrica 300 y 500, las demas 500
        #Hc 160 y 200
        H_fl = comprobar_individuo(0.30, 0.60, abs(random.uniform(0.30, 0.60)))
        if(Tipo_paila[0][i]==3):
            Ancho_max=1.2
            Ancho_min=0.8
        elif(Tipo_paila[0][i]==4):
            Ancho_max=1.6
            Ancho_min=1.0            
        else:
            Ancho_max=2.4
            Ancho_min=1.2
        if(i<4 and Tipo_paila[0][i]==3):
            Ancho_max=0.9
            Ancho_min=0.8
        A    = comprobar_individuo(Ancho_min, Ancho_max, abs(random.uniform(Ancho_min, Ancho_max)))
        if(Tipo_paila[0][i]==3 or Tipo_paila[0][i]==4):
            Max_Fn=(A/2)-0.1
            Min_Fn=0.3
        else:
            Max_Fn=0.5
            Min_Fn=0.4
        H_fn  = comprobar_individuo(Min_Fn, Max_Fn, abs(random.uniform(Min_Fn, Max_Fn)))
        L     = A*abs(random.uniform(1.2, 1.5))
        H     = comprobar_individuo(0.10, 1.20, abs(random.uniform(0.10, 1.20)))
        Hc    = comprobar_individuo(0.16, 0.20, abs(random.uniform(0.16, 0.20)))
        f_tem = Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))
        f     = f_tem[0]

        #Memorias temporales       
        H_fl_1 = 0
        H_fn_1 = 0
        A_1    = 0
        L_1    = 0
        H_1    = 0
        Hc_1   = 0        
        primer_ite=False
        while ((0.1<f)and(iteraciones<200000)):
            if(f_1<f):
                H_fl  = H_fl_1
                H_fn  = H_fn_1
                A     = A_1
                L     = L_1
                H     = H_1
                Hc    = Hc_1
                f_tem = Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))
                f     = f_tem[0]
                lista_par = f_tem[1][1:10]  
                primer_ite=True
            n11 = numpy.random.normal(0,1) 
            H_fl_1 = H_fl + n11
            H_fl_1 = comprobar_individuo(0.30, 0.60, H_fl_1)            #abs(random.uniform(0.30, 0.60)))
            n11 = numpy.random.normal(0,1) 
            A_1    = A + n11
            A_1    = comprobar_individuo(Ancho_min, Ancho_max, A_1)     # abs(random.uniform(Ancho_min, Ancho_max)))
            if(Tipo_paila[0][i]==3 or Tipo_paila[0][i]==4):
                Max_Fn=(A_1/2)-0.1
                Min_Fn=0.3
            else:
                Max_Fn=0.5
                Min_Fn=0.4
            n11    = numpy.random.normal(0,1) 
            H_fn_1 = H_fn + n11 
            H_fn_1 = comprobar_individuo(Min_Fn, Max_Fn, H_fn_1)        #abs(random.uniform(0.40, Max_Fn)))
            n11    = numpy.random.normal(0,1) 
            L_1    = A*abs(random.uniform(1.2, 1.5))
            n11    = numpy.random.normal(0,1) 
            H_1    = H + n11 
            H_1    = comprobar_individuo(0.10, 1.20, H_1)               #abs(random.uniform(0.10, 1.20)))
            n11    = numpy.random.normal(0,1) 
            Hc_1   = Hc + n11 
            Hc_1   = comprobar_individuo(0.16, 0.20, Hc_1)              #abs(random.uniform(0.16, 0.20)))
            f_tem  = Valor_Aptitud(Volumen,int(Tipo_paila[0][i]),H_fl_1,H_fn_1,A_1,L_1,H_1,Hc_1,bool(Tipo_paila[1][i]))
            f_1    = f_tem[0]
            if(primer_ite==True):
                a1=int(Tipo_paila[0][i])
                a2=H_fl
                a3=H_fn
                a4=A
                a5=L
                a6=H
                a7=Hc
                a8=lista_par[1]
                a9=lista_par[2]
                a10=lista_par[0]
                a11=lista_par[5]
                a12=lista_par[4]
                a13=lista_par[6]
                a14=lista_par[8]
                a15=lista_par[7]
                a16=bool(Tipo_paila[1][i])   
            iteraciones=iteraciones+1
        #print(f)
        #print(f_1)
        #print(Volumen)
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16)
        #print(Lista2)
        Lista.append(a2)
        Lista2.append([a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16])                
        """--->>>Llamado a la función para esquematizar un plano en archivo pdf<<<----"""
        #lista_par[0]>>>Ang
        #lista_par[1]>>>N_Aletas_Canal ó N_Aletas
        #lista_par[2]>>>h_Aletas
        #lista_par[3]>>>Seperacion_Aletas
        #lista_par[4]>>>dT
        #lista_par[5]>>>nT
        #lista_par[6]>>>lT
        #lista_par[7]>>>N_Canales
        #lista_par[8]>>>lC
    #print(Lista2)
    Lista2.sort(key=lambda x: x[3])
    Lista_Temp=[]
    for i in range(Etapas):
        if (Lista2[i][0]==3):
            Lista_Temp.append(Lista2[i])
    for i in range(Etapas):
        if (Lista2[i][0]==4):
            Lista_Temp.append(Lista2[i])  
    for i in range(Etapas):
        if (Lista2[i][0]!=3 and Lista2[i][0]!=4):
            Lista_Temp.append(Lista2[i])
    Lista2=Lista_Temp
    Lista2[0], Lista2[1] = Lista2[1], Lista2[0]
    a2=max(Lista)
    for i in range(Etapas):
        Lista2[i][1]=a2
    #print(Lista2)
    #Lista2.reverse()
    for i in range(Etapas):
        Lista_Falcas.append(Lista2[i][4])
    for i in range(Etapas):       
        if(i<9):
            Texto_etapa= "0"+str(i+1)
        else:
            Texto_etapa= str(i+1)
        Nombres_Ubi.append(Sitio+" [Paila: "+Texto_etapa+"]")
        Dibujar_plano(Sitio+" [Paila: "+Texto_etapa+"]","static/pdf01/B2_Etapa_"+Texto_etapa,Lista2[i][0],
                      Lista2[i][1],Lista2[i][2],Lista2[i][3],Lista2[i][4],Lista2[i][5],Lista2[i][6],
                      Lista2[i][7],Lista2[i][8],Lista2[i][9],Lista2[i][10],Lista2[i][11],Lista2[i][12],
                      Lista2[i][13],Lista2[i][14],Lista2[i][15])
        Pailas_Planta.append([Lista2[i][0],Lista2[i][15],An_g,Lo_g]) 
        if(i==Etapas-1):
            R_A=(Lista2[i][1]+Lista2[i][2])*1000
            R_B=(Lista2[i][3]*1000)+100
            #Melotera
            Dibujar_plano("Paila Melotera","static/pdf01/B2_Etapa_"+"Zelotera",1,
                          Lista2[i][1],Lista2[i][2],Lista2[i][3],Lista2[i][4],Lista2[i][5],Lista2[i][6],
                          Lista2[i][7],Lista2[i][8],Lista2[i][9],Lista2[i][10],Lista2[i][11],Lista2[i][12],
                          Lista2[i][13],Lista2[i][14],False)
            #>>>>>>>>
        """Eliminar comentarios para probar el algoritmo de optimización"""
        #Comprobar_diseno(float(Vol_aux[Etapas-1-i]), i, Lista2[i][0], Lista2[i][1],Lista2[i][2],Lista2[i][3],Lista2[i][4],Lista2[i][5],
        #                 Lista2[i][6],Lista2[i][15])
                         #int(Tipo_paila[0][i]),H_fl,H_fn,A,L,H,Hc,bool(Tipo_paila[1][i]))
        #print("________>>>>>>>>>>>>>____________")
        #print(str(iteraciones))
        #print(str(f)) 
    Dibujar_planta(Pailas_Planta,T_Hornilla, sum(Cantidad_pailas), Nombres_Ubi, Cap_hornilla, R_A, R_B, Lista_Falcas, Diccionario)    
    df = pd.DataFrame([Lista_de_pailas, Cantidad_pailas])
    df.to_excel('static/Temp/Temp2.xlsx')
    Cantidad_pailas=[0,0,0,0,0,0,0,0,0,0,0]
    Lista_de_pailas=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']