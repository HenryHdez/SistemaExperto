# !/usr/bin/env python 
# -*- coding: utf-8 -*-
"""----Definición de las librerías requeridas para la ejecución de la aplicación---"""
from flask import Flask, request, render_template        #Interfaz gráfica WEB
from werkzeug.utils import secure_filename               #Encriptar información archivos de pdf
from email.mime.multipart import MIMEMultipart           #Creación del cuerpo del correo electrónico 1
from email.mime.application import MIMEApplication       #Creación del cuerpo del correo electrónico 2            
from email.mime.text import MIMEText                     #Creación del cuerpo del correo electrónico 3
from shutil import rmtree                                #Gestión de directorios en el servidor
import smtplib                                           #Conexión con el servidor de correo
#from rpy2.robjects import r                              #Interfaz entre PYTHON y R
#from rpy2.robjects import numpy2ri                       #Interfaz entre PYTHON y R
from time import sleep                                   #Suspensión temporal
from os import remove
import pandas as pd                                      #Gestión de archivos de texto
import os                                                #Hereda funciones del sistema operativo para su uso en PYTHON                    
import base64                                            #Codifica contenido en base64 para su almacenamiento en una WEB
import pymssql                                           #Interfaz de conexión con la base de datos
import Consideraciones_generales                         #Gestión de documentos en LATEX en PYTHON debe tener preinstalado MIKTEX
import Graficas_comportamiento
import Tuberia_rec
'''---Componentes y librería de elaboración propia---'''
import Diseno_inicial                                    #Calculo preliminar de la hornilla
import Costos_funcionamiento                             #Calculo del costo financiero de la hornilla
import Pailas                                            #Calculo de las dimensiones de las pailas
import Gases                                             #Calculo de las propiedades de los gases
import Areas                                             #Calcular Areas
import EvaluacionHornilla                                #Calcular Areas
import random
import numpy as np

#Generación de la interfaz WEB
app = Flask(__name__)
#Creación de directorio temporal para almacenar archivos
uploads_dir = os.path.join(app.instance_path, 'uploads')
try:
    os.makedirs(uploads_dir, True)
except OSError: 
    print('Directorio existente')
   
'''---Funciones de direccionamiento en la interfaz WEB---'''
#Eliminar datos cargados en cache al actualizar la página.
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

#Directorio raíz (página principal)
@app.route('/')
def index():
    try:
        rmtree('static/pdf2')
    except OSError: 
        print('Directorio eliminado')
    return render_template('principal.html')

#Formulario para el ingreso de datos de usuario
@app.route('/usuario')
def usua():
    global df  
    global paises
    global Deptos_cana
    global Ciudad_cana
    df             = pd.read_json("static/Catalogos/Colombia.json")
    paises         = pd.read_excel("static/Catalogos/Paises.xlsx", engine='openpyxl') 
    cana           = pd.read_excel("static/Catalogos/Variedades.xlsx", engine='openpyxl')
    Deptos_cana    = cana['Depto'].values
    Ciudad_cana    = cana['Ciudad'].values
    
    return render_template('usuario.html', 
                           paises_lista=paises['Nombre'],
                           departamentos=df.departamento, 
                           provincia=df.ciudades,
                           Ciudad_cana_1=Ciudad_cana
                           )   

#Codificar los pdf en formato de texto plano
def Crear_archivo_base_64(ruta):
    with open(ruta, 'rb') as Archivo_codificado_1:
        Archivo_binario_1 = Archivo_codificado_1.read()
        Archivo_binario_64_1 = base64.b64encode(Archivo_binario_1)
        Mensaje_base_64_1 = Archivo_binario_64_1.decode('utf-8')
        return Mensaje_base_64_1
    
#De-codificar los pdf en formato de texto plano
def Leer_pdf_base64(Nombre_pdf, Texto_base64):
    PDF_Base64 = Texto_base64.encode('utf-8')
    with open(Nombre_pdf, 'wb') as Archivo_Normal:
        Archivo_deco = base64.decodebytes(PDF_Base64)
        Archivo_Normal.write(Archivo_deco)

