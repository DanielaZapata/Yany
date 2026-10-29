from yany.persona import Persona

class Pasajera(Persona):
    def __init__(self, id=int, nombre=str, telefono=str, contacto_emergencia=str):
        #HEREDA LOS ATRIBUTOS DE LA CLASE PADRE (PERSONA) 
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

    #MÉTODOS 
    #MÉTODO CALCULAR DESCUENTO
    def calcular_descuento(self, valor_viaje= float):
        #LA PASAJERA ESTÁNDAR TIENE UN DESCUENTO DEL 2% (0.02)
        return valor_viaje * 0.02
  
      # MÉTODO MOSTRAR INFORMACIÓN 
    def mostrar_info(self):
        info_persona = super().mostrar_info()
        return f"{info_persona}, y el contacto de emergencia es: {self.__contacto_emergencia}."  