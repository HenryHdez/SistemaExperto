from flask import Flask, request, render_template
from difflib import SequenceMatcher as SM
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import os
import math
from werkzeug.utils import secure_filename
import Diseno_inicial
import Costos_funcionamiento
import Pailas
import pandas as pd
#import Gases

app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'uploads')
try:
    os.makedirs(uploads_dir, True)
except OSError: 
    print('Directorio existente')
    
#class MyFPDF(FPDF, HTMLMixin):
#    pass

@app.route('/')
def index():
   return render_template('principal.html')

#Está función permite llamar al esquema de generar dotas de usuario
@app.route('/usuario')
def usua():
    global df  
    global Deptos_cana
    global Ciudad_cana
    global Tipo_cana
    global Grados_Bx
    global Nivel_pH
    global Nivel_azucar
    global Nivel_Sacarosa
    global Nivel_pureza
    global Nivel_Fosforo
    global Nivel_Calidad
    global Nivel_brpane
    df            = pd.read_json("static/Catalogos/Colombia.json")
    cana          = pd.read_excel('static/Catalogos/Variedades.xlsx')
    Deptos_cana   = cana['Depto'].values
    Ciudad_cana   = cana['Ciudad'].values
    Tipo_cana     = cana['Tipo'].values
    Grados_Bx     = cana['Br'].values
    Nivel_pH      = cana['pH'].values
    Nivel_azucar  = cana['Azucares'].values
    Nivel_Sacarosa= cana['Sacarosa'].values
    Nivel_pureza  = cana['Pureza'].values
    Nivel_Fosforo = cana['Forforo'].values
    Nivel_Calidad = cana['Calidad'].values 
    Nivel_brpane  = cana['BrPanela'].values
    Variedad_cana =[]
    for i in range(0,len(Deptos_cana)):
        if(i==0):
            Variedad_cana.append(Tipo_cana[i]+", -Valor por defecto-, °Brix= "+str(Grados_Bx[i]))
        else:
            Variedad_cana.append(Tipo_cana[i]+", Disponible en: "+Deptos_cana[i]+"-"+Ciudad_cana[i]+", °Brix= "+str(Grados_Bx[i]))
    return render_template('usuario.html', 
                           departamentos=df.departamento, 
                           provincia=df.ciudades,
                           Ciudad_cana_1=Ciudad_cana,
                           Variedad_cana_1=Variedad_cana,
                           )      

