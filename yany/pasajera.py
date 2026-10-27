from persona import Persona

class Pasajera(Persona):
    def __init__(self, id= int, nombre= str, telefono= str, contacto_emergencia= str):
        # Heredamos los atributos de la clase (Persona)
        super().__init__(id, nombre, telefono)
        self.contacto_emergencia = contacto_emergencia

    