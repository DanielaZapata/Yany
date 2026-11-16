import pytest
from estructuras.arbol import Arbol, NodoArbol

# zona de prueba, solo necesita tener id
class ZonaPrueba:
    def _init_(self, id, nombre):
        self.id = id
        self.nombre = nombre

def crear_arbol():
    arbol = Arbol()
    for id in [5, 3, 8, 1, 4]:
        arbol.insertar(ZonaPrueba(id, "Zona " + str(id)))
    return arbol

def test_arbol_nuevo_esta_vacio():
    arbol = Arbol()
    assert arbol.raiz is None
    assert arbol.inorden() == []

def test_primer_insertado_es_la_raiz():
    arbol = Arbol()
    arbol.insertar(ZonaPrueba(5, "Centro"))
    assert isinstance(arbol.raiz, NodoArbol)
    assert arbol.raiz.dato.id == 5

def test_menor_va_a_la_izquierda_y_mayor_a_la_derecha():
    arbol = crear_arbol()
    assert arbol.raiz.izquierdo.dato.id == 3
    assert arbol.raiz.derecho.dato.id == 8

def test_buscar_zona_existente():
    arbol = crear_arbol()
    assert arbol.buscar(4).nombre == "Zona 4"
    assert arbol.buscar(8).nombre == "Zona 8"

def test_buscar_zona_inexistente_devuelve_none():
    arbol = crear_arbol()
    assert arbol.buscar(99) is None

def test_buscar_en_arbol_vacio():
    assert Arbol().buscar(1) is None

def test_inorden_devuelve_zonas_ordenadas():
    arbol = crear_arbol()
    ids = [zona.id for zona in arbol.inorden()]
    assert ids == [1, 3, 4, 5, 8]

def test_insertar_id_repetido_lanza_error():
    arbol = crear_arbol()
    with pytest.raises(ValueError):
        arbol.insertar(ZonaPrueba(3, "Repetida"))