def generar_valores_informe():
    """Está función genera los rotulos de las páginas 1 y 2 del informe en HTML"""
    global df
    global result
    global altura_media
    global NivelFre
    global Diccionario
    global Formulario_1_Etiquetas
    global Formulario_1_Valores
    global Formulario_2_Etiquetas
    global Formulario_2_Valores
    global Formulario_2a_Etiquetas
    global Formulario_2a_Valores
    global Directorio
    global Deptos_cana
    global Ciudad_cana
    global Tipo_cana
    global Grados_Bx
    global Nivel_pH
    global Nivel_azucar
    global Nivel_Sacarosa
    global Nivel_pureza
    global Nivel_Fosforo
    global Nivel_Calidad
    global Nivel_brpane
    global Diccionario 
    global Diccionario_2
    global Diccionario_3
    global Diccionario_4
    """Creación de la primer parte del diccionario"""
    Dept=result.get('Departamento')
    D_aux=df.departamento
    D_aux=D_aux.tolist()
    amsnm=df.altura
    amsnm=amsnm.tolist()
    H2O=df.aguasubterranea
    H2O=H2O.tolist()
    altura_media=amsnm[D_aux.index(Dept)]
    NivelFre=H2O[D_aux.index(Dept)]
    vector=['Nombre de usuario','Departamento','Ciudad','Crecimiento aproximado del área sembrada',
            'Área caña sembrada','Caña por esperada hectárea',
            'Periodo vegetativo','Caña por hectárea esperada','Número de moliendas',
            'Días de trabajo a la semana','Horas de trabajo al día','Variedad de Caña 1']
    #---------------->>>>>>>>>"""Calculo del periodo vegetativo"""<<<<<<<<<<<<<<<<<<<
    Formulario_1_Etiquetas=[]
    Formulario_1_Valores=[]
    a=result.to_dict()        
    for i in a:
        Formulario_1_Etiquetas.append(i)
        Formulario_1_Valores.append(a[i])
    r=len(a)
    del(Formulario_1_Etiquetas[r-1])
    del(Formulario_1_Valores[r-1])
    Formulario_1_Etiquetas.append('Altura media sobre el nivel del mar')
    Formulario_1_Valores.append(str(altura_media)+' m')
    Formulario_1_Etiquetas.append('Nivel freático')
    Formulario_1_Valores.append(str(NivelFre)) 
    #Determinar periodo vegetativo
    Formulario_1_Etiquetas.append('Periodo vegetativo')
    if(altura_media<=1200):
        Formulario_1_Valores.append(str(12))
    elif (altura_media>1200 and altura_media<=1500):
        Formulario_1_Valores.append(str(15))
    else:
        Formulario_1_Valores.append(str(18))
        
    Diccionario=dict(zip(Formulario_1_Etiquetas,Formulario_1_Valores))  
    """Creación de la segunda parte del diccionario"""
    a=result.to_dict()
    cantidadcanas=int(a['Cantidad de variedades de caña sembrada'])+1
    Formulario_2_Etiquetas=[]
    Formulario_2_Valores=[] 
    Formulario_2a_Etiquetas=[]
    Formulario_2a_Valores=[]
    Directorio =[]
    G_brix_cana=0.0;
    G_brix_panela=0.0;    
    for contacana in range(1,cantidadcanas):
        try:
            Valor_cana_buscar='Variedad de Caña '+str(contacana)
            index=int(a[Valor_cana_buscar])-1 
            Formulario_2_Etiquetas.append(Valor_cana_buscar)
            Formulario_2_Valores.append(Tipo_cana[index])    
            Formulario_2_Etiquetas.append('Grados Brix de la caña '+str(contacana))
            Formulario_2_Valores.append(Grados_Bx[index]) 
            Formulario_2_Etiquetas.append('pH')
            Formulario_2_Valores.append(Nivel_pH[index])    
            Formulario_2_Etiquetas.append('Azúcares reductores (%)')
            Formulario_2_Valores.append(Nivel_azucar[index]) 
            Formulario_2_Etiquetas.append('Sacarosa (%)')
            Formulario_2_Valores.append(Nivel_Sacarosa[index])    
            Formulario_2_Etiquetas.append('Pureza (%)')
            Formulario_2_Valores.append(Nivel_pureza[index])  
            Formulario_2_Etiquetas.append('Fósforo (ppm)')
            Formulario_2_Valores.append(Nivel_Fosforo[index])    
            #Formulario_2_Etiquetas.append('Calidad de la panela')
            #Formulario_2_Valores.append(Nivel_Calidad[index])  
            Formulario_2_Etiquetas.append('Grados Brix de la panela '+str(contacana))
            Formulario_2_Valores.append(Nivel_brpane[index])
            #Formulario_2_Etiquetas.append('Posible ubicación')
            #Formulario_2_Valores.append(Deptos_cana[index]+', '+Ciudad_cana[index]) 
            Formulario_2_Etiquetas.append('>---------------------------------<')
            Formulario_2_Valores.append('>---------------------------------<')
            G_brix_cana=G_brix_cana+float(Grados_Bx[index])
            G_brix_panela=G_brix_panela+float(Nivel_brpane[index])
            Directorio.append('Cana/'+Tipo_cana[index]+'.png')
        except:
            print("Variedad no disponible")
    #Exportar variedades de caña seleccionadas
    datos_temp=[Formulario_2_Etiquetas,Formulario_2_Valores]
    df = pd.DataFrame(datos_temp)
    df.to_excel('static/Temp/Temp4.xlsx')   
    datos_temp=[Directorio]
    df = pd.DataFrame(datos_temp)
    df.to_excel('static/Temp/Temp5.xlsx')  
    #Grados brix promedio para publicar en el informe
    G_brix_cana=round(G_brix_cana/len(Directorio),3)       
    G_brix_panela=round(G_brix_panela/len(Directorio),3)
    Formulario_2a_Etiquetas.append('Grados Brix de la caña (promedio)')
    Formulario_2a_Valores.append(G_brix_cana)
    Formulario_2a_Etiquetas.append('Grados Brix de la panela (promedio)')
    Formulario_2a_Valores.append(G_brix_panela)    
    Dict_aux=dict(zip(Formulario_2a_Etiquetas,Formulario_2a_Valores))
    Diccionario.update(Dict_aux)
    
    """------------>>>>>>>>>>HORNILLA<<<<<<<<<<<<<<<<"""
    """Calculo de la hornilla"""
    Diccionario   = Diseno_inicial.datos_entrada(Diccionario,0,0)
    Diccionario_2 = Diseno_inicial.Calculo_por_etapas(Diccionario)
    Pailas.Mostrar_pailas(
            Diccionario_2['Volumen de jugo [m^3/kg]'],
            int(Diccionario_2['Etapas']),
            "Hornilla: "+Diccionario['Nombre de usuario']+" ("+Diccionario['Departamento']+'-'+Diccionario['Ciudad']+')'
            )
    """Presentar información del molino"""
    Formulario_3_Etiquetas=['Caña molida al mes', 'Area Cosechada al mes',	 'Caña molida a la semana',		
                            'Caña Molida por Hora', 'Jugo Crudo',	 'Jugo Clarificado', 'Masa de panela',		
                            'Capacidad del Molino']
    Formulario_3_Valores=[]
    for i in Formulario_3_Etiquetas:
        Formulario_3_Valores.append(Diccionario[i])
        
    Molino=pd.read_excel('static/Temp/Temp.xlsx',skipcolumn = 0,)
    Marca=Molino['Marca'].values
    Modelo=Molino['Modelo'].values
    Kilos=Molino['kg/hora'].values
    Diesel=Molino['Diesel'].values
    Electrico=Molino['Electrico'].values
    Valor=Molino['Precio'].values
    Enlaces=Molino['Link'].values
    Diccionario_4={'Marca':Marca,
                   'Modelo':Modelo,
                   'Capacidad':Kilos,
                   'Disponible en':Enlaces
            }

    Formulario_3_Etiquetas.append('Valor aproximado de un molino')
    Formulario_3_Valores.append('$'+str(math.ceil(sum(Valor)/len(Valor))))
    Diccionario_3=dict(zip(Formulario_3_Etiquetas,Formulario_3_Valores))
    
    """Estimar propiedades de los gases"""
