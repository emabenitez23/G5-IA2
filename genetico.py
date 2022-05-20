from temple_simulado import*
import itertools
from pylab import plt
import numpy as np

def algoritmo_genetico(genetica_inicial, dicc):

    print("\nIngrese la cantidad de individuos por poblacion")
    num_poblacion=int(input())
    poblacion=[]
    fitness=[]
    mejor_individuo=[]
    historico_mejor_fitnes=[]
    lista_costos=dict.values(dicc)
    cont=1
    print("\nIngrese la cantidad de órdenes a analizar (max 100)")
    cant_ordenes=int(input())
    t_total=0
    print("\nIngrese la cantidad de generaciones que desea generar")
    max_iteracion=int(input())

    #ESTADO INICIAL USANDO SHUFFLE

    individuo_inicial=genetica_inicial
    poblacion.append(list(individuo_inicial))
   
    while cont!=num_poblacion:
        individuo_aux=sample(list(individuo_inicial[0:-1]), len(list(individuo_inicial))-1)+individuo_inicial[-1:]
        if individuo_aux not in poblacion:
            poblacion.append(list(individuo_aux))
            cont+=1

    start=time.time()

    for i in range(len(poblacion)):

        costos_ind=[]  ##graficas   
        suma=0
        lista_combinada=list(itertools.combinations(poblacion[i], 2))
        diccionario_aux=dict(zip(lista_combinada, lista_costos))

        for j in range(cant_ordenes):
            pedido=list(leer_archivo(str(j)))
            pedido.insert(0,len(individuo_inicial))
            pedido.append(len(individuo_inicial))
            costo=temple_simulado(pedido, diccionario_aux,1)
            suma+=costo
        fitness.append(int(suma/cant_ordenes))
    costos_ind+=fitness
    end=time.time()
    t_total=end-start
    print("Fitness promedio de la población 0 :", round(sum(fitness)/len(fitness),2),"  Tiempo:",str(round((end-start), 2)),"seg")
    #print(fitness)
  
    iteracion=0
    mejor_fitness=10000000000
    historico_mejor_fitnes.append(min(fitness))
    while True:
        
        start=time.time()
        iteracion+=1
        indice1=fitness.index(min(fitness))
        padre1=list(poblacion[indice1])
        fitness_padre1=fitness[indice1]
        fitness[indice1]=100000
        indice2=fitness.index(min(fitness))
        padre2=list(poblacion[indice2])

        while padre1==padre2:
            fitness[indice2]=100000
            indice2=fitness.index(min(fitness))
            padre2=list(poblacion[indice2])

        poblacion=[]
        for i in range(int(num_poblacion/2)):
            padre1=padre1[-7:-1]+padre1[0:-7]+padre1[-1:]
            padre2=padre2[-7:-1]+padre2[0:-7]+padre2[-1:]
            poblacion.append(list(padre1))
            poblacion.append(list(padre2))

        fitness=[]
        for i in range(len(poblacion)):
            lista_combinada=list(itertools.combinations(poblacion[i], 2))
            diccionario_aux=dict(zip(lista_combinada, lista_costos))
            suma=0
            for j in range(cant_ordenes):
                pedido=list(leer_archivo(str(j)))
                pedido.insert(0,len(individuo_inicial))
                pedido.append(len(individuo_inicial))
                costo=temple_simulado(pedido, diccionario_aux,1)
                suma+=costo
            fitness.append(int(suma/cant_ordenes))
        costos_ind+=fitness

        end=time.time()
        t_total+=end-start
        print("Fitness promedio de la población",iteracion,":", round(sum(fitness)/len(fitness),2),"  Tiempo:",str(round((end-start), 2)),"seg")
        #print(poblacion)
        #print("\n",fitness)

        ##SELECCIONA AL MEJOR CANDIDATO HISTORICO

        fitnes_hijo1=min(fitness)
        #print(fitnes_hijo1)
        #print(fitness_padre1)

        if mejor_fitness<fitnes_hijo1:
            #print("if",mejor_fitness)
            pass
        else:
            mejor_individuo=poblacion[fitness.index(min(fitness))]
            mejor_fitness=fitnes_hijo1
            #print("else",mejor_fitness)

        if iteracion==max_iteracion:
            solucion=mejor_individuo
            break

        historico_mejor_fitnes.append(mejor_fitness)
    
    solucion.pop()
    print("\n----------------------------------------------------------------------------")
    print("\nLA DISTRIBUCION MAS OPTIMA ENCONTRADA, DE LOS PRODUCTOS EN EL ALMACEN ES: \n")
    print(solucion)
    print("\nCON UN VALOR DE FITNESS DE:",mejor_fitness)
    print("EL ALGORITMO DEMORO EN TOTAL:",str(round(t_total,2)),"seg")
    print("EL MEJOR INDIVIDUO SE HA REPRESENTADO EN EL MAPA")
    print("\n----------------------------------------------------------------------------")

    ##GRAFICAS
    #print(len(costos_ind))
    #print(costos_ind)
    plt.figure(1)
    linea_media=np.mean(costos_ind)
    plt.axhline(linea_media, color='r', linestyle='dashed')
    plt.xticks(np.arange(0, len(costos_ind), step=1),rotation=90)
    plt.plot(costos_ind,'o-',label="Historico fitness")
    plt.legend(loc="upper left")
    plt.title("Historico de Fitness de cada individuo generado")
    plt.xlabel("Numero de individuo")
    plt.ylabel("Valor de fitnes")
    plt.grid(True)
    plt.figure(2)
    linea_media=np.mean(historico_mejor_fitnes)
    plt.axhline(linea_media, color='r', linestyle='dashed')
    plt.xticks(np.arange(0, len(historico_mejor_fitnes), step=1))
    plt.plot(historico_mejor_fitnes,'o-',label="Historico mejor fitness")
    plt.legend(loc="upper left")
    plt.title("Evolucion del algoritmo genetico hacia el individuo optimo")
    plt.xlabel("Numero de generacion")
    plt.ylabel("Valor de fitnes")
    plt.grid(True)
    plt.show()
    plt.ion()

    return(solucion)