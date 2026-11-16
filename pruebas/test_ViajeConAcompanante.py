import pytest
from yany.ViajeConAcompanante import ViajeConAcompanante
from yany.viaje import Viaje
from yany.pasajera import Pasajera
from yany.conductora import Conductora

def crear_viaje(num=0, mascota=False):
    pasajera = Pasajera(1, "Ana", "3001234567", "3009876543")
    conductora = Conductora(2, "Sara", "3111111111", True, True)
    return ViajeConAcompanante(5, pasajera, conductora, "Centro", "Poblado", num, mascota)

def test_es_un_viaje():
    assert isinstance(crear_viaje(), Viaje)

def test_crear_viaje_con_acompanante():
    v = crear_viaje(2, True)
    assert v.num_acompanantes == 2
    assert v.lleva_mascota is True
    assert v.estado == "Solicitado"

def test_tarifa_sin_recargos_es_la_normal():
    assert crear_viaje().calcular_tarifa() == pytest.approx(7840)

def test_tarifa_con_acompanantes():
    assert crear_viaje(2).calcular_tarifa() == pytest.approx(7840 + 4000)

def test_tarifa_con_mascota():
    assert crear_viaje(0, True).calcular_tarifa() == pytest.approx(7840 + 1500)

def test_tarifa_con_acompanantes_y_mascota():
    assert crear_viaje(2, True).calcular_tarifa() == pytest.approx(7840 + 4000 + 1500)

def test_acompanantes_negativos_falla():
    with pytest.raises(ValueError):
        crear_viaje(-1)

def test_acompanantes_no_entero_falla():
    with pytest.raises(ValueError):
        crear_viaje("dos")

def test_mascota_no_booleana_falla():
    with pytest.raises(ValueError):
        crear_viaje(0, "si")

def test_mostrar_info_contiene_acompanantes_y_mascota():
    info = crear_viaje(1, True).mostrar_info()
    assert "Centro" in info
    assert "acompañantes: 1" in info
    assert "con mascota" in info