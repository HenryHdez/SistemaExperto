# !/usr/bin/env python 
# -*- coding: utf-8 -*-

import numpy as np 
import pandas as pd
import shutil
import math 
from difflib import SequenceMatcher as SM
# importing from a pylatex module 
from pylatex import Document, Section, Subsection, Tabular, Command, MediumText, SmallText, HugeText, LargeText, TextColor, LineBreak, NewPage, Itemize
from pylatex import Math, TikZ, Axis, Plot, SubFigure, Figure, Matrix, Alignat, VerticalSpace, Center
from pylatex.utils import italic, NoEscape, bold
from pylatex.package import Package
from os import remove

def Diam_Tub(ind, Entalpia_vaporacion2, Calor_Recuperar, Densidad_Vapor):
    #Diametro de tuberia de alimentacion según la presion y masa de vapor producida
    if(ind<4):
        Flujo_masico_Vapor=(Calor_Recuperar*3600)/Entalpia_vaporacion2
    else:
        Flujo_masico_Vapor=(526*3600)/Entalpia_vaporacion2
    Potencia_Caldera=Flujo_masico_Vapor/34.5
    Caudal_Vapor=Flujo_masico_Vapor/Densidad_Vapor
    Velocidad_limite=20
    Diametro_Calculado=(((4*Caudal_Vapor/3600)/(Velocidad_limite*math.pi))**(0.5))*1000
    Diametro_Seleccionado=Diametro_Calculado/25.4#3
    
    A=math.floor(Diametro_Seleccionado)
    B=round(Diametro_Seleccionado-A,3)
    if(B<0.125):
        B=0.125
    elif(B>=0.125 and B<0.25):
        B=0.25
    elif(B>=0.25 and B<=0.6):
        B=0.5
    else:
        B=0.75
    C=str(B.as_integer_ratio()).replace("(", " ")
    C=C.replace(")", " ")
    C=C.replace(", ", "/")
    return [Flujo_masico_Vapor, A+B, str(A)+C]

def Par_Tub_Rec():
    #def Calor_recuperar():
    #Datos de la hornilla
    Temp_Gas_Antes_Chimenea=650
    Temp_Despues_Chimenea=250
    Masa_Gases=(0.662741979997669*3600)
    Valor_Integracion1=0.000355
    Valor_Integracion2=1.12116
    Memo1=Valor_Integracion1*(Temp_Gas_Antes_Chimenea**2-Temp_Despues_Chimenea**2)
    Memo2=Valor_Integracion2*(Temp_Gas_Antes_Chimenea-Temp_Despues_Chimenea)
    Calor_Recuperar=(Masa_Gases*(Memo1+Memo2))/3600
    
    
    Temp_Gas_Entrada_Recuperador=Temp_Gas_Antes_Chimenea
    Temp_Gas_Salida_Recuperador=Temp_Despues_Chimenea
    Temp_Vapor_saturado_100_psi=170
    A=Temp_Gas_Entrada_Recuperador-Temp_Gas_Salida_Recuperador
    B=Temp_Gas_Entrada_Recuperador-Temp_Vapor_saturado_100_psi
    C=Temp_Gas_Salida_Recuperador-Temp_Vapor_saturado_100_psi
    Media_termica_logaritmica=A/math.log(B/C)
    Coeficiente_global_Tranferencia_calor=25
    Area_Calculada_Recuperador=(Calor_Recuperar*1000)/(Media_termica_logaritmica*Coeficiente_global_Tranferencia_calor)
    
    
    Calor_disponible=Calor_Recuperar
    Temp_Ambiente=22
    Temp_Final_Concentracion=138.727531502368
    Entalpia_Vaporizacion=2269.47056052965
    Calor_especifico_jugo_Inicial=3.75364
    A=Calor_disponible*3600
    B=5.882*(Temp_Final_Concentracion-Temp_Ambiente)*Calor_especifico_jugo_Inicial
    C=4.5882*Entalpia_Vaporizacion
    Masa_Panela_Producida=(A/(B+C))*0.75
    
    
    N_tubos_Intercambiador_externo=16+16+13+13
    N_tubos_Intercambiador_Interno=136-N_tubos_Intercambiador_externo
    Long_Tubo_8=8
    Long_Tubo_2_1_2=28.156
    Long_Tubo_3=2.4
    Long_Tubo_1_1_2=2
    Area_de_tubo_1_1_2=math.pi*(48.26/1000)*Long_Tubo_1_1_2
    Area_total_Tubo=Area_de_tubo_1_1_2*(N_tubos_Intercambiador_externo+N_tubos_Intercambiador_Interno)
    Area_total_Tubo_8=math.pi*(219/1000)*Long_Tubo_8
    Area_total_tubo_Conexion_2_1_2=math.pi*(219/1000)*Long_Tubo_2_1_2
    Area_total_tubo_3=math.pi*(88.9/1000)*Long_Tubo_3
    Area_total_recuperador=Area_total_Tubo+Area_total_Tubo_8+Area_total_tubo_Conexion_2_1_2+Area_total_tubo_3
    
    Area_Serpentin_Reci_0=Area_de_tubo_1_1_2*Long_Tubo_1_1_2*15
    Area_Serpentin_Evap_1=Area_de_tubo_1_1_2*Long_Tubo_1_1_2*12
    Area_Serpentin_Evap_3=Area_de_tubo_1_1_2*Long_Tubo_1_1_2*10
    
    Densidades=[1.33495, 2.0459, 2.74307, 2.74307, 5.13291]
    Entalpia_vap=[2185.49, 2139.99, 2104.72, 2104.72, 2015.19]
    Lista_Diam=[]
    for ind, e in enumerate(Densidades):
        Lista_Diam.append(Diam_Tub(ind, Entalpia_vap[ind], Calor_Recuperar, e))
       
    Flujo_masico_Agua=Lista_Diam[4][0]/1000
    Flujo_Vol_Agua=1.4
    Densi_Agua=1000
    Presion_Vapor=130
    F_masico_Vapor=Flujo_Vol_Agua*Densi_Agua
    Entalpia_vapo=2015.19
    Calor_Recu=F_masico_Vapor*Entalpia_vapo
    Potencia_Caldera=F_masico_Vapor/34.5
    Potencia_Kw=Calor_Recu/3600
    
    Flujo_diseño_bomba=4.25
    Tiempo_real_operac=0.238333333
    Flujo_volumet_Agua=Tiempo_real_operac*Flujo_diseño_bomba
    Densidad_Agua=1000
    Presion_Vapor=130
    Calor_Recuperado=Entalpia_vapo*F_masico_Vapor
    Potencia_Caldera=F_masico_Vapor/34.5
    Potencia_Kw=Calor_Recuperado/3600
    Eficiencia_Caldera=0.644327679
    
    Etiquetas=[
            'Calor a recuperar [kw]',
            'Area calculada del recuperador [m^2]',
            'Masa panela producida [kg]',
            'Número de tubos del intercambiador externo',
            'Número de tubos del intercambiador interno',
            'Longitud tubo de 8"',
            'Longitud tubo de 2 1/2"',
            'Longitud tubo de 3"',
            'Longitud tubo de 1 1/2"',
            'Area del tubo 1 1/2"',
            'Area total de los tubos [m^2]',
            'Area total del tubo de 8" [m^2]',
            'Area total de conexión del tubo 2 1/2" [m^2]',
            'Area total tubo de 3" [m^2]',
            'Area total del recuperador [m^2]',
            'Area Serpentin Recibidora [m^2]',
            'Area Serpentin Evaporadora 1 [m^2]',
            'Area Serpentin Evaporadora 2 [m^2]',
            ]

    Valores=[
            Calor_Recuperar,
            Area_Calculada_Recuperador,
            Masa_Panela_Producida,
            N_tubos_Intercambiador_externo,
            N_tubos_Intercambiador_Interno,
            Long_Tubo_8,
            Long_Tubo_2_1_2,
            Long_Tubo_3,
            Long_Tubo_1_1_2,
            Area_de_tubo_1_1_2,
            Area_total_Tubo,
            Area_total_Tubo_8,
            Area_total_tubo_Conexion_2_1_2,
            Area_total_tubo_3,
            Area_total_recuperador,
            Area_Serpentin_Reci_0,
            Area_Serpentin_Evap_1,
            Area_Serpentin_Evap_3,
            ]  
    
    Dicc_1=dict(zip(Etiquetas, Valores))
    
    Etiquetas=[]
    Valores=[]
    Presiones=['20','40','60','60','130']
    for e in range(len(Presiones)):
        Etiquetas.append(str(e+1)+'- Diametro para una tubería con una presión de trabajo de '+ Presiones[e] + 'PSI')
        Valores.append(Lista_Diam[e][2]+'"')
    Dicc_2=dict(zip(Etiquetas, Valores))
    return [Dicc_1, Dicc_2]
    