def Enviar_msn(Correo, Nombre_cli, Estado):
    try:
        for i in range(0,Estado):
            # Crear el objeto mensaje
            mensaje = MIMEMultipart()             
            mensaje['From']     = 'hornillapp@agrosavia.co'                                 #Correo de prueba para enviar algo desde la página
            mensaje['To']       = Correo                                                    #Correo funcionario a cargo    
            mensaje['Subject']  = 'Informe generado con HornillAPP'                         #Correo funcionario a cargo          
            #Cuerpo del mensaje
            msn = ('Cordial saludo.\n En este correo encontrara el resultado generado con HornillAPP a través de un informe (Es posible que le lleguen dos correos debido a la gran cantidad de información disponible para usted).\n Atentamente: Equipo técnico de AGROSAVIA.')
            mensaje.attach(MIMEText(msn, 'plain'))
            # Adjuntar el archivo dado por el usuario
            # Estructura para adjuntar un archivo usando flask y HTML desde la raiz del directorio      
            archivo_adjunto = MIMEApplication(open('static/Descarga/Resumen'+Nombre_cli+'.pdf',"rb").read())
            archivo_adjunto.add_header('Content-Disposition', 'attachment', filename='Resumen.pdf')
            mensaje.attach(archivo_adjunto)
                       
            if(i==0):
                archivo_adjunto = MIMEApplication(open('static/Descarga/Financiero1'+Nombre_cli+'.pdf',"rb").read())
                archivo_adjunto.add_header('Content-Disposition', 'attachment', filename='Analisis.pdf')
                mensaje.attach(archivo_adjunto)
                
                archivo_adjunto = MIMEApplication(open('static/Descarga/Planos_WEB1'+Nombre_cli+'.pdf',"rb").read())
                archivo_adjunto.add_header('Content-Disposition', 'attachment', filename='Planos.pdf')
                mensaje.attach(archivo_adjunto)
            else:
                archivo_adjunto = MIMEApplication(open('static/Descarga/Financiero2'+Nombre_cli+'.pdf',"rb").read())
                archivo_adjunto.add_header('Content-Disposition', 'attachment', filename='Analisis2.pdf')
                mensaje.attach(archivo_adjunto)
                
                archivo_adjunto = MIMEApplication(open('static/Descarga/Planos_WEB2'+Nombre_cli+'.pdf',"rb").read())
                archivo_adjunto.add_header('Content-Disposition', 'attachment', filename='Planos2.pdf')
                mensaje.attach(archivo_adjunto)                
            # Datos de acceso a la cuenta de usuario
            usuario   ='hornillapp@agrosavia.co'
            contrasena='Contrasena123@'          
            #Interfaz de conexión con el servidor de gmail
            servidor = smtplib.SMTP('correoapp.agrosavia.co:587')
            servidor.starttls()
            servidor.login(usuario, contrasena)
            servidor.sendmail(mensaje['From'], mensaje['To'], mensaje.as_string())
            servidor.quit()         
    except:
        print('No se pudo enviar el informe')

def Diseño_Hornilla(Nombre_Rot, Ite, Rec_opt):
    global Diccionario 
    global Diccionario_2
    conta=0
    Eta=0
    while(Ite==0 and conta<1):
        """------------>>>>>>>>>>HORNILLA<<<<<<<<<<<<<<<<----------------"""
        """Calculo de la hornilla (Diseño inicial)"""
        Diccionario   = Diseno_inicial.datos_entrada(Diccionario,0,0)
        Diccionario_2 = Diseno_inicial.Calculo_por_etapas(Diccionario)
        Gases.diccionarios_sis(Diccionario,Diccionario_2)
        Calor_0=Diccionario_2['Calor Nece Calc por Etapa [kW]']
#        print(Calor_0)
#        print(int(Diccionario_2['Etapas']))
        Eta=int(Diccionario_2['Etapas'])
        Vo=np.ones(Eta)
        Gases.Propiedades(Calor_0,Vo,Vo,Vo, Eta)
        """Calcular volumenes iniciales"""
        
        Dimensi_Pail = Pailas.Mostrar_pailas(Diccionario_2['Volumen de jugo [m^3/kg]'],
                                            Eta,
                                            Nombre_Rot,
                                            Diccionario['Tipo de cámara de combustión'],
                                            Diccionario['Capacidad estimada de la hornilla'],
                                            altura_media,
                                            Diccionario,
                                            Rec_opt) 
