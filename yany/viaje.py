class Viaje:
    ESTADOS_VALIDOS = ["Solicitado", "En_curso", "Finalizado", "Cancelado"]
    TARIFA_BASE = 8000

    def _init_(self, id: int, pasajera: Pasajera, conductora: Conductora, origen: str, destino: str, estado: str = "Solicitado"):
        self.__id = id
        self.pasajera = pasajera
        self.conductora = conductora
        self.origen = origen    
        self.destino = destino
        self.estado = estado

    # getters

    @property
    def id(self):
        return self.__id

    @property
    def pasajera(self):
        return self.__pasajera

    @property
    def conductora(self):
        return self.__conductora

    @property
    def origen(self):
        return self.__origen

    @property
    def destino(self):
        return self.__destino

    @property
    def estado(self):
        return self.__estado


    # setters
    @pasajera.setter
    def pasajera(self, pasajera):
        self.__pasajera = pasajera

    @conductora.setter
    def conductora(self, conductora):
        self.__conductora = conductora

    @origen.setter
    def origen(self, origen):
        if not origen.strip():
            raise ValueError("El origen no puede estar vacío.")
        self.__origen = origen

    @destino.setter
    def destino(self, destino):
        if not destino.strip():
            raise ValueError("El destino no puede estar vacío.")
        self.__destino = destino

    @estado.setter
    def estado(self, estado):
        if estado not in Viaje.ESTADOS_VALIDOS:
            raise ValueError("El estado debe ser uno de: " + ", ".join(Viaje.ESTADOS_VALIDOS))
        self.__estado = estado
