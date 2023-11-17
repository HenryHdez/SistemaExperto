# !/usr/bin/env python 
# -*- coding: utf-8 -*-

import numpy as np 
import pandas as pd
import shutil
from difflib import SequenceMatcher as SM
from os import remove
# importing from a pylatex module 
from pylatex import Document, Section, Subsection, Tabular, Command, MediumText, SmallText, HugeText, LargeText, TextColor, LineBreak, NewPage, Itemize
from pylatex import Math, TikZ, Axis, Plot, SubFigure, Figure, Matrix, Alignat, VerticalSpace, Center
from pylatex.utils import italic, NoEscape, bold
from pylatex.package import Package

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
                    if(estado==1):
                        centered.append(HugeText('DIAGRAMAS MECÁNICOS PARA LA CONSTRUCCIÓN DE LA HORNILLA CON RECUPERADOR DE CALOR'))
                    else:
                        centered.append(HugeText('DIAGRAMAS MECÁNICOS PARA LA CONSTRUCCIÓN DE LA HORNILLA SIN RECUPERADOR DE CALOR'))
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
               
    def generar_pdf(nombre_arch, ubi):  
        global doc
        doc.generate_pdf('static/Latex/'+nombre_arch, clean_tex=False) 
        shutil.copy('static/Latex/'+nombre_arch+'.pdf', 'static/'+ubi+nombre_arch+'.pdf')
        remove('static/Latex/'+nombre_arch+'.pdf')
        remove('static/Latex/'+nombre_arch+'.tex')  


