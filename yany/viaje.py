from yany.pasajera import Pasajera
from yany.conductora import Conductora


class Viaje:

    ESTADOS_VALIDOS = ["Solicitado", "En_curso", "Finalizado", "Cancelado"]

    TARIFA_BASE = 8000
    VALOR_KM = 1500

    def __init__(
        self,
        id: int,
        pasajera: Pasajera,
        conductora: Conductora,
        origen: str,
        destino: str,
        estado: str = "Solicitado",
        distancia_km: float = 0
    ):

        self.__id = id
        self.pasajera = pasajera
        self.conductora = conductora
        self.origen = origen
        self.destino = destino
        self.estado = estado
        self.distancia_km = distancia_km

    # GETTERS

    @property
    def id(self):
        return self.__id

    @property
    def pasajera(self):
        return self.__pasajera

    @property
    def conductora(self):
        return self.__conductora

    @property
    def origen(self):
        return self.__origen

    @property
    def destino(self):
        return self.__destino

    @property
    def estado(self):
        return self.__estado

    @property
    def distancia_km(self):
        return self.__distancia_km

    # SETTERS

    @pasajera.setter
    def pasajera(self, pasajera):
        self.__pasajera = pasajera

    @conductora.setter
    def conductora(self, conductora):
        self.__conductora = conductora

    @origen.setter
    def origen(self, origen):
        if not origen.strip():
            raise ValueError("El origen no puede estar vacío.")
        self.__origen = origen

    @destino.setter
    def destino(self, destino):
        if not destino.strip():
            raise ValueError("El destino no puede estar vacío.")
        self.__destino = destino

    @estado.setter
    def estado(self, estado):
        if estado not in Viaje.ESTADOS_VALIDOS:
            raise ValueError(
                "El estado debe ser uno de: "
                + ", ".join(Viaje.ESTADOS_VALIDOS)
            )
        self.__estado = estado

    @distancia_km.setter
    def distancia_km(self, distancia):
        if not isinstance(distancia, (int, float)) or distancia < 0:
            raise ValueError("La distancia debe ser un número positivo.")

        self.__distancia_km = distancia

    # MÉTODOS

    def calcular_tarifa(self):

        base = Viaje.TARIFA_BASE + (
            self.distancia_km * Viaje.VALOR_KM
        )

        descuento = self.pasajera.calcular_descuento(base)

        return base - descuento

    def cambiar_estado(self, estado: str):

        if self.estado in ("Finalizado", "Cancelado"):
            raise ValueError(
                "No se puede cambiar el estado de un viaje "
                + self.estado + "."
            )

        self.estado = estado

    def mostrar_info(self):

        return (
            f"Viaje {self.id}: de {self.origen} a {self.destino}, "
            f"estado: {self.estado}, "
            f"distancia: {self.distancia_km} km, "
            f"tarifa: {self.calcular_tarifa()}."
        )