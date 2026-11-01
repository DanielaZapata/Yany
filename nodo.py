class Nodo:
    def __init__(self, dato):
        self.__dato = dato
        self.__siguiente = None

    # GETTERS
    @property
    def dato(self):
        return self.__dato

    @property
    def siguiente(self):
        return self.__siguiente

    # SETTERS
    @dato.setter
    def dato(self, dato):
        self.__dato = dato

    @siguiente.setter
    def siguiente(self, siguiente):
        self.__siguiente = siguiente