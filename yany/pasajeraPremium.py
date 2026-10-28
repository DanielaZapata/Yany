from pasajera import Pasajera

class PasajeraPremium:
    def __init__(self, id = int, nombre = str, telefono = str, contacto_emergencia = str, porcentaje_descuento = float):
        #Hereda de Pasajera
        super().__init__(id, nombre, telefono, contacto_emergencia)
        self.porcentaje_descuento = 0.05

    #GETTER
    def porcentaje_descuento(self):
        return self.__porcentaje_descuento

    #SETTER 
    @porcentaje_descuento.setter
    def porcentaje_descuento(self, porcentaje_descuento):
        self.__porcentaje_descuento = porcentaje_descuento 
        