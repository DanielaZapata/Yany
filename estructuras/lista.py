from estructuras.nodo import Nodo

class Lista:
    def __init__(self):
        self.__cabeza = None
        self.__tamano = 0

    # GETTERS
    @property
    def cabeza(self):
        return self.__cabeza

    @property
    def tamano(self):
        return self.__tamano

  # VERIFICAR SI LA LISTA ESTA VACIA
    def esta_vacia(self):
        return self.__cabeza is None

    # AGREGAR ELEMENTO
    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.__cabeza = nuevo_nodo
        else:
            actual = self.__cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.__tamano += 1

    # BUSCAR ELEMENTO
    def buscar(self, dato):
        actual = self.__cabeza
        while actual is not None:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
        return None

    # ELIMINAR ELEMENTO
    def eliminar(self, dato):
        actual = self.__cabeza
        anterior = None
        while actual is not None:
            if actual.dato == dato:
                if anterior is None:
                    self.__cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self.__tamano -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    # MOSTRAR ELEMENTOS
    def mostrar(self):
        elementos = []
        actual = self.__cabeza
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos