from pickle import NONE
import numpy as np
import matplotlib.pyplot as plt
import openpyxl as px
import os

""" En este código se desarrollan las siguientes consignas del TP3:
    2.a) Medir la precisión de clasificacion (Accuracy).
    2.b) Generacion de un nuevo conjunto de Test.
    3)   Criterio de parada temprana con conjunto de validacion nuevo.
    4)   Alternativa de función generadora de datos (generar_datos_complejos) y evaluación de su rendimiento con distintos parámetros del algoritmo.
    5.a) Problema de regresión, modificando la funcion de perdida y utilizando MSE.
    5.b) Generacion de un nuevo conjunto de datos, a partir de un archivo excel.
    6)   Analisis del barrido de parametros, a partir de una funcion de activacion ReLU y Sigmoide. """

# Generador basado en ejemplo del curso CS231 de Stanford: 
# CS231n Convolutional Neural Networks for Visual Recognition
# (https://cs231n.github.io/neural-networks-case-study/)

def generar_datos_regresion(inicio_lectura, final_lectura):

    """ Para generar los datos de regresion se utilizo una base de datos de: 
    UrbanGB, coordenadas de accidentes de tráfico urbano vs cantidad de accidentes, etiquetados por el centro urbano
    https://archive.ics.uci.edu/ml/datasets/UrbanGB%2C+urban+road+accidents+coordinates+labelled+by+the+urban+center """

    arc = px.load_workbook('DataSet-Accid-Trafic.xlsx')
    data=arc["Hoja1"]
    dim=int(final_lectura-inicio_lectura)
    var=np.zeros((dim, 3))
    i=0
    ini=inicio_lectura
    fin=final_lectura
    for row in data.rows:
        j=0
        for cell in row:
            if ini < fin:
                var[i][j]=data.cell(row=ini+1,column=j+1).value
            j+=1
        i+=1
        ini+=1
    ### Normalizo y centro todas las variables para que estén en escalas iguales.
    var_cen = var - var.mean(axis=0)
    var_norm = var_cen / var_cen.max(axis=0)
    variables=var_norm[:,0:2]
    pe=var_norm[:,2]        ### La última columna es el resultado de cada medición.
    arc.close()
    return variables,pe

def generar_datos_basicos(cantidad_ejemplos, cantidad_clases, AMPLITUD_ALEATORIEDAD):
    
    FACTOR_ANGULO = 0.79
    
    n = int(cantidad_ejemplos / cantidad_clases)    # Cantidad de puntos por cada clase, misma cantidad para cada una.
    x = np.zeros((cantidad_ejemplos, 2))            # Entradas: 2 columnas (x1 y x2)
    t = np.zeros(cantidad_ejemplos, dtype="uint8")  # 1 columna: la clase correspondiente (t -> "target") Salida deseada

    randomgen = np.random.default_rng()

    for clase in range(cantidad_clases):
        # Tomando la ecuacion parametrica del circulo (x = r * cos(t), y = r * sin(t)), generamos 
        # radios distribuidos uniformemente entre 0 y 1 para la clase actual, y agregamos un poco de
        # aleatoriedad
        radios = np.linspace(0, 1, n) + AMPLITUD_ALEATORIEDAD * randomgen.standard_normal(size=n)

        # ... y angulos distribuidos tambien uniformemente, con un desfasaje por cada clase
        angulos = np.linspace(clase * np.pi * FACTOR_ANGULO, (clase + 1) * np.pi * FACTOR_ANGULO, n)

        # Generamos un rango con los subindices de cada punto de esta clase. Este rango se va
        # desplazando para cada clase: para la primera clase los indices estan en [0, n-1], para
        # la segunda clase estan en [n, (2 * n) - 1], etc.
        indices = range(clase * n, (clase + 1) * n)

        # Generamos las "entradas", los valores de las variables independientes. Las variables:
        # radios, angulos e indices tienen n elementos cada una, por lo que le estamos agregando
        # tambien n elementos a la variable x (que incorpora ambas entradas, x1 y x2)
        x1 = radios * np.sin(angulos)
        x2 = radios * np.cos(angulos)
        x[indices] = np.c_[x1, x2]

        # Guardamos el valor de la clase que le vamos a asociar a las entradas x1 y x2 que acabamos
        # de generar
        t[indices] = clase
    return x, t

