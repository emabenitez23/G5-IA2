from io import open
import re
from a_estrella import *
from math import *
from random import *
import time
from pylab import plt
import numpy as np


def leer_archivo(n_orden):
    nombre_archivo="orders.txt"
    archivo = open(nombre_archivo, "r")
    lineas=archivo.readlines()
    archivo.close()

    orden = ("Order " + str (n_orden) + "\n")
    pedido = []

    if orden in lineas:
        
        pos = lineas.index (orden)+1

        while lineas[pos] != "\n":
            lineas[pos]= int (re.sub("P|\n","",lineas[pos])) #filtramos las P y los \n de cada linea y convertimos el valor en entero
            pedido.append(lineas[pos]) #se crea una lista con los nombres de cada producto acorde al pedido
            pos+=1
    
    #plt.figure(1)
    plt.title("Historico de Fitness por iteracion de la orden: "+str(n_orden))
    
    return pedido

def analizar_pedido(pedido, f_dicc):
    costo_piking=0
    lista=f_dicc.keys()

    for i in range(len(pedido)-1):
        tupla1=(pedido[i],pedido[i+1])
        tupla2=(pedido[i+1],pedido[i])
        
        if tupla1 in lista:
            costo_piking+=int(f_dicc[tupla1])
        else:
            costo_piking+=int(f_dicc[tupla2])

    return costo_piking

def combinatoria(f_nodo):

    lista1=list(f_nodo)
    indice1=randint(1, len(lista1)-2)
    indice2=randint(1, len(lista1)-2)
    while indice2==indice1:
        indice2=randint(1, len(lista1)-2)
    aux=lista1[indice1]
    lista1[indice1]=lista1[indice2]
    lista1[indice2]=aux

    return lista1

def temple_simulado(f_pedido, f_dicc, opcion=0):
    
    T=10.0
    Tf=0.20
    iter=1
    max_iter=50000
    
    start=time.time()

    nodo_actual=list(f_pedido)
    costo_actual=analizar_pedido(nodo_actual, f_dicc)


    lista_pedidos=[]
    lista_costos=[]
    lista_costo_grafica=[]


    while T>Tf:
        nodo_candidato=combinatoria(nodo_actual)
        costo_candidato=analizar_pedido(nodo_candidato, f_dicc)
        delta_energia=costo_actual-costo_candidato
        if delta_energia>0 or round(uniform(0,1), 2)<round(exp(delta_energia/T), 2):
            costo_actual, nodo_actual=costo_candidato, nodo_candidato
        
        lista_costo_grafica.append(costo_actual)
        T=1/log10(iter+1)
        iter+=1
        lista_pedidos.append(list(nodo_actual))
        lista_costos.append(costo_actual)
        
        if iter>max_iter:
            break
  
    if opcion==0:
        plt.plot(lista_costo_grafica,label="T"+str(iter))
        plt.xlabel("Iteraciones")
        plt.ylabel("Fitness")
        plt.legend(loc="upper left")
        plt.grid(True)  

    costo_solucion=min(lista_costos)
    aux=lista_costos.index(costo_solucion)
    nodo_solucion=list(lista_pedidos[aux])

    end=time.time()
    
    if opcion==0:
        print("El tiempo de calculo fue:", str(round(end-start, 2)), "segundos\n")
        print("EL PICKING MAS EFICIENTE PARA LA ORDEN, ES:\n")
        print(nodo_solucion)
        print("\nCON UN COSTO MINIMO DE:", costo_solucion)
    else:
        return costo_solucion
    
    plt.show()
    plt.ion()