#        print(Dimensi_Pail)
        """Optimizar valores"""
        L_temp = Areas.Areas_lisas(Dimensi_Pail)
        Gases.Propiedades(Calor_0,L_temp[0],L_temp[1],L_temp[2], Eta)
        Gases.Optimizacion(Diccionario, Diccionario_2, L_temp, Eta)       
        if(float(Diccionario['Bagazo suministrado'])<float(Diccionario['Bagazo seco'])):
            Ite=1
        conta=conta+1

def Exportar_diseno_excel(Dic, Nombre, Opt):
    Lista_temp1=[]
    Lista_temp2=[]
    for key in Dic.keys():
        Lista_temp1.append(key)
        if(key!='Etapas'):
            for item in Dic[key]:
                Lista_temp1.append(item)
            Lista_temp2.append(Lista_temp1)
            Lista_temp1=[]

    #Estructura para enviar datos a excel
    df1=pd.read_excel('static/Reporte1.xlsx')
    df2=pd.read_excel('static/Reporte2.xlsx')
    writer = pd.ExcelWriter('static/'+Nombre+'.xlsx')     
    df1.to_excel(writer, sheet_name='Gases')
    df2.to_excel(writer, sheet_name='Inicial')
    df3 = pd.DataFrame(Lista_temp2)
    df3.to_excel(writer, sheet_name='Diseno E')
    df4=pd.read_excel('static/Camara.xlsx')
    df4.to_excel(writer, sheet_name='Camara')
    
    if(Opt==0):
        df5=pd.read_excel('static/Chimenea.xlsx')
        df5.to_excel(writer, sheet_name='Chimenea')
        Direct='static/Pai_sin_rec.xlsx'
    else:
        Direct='static/Pai_con_rec.xlsx'     
    try:
        import openpyxl
        wb=openpyxl.load_workbook(Direct)
        sheets=wb.sheetnames
        for ii in sheets:
            df6=pd.read_excel(Direct, sheet_name=ii)
            df6.to_excel(writer, sheet_name=ii)
    except:
        print('Sin pailas')
    writer.save()
    


