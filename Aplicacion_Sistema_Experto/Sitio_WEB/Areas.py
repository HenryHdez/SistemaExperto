# -*- coding: utf-8 -*-
import numpy as np
import math
 
def Area_Semiesferica(Diametro_de_Paila, Altura_de_Paila, Altura_de_Ducto, Ancho_ducto_Fondo):
#Area de Flujo semiesferica
# R = Radio, h Altura, o1 = Angulo, s = Arco , d = Altura desde el centro, c= Ancho de Paila   
    D=Ancho_ducto_Fondo/2
    C=Diametro_de_Paila/2
    A=(C**2-D**2+Altura_de_Ducto**2+2*Altura_de_Ducto*Altura_de_Paila+Altura_de_Paila**2)/(2*Altura_de_Ducto+2*Altura_de_Paila)
    B=Altura_de_Paila+Altura_de_Ducto-A
    Rt=(A**2+D**2)**(1/2)
    R=((Diametro_de_Paila/2)**2+Altura_de_Paila**2)/(2*Altura_de_Paila)
    pi=math.pi
    Area_Total= pi*Rt**2
    o1=2*math.acos(B/Rt)
    o2=2*math.acos((R-Altura_de_Paila)/R)
    o3=2*math.acos(A/Rt)
    A1=(Rt**2/2)*(o1-math.sin(o1))
    A2=(R**2/2)*(o2-math.sin(o2))
    A3=(Rt**2/2)*(o3-math.sin(o3))
    Area_Flujo=Area_Total-A1-A2-A3
    s1=Rt*o1
    s2=R*o2
    s3=Rt*o3
    Perimetro_de_Flujo= pi*2*Rt-(s3+s1)+Ancho_ducto_Fondo+s2
    return [Area_Flujo, Perimetro_de_Flujo]

def Area_semicilindrica(Ancho_de_Paila, Altura_de_Paila, Altura_de_Ducto, Ancho_ducto_Fondo):
#Area de Flujo semicilindrica
# R = Radio, h Altura, o1 = Angulo, s = Arco , d = Altura desde el centro, c= Ancho de Paila   
    D=Ancho_ducto_Fondo/2
    C=Ancho_de_Paila/2
    A=(C**2-D**2+Altura_de_Ducto**2+2*Altura_de_Ducto*Altura_de_Paila+Altura_de_Paila**2)/(2*Altura_de_Ducto+2*Altura_de_Paila)
    B=Altura_de_Paila+Altura_de_Ducto-A
    Rt=(A**2+D**2)**(1/2)
    R=((Ancho_de_Paila/2)**2+Altura_de_Paila**2)/(2*Altura_de_Paila)
    pi=math.pi
    Area_Total= pi*Rt**2
    o1=2*math.acos(B/Rt)
    o2=2*math.acos((R-Altura_de_Paila)/R)
    o3=2*math.acos(A/Rt)
    A1=(Rt**2/2)*(o1-math.sin(o1))
    A2=(R**2/2)*(o2-math.sin(o2))
    A3=(Rt**2/2)*(o3-math.sin(o3))
    Area_Flujo1=Area_Total-A1-A2-A3
    s1=Rt*o1
    s2=R*o2
    s3=Rt*o3
    Perimetro_de_Flujo1= pi*2*Rt-(s3+s1)+Ancho_ducto_Fondo+s2
    return [Area_Flujo1, Perimetro_de_Flujo1]

def Area_plana(Ancho_de_paila, Altura_de_fondo, Ancho_Fondo_Ducto, Altura_Ducto):
#Area de Flujo Paila Plana 
#inputs:  Ancho de Paila, altura de fondo paila, altura de ducto, ancho fondo ducto    
    Area_de_flujo2=((Ancho_de_paila+0.1+Ancho_Fondo_Ducto)/2)*Altura_Ducto+2*(0.05*Altura_de_fondo/2)
    Perimetro_de_Flujo2=Ancho_Fondo_Ducto+2*Altura_de_fondo+Ancho_de_paila+2*(0.05**2+Altura_de_fondo**2)**(1/2)+2*(Altura_de_fondo**2+(((Ancho_de_paila+0.1)-Ancho_Fondo_Ducto)/2)**2)**(1/2)
    return [Area_de_flujo2, Perimetro_de_Flujo2]

