from estructuras.lista import Lista

def test_lista_vacia():
    lista = Lista()
    assert lista.esta_vacia() is True
    assert lista.tamano == 0

def test_agregar_elementos():
    lista = Lista()
    lista.agregar("Camila")
    lista.agregar("Daniela")
    assert lista.tamano == 2
    assert lista.mostrar() == ["Camila", "Daniela"]

def test_buscar_elemento():
    lista = Lista()
    lista.agregar("Camila")
    lista.agregar("Daniela")
    assert lista.buscar("Daniela") == "Daniela"
    assert lista.buscar("Laura") is None

def test_eliminar_elemento():
    lista = Lista()
    lista.agregar("Camila")
    lista.agregar("Daniela")
    assert lista.eliminar("Camila") is True
    assert lista.mostrar() == ["Daniela"]
    assert lista.tamano == 1