from estructuras.pila import Pila

def test_pila_vacia():
    pila = Pila()
    assert pila.esta_vacia() is True
    assert pila.tamano == 0

def test_agregar_pila():
    pila = Pila()
    pila.agregar_pila("Laura")
    pila.agregar_pila("Camila")
    assert pila.mostrar() == ["Camila", "Laura"]
    assert pila.tamano == 2

def test_sacar_pila():
    pila = Pila()
    pila.agregar_pila("Laura")
    pila.agregar_pila("Camila")
    dato = pila.sacar_pila()
    assert dato == "Camila"
    assert pila.mostrar() == ["Laura"]
    assert pila.tamano == 1

def test_ver_cima():
    pila = Pila()
    pila.agregar_pila("Laura")
    pila.agregar_pila("Camila")
    assert pila.ver_cima() == "Camila"