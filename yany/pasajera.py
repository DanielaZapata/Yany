from persona import Persona

class Pasajera(Persona):
    def __init__(self, id= int, nombre= str, telefono= str, contacto_emergencia= str):
        # Heredamos los atributos de la clase (Persona)
        super().__init__(id, nombre, telefono)
        self.contacto_emergencia = contacto_emergencia

class Pasajera(Persona):
    def __init__(self, id=int, nombre=str, telefono=str, contacto_emergencia=str):
        # Heredamos los atributos de la clase padre (Persona)
        super().__init__(id, nombre, telefono)
        self.contacto_emergencia = contacto_emergencia

    #GETTER
    @property
    def contacto_emergencia(self):
        return self.__contacto_emergencia

    #SETTER
    @contacto_emergencia.setter
    def contacto_emergencia(self, contacto_emergencia):
        if not contacto_emergencia.strip():
            raise ValueError("El contacto de emergencia no puede estar vacío.")
        self.__contacto_emergencia = contacto_emergencia

    