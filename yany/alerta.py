from yany.viaje import Viaje

class Alerta:
    # tipos de alertas que se pueden activar en un viaje
    TIPOS_VALIDOS = ["Emergencia", "Acoso", "Accidente", "Ruta desviada"]

    def _init_(self, id: int, viaje: Viaje, tipo: str, hora: str):
        self.__id = id
        self.viaje = viaje
        self.tipo = tipo
        self.hora = hora
        self.__atendida = False

    @property
    def id(self):
        return self.__id
    @property
    def viaje(self):
        return self.__viaje
    @property
    def tipo(self):
        return self.__tipo
    @property
    def hora(self):
        return self.__hora
    @property
    def atendida(self):
        return self.__atendida


    @viaje.setter
    def viaje(self, viaje):
        self.__viaje = viaje
    @tipo.setter
    def tipo(self, tipo):
        if tipo not in Alerta.TIPOS_VALIDOS:
            raise ValueError("El tipo debe ser uno de: " + ", ".join(Alerta.TIPOS_VALIDOS))
        self.__tipo = tipo
    @hora.setter
    def hora(self, hora):
        if not hora.strip():
            raise ValueError("La hora no puede estar vacía.")
        self.__hora = hora

    # metodos
    # metodo atender (marca la alerta como atendida)
    def atender(self):
        if self.__atendida:
            raise ValueError("La alerta ya fue atendida.")
        self.__atendida = True

    # metodo mostrar info
    def mostrar_info(self):
        estado = "atendida" if self.atendida else "pendiente"
        return f"Alerta {self.id} ({self.tipo}) a las {self.hora}, viaje {self.viaje.id}: {estado}."