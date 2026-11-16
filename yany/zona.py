class Zona:
    def __init__(self, id: int, nombre: str):
        self.__id = id
        self.__nombre = nombre

    #GETTERS
    @property
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre

    #SETTERS
    @nombre.setter
    def nombre(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre de la zona no puede estar vacío.")
        self.__nombre = nombre

    #MÉTODO MOSTRAR INFO
    def mostrar_info(self):
        return f"Zona {self.id}: {self.nombre}."
