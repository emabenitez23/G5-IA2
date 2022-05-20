import pygame
import time
from a_estrella import *
from temple_simulado import *
from genetico import*

# PALETA DE COLORES
blanco = (255,255,255)
negro = (0,0,0)
morado = (128,0,128)
naranja = (255,165,0)
gris = (128,128,128)
turquesa = (64,224,208)
verde=(0,255,0)

class Punto:    # CLASE PUNTO
    def __init__(self, fila, columna, f_tamanio_celdax, f_tamanio_celday, f_filas, f_columnas):
        self.fila = fila
        self.columna = columna
        self.f_tamanio_celdax = f_tamanio_celdax
        self.f_tamanio_celday = f_tamanio_celday
        self.f_filas = f_filas
        self.f_columnas = f_columnas
        self.producto = 0
        self.costo = 0
        self.x = columna * f_tamanio_celdax
        self.y = fila * f_tamanio_celday
        self.color = blanco
        self.vecinos = []

    def get_fil_col (self):
        return self.fila, self.columna

    def set_producto (self, f_producto):
        self.producto = f_producto

    def set_costo (self, f_costo):
        self.costo = f_costo

    def get_costo(self):
        return self.costo

    def get_producto(self):
        return self.producto
    
    def dibujar_celda (self, f_ventana):
        pygame.draw.rect(f_ventana, self.color, (self.x, self.y, self.f_tamanio_celdax, self.f_tamanio_celday ))
    
    def marcar_inicio (self):
        self.color = turquesa

    def marcar_final (self):
        self.color = naranja

    def es_estante (self):
        self.color = gris

    def ruta (self):
        self.color = morado

    def actualizar_vecinos (self, f_puntos):
        self.vecinos=[]
        if self.fila < self.f_filas-1 and f_puntos[self.fila+1][self.columna].color != gris:
            self.vecinos.append(f_puntos[self.fila+1][self.columna])
        if self.fila > 0 and f_puntos[self.fila-1][self.columna].color != gris:
            self.vecinos.append(f_puntos[self.fila-1][self.columna])
        if self.columna < self.f_columnas-1 and f_puntos[self.fila][self.columna+1].color != gris:
            self.vecinos.append(f_puntos[self.fila][self.columna+1])
        if self.columna > 0 and f_puntos[self.fila][self.columna-1].color != gris:
            self.vecinos.append(f_puntos[self.fila][self.columna-1])

    def __lt__(self, otro):
        return False

def crear_puntos (f_tamanio, f_matriz): # CREA LA MATRIZ DE PUNTOS
    lista_puntos = []
    tamanio_celdax = f_tamanio[0]//f_matriz[1]
    tamanio_celday = f_tamanio[1]//f_matriz[0]
    for i in range (f_matriz[0]):
        lista_puntos.append([])
        for j in range (f_matriz[1]):
            punto=Punto(i, j, tamanio_celdax, tamanio_celday, f_matriz[0], f_matriz[1])
            lista_puntos[i].append(punto)
    return lista_puntos

