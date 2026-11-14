class NodoArbol:
    def _init_(self, dato):
        self.__dato = dato
        self.__izquierdo = None
        self.__derecho = None

    @property
    def dato(self):
        return self.__dato
    @property
    def izquierdo(self):
        return self.__izquierdo
    @property
    def derecho(self):
        return self.__derecho

    #SETTERS
    @izquierdo.setter
    def izquierdo(self, izquierdo):
        self.__izquierdo = izquierdo
    @derecho.setter
    def derecho(self, derecho):
        self.__derecho = derecho


class Arbol:
    def _init_(self):
        self.__raiz = None

    @property
    def raiz(self):
        return self.__raiz

    #INSERTA una zona ordenada por su id
    def insertar(self, zona):
        if self.__raiz is None:
            self.__raiz = NodoArbol(zona)
        else:
            self.insertar_en(self._raiz, zona)

    def _insertar_en(self, nodo, zona):
        if zona.id == nodo.dato.id:
            raise ValueError("Ya existe una zona con el id " + str(zona.id) + ".")
        if zona.id < nodo.dato.id:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(zona)
            else:
                self._insertar_en(nodo.izquierdo, zona)
        else:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(zona)
            else:
                self._insertar_en(nodo.derecho, zona)

    # busca una zona por id, si no existe devuele None
    def buscar(self, id):
        actual = self.__raiz
        while actual is not None:
            if id == actual.dato.id:
                return actual.dato
            if id < actual.dato.id:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

    # devuelve las zonas ordenadas por id (izquerda, raiz, derecha)
    def inorden(self):
        zonas = []
        self.inorden_en(self._raiz, zonas)
        return zonas

    def _inorden_en(self, nodo, zonas):
        if nodo is not None:
            self._inorden_en(nodo.izquierdo, zonas)
            zonas.append(nodo.dato)
            self._inorden_en(nodo.derecho, zonas)