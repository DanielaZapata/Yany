from yany.viaje import Viaje 

class ViajeNormal(Viaje):
    # Viaje sin acompañante ni mascotas usa la tarifa base de la clase padre

    def calcular_tarifa(self):
        return super().calcular_tarifa()
    