#Función para crear los diccionarios a partir de los calculos de la aplicación
def generar_valores_informe(Cliente_actual, Nombre_cli):
    #----------->>>>>>>>>>>Variables globales<<<<<<<<<<<<<<<---------
    global df
    global altura_media
    global NivelFre
    global Formulario_1_Etiquetas
    global Formulario_1_Valores
    global Formulario_2a_Etiquetas
    global Formulario_2a_Valores
    global Directorio
    global Deptos_cana
    global Ciudad_cana
    global Diccionario 
    global Diccionario_2
    global Diccionario_3
    global Diccionario_4
    global Result_Financie
    result=Cliente_actual
    """Creación de la primer parte del diccionario (leer del formulario de usuario)"""
    Pais_sel=result.get('Pais')
    a=result.to_dict()
    if(Pais_sel=='Colombia'):
        altura_media=float(result.get('Altura'))
        Nombre_Rot="Hornilla: "+a['Nombre de usuario']+" ("+a['Departamento']+'-'+a['Ciudad']+")"
    else:
        altura_media=1600  
        a['Departamento']='--'
        a['Ciudad']='--'
        Nombre_Rot="Hornilla: "+a['Nombre de usuario']+" ("+a['Pais']+")"
    #---------------->>>>>>>>>"""Cálculo del periodo vegetativo"""<<<<<<<<<<<<<<<<<<<
    Formulario_1_Etiquetas=[]
    Formulario_1_Valores=[]
    aux_i=' '      

    for i in a:
        if(i!='x' and i!='y' and i!='Panela producida por hora [kg/hora]' 
           and i!='Variedades de caña sembrada' and i!='Conoce el rendimiento de la caña' 
           and i!='Conece las variedades de caña'
           ):
            try:
                if(i!='Telefono'):
                    aux_i=str(round(float(a[i]),3))
                else:
                    aux_i=a[i]
            except:
                aux_i=a[i]
            Formulario_1_Etiquetas.append(i)
            Formulario_1_Valores.append(aux_i)
            
    Formulario_1_Etiquetas.append('Altura media sobre el nivel del mar')
    Formulario_1_Valores.append(str(altura_media)+' m')
    Formulario_1_Etiquetas.append('Nivel freático requerido')
    Formulario_1_Valores.append('Mínimo 4 metros')    
    """Creación de la segunda parte del diccionario"""
    a=result.to_dict()
    Formulario_2a_Etiquetas=[]
    Formulario_2a_Valores=[]
    G_brix_cana=0.0
    G_brix_panela=0.0
      
    #FORMULARIO 2a
    G_brix_cana=17     
    G_brix_panela=96
    Formulario_2a_Etiquetas.append('Grados Brix de la caña (promedio)')
    Formulario_2a_Valores.append(G_brix_cana)
    Formulario_2a_Etiquetas.append('Grados Brix de la panela (promedio)')
    Formulario_2a_Valores.append(G_brix_panela)    
    
    """----------->>>>Actualización de diccionarios<<<<<<<<<<--------"""
    Diccionario=dict(zip(Formulario_1_Etiquetas, Formulario_1_Valores))
    Dict_aux=dict(zip(Formulario_2a_Etiquetas, Formulario_2a_Valores))
    Diccionario.update(Dict_aux)  
    
    #Eliminar cosas que no se van a mostrar
    aux_form_1=[]
    aux_form_2=[]
    for w in Formulario_1_Etiquetas:
        if(w!='Etapas' and w!='Producción de la hornilla [kg/hora]' 
           and w!='Capacidad del molino [kg/hora]' and w!='Caña molida por hora [t]'
           and w!='Producción de panela anual [t]'):
            aux_form_1.append(w)
            aux_form_2.append(Formulario_1_Valores[Formulario_1_Etiquetas.index(w)])    
    Formulario_1_Etiquetas=aux_form_1
    Formulario_1_Valores=aux_form_2

    """Cálculo de las configuraciones de pailas de la hornilla (Diseño inicial)"""
    #Sin recuperador
    Diseño_Hornilla(Nombre_Rot, 0, 0) 
    Exportar_diseno_excel(Diccionario_2, 'Calculos_sin_rec', 0)
    Diccionario['Etapas']=str(int(float(Diccionario['Etapas']))-1)
    #Con recuperador
    Diseño_Hornilla(Nombre_Rot, 0, 1)
    Exportar_diseno_excel(Diccionario_2, 'Calculos_con_rec', 1)
    #Eliminar archivos
    remove("static/Camara.xlsx")
    remove("static/Chimenea.xlsx")
    remove("static/Pai_sin_rec.xlsx")
    remove("static/Reporte1.xlsx")
    remove("static/Reporte2.xlsx")    
    try:
        remove("static/Pai_con_rec.xlsx")
    except:
        print("El archivo no existe")
    
    """Presentar información del molino"""
    Formulario_3_Etiquetas=['Caña molida por hora [t]', 'Capacidad del molino [kg/hora]']
    Formulario_3_Valores=[]
    for i in Formulario_3_Etiquetas:
        Formulario_3_Valores.append(Diccionario[i])
        
    Molino=pd.read_excel('static/Temp/Temp.xlsx', engine='openpyxl',skipcolumn = 0,)
    
    Marca=Molino['Marca'].values
    Modelo=Molino['Modelo'].values
    Kilos=Molino['kg/hora'].values
    Valor=Molino['Precio'].values
    Enlaces=Molino['Link'].values
    Diccionario_4={'Marca':Marca,
                   'Modelo':Modelo,
                   'Capacidad [kg/h]':Kilos,
                   'Disponible en':Enlaces
            }

    Formulario_3_Etiquetas.append('Valor aproximado de un molino')
    Formulario_3_Valores.append(Costos_funcionamiento.Formato_Moneda(sum(Valor)/len(Valor), "$", 2))
    Diccionario_3=dict(zip(Formulario_3_Etiquetas,Formulario_3_Valores))
    
    """Analisis financiero"""
    Costos_funcionamiento.Variables(float(Diccionario['Capacidad estimada de la hornilla']),
                                    float(Diccionario['Horas de trabajo de la hornilla por día']), 
                                    float(Diccionario['Días trabajados a la semana']), 
                                    float(Diccionario['Moliendas al año']),
                                    float(Diccionario['Producción anual de caña [t]']),
                                    float(Diccionario['Caña molida por hora [t]']))
    
    Result_Financie=Costos_funcionamiento.costos() #Sin recuperador
    
    """Generar portada"""
    Memoria_temp=' ha'
    Crecimiento=float(result.get('Área de caña disponible (Hectáreas)'))
    #Crecimiento=Crecimiento+float(result.get("Área de caña proyectada que se espera moler en los próximos 5 años (Hectáreas)"))
    
    if(float(Diccionario['Capacidad estimada de la hornilla'])<250):
        Memoria_temp=' ha'
    else:
        Memoria_temp=' ha (ajustado de acuerdo con la capacidad de diseño de HornillApp)'
        
    Consideraciones_generales.Documento_Latex.portada(Diccionario,
                                      Diccionario['Tipo de hornilla'],
                                      Diccionario['Área de la bagacera (m^2)'],
                                      str(Crecimiento), 
                                      Memoria_temp)
    Consideraciones_generales.Documento_Latex.seccion1(Diccionario, Diccionario_2)
    Consideraciones_generales.Documento_Latex.generar_pdf()
    
    if(float(Diccionario['Capacidad estimada de la hornilla'])<=150):
        Tuberia_rec.Documento_Latex.portada()
        Tuberia_rec.Documento_Latex.Mostrar_rec()
        Tuberia_rec.Documento_Latex.generar_pdf() 
    sleep(5)
    """Creación del pdf"""
    Pailas.Generar_reporte(Diccionario, Diccionario_2, Nombre_cli)
    Graficas_comportamiento.Documento_Latex.reporte(Nombre_cli)

    """>>>>>>>>>>>>>>>>Actualizar base de datos<<<<<<<<<<<<<<""" 
    Archivo1=Crear_archivo_base_64('static/Calculos_sin_rec.xlsx')
    Archivo2=Crear_archivo_base_64("static/Descarga/Planos_WEB1"+Nombre_cli+".pdf")
    Archivo3=' '
    Archivo4=' '
    bandera_correo=2
    if(float(Diccionario['Capacidad estimada de la hornilla'])<=150):
        bandera_correo=2
        Archivo3=Crear_archivo_base_64('static/Calculos_con_rec.xlsx')
        Archivo4=Crear_archivo_base_64("static/Descarga/Planos_WEB2"+Nombre_cli+".pdf")
    else:
        bandera_correo=1
        Archivo3=' '
        Archivo4=' '
    try:
        Telef=int(float(Diccionario['Telefono']))
    except:
        Telef=0  
    usuarios = (Diccionario['Nombre de usuario'],
                Diccionario['Correo'],
                Telef,
                Diccionario['Pais'], 
                Diccionario['Departamento'],
                Diccionario['Ciudad'], 
                Archivo1, 
                Archivo2, 
                Archivo3, 
                Archivo4
                )
    Operaciones_db(2,tuple(usuarios))        #Usar base de datos
    sleep(1)
    
    Enviar_msn(str(Diccionario['Correo']),Nombre_cli, bandera_correo)

       