def generar_datos_complejos(cantidad_ejemplos, cantidad_clases,AMPLITUD_ALEATORIEDAD): # GENERADOR ALTERNATIVO DE DATOS

    ### FUNCION --> Z = -3X + Y^5    

    n = int(cantidad_ejemplos / cantidad_clases)    # Cantidad de puntos por cada clase, misma cantidad para cada una.
    x = np.zeros((cantidad_ejemplos, 2))            # Entradas: 2 columnas (x1 y x2)
    t = np.zeros(cantidad_ejemplos, dtype="uint8")  # 1 columna: la clase correspondiente (t -> "target") Salida deseada
    yx = np.zeros(cantidad_ejemplos)              
    aux=16

    for i in range(cantidad_ejemplos): 
        if i % n==0:
            aux*=0.5
        yx[i]=aux                                   # Valores para las curvas de nivel
    randomgen = np.random.default_rng()

    for clase in range(cantidad_clases):

        x1 = np.linspace(0, 2, n)                   # Dominio en el intervalo (0, 2) particionado n veces

        # Generamos un rango con los subindices de cada punto de esta clase. Este rango se va
        # desplazando para cada clase: para la primera clase los indices estan en [0, n-1], para
        # la segunda clase estan en [n, (2 * n) - 1], etc.
        indices = range(clase * n, (clase + 1) * n)

        aleat = yx[indices] * AMPLITUD_ALEATORIEDAD * randomgen.standard_normal(size=n)
        x2 = (yx[indices]+3*x1)**0.2 + aleat
        x[indices] = np.c_[x1, x2]
        t[indices] = clase

    return x, t

def inicializar_pesos(n_entrada, n_capa_2, n_capa_3):
    randomgen = np.random.default_rng()

    w1 = 0.1 * randomgen.standard_normal((n_entrada, n_capa_2))
    b1 = 0.1 * randomgen.standard_normal((1, n_capa_2))

    w2 = 0.1 * randomgen.standard_normal((n_capa_2, n_capa_3))
    b2 = 0.1 * randomgen.standard_normal((1,n_capa_3))

    return {"w1": w1, "b1": b1, "w2": w2, "b2": b2}

def ejecutar_adelante(x, pesos):  #Sigmoide o ReLU

    # Funcion de entrada ("regla de propagacion") para la capa oculta
    z = x.dot(pesos["w1"]) + pesos["b1"]

    """Funcion de activacion ReLU para la capa oculta"""
    h = np.maximum(0, z)

    """Funcion de activacion Sigmoide"""
    #h = 1/(1+np.exp(-z)) #Sigmoide

    # Salida de la red (funcion de activacion lineal). Esto incluye la salida de todas
    # las neuronas y para todos los ejemplos proporcionados
    y = h.dot(pesos["w2"]) + pesos["b2"]

    return {"z": z, "h": h, "y": y}

def clasificar(x, pesos):
    # Corremos la red "hacia adelante"
    resultados_feed_forward = ejecutar_adelante(x, pesos)
    
    # Buscamos la(s) clase(s) con scores mas altos (en caso de que haya mas de una con 
    # el mismo score estas podrian ser varias). Dado que se puede ejecutar en batch (x 
    # podria contener varios ejemplos), buscamos los maximos a lo largo del axis=1 
    # (es decir, por filas)
    max_scores = np.argmax(resultados_feed_forward["y"], axis=1)

    # Tomamos el primero de los maximos (podria usarse otro criterio, como ser eleccion aleatoria)
    # Nuevamente, dado que max_scores puede contener varios renglones (uno por cada ejemplo),
    # retornamos la primera columna
    return max_scores[:]

