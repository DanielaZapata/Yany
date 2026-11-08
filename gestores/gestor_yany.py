from estructuras.lista import Lista
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.arbol import Arbol
from gestores.gestor_yany import GestorArchivos

class GestorYANY:
    def __init__(self):
        # listas
        self.lista_pasajera = Lista()
        self.lista_conductoras = Lista()
        self.lista_viajes = Lista()

        # colas
        self.cola_solicitudes = Cola()
        self.cola_alertas = Cola()
 
        # pila del historial (el ultimo viaje queda arriba)
        self.pila_historial = Pila()
 
        # arbol de zonas
        self.arbol_zonas = Arbol()
 
        # para guardar y cargar los datos en archivos
        self.archivos = GestorArchivos()


    def registrar_pasajera(self, pasajera):
        # 1. revisar que no este repetida (por id o cedula)
        # 2. agregarla a lista_pasajeras
        pass