#>>>>>>>>>>>------------Enlace para la generación del informe económico------<<<<<<<<<<
#Segmento 2 del informe (presentación de las caracteristicas de la caña)
@app.route('/Economico1')
def Eco1():
    global Result_Financie
    global Diccionario 
    if(float(Diccionario['Capacidad estimada de la hornilla'])<=150):
        Bande=0
    else:
        Bande=1    
    return render_template('Economico1.html', 
                           a=Result_Financie[0],
                           b=Result_Financie[1],
                           Activa=Bande) 

def Arch_hilo():
    try:
        rmtree('static/Temp')
        os.mkdir('static/Temp')
    except:
        os.mkdir('static/Temp')
    try:  
        rmtree('static/pdf00')
        os.mkdir('static/pdf00')
    except:
        os.mkdir('static/pdf00')
    try:  
        rmtree('static/pdf01')
        os.mkdir('static/pdf01')
    except:
        os.mkdir('static/pdf01')
    try:  
        rmtree('static/pdf02')
        os.mkdir('static/pdf02')
    except:
        os.mkdir('static/pdf02')
    try:  
        rmtree('static/pdf03')
        os.mkdir('static/pdf03')
    except:
        os.mkdir('static/pdf03')
    try:  
        rmtree('static/pdf04')
        os.mkdir('static/pdf04')
    except:
        os.mkdir('static/pdf04')