def dibujar_grilla(f_ventana, f_tamanio, f_matriz, f_estante, f_estanterias, f_puntos, f_nueva_distribucion): # DIBUJA LA DISTRIBUCION DEL ALMACEN
    tamanio_celdax = f_tamanio[0]//f_matriz[1]
    tamanio_celday = f_tamanio[1]//f_matriz[0]
    contador=0
    contador_aux=0

    if f_nueva_distribucion==[]:
        contador_produ = list(range(1,(f_estante[0]*f_estante[1]*f_estanterias)+1,1))
        color=gris
    else:
        contador_produ=list(f_nueva_distribucion)
        color=verde
    #DIBUJAR ESTANTERIAS
    for i in range (1, f_matriz[1], f_estante[1]+1):
        for j in range (1, f_matriz[0], f_estante[0]+1):
            contador+=1
            if f_estanterias>=contador:
                for k in range (1,f_estante[1]+1):
                    for l in range (1,f_estante[0]+1):
                        pygame.draw.rect(f_ventana, color, ((i-1)*tamanio_celdax+k*tamanio_celdax, (j-1)*tamanio_celday+l*tamanio_celday, tamanio_celdax, tamanio_celday))
                        pygame.font.init()
                        fuente = pygame.font.Font(None, min(tamanio_celdax,tamanio_celday)//2)
                        texto = fuente.render("P{}".format(contador_produ[contador_aux]), True, negro)
                        f_ventana.blit(texto, [(i-1)*tamanio_celdax+k*tamanio_celdax+tamanio_celdax//6, (j-1)*tamanio_celday+l*tamanio_celday+tamanio_celday//3])
                        f_puntos[j-1+l][i-1+k].set_producto(contador_produ[contador_aux])
                        f_puntos[j-1+l][i-1+k].es_estante()
                        contador_aux+=1
              
    #DIBUJAR GRILLA
    for i in range (f_matriz[1]+1):
        pygame.draw.line(f_ventana, negro, (i*tamanio_celdax, 0), (i*tamanio_celdax, f_matriz[0]*tamanio_celday))
        for j in range (f_matriz[0]+1):
            pygame.draw.line(f_ventana, negro, (0, j*tamanio_celday), (f_matriz[1]*tamanio_celdax, j*tamanio_celday))

def obtener_posicion (f_posicion, f_matriz, f_tamanio): # DEVUELVE LAS COORDENADAS DEL PUNTO QUE SE CLIKEA POR PANTALLA
    tamanio_celdax = f_tamanio[0]//f_matriz[1]
    tamanio_celday = f_tamanio[1]//f_matriz[0]           
    y, x = f_posicion
    fila = x//tamanio_celday
    columna = y//tamanio_celdax
    return fila, columna

def calcular_costo(f_camino, f_pi, f_pf):
    costo=0
    while True:
        if f_pf in f_camino:
            f_pf=f_camino[f_pf]
            costo+=1
        elif f_pf==f_pi:
            return costo

def costo_individuo(f_puntos, f_estanterias, f_productos, f_sentido):
    start=time.time()
    cant_prod_total=f_estanterias*f_productos+2
    lista_combinada=list(itertools.combinations(range(1,cant_prod_total,1), 2))
    lista2=[]
    var_costo=0
    lista1=list(itertools.combinations(range(1,cant_prod_total,1), 2))       

    for i in range(len(lista_combinada)):
        lista_combinada[i]=list(lista_combinada[i])
    
    it=0
    for i in lista_combinada:
        aux1=i[0]
        aux2=i[1]
        for lista in f_puntos:
            for punto in lista:
                if aux1==punto.get_producto():
                    aux1=punto
                    aux1.actualizar_vecinos(f_puntos)
                    if aux1.color==naranja:
                        pass
                    elif len(aux1.vecinos) == 2 and f_sentido=="h":
                        if aux1.columna==aux1.vecinos[0].columna:
                            aux1=aux1.vecinos[0]
                        else:
                            aux1=aux1.vecinos[1]
                    elif len(aux1.vecinos)==2 and f_sentido=="v":
                        if aux1.fila==aux1.vecinos[0].fila:
                            aux1=aux1.vecinos[0]
                        else:
                            aux1=aux1.vecinos[1]
                    else:
                        aux1=aux1.vecinos[0]                                    
                    
                elif  aux2==punto.get_producto():
                    aux2=punto
                    aux2.actualizar_vecinos(f_puntos)
                    if aux2.color==naranja:
                        pass
                    elif len(aux2.vecinos) == 2 and f_sentido=="h":
                        if aux2.columna==aux2.vecinos[0].columna:
                            aux2=aux2.vecinos[0]
                        else:
                            aux2=aux2.vecinos[1]
                    elif len(aux2.vecinos)==2 and f_sentido=="v":
                        if aux2.fila==aux2.vecinos[0].fila:
                            aux2=aux2.vecinos[0]
                        else:
                            aux2=aux2.vecinos[1]
                    else:
                        aux2=aux2.vecinos[0] 

        lista_combinada[it][0]=aux1
        lista_combinada[it][1]=aux2
        it+=1

    for i in lista_combinada:
        var_costo=calcular_costo(algoritmo_A_estrella(f_puntos, i[0], i[1]), i[0], i[1])
        lista2.append(var_costo)

    end=time.time()
    print("\nEl tiempo de calculo fue: ", round(end-start,2))

    return (dict(zip(lista1,lista2)))

class interfaz_grafica: # CLASE INTERFAZ GRAFICA
    def __init__(self):
        self.TAMANIO_X = 0
        self.TAMANIO_Y = 0
        self.ESTANTERIAS = 0
        self.SENTIDO = ""
        self.PRODUCTOS = 0
        self.PASILLOS_V = 0
        self.PASILLOS_H = 0
        self.DICC={}
        self.PUNTO_F=0
        self.GENETICA=[]

    def set_param(self):
        self.TAMANIO_X = int (input("Ingrese ancho de ventana en px: "))
        self.TAMANIO_Y = int (input("Ingrese alto de ventana en px: "))
        self.ESTANTERIAS = int (input("Ingrese la cantidad de estanterias a ubicar: "))
        self.SENTIDO = input ("Desea ubicarlas de manera horizontal (h) o vertical (v): ")
        self.PRODUCTOS = int (input("Indique la cantidad de productos por estanteria (numero par): "))
        self.PASILLOS_V = int (input("Ingrese la cantidad de pasillos verticales: "))
        self.PASILLOS_H = int (input("Ingrese la cantidad de pasillos horizontales: "))
    
    def dibujar(self, comando):
        m, n = None, None
        if self.SENTIDO == "h":
            m=2
            n=self.PRODUCTOS//2
        elif self.SENTIDO == "v":
            m=self.PRODUCTOS//2
            n=2

        FILAS = self.PASILLOS_H+m*(self.PASILLOS_H-1)
        COLUMNAS = self.PASILLOS_V+n*(self.PASILLOS_V-1)

        tamanio=[self.TAMANIO_X, self.TAMANIO_Y]
        matriz=[FILAS, COLUMNAS]
        estante=[m,n]

        #GENETICA
        self.GENETICA=list(range(1,self.ESTANTERIAS*self.PRODUCTOS+2,1))

        puntos = crear_puntos (tamanio, matriz)
        p_inicio = None
        p_bahia_carga = None

        # LEYENDAS PARA LOS DISTINTOS COMANDOS
        if comando == 1:
            print("\nSeleccione el punto de bahia de carga para el algoritmo Temple Simulado o Genetico")
            print("\nPresione la letra x para salir")
        elif comando == 2:
            print("Marcar el punto inicial con un Click en un cuadro blanco (Celeste)"+\
            "\nMarcar el punto final con un Click en un cuadro blanco (Naranja)"+\
            "\nPara generar ruta precione la tecla espacio (Violeta)"+\
            "\nPara limpiar pantalla presione la tecla d"+\
            "\nPara continuar cierre la ventana grafica")
        elif comando == 3:
            n_orden = input("\nIngrese el numero de orden a analizar: ")
            pedido=leer_archivo(n_orden)
            print("\nPara iniciar temple simulado presione la tecla espacio"+\
            "\nPara limpiar pantalla presione la tecla d"+\
            "\nPara continuar cierre la ventana grafica\n")
        else:
            print("\nPara iniciar el algoritmo genetico presione la tecla espacio")
            print("\nPresione X para salir")

        VENTANA = pygame.display.set_mode ((self.TAMANIO_X, self.TAMANIO_Y))
        pygame.display.set_caption ("ALMACEN DE PRODUCTOS")

        run=True
        camino={}
        costo=0
        nueva_distribucion=[]

        while run:
            VENTANA.fill(blanco)
            for lista in puntos:
                for punto in lista:
                    punto.dibujar_celda(VENTANA)
            dibujar_grilla(VENTANA, tamanio, matriz, estante, self.ESTANTERIAS, puntos, nueva_distribucion)
            pygame.display.update()

            if comando == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_x:
                            run=False
                    if pygame.mouse.get_pressed()[0]:
                        print("\nCalculando...")
                        posicion=pygame.mouse.get_pos()
                        fila, columna=obtener_posicion(posicion, matriz, tamanio)
                        click = puntos[fila][columna]
                        if not p_bahia_carga:
                            self.PUNTO_F = click
                            self.PUNTO_F.marcar_final()
                            self.PUNTO_F.set_producto(self.ESTANTERIAS*self.PRODUCTOS+1)
                            self.DICC=costo_individuo(puntos, self.ESTANTERIAS, self.PRODUCTOS, self.SENTIDO)

            elif comando == 2:
                if camino != {}:
                    if p_bahia_carga in camino:
                        p_bahia_carga = camino[p_bahia_carga]
                        p_bahia_carga.ruta()
                        costo+=1
                        p_bahia_carga.set_costo(costo)
                    elif p_bahia_carga==p_inicio and p_aux!=None:
                        print("\n>> El costo del Pi " + str(p_inicio.get_fil_col())+" para llegar al Pf "+ str(p_aux.get_fil_col())+" es: "+ str(costo))
                        p_aux=None
                    p_inicio.marcar_inicio()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if pygame.mouse.get_pressed()[0]:
                        posicion=pygame.mouse.get_pos()
                        fila, columna=obtener_posicion(posicion, matriz, tamanio)
                        click = puntos[fila][columna]
                        if not p_inicio and click != p_bahia_carga:
                            p_inicio = click
                            p_inicio.marcar_inicio()
                        elif not p_bahia_carga and click != p_inicio:
                            p_bahia_carga = click
                            p_bahia_carga.marcar_final()
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE and p_inicio and p_bahia_carga:         
                            camino = algoritmo_A_estrella(puntos,p_inicio,p_bahia_carga)
                            p_aux = p_bahia_carga                
                        if event.key==pygame.K_d:
                            p_inicio = None
                            p_bahia_carga = None
                            puntos = crear_puntos (tamanio, matriz)
                            camino = {}
                            costo = 0

            elif comando == 3:
                p_bahia_carga=puntos[self.PUNTO_F.fila][self.PUNTO_F.columna]
                p_bahia_carga.marcar_final()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE:
                            pedido.insert(0, self.ESTANTERIAS*self.PRODUCTOS+1)
                            pedido.append(self.ESTANTERIAS*self.PRODUCTOS+1)
                            temple_simulado(pedido, self.DICC)
                        if event.key==pygame.K_d:
                            pedido.pop(0)
                            pedido.pop()                   
            
            elif comando == 4:
                p_bahia_carga=puntos[self.PUNTO_F.fila][self.PUNTO_F.columna]
                p_bahia_carga.marcar_final()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE:
                            print("\nCalculando...")
                            nueva_distribucion=algoritmo_genetico(self.GENETICA, self.DICC)

        pygame.quit()