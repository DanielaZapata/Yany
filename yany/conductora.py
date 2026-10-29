from yany.persona import Persona

class Conductora(Persona):
    def __init__(self, id: int, nombre: str, telefono: str, certificada: bool, disponible: bool, vehiculo = None, resenas = None):
        #HEREDA LOS ATRIBUTOS DE LA CLASE PADRE(Persona)
        super().__init__(id, nombre, telefono)
        self.certificada = certificada 
        self.disponible = disponible 
        self.vehiculo = vehiculo 
        self.resenas = resenas if resenas is not None else []

    #GETTERS 
    @property
    def certificada(self):
        return self.__certificada
    @property
    def disponible(self):
        return self.__disponible 
    @property
    def vehiculo(self):
        return self.__vehiculo 
    @property
    def resenas(self):
        return self.__resenas

    #SETTERS 
    @certificada.setter
    def certificada(self, certificada):
        if not isinstance(certificada, bool):
            raise ValueError("certificada debe ser True o False.")
        self.__certificada = certificada 
    @disponible.setter
    def disponible(self, disponible):
        if not isinstance(disponible, bool):
            raise ValueError("disponible debe ser True o False.")
        self.__disponible = disponible 
    @vehiculo.setter 
    def vehiculo(self, vehiculo):
        self.__vehiculo = vehiculo 
    @resenas.setter
    def resenas(self, resenas):
        self.__resenas = resenas