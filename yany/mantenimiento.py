class Mantenimiento:
    def __init__(self, fecha: str, descripcion: str):
        self.fecha = fecha 
        self.descripcion = descripcion 

    #GETTERS 
    @property
    def fecha(self):
        return self.__fecha
    @property
    def descripcion(self):
        return self.__descripcion 
    
    #SETTERS 
    @fecha.setter
    def fecha(self, fecha):
        self.__fecha = fecha 
    @descripcion.setter
    def descripcion(self, descripcion):
        if not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")
        self.__descripcion = descripcion 

    #MÉTODO MOSTRAR INFO
    def mostrar_info(self):
        return f"el mantenimiento del vehículo tiene como fecha: {self.fecha}, y aparte: {self.descripcion}."