#Presentación del informe al usuario  
@app.route('/informe', methods = ['GET', 'POST'])
def infor():
    global cliente
    global cuenta_cliente
    global result
    global Lista_clientes
    global Estado_Cliente
    global Diccionario 
    #Limpiar directorios de uso temporal
    #Continuar ejecución
    if request.method == 'POST':
        result = request.form
        cliente=cliente+1
        temp_cli="c"+str(cliente)
        cuenta_cliente.append(temp_cli)
        Lista_clientes.append(result)
        Bande=0
        if(cliente>1):
            globals()[temp_cli]=True
        else:
            globals()[temp_cli]=False
            
        while(globals()[temp_cli]==True):
            print("Espere: "+temp_cli+"Estado="+str(globals()[temp_cli]))
            print(cliente)
            print(cuenta_cliente)
            sleep(1)
        
        Nombre_cli="cli_"+str(random.randint(0, 100))
        Arch_hilo()
        generar_valores_informe(Lista_clientes[0], Nombre_cli)
        
        try:
            Lista_clientes.pop(0)
            cuenta_cliente.pop(0)
            globals()[cuenta_cliente[0]]=False     
        except:
            print("Cliente no disponible")   
        cliente=cliente-1
        
        if(float(Diccionario['Capacidad estimada de la hornilla'])<=150):
            Bande=0
        else:
            Bande=1
            
        return render_template('informe.html', 
                               Nom1="/static/Descarga/Financiero1"+Nombre_cli+".pdf",
                               Nom2="/static/Descarga/Financiero2"+Nombre_cli+".pdf",
                               Nom3="/static/Descarga/Resumen"+Nombre_cli+".pdf",
                               Nom4="/static/Descarga/Planos_WEB1"+Nombre_cli+".pdf",
                               Nom5="/static/Descarga/Planos_WEB2"+Nombre_cli+".pdf",
                               Nom6="static/Descarga/Graf"+Nombre_cli+".pdf",
                               Activa=Bande
                               )
       
#------->>>>>>>>Operaciones básicas con la base de datos<<<<<<<<--------
def Operaciones_db(Operacion, usuarios):
    db_1=[]
    r_b=[]
    Cadena_sql= "DELETE FROM Clientes WHERE ID IN "
    try:
        cnxn = pymssql.connect(host='COMOSPSQL02/MSSQL2016',
                               database='DbSistemaExpertoPanela',
                               user='SistemaExpertoPanela',
                               password='LoGhofIrUmb3oeDET8RW')
                               #host='172.16.11.44\MSSQL2016DSC', 
                               #database='SistemaExpertoPanela', 
                               #user='WebSisExpPanela', 
                               #password='sIuusnOsE9bLlx7g60Mz') 
        cursor = cnxn.cursor()
        #Consulta
        if(Operacion==0):             
            cursor.execute("SELECT * FROM Clientes")
            for tdb in cursor:
                db_1.append(tdb)
        #Borrar
        elif(Operacion==1):
            cursor.execute("DELETE FROM Clientes WHERE CONVERT(NVARCHAR(MAX), Nombre)!='NO_BORRAR'")
        #Insertar
        elif(Operacion==2):
            cursor.execute("INSERT INTO Clientes (Nombre, Correo, Telefono, Pais, Departamento, Ciudad, Usuario, Planos, Recinto, Calculos) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", usuarios)
        #Busqueda
        elif(Operacion==3):
            cursor.execute("SELECT * FROM Clientes")
            for i,tdb in enumerate(cursor, start=0):
                #print(tdb[0])
                try:
                    if(usuarios.get('CH_'+str(tdb[0]))=='on'):
                        #r_b.append(str(tdb[0]))
                        T1=str(tdb[0]).replace("[","(")
                        T1=T1.replace("]",")")
                        Cadena_sql=Cadena_sql+"("+T1+")"
                        cursor.execute(Cadena_sql)
                except:
                    print('No existe')
        try:
            cnxn.commit()
            cnxn.close()
        except:
            print('Error db')         
        return db_1
    except:
        print('Error db') 

