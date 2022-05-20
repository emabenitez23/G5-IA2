from interfaz import *
from cmd import Cmd
import os

class Consola (Cmd):    # CLASE CONSOLA

    def __init__(self): # INICIALIZACION DE LA CONSOLA
        Cmd.__init__(self)
        self.Interfaz=interfaz_grafica()
    
    def do_6 (self, arg):  #EXIT
        """Finaliza el programa en ejecución"""
        raise SystemExit

    def do_5 (self, args):  # MENU
        """Brinda ayuda al usuario acerca de los comandos"""
        os.system ('cls')
        if args==2:
            text="\n'INTELIGENCIA ARTIFICIAL 2'  Grupo 5: Benitez Lautaro - Benitez Emanuel\n"
        else:
            text="\n'INTELIGENCIA ARTIFICIAL 2'  Grupo 5: Benitez Lautaro - Benitez Emanuel\n\n" + \
                " Indice de comandos:\n\n"+\
                "   - Diseño del escenario (1)          - Algoritmo A* (2)\n"+\
                "   - Algoritmo Temple Simulado (3)     - Algoritmo Genético (4)\n"+\
                "   - Menu (5)                          - Exit (6)\n\n" +\
                "Para obtener ayuda sobre un comando presione 'help (n° de comando)' \n"
        print(text)

    def do_1(self, arg): # DISEÑO DEL ESCENARIO
        """Diseña el layout del almacen"""
        try:
            self.do_5(2)
            self.Interfaz.set_param()
            self.Interfaz.dibujar(1)
            self.do_5(1)
        except:
            self.do_5(1)
            print("ERROR al cargar los datos, vuelva a intentar")

    def do_2 (self, arg):    # ALGORITMO A*
        """El algoritmo A* calcula el camino mas optimo entre 2 puntos"""
        self.do_5(2)
        try:
            self.Interfaz.dibujar(2)
            self.do_5(1)
        except:
            self.do_5(1)
            print("ERROR: Primero debe diseñar el escenario del almacen")

    def do_3 (self, arg):    # ALGORITMO TEMPLE SIMULADO
        """El algoritmo Temple Simulado calcula el camino mas optimo para el picking de una orden de pedido"""
        self.do_5(2)
        try:
            self.Interfaz.dibujar(3)
            self.do_5(1)
        except:
            self.do_5(1)
            print("ERROR: Primero debe diseñar el escenario del almacen")

    def do_4 (self, arg):    # ALGORITMO GENETICO
        """El algoritmo Genetico calcula la mejor distribucion de los productos en el almacen en base a un conjunto de ordenes de pedido"""
        self.do_5(2)
        try:
            self.Interfaz.dibujar(4)
            self.do_5(1)
        except:
            self.do_5(1)
            print("ERROR: Primero debe diseñar el escenario del almacen")

if __name__=='__main__':    # INICIALIZACION DEL PROGRAMA
    
    os.system ('cls')
    menu = Consola()
    menu.prompt = ' >> '
    menu.doc_header = 'Indice de comandos:'
    text="\n'INTELIGENCIA ARTIFICIAL 2'  Grupo 5: Benitez Lautaro - Benitez Emanuel\n\n" + \
        " Indice de comandos:\n\n"+\
        "   - Diseño del escenario (1)          - Algoritmo A* (2)\n"+\
        "   - Algoritmo Temple Simulado (3)     - Algoritmo Genético (4)\n"+\
        "   - Menu (5)                          - Exit (6)\n\n" +\
        "Para obtener ayuda sobre un comando presione 'help (n° de comando)' \n"
    menu.cmdloop(text)        