def train(x, t, pesos, learning_rate, epochs,nv,xv,tv):
    # Cantidad de filas (i.e. cantidad de ejemplos)
    m = np.size(x, 0) 
    val=0
    for i in range(epochs+1):
        # Ejecucion de la red hacia adelante
        resultados_feed_forward = ejecutar_adelante(x, pesos)
        y = resultados_feed_forward["y"]
        h = resultados_feed_forward["h"]
        z = resultados_feed_forward["z"]

        # LOSS
        # a. Exponencial de todos los scores
        exp_scores = np.exp(y)

        # b. Suma de todos los exponenciales de los scores, fila por fila (ejemplo por ejemplo).
        #    Mantenemos las dimensiones (indicamos a NumPy que mantenga la segunda dimension del
        #    arreglo, aunque sea una sola columna, para permitir el broadcast correcto en operaciones
        #    subsiguientes)
        sum_exp_scores = np.sum(exp_scores, axis=1, keepdims=True)

        # c. "Probabilidades": normalizacion de las exponenciales del score de cada clase (dividiendo por 
        #    la suma de exponenciales de todos los scores), fila por fila
        p = exp_scores / sum_exp_scores

        # d. Calculo de la funcion de perdida global. Solo se usa la probabilidad de la clase correcta, 
        #    que tomamos del array t ("target")
        loss = (1 / m) * np.sum( -np.log( p[range(m), t] ))

        # Mostramos solo cada 1000 epochs
        if i %nv == 0:
            print("Training LOSS epoch", str(i).rjust(4, '0'), ": {:.6f}".format(loss),end="  <->  ")

        # Extraemos los pesos a variables locales
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation
        dL_dy = p                # Para todas las salidas, L' = p (la probabilidad)...
        dL_dy[range(m), t] -= 1  # ... excepto para la clase correcta
        dL_dy /= m

        dL_dw2 = h.T.dot(dL_dy)                         # Ajuste para w2
        dL_db2 = np.sum(dL_dy, axis=0, keepdims=True)   # Ajuste para b2

        dL_dh = dL_dy.dot(w2.T)
        
        dL_dz = dL_dh       # El calculo dL/dz = dL/dh * dh/dz. La funcion "h" es la funcion de activacion de la capa oculta,
        dL_dz[z <= 0] = 0   # para la que usamos ReLU. La derivada de la funcion ReLU: 1(z > 0) (0 en otro caso)

        dL_dw1 = x.T.dot(dL_dz)                         # Ajuste para w1
        dL_db1 = np.sum(dL_dz, axis=0, keepdims=True)   # Ajuste para b1

        # Aplicamos el ajuste a los pesos
        w1 += -learning_rate * dL_dw1
        b1 += -learning_rate * dL_db1
        w2 += -learning_rate * dL_dw2
        b2 += -learning_rate * dL_db2

        # Actualizamos la estructura de pesos
        # Extraemos los pesos a variables locales
        pesos["w1"] = w1
        pesos["b1"] = b1
        pesos["w2"] = w2
        pesos["b2"] = b2

    #### CAMBIAR LA PRECISION CON RESPECTO A LA MISMA CURVA DE VALIDACION 

        ### Validación
        if i %nv ==0:
            valN=validar(xv,tv,pesos)
            print("Precisión en epoch",str(i).rjust(4, '0'),": {0:.2f}".format(valN*100),"%")
            if valN >= val:     
                val=valN
            elif valN < (val * 0.85):                # Tolerancia del 15% en oscilación
                if valN < (val * 0.7):               # Corta por Overfitting mayor al 30%
                    print("ALERTA parada temprana en epoch", str(i).rjust(4, '0'),"por overfitting con oscilación mayor al 30%")
                    break
                else:
                    print("Posible overfitting, presenta oscilación mayor al 15%")

