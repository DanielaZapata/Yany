from yany.estructuras.nodo import Nodo
class Cola:
    def __init__(self):
        self.__frente = None
        self.__final = None
        self.__tamano = 0

    # GETTERS
    @property
    def frente(self):
        return self.__frente
    @property
    def final(self):
        return self.__final
    @property
    def tamano(self):
        return self.__tamano

    # VERIFICAR SI LA COLA ESTA VACIA
    def esta_vacia(self):
        return self.__frente is None

    # AGREGAR A LA COLA
    def agregar_cola(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.__frente = nuevo_nodo
            self.__final = nuevo_nodo
        else:
            self.__final.siguiente = nuevo_nodo
            self.__final = nuevo_nodo
        self.__tamano += 1

    # SACAR DE LA COLA
    def sacar_cola(self):
        if self.esta_vacia():
            return None
        dato = self.__frente.dato
        self.__frente = self.__frente.siguiente
        self.__tamano -= 1
        if self.__frente is None:
            self.__final = None
        return dato

    # EL PRIMER ELEMENTO
    def ver_frente(self):
        if self.esta_vacia():
            return None
        return self.__frente.dato

    # MOSTRAR LA COLA
    def mostrar(self):
        elementos = []
        actual = self.__frente
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos