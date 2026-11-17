from datetime import datetime
from estructuras.lista import Lista
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.arbol import Arbol
from gestores.gestor_archivos import GestorArchivos
from yany.alerta import Alerta
from yany.excepciones import ViajeNoEncontrado, ConductoraNoDisponible, ColaVaciaError

class GestorYANY:
    def __init__(self):
        # listas
        self.__lista_pasajeras = Lista()
        self.__lista_conductoras = Lista()
        self.__lista_viajes = Lista()

        # colas
        self.__cola_solicitudes = Cola()
        self.__cola_alertas = Cola()
 
        # pila del historial (el ultimo viaje queda arriba)
        self.__pila_historial = Pila()
 
        # arbol de zonas
        self.__arbol_zonas = Arbol()
 
        # para guardar y cargar los datos en archivos
        self.__archivos = GestorArchivos()

        # para darle un id distinto a cada alerta
        self.__contador_alertas = 1

    @property
    def lista_pasajeras(self):
        return self.__lista_pasajeras

    @property
    def lista_conductoras(self):
        return self.__lista_conductoras

    @property
    def lista_viajes(self):
        return self.__lista_viajes

    @property
    def pila_historial(self):
        return self.__pila_historial

    @property
    def arbol_zonas(self):
        return self.__arbol_zonas

    def registrar_pasajera(self, pasajera):
        for p in self.__lista_pasajeras.mostrar():
            if p.id == pasajera.id:
                return False
        self.__lista_pasajeras.agregar(pasajera)
        return True


    def registrar_conductora(self, conductora):
        for c in self.__lista_conductoras.mostrar():
            if c.id == conductora.id:
                return False
        self.__lista_conductoras.agregar(conductora)
        return True

 
    def solicitar_viaje(self, viaje):
        self.__cola_solicitudes.agregar_cola(viaje)
        return True


    def __buscar_conductora_disponible(self):
        for c in self.__lista_conductoras.mostrar():
            if c.disponible and c.certificada:
                return c
        return None

 
    def asignar_viajes(self):
        asignados = 0
        while not self.__cola_solicitudes.esta_vacia():
            conductora = self.__buscar_conductora_disponible()
            if conductora is None:
                if asignados == 0:
                    raise ConductoraNoDisponible("No hay conductoras disponibles.")
                break

            viaje = self.__cola_solicitudes.sacar_cola()
            viaje.conductora = conductora
            viaje.cambiar_estado("En_curso")
            conductora.disponible = False

            self.__lista_viajes.agregar(viaje)
            asignados += 1
        return asignados

    def __buscar_viaje(self, id_viaje):
        for v in self.__lista_viajes.mostrar():
            if v.id == id_viaje:
                return v
        return None    
 
    def activar_alerta(self, id_viaje, tipo):
        viaje = self.__buscar_viaje(id_viaje)
        if viaje is None:
            raise ViajeNoEncontrado(f"No se encontró el viaje {id_viaje}.")
 
        hora = datetime.now().strftime("%H:%M")
        alerta = Alerta(self.__contador_alertas, viaje, tipo, hora)
        self.__contador_alertas += 1
 
        self.__cola_alertas.agregar_cola(alerta)
        return alerta
 
    def atender_alerta(self):
        alerta = self.__cola_alertas.sacar_cola()
        if alerta is None:
            raise ColaVaciaError("No hay alertas pendientes por atender.")
        alerta.atender()
        return alerta

    def finalizar_viaje(self, id_viaje):
        viaje = self.__buscar_viaje(id_viaje)
        if viaje is None:
            raise ViajeNoEncontrado(f"No se encontró el viaje {id_viaje}.")

        viaje.cambiar_estado("Finalizado")
 
        if viaje.conductora is not None:
            viaje.conductora.disponible = True

        self.__pila_historial.agregar_pila(viaje)
        return True
 
    def guardar_todo(self):
        self.__archivos.guardar_pasajeras(self.__lista_pasajeras)
        self.__archivos.guardar_conductoras(self.__lista_conductoras)
        self.__archivos.guardar_viajes(self.__lista_viajes)
        self.__archivos.guardar_zonas(self.__arbol_zonas)
 
    def cargar_todo(self):
        self.__lista_pasajeras = self.__archivos.cargar_pasajeras()
        self.__lista_conductoras = self.__archivos.cargar_conductoras()
        self.__lista_viajes = self.__archivos.cargar_viajes(
            self.__lista_pasajeras, self.__lista_conductoras)
        self.__arbol_zonas = self.__archivos.cargar_zonas()

 
        self.__pila_historial = Pila()
        for v in self.__lista_viajes.mostrar():
            if v.estado == "Finalizado":
                self.__pila_historial.agregar_pila(v)
 