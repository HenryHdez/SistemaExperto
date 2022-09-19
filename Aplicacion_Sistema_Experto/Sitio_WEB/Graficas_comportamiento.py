# !/usr/bin/env python 
# -*- coding: utf-8 -*-

import numpy as np 
import pandas as pd
import shutil
from os import remove
from time import sleep
from difflib import SequenceMatcher as SM
# importing from a pylatex module 
from pylatex import Document, Section, Subsection, Tabular, Command, MediumText, SmallText, HugeText, LargeText, TextColor, LineBreak, NewPage, Itemize
from pylatex import Math, TikZ, Axis, Plot, SubFigure, Figure, Matrix, Alignat, VerticalSpace, Center
from pylatex.utils import italic, NoEscape, bold
from pylatex.package import Package

#Modificar las viñetas y ortografia
class Documento_Latex():
    global doc
    
    def reporte(Nombre_Cli):
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
                    centered.append(HugeText('COMPORTAMIENTO FINANCIERO'))
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
                       
        with doc.create(Figure(position='h!')) as imagesRow1:
            with doc.create(SubFigure(
                    position='b',
                    width=NoEscape(r'0.7\linewidth'))) as left_imagesRow1:
                left_imagesRow1.add_image('Graficas/Depreciacion.png')
            imagesRow1.append(LineBreak())

        with doc.create(Figure(position='h!')) as imagesRow1:
            with doc.create(SubFigure(
                    position='b',
                    width=NoEscape(r'0.7\linewidth'))) as left_imagesRow1:
                left_imagesRow1.add_image('Graficas/Flujo_Caja_1.png')
            imagesRow1.append(LineBreak())
            
        with doc.create(Figure(position='h!')) as imagesRow1:
            with doc.create(SubFigure(
                    position='b',
                    width=NoEscape(r'0.7\linewidth'))) as left_imagesRow1:
                left_imagesRow1.add_image('Graficas/RI_Anos.png')
            imagesRow1.append(LineBreak())

        with doc.create(Figure(position='h!')) as imagesRow1:
            with doc.create(SubFigure(
                    position='b',
                    width=NoEscape(r'0.7\linewidth'))) as left_imagesRow1:
                left_imagesRow1.add_image('Graficas/RI_Meses.png')
            imagesRow1.append(LineBreak())
                   
        doc.append(NewPage())
        doc.generate_pdf('static/Latex/Graf'+Nombre_Cli, clean_tex=False) 
        shutil.copy('static/Latex/Graf'+Nombre_Cli+'.pdf', 'static/Descarga/Graf'+Nombre_Cli+'.pdf')
        remove('static/Latex/Graf'+Nombre_Cli+'.pdf')
        remove('static/Latex/Graf'+Nombre_Cli+'.tex')