#Modificar las viñetas y ortografia
class Documento_Latex():
    global doc
    
    def portada():
        global doc
        doc = Document()
        geometry_options = {"tmargin": "4cm", "rmargin": "2cm", "lmargin": "4cm", "bmargin": "3cm"} 
        doc = Document(geometry_options=geometry_options)
        doc.packages.append(Package('babel', options=['spanish']))
        doc.packages.append(Package('background', options=['pages=all']))
        doc.packages.append(NoEscape('\\backgroundsetup{placement=center,\n angle=0, scale=1, contents={\includegraphics{Membrete.pdf}}, opacity=1}\n'))   
        doc.append(NewPage())

    def Mostrar_rec():
        global doc
        '''>>>>>>>>>>>>>>>Presentación de los datos de usuario<<<<<<<<<<<<<<<<<'''        
        doc = Documento_Latex.titulos_I (doc, 'INFORMACIÓN DEL RECUPERADOR')  
        Dicc=Par_Tub_Rec()[0]
        with doc.create(Tabular('lcccc')) as table:
            for i in Dicc:
                try:
                    a=round(float(Dicc[i]))
                except:
                    a=Dicc[i]       
                table.add_row((bold(str(i)), ' ', ' ',' ',a))

        doc = Documento_Latex.titulos_I (doc, 'TUBERIAS DE CONEXIÓN AL PROCESO')  
        Dicc=Par_Tub_Rec()[1]
        with doc.create(Tabular('lcccc')) as table:
            for i in Dicc:
                try:
                    a=round(float(Dicc[i]))
                except:
                    a=Dicc[i]       
                table.add_row((bold(str(i)), ' ', ' ',' ',a))
               
    #Contenido
    def titulos_I (texto, Palabra):
        with texto.create(Center()) as centered:
                    centered.append(HugeText(Palabra))
                    centered.append(LineBreak()) 
        return texto
    
               
    def generar_pdf():  
        global doc
        
        doc.generate_pdf('static/Latex/B1a_Tuberia_rec', clean_tex=False) 
        shutil.copy('static/Latex/B1a_Tuberia_rec.pdf', 'static/pdf04/B1a_Tuberia_rec.pdf')
        remove('static/Latex/B1a_Tuberia_rec.pdf')
        remove('static/Latex/B1a_Tuberia_rec.tex')  