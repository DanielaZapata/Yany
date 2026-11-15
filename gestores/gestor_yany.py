from datetime import datetime
from estructuras.lista import Lista
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.arbol import Arbol
from gestores.gestor_archivos import GestorArchivos
from yany.alerta import Alerta

class GestorYANY:
    def __init__(self):
        # listas
        self.lista_pasajeras = Lista()
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
        # revisar que no este repetida (por id)
        for p in self.__lista_pasajeras.mostrar():
            if p.id == pasajera.id:
                return False
        self.__lista_pasajeras.agregar(pasajera)
        return True


    def registrar_conductora(self, conductora):
        # igual que la pasajera pero con lista_conductoras
        for c in self.__lista_conductoras.mostrar():
            if c.id == conductora.id:
                return False
        self.__lista_conductoras.agregar(conductora)
        return True

 
    def solicitar_viaje(self, viaje):
        # meter el viaje al final de cola_solicitudes
        self.__cola_solicitudes.agregar_cola(viaje)
        return True


    def __buscar_conductora_disponible(self):
        for c in self.__lista_conductoras.mostrar():
            if c.disponible and c.certificada:
                return c
        return None

 
    def asignar_viajes(self):
        # mientras haya solicitudes y conductoras libres, se van asignando
        asignados = 0
        while not self.__cola_solicitudes.esta_vacia():
            conductora = self.__buscar_conductora_disponible()
            if conductora is None:
                # si no hay conductoras libres, las demas solicitudes esperan
                break
 
            # sacar la primera solicitud de la cola y asignarle la conductora
            viaje = self.__cola_solicitudes.sacar_cola()
            viaje.conductora = conductora
            viaje.cambiar_estado("En_curso")
            conductora.disponible = False
 
            # guardar el viaje en lista_viajes
            self.__lista_viajes.agregar(viaje)
            asignados += 1
        return asignados
 
 
    def activar_alerta(self, id_viaje, tipo):
        # buscar el viaje, si no existe no se crea la alerta
        viaje = self.__buscar_viaje(id_viaje)
        if viaje is None:
            return None
 
        # crear la alerta con un id nuevo y la hora de ahora
        hora = datetime.now().strftime("%H:%M")
        alerta = Alerta(self.__contador_alertas, viaje, tipo, hora)
        self.__contador_alertas += 1
 
        # meterla en cola_alertas
        self.__cola_alertas.agregar_cola(alerta)
        return alerta
 
    def atender_alerta(self):
        # sacar la siguiente alerta de la cola (la que lleva mas tiempo)
        alerta = self.__cola_alertas.sacar_cola()
        if alerta is None:
            return None
        alerta.atender()
        return alerta
 
 
    def finalizar_viaje(self, id_viaje):
        # 1. buscar el viaje en lista_viajes
        viaje = self.__buscar_viaje(id_viaje)
        if viaje is None:
            return False
 
        # 2. cambiar su estado a finalizado
        viaje.cambiar_estado("Finalizado")
 
        # la conductora queda libre otra vez
        if viaje.conductora is not None:
            viaje.conductora.disponible = True
 
        # 3. apilarlo en pila_historial
        self.__pila_historial.agregar_pila(viaje)
        return True
 
    def guardar_todo(self):
        # cada lista se guarda en su propio archivo json
        self.__archivos.guardar_pasajeras(self.__lista_pasajeras)
        self.__archivos.guardar_conductoras(self.__lista_conductoras)
        self.__archivos.guardar_viajes(self.__lista_viajes)
        # falta: self.__archivos.guardar_zonas(self.__arbol_zonas)
 
    def cargar_todo(self):
        # el orden importa: los viajes necesitan las pasajeras y conductoras
        self.__lista_pasajeras = self.__archivos.cargar_pasajeras()
        self.__lista_conductoras = self.__archivos.cargar_conductoras()
        self.__lista_viajes = self.__archivos.cargar_viajes(
            self.__lista_pasajeras, self.__lista_conductoras)
        # falta: self.__arbol_zonas = self.__archivos.cargar_zonas()
 
        # el historial no se guarda: se arma de nuevo con los viajes finalizados
        self.__pila_historial = Pila()
        for v in self.__lista_viajes.mostrar():
            if v.estado == "Finalizado":
                self.__pila_historial.agregar_pila(v)
 