# IMPORTAR LIBRERIA
import numpy as np
import pandas as pd
import math

def numero_tubos(x):
    Diamext=DIMENSIONES.loc[x,['Diametro exterior.mm']]
    Diamext=Diamext.to_numpy()
    Diamext=Diamext/1000
    Areatotal=Area_TranCalor
    Ltotaltuberia=Areatotal/(Diamext*math.pi)
    lista_LDisTube=[6.0,3.0,2.0,1.5,1.0]
    LongSel=lista_LDisTube[3]
    LcomerTube=6
    N_Tubos=Ltotaltuberia/LongSel
    return [round(N_Tubos[0]), Diamext] 

#IMPORTAR ARCHIVO EXCEL
#path = "C:/Users/Camila Rodriguez/Documents/CAMILA/Camila/Escritorio/"
rcalor1 = pd.read_excel('rcalor1.xlsx')
rcalor1.info()
#codigo variables de entrada
Pro_hornilla=40 #kg/h
Consum_Bagazo=3 #kg/h
Eff_Calculada=30 #%
Temp_Ultmpaila=450 #°C
Temp_DespRecup=200
Exceso_aire=1.6
hum_bagazo=30 #%
Pre_Trabajo=100 #PSI
Temp_dentroRecup=169.936 #°C

Flujo_Masico=0.276093100*3600
Calor_gases=Flujo_Masico*(0.000355*(Temp_Ultmpaila**2-Temp_DespRecup**2)+1.1216*(Temp_Ultmpaila-Temp_DespRecup)) #KJ/h
print(Calor_gases)
Calor_gases1=Calor_gases/3600 #KW
Media_TermLog=((Temp_Ultmpaila-Temp_DespRecup)/math.log((Temp_Ultmpaila-Temp_dentroRecup)/(Temp_DespRecup-Temp_dentroRecup))) #°C
Coefglob_transCalor=25 #w/m2°k
Area_TranCalor=(Calor_gases1*1000)/(Coefglob_transCalor*Media_TermLog)

#RESULTADOS DE VARIABLES CALCULADAS
print (Flujo_Masico)
print(Calor_gases)
print(Calor_gases1)
print(Media_TermLog)
print(Coefglob_transCalor)
print(Area_TranCalor)

#LEER DATOS HOJA 2 DIMENSIONES
DIMENSIONES = pd.read_excel('rcalor1.xlsx',sheet_name = "DIMENSIONES")
DIMENSIONES.info()

import pandas as pd
DIMENSIONES.set_index('Diametro nominal Nps', inplace=True)
DIMENSIONES

lista_numero_tubos= numero_tubos('1.1/2')
print(lista_numero_tubos[0])

import math
Diamext=lista_numero_tubos[1]
DiametroChimenea=(1.5*Diamext)+(1.5*Diamext)+(0.5*Diamext)+0.02 

print(DiametroChimenea)