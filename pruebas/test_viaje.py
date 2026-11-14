import pytest
from yany.viaje import Viaje
from yany.pasajera import Pasajera
from yany.pasajeraPremium import PasajeraPremium
from yany.conductora import Conductora

def crear_viaje(pasajera=None):
    if pasajera is None:
        pasajera = Pasajera(1, "Ana", "3001234567", "3009876543")
    conductora = Conductora(2, "Sara", "3111111111", True, True)
    return Viaje(1, pasajera, conductora, "Centro", "Poblado")

def test_crear_viaje():
    v = crear_viaje()
    assert v.id == 1
    assert v.origen == "Centro"
    assert v.destino == "Poblado"

def test_estado_inicial_es_solicitado():
    v = crear_viaje()
    assert v.estado == "Solicitado"

def test_origen_vacio_lanza_error():
    pasajera = Pasajera(1, "Ana", "3001234567", "3009876543")
    conductora = Conductora(2, "Sara", "3111111111", True, True)
    with pytest.raises(ValueError):
        Viaje(1, pasajera, conductora, "  ", "Poblado")

def test_destino_vacio_lanza_error():
    pasajera = Pasajera(1, "Ana", "3001234567", "3009876543")
    conductora = Conductora(2, "Sara", "3111111111", True, True)
    with pytest.raises(ValueError):
        Viaje(1, pasajera, conductora, "Centro", "")

def test_estado_invalido_lanza_error():
    pasajera = Pasajera(1, "Ana", "3001234567", "3009876543")
    conductora = Conductora(2, "Sara", "3111111111", True, True)
    with pytest.raises(ValueError):
        Viaje(1, pasajera, conductora, "Centro", "Poblado", "volando")

def test_cambiar_estado():
    v = crear_viaje()
    v.cambiar_estado("En_curso")
    assert v.estado == "En_curso"

def test_cambiar_a_estado_invalido_lanza_error():
    v = crear_viaje()
    with pytest.raises(ValueError):
        v.cambiar_estado("otro")

def test_viaje_finalizado_no_se_puede_cambiar():
    v = crear_viaje()
    v.cambiar_estado("Finalizado")
    with pytest.raises(ValueError):
        v.cambiar_estado("En_curso")

def test_tarifa_pasajera_normal():
    #8000 MENOS EL 2% DE DESCUENTO (160) = 7840
    v = crear_viaje()
    assert v.calcular_tarifa() == pytest.approx(7840)

def test_tarifa_pasajera_premium():
    #8000 MENOS EL 5% DE DESCUENTO (400) = 7600
    premium = PasajeraPremium(1, "Ana", "3001234567", "3009876543")
    v = crear_viaje(premium)
    assert v.calcular_tarifa() == pytest.approx(7600)

def test_mostrar_info_contiene_origen_y_destino():
    v = crear_viaje()
    assert "Centro" in v.mostrar_info()
    assert "Poblado" in v.mostrar_info()