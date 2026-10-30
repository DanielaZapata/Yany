class Vehiculo: 
    def __init__(self, placa: str, color: str, anio: int, mantenimientos: list):
        self.placa = placa 
        self.color = color 
        self.anio = anio 
        self.mantenimientos = mantenimientos 

    #GETTERS 
    @property
    def placa(self):
        return self.__placa 
    @property 
    def color(self):
        return self.__color 
    @property 
    def anio(self):
        return self.__anio 
    @property 
    def mantenimientos(self):
        return self.__mantenimientos

    #SETTERS 
    @placa.setter
    def placa(self, placa):
        self.__placa = placa 
    @color.setter
    def color(self, color):
        self.__color = color 
    @anio.setter
    def anio(self, anio):
        self.__anio = anio 
    @mantenimientos.setter
    def mantenimientos(self, mantenimientos):
        self.__mantenimientos = mantenimientos 