#Formulario para borrar usuarios completamente
@app.route('/borrar')
def borrar_base_1():
    Operaciones_db(1,0)
    return render_template('principal.html')

#Formulario para borrar usuarios seleccioandos
@app.route('/borrar2', methods = ['POST','GET'])
def borrar_base_2():
    if request.method == 'POST':
        Eliminar = request.form    
        Operaciones_db(3,Eliminar)
    
    return render_template('Construccion.html', aviso="Operación finalizada.")


#Formulario de bienvenida para el acceso a la base de datos
@app.route('/acceso', methods = ['POST','GET'])
def acceso_base():
   return render_template('acceso.html', aviso="Por favor, complete los siguientes campos.")

@app.route('/Evaluacion')
def Eva_horni():
   return render_template('Evaluacion.html', entrada=0)

@app.route('/EvaRta', methods = ['POST','GET'])
def Eva_horni2():
    try:
        if(request.files['adjunto'].filename!=''):
            archivo = request.files['adjunto']
            nombre_archivo_xls=os.path.join(uploads_dir, secure_filename(archivo.filename))
            archivo.save(nombre_archivo_xls)
            print(nombre_archivo_xls)
            EvaluacionHornilla.EvaluacionPar(nombre_archivo_xls)
            return render_template('Evaluacion.html', entrada=1)
    except:
        return render_template('Evaluacion.html', entrada=0)

@app.route('/Modificacion')
def Mod_horni():
   return render_template('Construccion.html', aviso="En construcción.")

                
@app.route('/Menubase', methods = ['POST','GET'])
def Acceso_Menu():
    if request.method == 'POST':
        datos_usuario = request.form
        Nombre_Usuario=datos_usuario.get('Documentoa')
        Clave_Usuario=datos_usuario.get('Clavea')
        if(Nombre_Usuario=="1234567" and Clave_Usuario=="112233"):
            return render_template('Accesomenu.html')
        else:
            return render_template('acceso.html', aviso="Verifique su nombre de usuario o contraseña.")
        
#Formulario de respuesta al acceder a la base de datos
@app.route('/base')
def base_batos():
    #Listas para almacenamiento temporal de los datos de usuario
    Etiquetas_ID=[]
    Etiquetas_Nombres=[]
    Etiquetas_Correo=[]
    Etiquetas_Telefono=[]
    Etiquetas_Pais=[]
    Etiquetas_Departamento=[]
    Etiquetas_Ciudad=[]
    Etiquetas_U=[]
    Etiquetas_P=[]
    Etiquetas_R=[]
    Etiquetas_C=[]
    Cantidad_Clientes=0
    print("clientes1")
    try:
        os.mkdir('static/pdf2')
    except OSError: 
        print('Directorio existente') 
    #Consulta de la base de datos
    db=Operaciones_db(0,0)
    print("clientes2")
    #Creación de listas con los datos de usuario
    for listas_1 in db:
        Etiquetas_ID.append(listas_1[0])
        Etiquetas_Nombres.append(listas_1[1])
        Etiquetas_Correo.append(listas_1[2])
        Etiquetas_Telefono.append(listas_1[3])
        Etiquetas_Pais.append(listas_1[4])
        Etiquetas_Departamento.append(listas_1[5])
        Etiquetas_Ciudad.append(listas_1[6])
        Etiquetas_U.append("pdf2/U_"+str(Cantidad_Clientes)+".xlsx")
        Etiquetas_P.append("pdf2/P_"+str(Cantidad_Clientes)+".pdf")
        Etiquetas_R.append("pdf2/R_"+str(Cantidad_Clientes)+".xlsx")
        Etiquetas_C.append("pdf2/C_"+str(Cantidad_Clientes)+".pdf")
        try:
            print('Error aceptado: '+str(Cantidad_Clientes))
            Leer_pdf_base64("static/pdf2/U_"+str(Cantidad_Clientes)+".xlsx", listas_1[7])
            Leer_pdf_base64("static/pdf2/P_"+str(Cantidad_Clientes)+".pdf", listas_1[8])
            Leer_pdf_base64("static/pdf2/R_"+str(Cantidad_Clientes)+".xlsx", listas_1[9])
            Leer_pdf_base64("static/pdf2/C_"+str(Cantidad_Clientes)+".pdf", listas_1[10])         
        except:
            print('Error cliente: '+str(Cantidad_Clientes))
        Cantidad_Clientes=Cantidad_Clientes+1
    print("clientes3")
    return render_template('base.html',
                           Eti0=Etiquetas_ID,
                           Eti1=Etiquetas_Nombres,
                           Eti2=Etiquetas_Correo,
                           Eti3=Etiquetas_Telefono,
                           Eti3a=Etiquetas_Pais,
                           Eti4=Etiquetas_Departamento,
                           Eti5=Etiquetas_Ciudad,
                           Eti6=Etiquetas_U,
                           Eti7=Etiquetas_P,
                           Eti8=Etiquetas_R,
                           Eti9=Etiquetas_C,
                           Cant=Cantidad_Clientes)
 