#    Gases.Optimizacion(Diccionario,Diccionario_2)
    """Analisis financiero"""
    Costos_funcionamiento.Variables(float(Diccionario['Capacidad Estimada de la hornilla']),
                                    float(Diccionario['Horas de trabajo al día']), 
                                    float(Diccionario['Días de trabajo a la semana']), 
                                    float(Diccionario['Número de moliendas']),
                                    float(Diccionario['Caña molida al mes']))
    Costos_funcionamiento.costos()
    """Creación del pdf"""
    Pailas.Generar_reporte(Diccionario,Diccionario_2)
    
#Enlaces para la generación del informe
@app.route('/informe4')
def infor4():
    global Diccionario
    return render_template('informe4.html',result=Diccionario) 

@app.route('/informe3')
def infor3():
    global Diccionario_3
    global Diccionario_4
    return render_template('informe3.html',result=Diccionario_3, Molinos=Diccionario_4) 

@app.route('/informe2')
def infor2():
    global Formulario_2_Etiquetas
    global Formulario_2_Valores
    global Directorio
    return render_template('informe2.html', 
                           Etiquetas = Formulario_2_Etiquetas, 
                           Valores = Formulario_2_Valores,
                           Dir = Directorio,
                           Cant_fotos=len(Directorio))  

@app.route('/informe1')
def infor1():
    global Formulario_1_Etiquetas
    global Formulario_1_Valores
    #rutina para filtrar y eliminar la palabra variedad de caña
    lista_etiquetas_filtradas=[]
    lista_valores_filtrados=[]
    for i in range(len(Formulario_1_Etiquetas)):
        if(SM(None, 'Variedad de Caña', Formulario_1_Etiquetas[i]).ratio()<0.85):
            lista_etiquetas_filtradas.append(Formulario_1_Etiquetas[i])
            lista_valores_filtrados.append(Formulario_1_Valores[i])              
    return render_template('informe1.html', 
                           Etiquetas = lista_etiquetas_filtradas, 
                           Valores = lista_valores_filtrados)     
    
@app.route('/informe', methods = ['POST','GET'])
def infor():
    global result
    if request.method == 'POST':
        result = request.form
        generar_valores_informe()
        return render_template('informe.html') 

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
             
            mensaje['de']     = 'agropru1@gmail.com'       #Correo de prueba
            mensaje['para']   = 'hahernandez@agrosavia.co' #Correo funcionario
            
            #Construcción del mensaje
            msn = ('Este mensaje fue enviado por: '+Nombre+'\n'
                  +'Responder al correo electronico: '+Correo+'\n'
                  +'Contenido: '+Mensaje_HTML)
            
            mensaje.attach(MIMEText(msn, 'plain'))
            
            #Adjuntar el archivo .pdf
            # Estructura para adjuntar un archivo usando flask y HTML desde la raiz del directorio
            if(request.files['adjunto'].filename!=''):
                archivo = request.files['adjunto']
                nombre_archivo_pdf=os.path.join(uploads_dir, secure_filename(archivo.filename))
                archivo.save(nombre_archivo_pdf)            
                archivo_pdf = MIMEApplication(open(nombre_archivo_pdf,"rb").read())
                archivo_pdf.add_header('Content-Disposition', 'attachment', filename=nombre_archivo_pdf)
                mensaje.attach(archivo_pdf) 
                os.remove(nombre_archivo_pdf)
            # parámetros fijos de la cuenta de correo
            usuario   ='agropru1'
            contrasena='Agrosavia123'          
            #Iniciación del servidor de gmail
            servidor = smtplib.SMTP('smtp.gmail.com:587')
            servidor.starttls()
            servidor.login(usuario, contrasena)
            servidor.sendmail(mensaje['de'], mensaje['para'], mensaje.as_string())
            servidor.quit()  
            return render_template('respuesta.html',rta="MENSAJE ENVIADO CON EXITO.")
    except:
        return render_template('respuesta.html',rta="ERROR AL ENVIAR EL MENSAJE (INTENTE NUEVAMENTE).")
    
if __name__ == '__main__':
   app.run()