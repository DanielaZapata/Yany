import pytest
from yany.alerta import Alerta
from yany.viaje import Viaje
from yany.pasajera import Pasajera
from yany.conductora import Conductora

def crear_alerta(tipo="Emergencia", hora="10:30"):
    pasajera = Pasajera(1, "Ana", "3001234567", "3009876543")
    conductora = Conductora(2, "Sara", "3111111111", True, True)
    viaje = Viaje(5, pasajera, conductora, "Centro", "Poblado")
    return Alerta(1, viaje, tipo, hora)

def test_crear_alerta():
    a = crear_alerta()
    assert a.id == 1
    assert a.tipo == "Emergencia"
    assert a.hora == "10:30"
    assert a.viaje.id == 5

def test_alerta_empieza_sin_atender():
    a = crear_alerta()
    assert a.atendida is False

def test_atender_marca_como_atendida():
    a = crear_alerta()
    a.atender()
    assert a.atendida is True

def test_atender_dos_veces_lanza_error():
    a = crear_alerta()
    a.atender()
    with pytest.raises(ValueError):
        a.atender()

def test_tipo_invalido_lanza_error():
    with pytest.raises(ValueError):
        crear_alerta(tipo="otro")

def test_hora_vacia_lanza_error():
    with pytest.raises(ValueError):
        crear_alerta(hora="  ")

def test_id_no_se_puede_cambiar():
    a = crear_alerta()
    with pytest.raises(AttributeError):
        a.id = 2

def test_mostrar_info_contiene_tipo_y_estado():
    a = crear_alerta()
    assert "Emergencia" in a.mostrar_info()
    assert "pendiente" in a.mostrar_info()
    a.atender()
    assert "atendida" in a.mostrar_info()