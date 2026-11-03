class Vehiculo: 
    def __init__(self, placa: str, color: str, anio: int, mantenimientos: list = None):
        self.placa = placa 
        self.color = color 
        self.anio = anio 
        self.mantenimientos = mantenimientos if mantenimientos is not None else []

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
        if not placa.strip():
            raise ValueError("La placa no puede estar vacía.")
        self.__placa = placa 
    @color.setter
    def color(self, color):
        self.__color = color 
    @anio.setter
    def anio(self, anio):
        if not isinstance(anio, int) or not 1900 <= anio <= 2100:
            raise ValueError("El año debe ser un entero entre 1900 y 2100.")
        self.__anio = anio 
    @mantenimientos.setter
    def mantenimientos(self, mantenimientos):
        self.__mantenimientos = mantenimientos 

    #MÉTODO REGISTRAR_MANTENIMIENTO
    def registrar_mantenimiento(self, mantenimiento):
        self.__mantenimientos.append(mantenimiento)

    #MÉTODO MOSTRAR_INFO
    def mostrar_info(self):
        return f"Vehículo placa {self.placa}, color {self.color}, año {self.anio}, con {len(self.mantenimientos)} mantenimientos."