def Area_pirotubular_1(Ancho_de_paila, Altura_de_fondo, Ancho_Fondo_Ducto, Altura_Ducto, Lado_Tubo, Numero_de_Tubos):
#Area de flujo pirotubular Tubos cilindricos
#inputs:  Ancho de Paila, altura de fondo paila, altura de ducto, ancho fondo ducto, lado tubo, Numero de Tubos
# Nota: es importante que el Lado del Tubo sea menor que la altura del fondo 
    Area_de_Flujo= ((Ancho_de_paila+0.1+Altura_de_fondo)/2)*Altura_Ducto+2*((0.05*Altura_de_fondo)/2)+Numero_de_Tubos*Lado_Tubo**2
    Perimetro_de_Flujo= Ancho_Fondo_Ducto+Ancho_de_paila+2*Altura_de_fondo+2*((0.05**2+Altura_de_fondo**2)**(1/2))+4*Numero_de_Tubos*Lado_Tubo+2*((Altura_Ducto**2+((Ancho_de_paila+0.1-Ancho_Fondo_Ducto)/2)**2)**(1/2))
    return [Area_de_Flujo, Perimetro_de_Flujo]

def Area_pirotubular_2(Ancho_de_paila, Altura_de_fondo, Ancho_Fondo_Ducto, Altura_Ducto, Lado_Tubo1, Lado_Tubo2, Ancho_tubo, Numero_de_Tubos):
#Area de flujo pirotubular Tubos Cuadrados
#inputs:  Ancho de Paila, altura de fondo paila, altura de ducto, ancho fondo ducto, lado tubo 1, lado tubo 2, Ancho tubo Numero de Tubos
# Nota: es importante que el Lado del Tubo sea menor que la altura del fondo 
    Area_de_Flujo = ((Ancho_de_paila+0.1+Ancho_Fondo_Ducto)/2)*Altura_Ducto+2*((0.05*Altura_de_fondo)/2)+Numero_de_Tubos*((Lado_Tubo1+Lado_Tubo2)/2)*Ancho_tubo  
    Perimetro_de_Flujo= Ancho_Fondo_Ducto+Ancho_de_paila+2*Altura_de_fondo+2*(0.05**2+Altura_de_fondo**2)**(1/2)+Numero_de_Tubos*(Lado_Tubo1+Lado_Tubo2+Ancho_tubo+((Ancho_tubo**2+(Lado_Tubo1-Lado_Tubo2)**2)**(1/2)))+2*((Altura_Ducto**2+((Ancho_de_paila+0.1-Ancho_Fondo_Ducto)/2)**2)**(1/2))
    return [Area_de_Flujo, Perimetro_de_Flujo]

#def Area_pirotubular_3():
##Area de flujo pirotubular Tubos Elipticos
##inputs:  Ancho de Paila, altura de fondo paila, altura de ducto, ancho fondo ducto, lado tubo 1, lado tubo 2, Ancho tubo Numero de Tubos
## Nota: es importante que el eje mayor de la elipse sea menor que la altura del fondo 
#    Ancho_de_paila=1
#    Altura_de_fondo=0.3
#    Ancho_Fondo_Ducto=0.6
#    Altura_Ducto=0.5
#    Eje_mayor=0.2
#    Eje_menor=0.15
#    Ancho_tubo=0.1
#    Numero_de_Tubos=3
#    pi=math.pi
#    Area_de_Flujo = ((Ancho_de_paila+0.1+Ancho_Fondo_Ducto)/2)*Altura_Ducto+2*((0.05*Altura_Ducto)/2)+Numero_de_Tubos*pi*Eje_mayor*Eje_menor
#    Perimetro_de_Flujo = Ancho_Fondo_Ducto+Ancho_de_paila+2*Altura_de_fondo+2*((0.05**2+Altura_de_fondo**2)**(1/2))+Numero_de_Tubos*(pi*3*(Eje_mayor*Eje_menor)-((3*Eje_mayor+Eje_menor)*(Eje_mayor+3*Eje_menor))**(1/2))+2*((Altura_Ducto**2+((Ancho_de_paila+0.1-Ancho_Fondo_Ducto)/2)**2)**(1/2))
#    print(Area_de_Flujo,Perimetro_de_Flujo)

def Area_acanalada(Ancho_de_paila, Altura_de_fondo, Ancho_Fondo_Ducto, Altura_Ducto, Ancho_canal, Altura_canal, Numero_de_Canales):
#Area de flujo Acanalada Canales Cuadrados
#inputs:  Ancho de Paila, altura de fondo paila, altura de ducto, ancho fondo ducto, Ancho canal, Altura canal,Numero de Canales   
    Area_de_Flujo = ((Ancho_de_paila+0.1+Ancho_Fondo_Ducto)/2)*Altura_Ducto+2*((0.05*Altura_de_fondo)/2)+(Ancho_de_paila*Altura_canal-Numero_de_Canales*Ancho_canal*Altura_canal) 
    Perimetro_de_Flujo = Ancho_de_paila+(Numero_de_Canales*2-2)*Altura_canal+Ancho_Fondo_Ducto+2*((0.05**2+Altura_de_fondo**2)**(1/2))+2*((Altura_Ducto**2+((Ancho_de_paila+0.1-Ancho_Fondo_Ducto)/2)**2)**(1/2))
    return [Area_de_Flujo, Perimetro_de_Flujo]

