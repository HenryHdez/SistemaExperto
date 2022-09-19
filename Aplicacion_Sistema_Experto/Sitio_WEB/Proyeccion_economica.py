# !/usr/bin/env python 
# -*- coding: utf-8 -*-

import numpy as np 
import pandas as pd
import shutil
from difflib import SequenceMatcher as SM
# importing from a pylatex module 
from pylatex import Document, Section, Subsection, Tabular, Command, MediumText, SmallText, HugeText, LargeText, TextColor, LineBreak, NewPage, Itemize
from pylatex import Math, TikZ, Axis, Plot, SubFigure, Figure, Matrix, Alignat, VerticalSpace, Center
from pylatex.utils import italic, NoEscape, bold
from pylatex.package import Package
from os import remove

#Modificar las viñetas y ortografia
class Documento_Latex():
    global doc
    
    def portada(estado):
        global doc
        doc = Document()
        geometry_options = {"tmargin": "4cm", "rmargin": "2cm", "lmargin": "4cm", "bmargin": "3cm"} 
        doc = Document(geometry_options=geometry_options)
        doc.packages.append(Package('babel', options=['spanish']))
        doc.packages.append(Package('background', options=['pages=all']))
        doc.packages.append(NoEscape('\\backgroundsetup{placement=center,\n angle=0, scale=1, contents={\includegraphics{Membrete.pdf}}, opacity=1}\n'))   
        
        with doc.create(Center()) as centered:
                    centered.append(TextColor('white','HH')) 
                    for i in range(10):
                        centered.append(LineBreak())   
                    centered.append(HugeText('PROYECCIÓN ECONÓMICA DE LA HORNILLA PANELERA '+estado+' RECUPERADOR DE CALOR'))
                    centered.append(LineBreak()) 
                    centered.append(SmallText('(Generado por HornillAPP)'))
                    for i in range(8):
                        centered.append(LineBreak()) 
                    
        with doc.create(Figure(position='h!')) as imagesRow1:
            with doc.create(SubFigure(
                    position='b',
                    width=NoEscape(r'1\linewidth'))) as left_imagesRow1:
                left_imagesRow1.add_image('IconoAPP.png')
            imagesRow1.append(LineBreak())
                                    
        with doc.create(Center()) as centered:
                    centered.append(TextColor('white','HH')) 
                    for i in range(8):
                        centered.append(LineBreak())
                    #centered.append(VerticalSpace('50')) 
                    centered.append(LargeText('Presentado por: AGROSAVIA'))
                    centered.append(LineBreak())
                    centered.append(SmallText('(Corporación Colombiana de Investigación Agropecuaria)'))
        doc.append(NewPage())

    def Horn_sin(D_Hornilla, D_Operativo, D_Consolidado, D_Produccion, D_Financiero):
        global doc
        '''>>>>>>>>>>>>>>>Presentación de los datos de usuario<<<<<<<<<<<<<<<<<'''        
        doc = Documento_Latex.titulos_I (doc, 'INSUMOS DE CONSTRUCCIÓN')   
        with doc.create(Tabular('lccll')) as table:
            for i in D_Hornilla:
                try:
                    a=round(float(D_Hornilla[i][0]))
                except:
                    a=D_Hornilla[i][0]
                try:
                    b=Documento_Latex.Formato_Moneda(float(D_Hornilla[i][1]), "$", 0)
                except:
                    b=D_Hornilla[i][1]
                try:
                    c=Documento_Latex.Formato_Moneda(float(D_Hornilla[i][2]), "$", 0)
                except:
                    c=D_Hornilla[i][2]                    
                table.add_row((bold(str(i)), ' ', a, b, c))
                
        doc = Documento_Latex.titulos_I (doc, 'COSTO OPERATIVO')   
        with doc.create(Tabular('lccll')) as table:
            for i in D_Operativo:
                try:
                    a=round(float(D_Operativo[i][0]))
                except:
                    a=D_Operativo[i][0]
                try:
                    b=Documento_Latex.Formato_Moneda(float(D_Operativo[i][1]), "$", 0)
                except:
                    b=D_Operativo[i][1]
                try:
                    c=Documento_Latex.Formato_Moneda(float(D_Operativo[i][2]), "$", 0)
                except:
                    c=D_Operativo[i][2]
                table.add_row((bold(str(i)), ' ', a, b, c))

        doc = Documento_Latex.titulos_I (doc, 'COSTO DE FUNCIONAMIENTO')   
        conta=0
        with doc.create(Tabular('lcccl')) as table:
            for i in D_Produccion:
                try:
                    if(conta>1):
                        a=Documento_Latex.Formato_Moneda(float(D_Produccion[i][0]), "$", 0)
                    else:
                        a=round(float(D_Produccion[i][0]))
                    table.add_row((bold(str(i)), ' ', ' ', ' ', a))
                except:
                    a = ' '
                conta=conta+1
                
        doc.append(NewPage())

        doc = Documento_Latex.titulos_I (doc, 'CONSOLIDADO')   
        #conta=0
        with doc.create(Tabular('lccl')) as table:
            for i in D_Consolidado:
                try:
                    a=Documento_Latex.Formato_Moneda(float(D_Consolidado[i]), "$", 0)
                except:
                    a = ' '
                #if(conta!=2 and conta!=5):
                table.add_row((bold(str(i)), ' ', ' ', a))
                #conta=conta+1

        doc = Documento_Latex.titulos_I (doc, 'ANÁLISIS FINANCIERO')   
        conta=0
        with doc.create(Tabular('lccl')) as table:
            for i in D_Financiero:
                try:
                    if(conta>0 and conta<4 and conta!=2):
                        a=round(float(D_Financiero[i][0]))
                    elif(conta==2):
                        a=float(D_Financiero[i][0])
                    elif(conta>5 and conta<9):
                        a=round(float(D_Financiero[i][1]))
                    else:
                        a=Documento_Latex.Formato_Moneda(float(D_Financiero[i][1]), "$", 0)
                except:
                    a = ' '
                if(conta!=0):
                    table.add_row((bold(str(i)), ' ', ' ', a))
                conta=conta+1

    def Horn_con(D_Hornilla, D_Recuperador, D_Operativo, D_Consolidado, D_Produccion, D_Financiero):
        global doc
        '''>>>>>>>>>>>>>>>Presentación de los datos de usuario<<<<<<<<<<<<<<<<<'''        
        doc = Documento_Latex.titulos_I (doc, 'INSUMOS PARA LA CONSTRUCCIÓN DE LA HORNILLA')   
        with doc.create(Tabular('lccll')) as table:
            for i in D_Hornilla:
                try:
                    a=round(float(D_Hornilla[i][0]))
                except:
                    a=D_Hornilla[i][0]
                try:
                    b=Documento_Latex.Formato_Moneda(float(D_Hornilla[i][1]), "$", 0)
                except:
                    b=D_Hornilla[i][1]
                try:
                    c=Documento_Latex.Formato_Moneda(float(D_Hornilla[i][2]), "$", 0)
                except:
                    c=D_Hornilla[i][2]                    
                table.add_row((bold(str(i)), ' ', a, b, c))

        doc = Documento_Latex.titulos_I (doc, 'INSUMOS PARA LA CONSTRUCCIÓN DEL RECUPERADOR DE CALOR')   
        with doc.create(Tabular('lccll')) as table:
            for i in D_Recuperador:
                try:
                    a=round(float(D_Recuperador[i][0]))
                except:
                    a=D_Recuperador[i][0]
                try:
                    b=Documento_Latex.Formato_Moneda(float(D_Recuperador[i][1]), "$", 0)
                except:
                    b=D_Recuperador[i][1]
                try:
                    c=Documento_Latex.Formato_Moneda(float(D_Recuperador[i][2]), "$", 0)
                except:
                    c=D_Recuperador[i][2]                    
                table.add_row((bold(str(i)), ' ', a, b, c))

        doc.append(NewPage())
                
        doc = Documento_Latex.titulos_I (doc, 'COSTO OPERATIVO')   
        with doc.create(Tabular('lcccl')) as table:
            for i in D_Operativo:
                try:
                    a=round(float(D_Operativo[i][0]))
                except:
                    a=D_Operativo[i][0]
                try:
                    b=Documento_Latex.Formato_Moneda(float(D_Operativo[i][1]), "$", 0)
                except:
                    b=D_Operativo[i][1]
                try:
                    c=Documento_Latex.Formato_Moneda(float(D_Operativo[i][2]), "$", 0)
                except:
                    c=D_Operativo[i][2]
                table.add_row((bold(str(i)), ' ', a, b, c))
        
        doc = Documento_Latex.titulos_I (doc, 'COSTO DE FUNCIONAMIENTO')   
        conta=0
        with doc.create(Tabular('lcccl')) as table:
            for i in D_Produccion:
                try:
                    if(conta>1):
                        a=Documento_Latex.Formato_Moneda(float(D_Produccion[i][1]), "$", 0)
                    else:
                        a=round(float(D_Produccion[i][1]))
                    table.add_row((bold(str(i)), ' ', ' ', ' ', a))
                except:
                    a = ' '
                conta=conta+1
                

        doc = Documento_Latex.titulos_I (doc, 'CONSOLIDADO')   
        #conta=0
        with doc.create(Tabular('lccl')) as table:
            for i in D_Consolidado:
                try:
                    a=Documento_Latex.Formato_Moneda(float(D_Consolidado[i]), "$", 0)
                except:
                    a = ' '
                #if(conta!=6):
                table.add_row((bold(str(i)), ' ', ' ', a))
                #conta=conta+1

        doc = Documento_Latex.titulos_I (doc, 'ANÁLISIS FINANCIERO')   
        conta=0
        with doc.create(Tabular('lccl')) as table:
            for i in D_Financiero:
                try:
                    if(conta>0 and conta<4 and conta!=2):
                        a=round(float(D_Financiero[i][0]))
                    elif(conta==2):
                        a=float(D_Financiero[i][0])
                    elif(conta>5 and conta<9):
                        a=round(float(D_Financiero[i][1]))
                    else:
                        a=Documento_Latex.Formato_Moneda(float(D_Financiero[i][0]), "$", 0)
                except:
                    a = ' '
                if(conta!=0):
                    table.add_row((bold(str(i)), ' ', ' ', a))
                conta=conta+1
               
    #Contenido
    def titulos_I (texto, Palabra):
        with texto.create(Center()) as centered:
                    centered.append(HugeText(Palabra))
                    centered.append(LineBreak()) 
        return texto
    
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
               
    def generar_pdf(nombre_arch, ubi):  
        global doc
        doc.generate_pdf('static/Latex/'+nombre_arch, clean_tex=False) 
        shutil.copy('static/Latex/'+nombre_arch+'.pdf', 'static/'+ubi+nombre_arch+'.pdf')
        remove('static/Latex/'+nombre_arch+'.pdf')
        remove('static/Latex/'+nombre_arch+'.tex')        



