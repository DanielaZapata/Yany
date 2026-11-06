from estructuras.nodo import Nodo
class Pila:
    def __init__(self):
        self.__cima = None
        self.__tamano = 0

    # GETTERS
    @property
    def cima(self):
        return self.__cima
    @property
    def tamano(self):
        return self.__tamano

    # VERIFICAR SI LA PILA ESTA VACIA
    def esta_vacia(self):
        return self.__cima is None

    # AGREGAR A LA PILA
    def agregar_pila(self, dato):
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.__cima
        self.__cima = nuevo_nodo
        self.__tamano += 1

    # SACAR DE LA PILA
    def sacar_pila(self):
        if self.esta_vacia():
            return None
        dato = self.__cima.dato
        self.__cima = self.__cima.siguiente
        self.__tamano -= 1
        return dato

    # VER EL ELEMENTO DE ARRIBA
    def ver_cima(self):
        if self.esta_vacia():
            return None
        return self.__cima.dato

    # MOSTRAR LA PILA
    def mostrar(self):
        elementos = []
        actual = self.__cima
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos