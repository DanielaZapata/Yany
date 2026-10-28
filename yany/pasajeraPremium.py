from yany.pasajera import Pasajera

class PasajeraPremium(Pasajera):
    def __init__(self, id: int, nombre: str, telefono: str, contacto_emergencia: str, porcentaje_descuento: float = 0.05):
        #Hereda de Pasajera
        super().__init__(id, nombre, telefono, contacto_emergencia)
        self.porcentaje_descuento = porcentaje_descuento

    #GETTER
    @property
    def porcentaje_descuento(self):
        return self.__porcentaje_descuento

    #SETTER 
    @porcentaje_descuento.setter
    def porcentaje_descuento(self, porcentaje_descuento):
        if porcentaje_descuento < 0 or porcentaje_descuento > 1:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 1.")
        self.__porcentaje_descuento = porcentaje_descuento 


    #MÉTODO CALCULAR DESCUENTO
    def calcular_descuento(self, valor_viaje: float):
        #LA PASAJERA PREMIUM TIENE UN DESCUENTO DEL 5% (0.05)
        return valor_viaje * self.__porcentaje_descuento
