class Persona: 
    def __init__(self, id= int, nombre= str, telefono= str): 
        self.__id = id 
        self.__nombre = nombre 
        self.__telefono = telefono 

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
        self.__nombre = nombre 
    @telefono.setter
    def telefono(self, telefono):
        self.__telefono = telefono


