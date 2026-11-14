from yany.viaje import Viaje
from yany.pasajera import Pasajera
from yany.conductora import Conductora

class ViajeConAcompanante(Viaje):
    # Recargos que suman a la tarifa del viaje normal
    RECARGO_ACOMPANANTE = 2000
    RECARGO_MASCOTA = 1500

    def __init__(self, id: int, pasajera: Pasajera, conductora: Conductora, origen: str, destino: str, num_acompanantes: int = 0, lleva_mascota: bool = False, estado: str = "Solicitado"):
        super().__init__(id, pasajera, conductora, origen, destino, estado)
        self.num_acompanantes = num_acompanantes
        self.lleva_mascota = lleva_mascota

    @property
    def num_acompanantes(self):
        return self.__num_acompanantes

    @property
    def lleva_mascota(self):
        return self.__lleva_mascota

    @num_acompanantes.setter
    def num_acompanantes(self, num_acompanantes):
        if not isinstance(num_acompanantes, int) or isinstance(num_acompanantes, bool) or num_acompanantes < 0:
            raise ValueError("El número de acompañantes debe ser un entero mayor o igual a 0.")
        self.__num_acompanantes = num_acompanantes

    @lleva_mascota.setter
    def lleva_mascota(self, lleva_mascota):
        if not isinstance(lleva_mascota, bool):
            raise ValueError("lleva_mascota debe ser True o False.")
        self.__lleva_mascota = lleva_mascota

    # Métodos
    # Tarifa = tarifa del padre + recargos
    def calcular_tarifa(self):
        tarifa = super().calcular_tarifa()
        tarifa += self.num_acompanantes * ViajeConAcompanante.RECARGO_ACOMPANANTE
        if self.lleva_mascota:
            tarifa += ViajeConAcompanante.RECARGO_MASCOTA
        return tarifa

    def mostrar_info(self):
        mascota = "con mascota" if self.lleva_mascota else "sin mascota"
        return super().mostrar_info().rstrip(".") + f", acompañantes: {self.num_acompanantes}, {mascota}."
    
