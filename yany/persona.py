class Persona: 
    def __init__(self, id= int, nombre= str, telefono= str): 
        self.id = id 
        self.nombre = nombre 
        self.telefono = telefono 

    #GETTERS 
    @property 
    def id(self):
        return self.__id 
    @property 
    def nombre(self):
        return self.__nombre 
    @property 
    def telefono(self):
        return self.__telefono

    #SETTERS 
    @id.setter
    def id(self, id):
        self.__id = id 
    @nombre.setter
    def nombre(self, nombre):
        if not nombre.strip(): 
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nombre 
    @telefono.setter
    def telefono(self, telefono):
        self.__telefono = telefono

    #MÉTODO MOSTRAR INOFORMACIÓN
    def mostrar_info(self):
        return f"El id es: {self.__id}, el nombre es: {self.__nombre},  y el telefono es: {self.__telefono}."