def Area_Trape(Ancho_de_paila, Altura_de_fondo, Ancho_Fondo_Ducto, Altura_Ducto, Ancho_canal1, Ancho_canal2, Altura_canal, Numero_de_Canales):
#Area de flujo Acanalada Canales Trapezoidales
#inputs:  Ancho de Paila, altura de fondo paila, altura de ducto, ancho fondo ducto, Ancho canal, Altura canal,Numero de Canales
    Area_de_Flujo = ((Ancho_de_paila+0.1+Ancho_Fondo_Ducto)/2)*Altura_Ducto+2*((0.05*Altura_de_fondo)/2)+(Ancho_de_paila*Altura_canal-Numero_de_Canales*(Altura_canal*(Ancho_canal1+Ancho_canal2)/2))
    Perimetro_de_Flujo=Ancho_Fondo_Ducto+2*((0.05**2+Altura_de_fondo**2)**(1/2))+2*((Altura_Ducto**2+((Ancho_de_paila+0.1-Ancho_Fondo_Ducto)/2)**2)**(1/2))+Numero_de_Canales*(2*(Altura_canal**2+((Ancho_canal1 - Ancho_canal2)/2)**2)**(1/2))+(Ancho_de_paila-Numero_de_Canales*Ancho_canal1)                                                                                                                                                                  
    return [Area_de_Flujo, Perimetro_de_Flujo]

def Areas_lisas(Listado_general):
    Dim_Pailas=Listado_general[0]
    Dim_Chimenea=[]
    Dim_camara=[]
    Dim_ductos=[]
    Fila=[]
    Areas_F=[]
    Per_F=[]
    #Convertir medidas en metros
    for i in Listado_general[1]:
        try:
            Dim_Chimenea.append(round(i/1000,3))
        except:
            Dim_Chimenea.append(i)
            
    for i in Listado_general[2]:
        try:
            Dim_camara.append(round(i/1000,3))
        except:
            Dim_camara.append(i)

    for i in Listado_general[3]:
        for j in i:
            try:
                Fila.append(round(j/1000,3))
            except:
                Fila.append(j)
        Dim_ductos.append(Fila)
        Fila=[]
    #Falta ecuaciones de pailas con aletas y planos
    #Estimar areas
    for ind,i in enumerate(Dim_Pailas):
        if i[0]==1:
            #Plana
            A=Area_plana(i[3], i[2], Dim_ductos[ind][8], Dim_ductos[ind][2])
            Areas_F.append(A[0])
            Per_F.append(A[1])
        elif i[0]==2: 
            #Pirotubular
            A=Area_pirotubular_1(i[3], i[2], Dim_ductos[ind][8], Dim_ductos[ind][2], i[11], i[10])
            Areas_F.append(A[0])
            Per_F.append(A[1])
        elif i[0]==3:
            #Semiesferica
            A=Area_Semiesferica(i[3], i[2], Dim_ductos[ind][0], Dim_ductos[ind][5])
            Areas_F.append(A[0])
            Per_F.append(A[1])
        elif i[0]==4:
            #Semicilindrica
            A=Area_semicilindrica(i[3], i[2], Dim_ductos[ind][2], Dim_ductos[ind][8])
            Areas_F.append(A[0])
            Per_F.append(A[1])
        elif i[0]==5:
            #Pirotubular cuadrada
            A=Area_pirotubular_2(i[3], i[2], Dim_ductos[ind][3], Dim_ductos[ind][2], i[12], i[12], 0.1, i[10])
            Areas_F.append(A[0])
            Per_F.append(A[1])
        elif i[0]==6:
            #Acanalada
            if(i[15]==True):
                A=Area_Trape(i[3], i[5], Dim_ductos[ind][8], Dim_ductos[ind][2], i[12], i[13], i[7], i[14])
                Areas_F.append(A[0])
                Per_F.append(A[1])
            else:
                A=Area_acanalada(i[3], i[2],  Dim_ductos[ind][8], Dim_ductos[ind][2], i[13], i[13], i[14])
                Areas_F.append(A[0])
                Per_F.append(A[1])                
    return Areas_F, Per_F, Listado_general[4]