#Enlaces para las otras páginas referencias, nosotros, presentación, etc.        
@app.route('/referencias')
def refe():
   return render_template('referencias.html')

@app.route('/nosotros')
def nosot():
   return render_template('nosotros.html')

@app.route('/contacto', methods = ['GET'])
def contac_form():
   return render_template('contacto.html')

#Página de contacto.
@app.route('/contacto', methods = ['POST'])
def contac_rta():
    try:
        if request.method == 'POST':
            #Datos del correo eléctronico            
            Nombre       = request.form['nombre']
            Correo       = request.form['correo_electronico']
            Mensaje_HTML = request.form['mensaje_usuario']
            # Crear el objeto mensaje
            mensaje = MIMEMultipart()             
            mensaje['From']    = 'hornillapp@agrosavia.co'  #Correo de prueba para enviar algo desde la página
            mensaje['To']      = 'hornillapp@agrosavia.co'  #Correo funcionario a cargo        
            mensaje['Subject'] = 'Información clientes'     #Correo funcionario a cargo   
            #Cuerpo del mensaje
            msn = ('Este mensaje fue enviado por: '+Nombre+'\n'
                  +'Responder al correo electronico: '+Correo+'\n'
                  +'Contenido: '+Mensaje_HTML)
            mensaje.attach(MIMEText(msn, 'plain'))
            # Adjuntar el archivo dado por el usuario
            # Estructura para adjuntar un archivo usando flask y HTML desde la raiz del directorio
            if(request.files['adjunto'].filename!=''):
                archivo = request.files['adjunto']
                nombre_archivo_pdf=os.path.join(uploads_dir, secure_filename(archivo.filename))
                archivo.save(nombre_archivo_pdf)            
                archivo_pdf = MIMEApplication(open(nombre_archivo_pdf,"rb").read())
                archivo_pdf.add_header('Content-Disposition', 'attachment', filename=nombre_archivo_pdf)
                mensaje.attach(archivo_pdf) 
                os.remove(nombre_archivo_pdf)
            # Datos de acceso a la cuenta de usuario
            usuario   ='hornillapp@agrosavia.co'
            contrasena='Contrasena123@'          
            #Interfaz de conexión con el servidor de gmail
            servidor = smtplib.SMTP('correoapp.agrosavia.co:587')
            servidor.starttls()
            servidor.login(usuario, contrasena)
            
            servidor.sendmail(mensaje['From'], mensaje['To'], mensaje.as_string())
            servidor.quit()  
            return render_template('respuesta.html',rta="MENSAJE ENVIADO CON EXITO.")
    except:
        return render_template('respuesta.html',rta="ERROR AL ENVIAR EL MENSAJE (INTENTE NUEVAMENTE).")

#Función principal    
if __name__ == '__main__':
    global cliente
    global cuenta_cliente
    global Lista_clientes
    cliente = 0
    cuenta_cliente = []
    Lista_clientes=[]
    app.run(host='0.0.0.0', port='7000')