def train_regresion (x, t, pesos, learning_rate, epochs, nv, xv, tv):
    # x (nxm): n ejemplos para m entradas.
    # t (mx1): salida correcta (target) para n ejemplos
    # pesos: pesos (W y b)
    # Cantidad de filas (i.e. cantidad de ejemplos)
    n = len(x)
    LW=[]           ### Vectores para graficar Loss de Train y Valid
    ix=[]
    LWv=[]
    ixv=[]
    val=10000       ### Valor indistinto
    k=-1
    for i in range(epochs+1):
        # Ejecucion de la red hacia adelante
        res_ffw = ejecutar_adelante(x, pesos)
        y = res_ffw["y"]
        h = res_ffw["h"]
        z = res_ffw["z"]

        # LOSS TRAIN
        lw=np.zeros((n,1))
        aux=0
        for j in range(n):
            lw[j]=(t[j]-y[j])
            aux+=(lw[j]**2)
        aux/=n

        LW.append(aux) # Calculo de la funcion de perdida global con MSE.
        ix.append(i)

        # Extraemos los pesos a variables locales
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation
        ### Corregidas derivadas al utilizar MSE y la función Sigmoide o ReLU como 
        ### activación de la capa oculta.
        dL_dy = (-2/n)*lw
        dL_dw2 = h.T.dot(dL_dy)                         # Ajuste para w2
        dL_db2 = np.sum(dL_dy, axis=0, keepdims=True)   # Ajuste para b2
        dL_dh = dL_dy.dot(w2.T)      

        dL_dz = dL_dh                   ### Para usar ReLU
        dL_dz[z <= 0] = 0               ### ReLU
        # dh_dz = h.T.dot(1-h)          ### SIGMOIDE. El calculo dL/dz = dL/dh * sigma(x)*(1-sigma(x))
        # dL_dz = dL_dh.dot(dh_dz)      ### Sigmoide

        dL_dw1 = x.T.dot(dL_dz)                         # Ajuste para w1
        dL_db1 = np.sum(dL_dz, axis=0, keepdims=True)   # Ajuste para b1

        # Aplicamos el ajuste a los pesos (Gradiente Descendiente)
        w1 += -learning_rate * dL_dw1
        b1 += -learning_rate * dL_db1
        w2 += -learning_rate * dL_dw2
        b2 += -learning_rate * dL_db2

        # Actualizamos la estructura de pesos
        pesos["w1"] = w1
        pesos["b1"] = b1
        pesos["w2"] = w2
        pesos["b2"] = b2

        # Mostramos y validamos solo cada "nv" epochs
        if i %nv == 0:
            loss=float(LW[i])
            print("Training LOSS epoch", str(i).rjust(4, '0'), ": {:.6f}".format(loss),end="  <->  ")
            #print("Training LOSS epoch", str(i).rjust(4, '0'), ": {:.6f}".format(aux),end="  <->  ")
            LWvv=[]
            #LOSS VALIDATION
            aux1,aux2=(MSE(xv,tv,pesos))   ### Función "MSE" pero con datos de validación
            LWv.append(aux1)
            LWvv+=aux2
            ixv.append(i)
            nval=float(aux1)
            print("Precisión en epoch", str(i).rjust(4, '0'),": {0:.2f}".format(nval*100),"%")
            er_abs=(np.abs(LW[i]-LWv[k]))/LW[i]
            if LWv[k] <= val:          ### Actualiza el valor de "Loss" actual
                val=LWv[k]
            elif LWv[k] > (val*1.15):   ### Tolerancia del 15% por oscilación
                if LWv[k] > (val*1.5):   ### Corto por Overfitting
                    print("\t ERROR - Parada Temprana en epoch", i," por Overfitting (oscilación mayor al 50%).\n")
                    break
                else:
                    ### Advertencia de Overfitting
                    print("\t AVISO - Posible Overfitting (oscilación mayor al 15%).")
            
            if i>0:                     ### No reviso CORRELATION en la primer EPOCH
                if  (er_abs> 0.2):      ### Diferencia del 20% entre Train. y Valid.
                    if er_abs > 0.6:    ### Diferencia del 60% - Corta por Correlation
                        print("\t ERROR - Parada Temprana en epoch", i," por no Correlación\n")
                        break
                    else:
                        ### Advertencia de Correlación
                        print("\t AVISO - Posible error de Correlación (mayor al 20%).")
            print("\n")

    plt.figure()
    plt.title("Funcion de perdida - LOSS")
    plt.plot(ix,LW,label="Entrenamiento")
    plt.plot(ixv,LWv,label="Validación")
    plt.legend(loc="upper right")
    plt.show()

def MSE(xt,tt,pesos):  #Devuelve el error cuadratico medio MSE
    n=len(xt)
    valid_ffw = ejecutar_adelante(xt, pesos)
    yt = valid_ffw["y"]
    lwt=np.zeros((n,1))
    LWt=0
    LWtt=[]
    for j in range(n):
        lwt[j]=(tt[j]-yt[j])
        LWt+=(lwt[j]**2)
        LWtt.append(LWt/n)
    LWt/=n
    return LWt,LWtt

