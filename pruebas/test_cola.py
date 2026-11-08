from estructuras.cola import Cola

def test_cola_vacia():
    cola = Cola()
    assert cola.esta_vacia() is True
    assert cola.tamano == 0

def test_agregar():
    cola = Cola()
    cola.agregar_cola("Laura")
    cola.agregar_cola("Camila")
    assert cola.mostrar() == ["Laura", "Camila"]
    assert cola.tamano == 2

def test_sacar():
    cola = Cola()
    cola.agregar_cola("Laura")
    cola.agregar_cola("Camila")
    dato = cola.sacar_cola()
    assert dato == "Laura"
    assert cola.mostrar() == ["Camila"]
    assert cola.tamano == 1

def test_ver_frente():
    cola = Cola()
    cola.agregar_cola("Laura")
    cola.agregar_cola("Camila")
    assert cola.ver_frente() == "Laura"