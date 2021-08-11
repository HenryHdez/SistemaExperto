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


#Modificar las viñetas y ortografia
class Documento_Latex():
    global doc
    
    def portada(Diccionario, eficiencia, T_Hornilla, Area_bag, Area, Texto_Area):
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
                    centered.append(HugeText('PROPUESTA DE VALOR PARA LA CONSTRUCCIÓN DE UNA HORNILLA '))
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
        
        with doc.create(MediumText(' ')) as tlg:
                    tlg.append(TextColor('white','HH')) 
                    tlg.append(LineBreak())
                    tlg.append('Bogotá D.C., ')
                    tlg.append(Command(' ',NoEscape('\\today')))
                    tlg.append('\n \n') #Salto de línea en parráfo
                    tlg.append(LineBreak()) #Salto de línea en parráfo
                    tlg.append('\nSeñor (es):') 
                    tlg.append('\n'+str(Diccionario['Nombre de usuario']))
                    if(str(Diccionario['Departamento'])=='--'):
                        tlg.append('\n'+str(Diccionario['Pais'])+'.')    
                    else:
                        tlg.append('\n \n \n'+str(Diccionario['Ciudad'])+', '+str(Diccionario['Departamento'])+'.')
                    tlg.append('\n \n') #Salto de línea en parráfo
                    tlg.append('\nApreciado(s) productor(es):')
                    tlg.append('\n \n') #Salto de línea en parráfo
                    #Verificar area
                    Parrafo= ('Con base en la información suministrada, HornillApp propone (ver Sección 1) la construcción de una hornilla panelera tipo Cimpa con una '+
                              T_Hornilla+' con capacidad de '+ str(Diccionario['Capacidad estimada de la hornilla']) +' kg/h'+' con una eficiencia estimada del '+ str(round(Diccionario['Eficiencia de la hornilla']))+'%'+'; adecuada para el procesamiento de hasta '+
                              Area+
                              Texto_Area+' de caña, una producción de ' + str(round(float(Diccionario['Producción de caña (toneladas por hectárea)'])))+ ' toneladas por hectárea, un periodo vegetativo de '+ str(Diccionario['Periodo vegetativo'])+' meses, para realizar '+
                              str(round(float(Diccionario['Moliendas al año']),0))+' moliendas al año en una jornada laboral de '+ str(Diccionario['Jornada de trabajo al mes']) + ' de '+
                              str(Diccionario['Días trabajados a la semana'])+ ' días cada semana de '+str(Diccionario['Horas de trabajo de la hornilla por día'])+ ' horas de trabajo diarias.'+
                              '\n Está hornilla requiere un área para la(s) bagacera(s) aproximadamente de '+Area_bag+' m^2 y su productividad '
                              )
                    

                    tlg.append(Parrafo)                
                    Parrafo= (' puede alcanzar hasta '+str(round(Diccionario['Capacidad estimada de la hornilla']+25))+' kg/h con la incorporación del sistema de recuperación de calor. '
                              +' Adicionalmente, en este informe encontrará la siguiente información complementaria para la hornilla: ')
                    tlg.append(Parrafo)
                    
                    with tlg.create(Itemize()) as itemize:
                        itemize.add_item('Una sugerencia de los tipos de molinos que se encuentran disponibles en el mercado apropiados para su buen funcionamiento.')
                        itemize.add_item('Recomendaciones para su manejo, seguridad y mantenimiento.')
                        itemize.add_item('Un análisis financiero de su implementación con y sin recuperador de calor.')

                    Parrafo= ('Cualquier inquietud AGROSAVIA está presta a atenderla (atencionalcliente@agrosavia.co).\n'+
                              'Cordial saludo.\n'+
                              '\n \n'+
                              'AGROSAVIA (Corporación colombiana de investigación agropecuaria)')            
                    tlg.append(Parrafo)            

                    Parrafo= ('\n \n \n \n \n \nNota: Está propuesta de valor se basa en condiciones del terreno ideales y estacionarias, por lo que, '+
                              'AGROSAVIA no se hace responsable de la reproducción total o parcial del material aquí suministrado sin una aprobación '+
                              'corporativa.')
                    tlg.append(Parrafo)
                    
        doc.append(NewPage())
        
        with doc.create(MediumText(' ')) as tlg:
                    tlg.append(LargeText(bold('Contenido')))
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Sección 1')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Información del usuario.')
                                                        item.add_item('Características de la caña sembrada.')
                                                        item.add_item('Características del molino.')
                                                        item.add_item('Consideraciones generales para el manejo de la hornilla.')
                                                        item.add_item('Análisis financiero.')
                                            itemize.add_item('Sección 2')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Diagramas mecánicos de la hornilla.')
                                                        item.add_item('Diagramas mecánicos de la camára.')
                                                        item.add_item('Diagramas mecánicos de la chimenea.')
                                                        item.add_item('Diagramas mecánicos del ducto.')
                                                        item.add_item('Diagramas mecánicos de la hornilla con recuperador de calor.')
        doc.append(NewPage())

        #PORTADA PARA LA SECCIÓN 1 
        
        with doc.create(Center()) as centered:
                    centered.append(TextColor('white','HH')) 
                    for i in range(15):
                        centered.append(LineBreak())   
                    centered.append(HugeText('SECCIÓN 1:'))
                    centered.append(LineBreak())
                    centered.append(HugeText('INFORMACIÓN TÉCNICA Y FINANCIERA')) 
        doc.append(NewPage())
        
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
    
    def seccion1(D1, D2):
        global doc
        '''>>>>>>>>>>>>>>>Presentación de los datos de usuario<<<<<<<<<<<<<<<<<'''        
        doc = Documento_Latex.titulos_I (doc, 'DATOS DEL USUARIO PARA GENERAR EL INFORME')   
        with doc.create(Tabular('lccccl')) as table:
            for i in D1:
                if(str(i)=='DATOS DE ENTRADA'):
                    break
                else:
                    if((SM(None, 'Altura', i).ratio()<0.85) and
                       (SM(None, 'Variedad de Caña', i).ratio()<0.85) and
                       (SM(None, 'Usa fertilizante', i).ratio()<0.85) and
                       (SM(None, 'Grados Brix de la panela (promedio)', i).ratio()<0.85) and
                       (SM(None, '--', str(D1[i])).ratio()<0.85)):
                        T1=str(D1[i])
                        #Arreglo para asignar unidades y mostrarlas en el informe
                        if (str(i)=='Área caña sembrada'):
                            T1=str(D1[i])+" ha" 
                        elif (str(i)=='Área de caña proyectada que se espera moler en los próximos 5 años (Hectáreas)'):
                            i='Área proyectada en 5 años (hectáreas)'
                            #T1=str(D1[i])+" ha"
                        elif (str(i)=='Caña esperada por hectárea'):
                            T1=str(D1[i])+" t/ha"
                        elif (str(i)=='Número de moliendas'):
                            T1=str(D1[i])+" semanal(es)"                    
                        elif (str(i)=='Periodo vegetativo'):
                            T1=str(D1[i])+" mes(es)"                   
                        elif (str(i)=='Caña molida al mes'):
                            T1=str(D1[i])+" t/mes" 
                        elif (str(i)=='Área cosechada al mes'):
                            T1=str(D1[i])+" ha/mes" 
                        elif (str(i)=='Caña molida a la semana'):
                            T1=str(D1[i])+" t/semana" 
                        elif (str(i)=='Caña molida por Hora'):
                            T1=str(D1[i])+" t/hora"
                        elif (str(i)=='Área cosechada al mes'):
                            T1=str(D1[i]*12)+" L/año"
                        elif (str(i)=='Caña molida al año'):
                            T1=str(D1[i])+" t/año"
                        elif (str(i)=='Jugo producido al año'):
                            T1=str(D1[i])+" t/año"
                        elif (str(i)=='Bagazo secado al año'):
                            T1=str(D1[i])+" t/año"
                        table.add_row((bold(str(i)), ' ', ' ', ' ', ' ',T1))
        doc.append(NewPage())
        
        '''>>>>>>>>>>>>>>>>>>>>Presentación de los datos de la caña<<<<<<<<<<<<<<<<<<<<<<<'''
        doc = Documento_Latex.titulos_I (doc, 'CARACTERÍSTICAS DE LAS VARIEDADES DE CAÑA SELECCIONADAS')
        Canas=pd.read_excel('static/Temp/Temp4.xlsx',skipcolumn = 0,)
        Carpe=pd.read_excel('static/Temp/Temp5.xlsx',skipcolumn = 0,)
        Eti = Canas.iloc[0].values
        Val = Canas.iloc[1].values
        Car = Carpe.iloc[0].values
        
        conta=1
        for i in range (len(Car)-1):
            with doc.create(Tabular('lcccccl')) as table:
                for j in range (1,8):
                    table.add_row((bold(str(Eti[conta])), ' ', ' ', ' ', ' ', ' ', str(Val[conta])))
                    conta=conta+1
                conta=conta+1
            doc.append(LineBreak())
            doc.append('\n')
            doc.append(LineBreak())
        
        for i in range (1,len(Car),3):
            with doc.create(Figure(position='h!')) as imagesRow1:
                for j in range(3):
                    if((i+j)<len(Car)):
                        with doc.create(
                            SubFigure(width=NoEscape(r'0.33\linewidth'))) as left_imagesRow1:
                            left_imagesRow1.add_image(Car[i+j], width=NoEscape(r'0.95\linewidth'))
                            left_imagesRow1.add_caption('Variedad de caña '+str(i+j))
                imagesRow1.append(LineBreak())
                imagesRow1.append(NewPage())  
        
        doc.append(NewPage())
        doc.append(TextColor('white','HH')) 
        doc.append(NewPage())
        
        '''>>>>>>>>>>>>>>>>>>>>Presentación de los molinos seleccionados<<<<<<<<<<<<<<<<<<<<<<<'''   
        doc = Documento_Latex.titulos_I (doc, 'MOLINOS PRESELECCIONADOS PARA ESTE DISEÑO')
        Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
        Carpe=pd.read_excel('static/Temp/Temp5.xlsx',skipcolumn = 0,)
        Eti = Canas.iloc[0].values
        Val = Canas.iloc[1].values
        Car = Carpe.iloc[0].values
        Marca=Molino['Marca'].values
        Modelo=Molino['Modelo'].values
        Kilos=Molino['kg/hora'].values
        Diesel=Molino['Diesel'].values
        Electrico=Molino['Electrico'].values
        Valor=Molino['Precio'].values

        with doc.create(Tabular('lcccccl')) as table:
                table.add_row((TextColor('red',bold('VALOR APROXIMADO DE UN MOLINO: ')),
                               ' ', ' ', ' ', ' ', ' ', 
                               TextColor('red', Documento_Latex.Formato_Moneda(sum(Valor)/len(Valor), "$", 2))))
        doc.append(LineBreak())
                
        with doc.create(Tabular('ccccc')) as table:  
            table.add_row("MARCA", "MODELO", "KG POR HORA", "DIESEL O GASOLINA (HP)", "ELÉCTRICO (HP)")
            table.add_empty_row()
            for i in range(len(Marca)):
                table.add_row(str(Marca[i]),
                              str(Modelo[i]), 
                              str(Kilos[i]), 
                              str(Diesel[i]), 
                              str(Electrico[i]))
                
            doc.append(LineBreak())
            doc.append('\n')
            doc.append(LineBreak())
        
        for i in range (1,len(Modelo),3):
            with doc.create(Figure(position='h!')) as imagesRow1:
                for j in range(3):
                    if((i-1)+j<len(Modelo)):
                        with doc.create(
                            SubFigure(width=NoEscape(r'0.33\linewidth'))) as left_imagesRow1:
                            left_imagesRow1.add_image('Molinos/'+str(Modelo[(i-1)+j]+'.jpg'), width=NoEscape(r'0.95\linewidth'))
                            left_imagesRow1.add_caption(str(Modelo[(i-1)+j]))
                imagesRow1.append(LineBreak())
                imagesRow1.append(NewPage()) 
        
        doc.append(NewPage())
        doc.append(TextColor('white','HH')) 
        doc.append(NewPage())                

        #MANUAL DE OPERACIÓN DE LA HORNILLA                   
        with doc.create(MediumText(' ')) as tlg:
                    tlg.append(LargeText(bold('Consideraciones para el manejo de la hornilla')))
                    
                    Parrafo= ('\n \nEl trapiche panelero es un lugar donde se procesa la caña de azúcar para producir la panela. Está constituido por las áreas de molienda, prelimpieza, hornilla, moldeo y almacenamiento.')           
                    tlg.append(Parrafo)

                    Parrafo= ('\n La hornilla panelera, está conformada, por el cenicero, la cámara, la chimenea y el ducto, sobre el cual se asientan directamente los intercambiadores de calor, en los que se deposita el jugo. En la hornilla panelera, se genera y transfiere el calor necesario para concentrar en un sistema de evaporación abierta, el jugo de la caña; de tal forma que la cantidad de energía aprovechada se relaciona directamente con el suministro de aire y bagazo, la eficiencia de la combustión, y la cantidad de energía disipada a los alrededores. Estas variables de operación y transferencia se relacionan entre si y debido a su complejidad y cantidad, dificultan las tareas de manipulación y diseño de la hornilla.')           
                    tlg.append(Parrafo)
                    
                    tlg.append(LargeText(bold('\n \n Manejo de las hornillas paneleras')))
                    
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Tenga en cuenta las siguientes indicaciones.')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Durante las pruebas iniciales y periodos de capacitación, los operarios que manejan la hornilla deben tener experiencia para evitar la disminución en la calidad de la panela y vida util de los equipos instalados.')
                                                        item.add_item('El trabajo continuo de la hornilla aumenta la capacidad de producción y evita la perdida de energía, puesto que, al no enfriarse durante las horas de la noche se reduce el efecto del cambio térmico sobre los ladrillos de la estructura.')
                                                        item.add_item('La combustión en la hornilla será buena, si se alimenta con pequeñas cantidades de bagazo cada 150 segundos y la válvula de la chimenea tiene una apertura 60° para garantizar un flujo de aire suficientemente alto que produzca llama, sin arrastrar combustible en los gases residuales.')
                                                        item.add_item('La entrada de aire por orificios diferentes a los proyectados en el diseño inicial debe evitarse a toda costa, para aumentar la eficiencia de la combustión y reducir el material particulado de los gases en la chimenea.')
                                                        item.add_item('Elimine obstáculos en las entradas de aire diseñadas para la hornilla y retire periódicamente la ceniza la parrilla para evitar la formación de escoria.')
                                                        item.add_item('El cenicero y su entrada deben mantenerse despejada a fin de no obstruir el paso del aire.')
                                                        item.add_item('El bagazo para alimentar la hornilla debe tener las condiciones de humedad mencionadas en el diseño.')
                                                        item.add_item('Almacene el bagazo por dos semanas en la bagacera, y así, obtendrá un bagazo con al menos un 30% de humedad.')
                                                        item.add_item('Ajuste el tiro de la chimenea usando la válvula mariposa cuando tenga bagazo con mayor humedad.')
                                                        item.add_item('La válvula no opera en tiempo real y cuando se encuentra a medio cerrar se aumenta la velocidad de calentamiento en la zona de evaporación al pie de la entrada del bagazo. Sin embargo, cuando se encuentra abierta el calentamiento se presenta al pie de la chimenea.')
                                                        item.add_item('El tiempo de residencia del jugo en la hornilla, influye en la calidad de la panela y este es directamente proporcional al aumento de los azucares invertidos.')
                                                        item.add_item('Las falcas en las pailas son de seguridad, no deben usarse para contener una mayor cantidad de jugo. Por tanto para aumentar la transferencia de calor al jugo y mejorar la calidad de la panela es importante manejar la cantidad de jugo mínima en cada paila.')
                                                        item.add_item('El nivel del jugo en las pailas semiesféricas, siempre debe estar por encima de la línea de contacto de los gases de combustión con la paila a fin de evitar quemadura en la panela.')
                                                        item.add_item('La paila clarificadora debe calentar lo más rápido posible para que permita remover la cachaza. Además, la velocidad mínima de calentamiento debe ser de 1.5°C/min.')
                                                        item.add_item('Elimine residuos de la caña o jugos presentes sobre la superficie de las pailas concentradoras de panela y cachaza periódicamente, para que el producto se pegue al fondo. Lo cual disminuye el paso del calor y deterioran la calidad del producto.')

                    tlg.append(LargeText(bold('Mantenimiento de la hornilla')))
                    
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Después de cada molienda.')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Limpie y desinfecte las instalaciones, pailas, equipos y utensilios, antes de iniciar nuevamente la producción de panela.')
                                                        item.add_item('Un encelamiento de los moldes, utensilios de madera y prelimpiadores.')
                                                        item.add_item('Dejar en remojo con agua limpia las pailas durante el enfriamiento de la hornilla.')
                                                        item.add_item('Retirar la ceniza del cenicero y el ducto.')
                                                   
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Cada seis moliendas.')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Retirar el hollín formado en la superficie de las pailas, por donde se transfiere el calor.')
                                                        item.add_item('Limpiar los ductos de las pailas piro-tubulares, con ayuda de un raspador o un costal de fique.')
    
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Cada seis meses.')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('Realice una limpieza general e inspección del estado de los ductos.')
                                                        item.add_item('Realice un mantenimiento de las paredes del ducto y la cámara.')
                                                        
                    tlg.append(LargeText(bold('Recomendaciones de construcción del trapiche')))
                    
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Algunos parámetros para tener en cuenta son.')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('El suministro de agua ser potable y continuo.')
                                                        item.add_item('Los alrededores de las fábricas deben estar libre de posibles focos de infección.')
                                                        item.add_item('Las áreas de trabajo de cada subproceso deben estar delimitadas.')
                                                        item.add_item('Las áreas de procesamiento y empaque deben estar separadas de las áreas de recepción y desechos.')
                                                        item.add_item('Las uniones de las baldosas deben recubrirse de materiales plásticos que faciliten la limpieza.')
                                                        item.add_item('Las salientes de las paredes, dinteles de ventanas y suspensiones del techo deben ser curvas e inclinadas.')
                                                        item.add_item('Los pisos y las paredes se deben construir con materiales anticorrosivos, no absorbentes y de alto transito.')
                                                        item.add_item('Las áreas de procesos deben tener en el centro un canal de drenaje con 3° de inclinación y una parrilla removible para realizar su limpieza.')
                                                        item.add_item('Los pisos deben tener una leve inclinación (3°) para realizar el drenado.')
                                                        item.add_item('Los desagües deben tener rejillas de seguridad para impedir el paso de animales.')
                                                        item.add_item('Los ambientes debe ser ventilados.')
                                                        item.add_item('Los vapores deben contar con su propio escape para evitar la presencia de moho en paredes y techos.')
                                                        item.add_item('Los ductos de ventilación deben estar cubiertos de mallas protectoras.')
                                                        item.add_item('Los ambientes deben estar bien iluminados.')
                                                        item.add_item('Las bases o cimientos deben ser lisos para evitar la presencia de insectos o residuos.')
                                                        item.add_item('Los espacios entre los equipos o equipos y paredes deben estar sellados.')
                                                        item.add_item('Los baños, habitaciones y casilleros, deben estar aseados y alejados de las áreas de procesamiento y producto terminado.')
                                                        item.add_item('Las diferentes áreas deben disponer de un sitio para el aseo de las manos con sus respectivos implementos, tales como; jabón líquido, cepillos y toallas desechables.')

                    tlg.append(LargeText(bold('Higiene y desinfección en el trapiche')))
                   
                    with tlg.create(Itemize()) as itemize:
                                            itemize.add_item('Tenga en cuenta las siguientes indicaciones para su cuidado personal.')
                                            with itemize.create(Itemize()) as item:
                                                        item.add_item('El objetivo de la higiene en los alimentos es alargar la vida útil del producto, y proteger al consumidor final de las enfermedades producidas al ingerir alimentos contaminados.')
                                                        item.add_item('La higienización de un trapiche requiere de una limpieza con detergente y de una esterilización industrial o satanización (desinfectante y bactericida).')
                                                        item.add_item('Los equipos y utensilios deben limpiarse y desinfectarse al final e inicio de cada molienda.')
                                                        item.add_item('La limpieza se realiza siguiendo estas pautas: proteger las materias prima y los productos terminados, raspar los residuos sólidos con una espátula sobre un recogedor y lavar con agua limpia, cepillo y detergente')
                                                        item.add_item('La esterilización se realiza con calor (vapor de agua, agua hirviendo), o un esterilizante químico (bactericida, desinfectante).Cuando se emplea agua caliente debe estar hirviendo (90°C) o en el caso del esterilizante químico puede usarse una solución clorada, de vinagre y una lechada de cal.')
                                                        item.add_item('Las soluciones desinfectantes deben aplicarse en solución con un rociador, empezando por la parte inferior.')
                                                        item.add_item('Antes de la esterilización la superficie debe estar limpia y totalmente escurrida.')
                                                        item.add_item('Las superficies en contacto con el alimento deben ser lisas, exentas de huecos, grietas y evitar las esquinas cuadradas.')
                                                        item.add_item('La industria de alimentos usa ampliamente el acero inoxidable y plásticos como el teflón por la facilidad de higienización, y su poca alteración al contacto con los alimentos.')
                                                        item.add_item('No debe usarse el cobre, bronce, estaño, aluminio, madera y zinc para las superficies que están en contacto con el alimento.')
                                                        item.add_item('No emplee en la limpieza esponjas o cepillos metálicos que rayen las superficies.')
                                                        item.add_item('Las pailas se lavan con arena de peña y esponja para desmancharla.')
                                                        item.add_item('Ningún tipo de rosca debe estar en contacto con el alimento.')
                                                        item.add_item('Se debe mantener una inclinación de superficies y tubería para el drenaje de 1 centímetro por metro.')
                                                        item.add_item('Se deben usar conexiones hidraulicas y uniones que sean de fácil limpieza.')
                                                        item.add_item('Se debe evitar la unión de acero inoxidable con otros metales.')
                                                        item.add_item('El hipoclorito ejerce una rápida acción bactericida sin dejar residuos tóxicos.')
                                                        item.add_item('No es aconsejable el uso de cloro en material de acero inoxidable.')
                                                        item.add_item('En la esterilización del acero inoxidable, puede utilizarse agua caliente, vapor o solución de 0.25 litros de vinagre en 10 litros de agua.')
                                                        item.add_item('Los materiales plásticos se deben lavar con una solución de 5.0 gramos de bicarbonato (2 cucharadas) en l0 litros de agua clorada y dejar secar durante 30 minutos.')
                                                        item.add_item('La esterilización del acero inoxidable puede hacerse con agua caliente, vapor o solución de 0.25 litros de vinagre en 10 litros de agua.')
                                                        item.add_item('Las superficies de madera se limpian con espátula para eliminar los residuos sólidos. Después remojar en detergente durante 5 minutos, luego cepillar, lavar con agua limpia, y finalmente rociar con solución de 12 gramos de cal (una cucharadita) en 10 litros de agua dejar secar.')  
                                                        item.add_item('Los utensilios de madera se dejan en un recipiente plástico limpio, con solución de 12 gramos de cal (una cucharadita) en 10 litros de agua.')  
                                                        item.add_item('Cambiar la solución donde se sumergen los utensilios de madera cada cuatro horas.') 
                                                        item.add_item('Los utensilios y gaveras no deben dejarse sobre el suelo o superficies no desinfectadas.') 
                                                        item.add_item('Evitar la caída de grasa mecánica en los alimentos.')

        doc.append(NewPage())
            
    def generar_pdf():  
        global doc
        doc.generate_pdf('static/Latex/A0_Cotizacion', clean_tex=False) 
        shutil.copy('static/Latex/A0_Cotizacion.pdf', 'static/pdf01/A0_Cotizacion.pdf')