def iniciar(numero_clases, numero_ejemplos, funcion, LEARNING_RATE, EPOCHS, N_valid):
   
    aleatoriedad=0.03                      # Amplitud de aleatoriedad para datos

    if funcion == 0:
        x, t = generar_datos_basicos(int(numero_ejemplos*0.6), numero_clases, aleatoriedad) # 60% de los datos para entrenar
        xt,tt= generar_datos_basicos(int(numero_ejemplos*0.3), numero_clases, aleatoriedad) # 30% de los datos para testear
        xv,tv= generar_datos_basicos(int(numero_ejemplos*0.1), numero_clases, aleatoriedad) # 10% de los datos para validar

        opcion=0
        opcion=input("Si desea ver las graficas escriba (1) de lo contrario presione 'ENTER': ")
        if opcion=='1':
            plt.figure(1)
            plt.scatter(x[:, 0], x[:, 1], c=t)          # El parametro 'c' es un parametro de color
            plt.title("Conjunto de Entrenamiento")
            plt.figure(2)
            plt.scatter(xt[:, 0], xt[:, 1], c=tt)       # El parametro 'c' es un parametro de color
            plt.title("Conjunto de Test")
            plt.figure(3)
            plt.scatter(xv[:, 0], xv[:, 1], c=tv)       # El parametro 'c' es un parametro de color
            plt.title("Conjunto de Validacion")
            plt.show()
    
    elif funcion == 1:
        x, t = generar_datos_complejos(int(numero_ejemplos*0.6), numero_clases, aleatoriedad) # 60% de los datos para entrenar
        xt,tt= generar_datos_complejos(int(numero_ejemplos*0.3), numero_clases, aleatoriedad) # 30% de los datos para testear
        xv,tv= generar_datos_complejos(int(numero_ejemplos*0.1), numero_clases, aleatoriedad) # 10% de los datos para validar
        opcion=0
        opcion=input("Si desea ver las graficas escriba (1) de lo contrario presione 'ENTER': ")
        if opcion=='1':
            fig=plt.figure()
            ax1=fig.add_subplot(111,projection='3d')
            ax1.scatter(x[:,0],x[:,1],t,c=t,marker='o')
            plt.title("Conjunto de Entrenamiento")
            plt.show()
    
    elif funcion == 2:
        PORC_DATA_TRAIN=80
        datos_entrenar=int(PORC_DATA_TRAIN*95)
        datos_validar=int(datos_entrenar + (100-PORC_DATA_TRAIN)*0.5*95)
        datos_ejemplo=15501                                                 #Cantidad de datos a extraer del archivo (max 20000)
        print("...Extrayendo datos del archivo...")
        x ,t = generar_datos_regresion(1,datos_entrenar)  
        xv,tv= generar_datos_regresion(datos_entrenar,datos_validar)  
        xt,tt= generar_datos_regresion(datos_validar,datos_ejemplo)
        print("...Datos extraidos correctamente...")

        opcion=0
        opcion=input("Si desea ver las graficas escriba (1) de lo contrario presione 'ENTER': ")
        if opcion=='1':
            fig=plt.figure()
            ax1=fig.add_subplot(111,projection='3d')
            ax1.scatter(x[:,0],x[:,1],t,marker='o')
            plt.title("Conjunto de Entrenamiento")
            plt.show()


    NEURONAS_CAPA_OCULTA = int(input("Neuronas en capa oculta = "))  #Sugerido 100
    NEURONAS_ENTRADA = 2
    print("Neuronas de entrada =",NEURONAS_ENTRADA) 
    print("\n-------------------------------------------------\n")

    # Inicializa pesos de la red
    pesos = inicializar_pesos(n_entrada=NEURONAS_ENTRADA, n_capa_2=NEURONAS_CAPA_OCULTA, n_capa_3=numero_clases)

    # Entrenamiento de la red
    if funcion == 0 or funcion == 1:
        train(x, t, pesos, LEARNING_RATE, EPOCHS, N_valid, xv, tv)
    elif funcion == 2:
        train_regresion(x, t, pesos, LEARNING_RATE, EPOCHS, N_valid, xv, tv)

    # Datos de precision de Test y Validacion
    prec_test=100 * validar(xt,tt,pesos)
    print("\nPrecisión del MSE:         {0:.2f}".format(prec_test),"%")

    prec_valida=100 * validar(xv,tv,pesos)
    print("Precisión de la validacion: {0:.2f}".format(prec_valida),"%\n")

def validar(x,t,pesos):     # Función de validación que retorna el valor de la precisión.

    val=clasificar(x, pesos)                    # Clasifica un grupo nuevo (xx) y lo compara (restando) con los valores reales (tt).
    dif=np.array(len(t))
    dif=t-val
    acc=np.count_nonzero(dif==0) / len(dif)     # Cuenta los 0 y calcula el porcentaje de precisión.
    
    return acc


## -------------- PROGRAMA -------------- ##

os.system ('cls')
print("\n--------------------- DATOS ---------------------\n")
metodo=input("Metodo de clasificacion (1) - Regresion (2) --> ")
LEARNING_RATE=float(input("Learning Rate = "))                      #Sugerido 0.3
EPOCHS=int(input("Epochs = "))                                      #Sugerido 10000
if metodo=='1':
    numero_ejemplos=int(input("Cantidad de ejemplos = "))           #Sugerido 1000
    numero_clases=int(input("Clases = "))                           #Sugerido 4
else:
    numero_clases=1
    numero_ejemplos=None

N_valid=int(EPOCHS/10)                                              #Cantidad de epochs para validar
print("Se validaran los datos cada |",N_valid,"| epochs")

aux=int(input("Generar datos por defecto (0) - Generar datos complejos (1) - Generar datos para regresion (2): "))  # Generador de datos basicos o complejos
if aux==0: 
    funcion=aux
elif aux==1: 
    funcion=aux
elif aux==2:
    funcion=aux

iniciar(numero_clases, numero_ejemplos, funcion, LEARNING_RATE, EPOCHS, N_valid)