import pytest
from yany.viaje import Viaje
from yany.viajeNormal import ViajeNormal
from yany.pasajera import Pasajera
from yany.pasajeraPremium import PasajeraPremium
from yany.conductora import Conductora

def crear_viaje_normal(pasajera=None):
    if pasajera is None:
        pasajera = Pasajera(1, "Ana", "3001234567", "3009876543")
    conductora = Conductora(2, "Sara", "3111111111", True, True)
    return ViajeNormal(1, pasajera, conductora, "Centro", "Poblado")

def test_viaje_normal_es_un_viaje():
    v = crear_viaje_normal()
    assert isinstance(v, Viaje)

def test_estado_inicial_es_solicitado():
    v = crear_viaje_normal()
    assert v.estado == "Solicitado"

def test_tarifa_pasajera_normal():
    #8000 MENOS EL 2% DE DESCUENTO (160) = 7840
    v = crear_viaje_normal()
    assert v.calcular_tarifa() == pytest.approx(7840)

def test_tarifa_pasajera_premium():
    #8000 MENOS EL 5% DE DESCUENTO (400) = 7600
    premium = PasajeraPremium(1, "Ana", "3001234567", "3009876543")
    v = crear_viaje_normal(premium)
    assert v.calcular_tarifa() == pytest.approx(7600)

def test_mostrar_info_contiene_origen_y_destino():
    v = crear_viaje_normal()
    assert "Centro" in v.mostrar_info()
    assert "Poblado" in v.mostrar_info()