import pytest
from estructuras.nodo import Nodo

def test_crear_nodo():
    nodo = Nodo("Laura")
    assert nodo.dato == "Laura"
    assert nodo.siguiente is None

def test_conectar_nodos():
    nodo1 = Nodo("Laura")
    nodo2 = Nodo("Sofia")
    nodo1.siguiente = nodo2
    assert nodo1.siguiente.dato == "Sofia"