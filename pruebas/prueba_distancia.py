import pytest
from yany.viaje import Viaje
from yany.viajeNormal import ViajeNormal
from yany.ViajeConAcompanante import ViajeConAcompanante
from yany.pasajera import Pasajera
from yany.pasajeraPremium import PasajeraPremium
from yany.conductora import Conductora

def conductora():
    return Conductora(2, "Sara", "3111111111", True, True)

def normal():
    return Pasajera(1, "Ana", "3001234567", "3009876543")

def premium():
    return PasajeraPremium(3, "Luisa", "3001112233", "3009876543")

def test_sin_distancia_la_tarifa_es_la_base():
    v = ViajeNormal(1, normal(), conductora(), "Centro", "Poblado")
    assert v.calcular_tarifa() == pytest.approx(7840)

def test_la_distancia_suma_el_valor_por_km():
    v = ViajeNormal(1, normal(), conductora(), "Centro", "Poblado", distancia_km=10)
    assert v.calcular_tarifa() == pytest.approx((8000 + 10 * 1900) * 0.98)

def test_premium_tiene_mas_descuento_con_distancia():
    v = ViajeNormal(1, premium(), conductora(), "Centro", "Poblado", distancia_km=10)
    assert v.calcular_tarifa() == pytest.approx((8000 + 10 * 1900) * 0.95)

def test_con_acompanantes_y_mascota_se_suman_los_recargos():
    v = ViajeConAcompanante(1, normal(), conductora(), "Centro", "Poblado", 2, True, "Solicitado", 10)
    assert v.calcular_tarifa() == pytest.approx((8000 + 10 * 1900) * 0.98 + 2 * 2000 + 1500)

def test_distancia_negativa_lanza_error():
    with pytest.raises(ValueError):
        ViajeNormal(1, normal(), conductora(), "Centro", "Poblado", distancia_km=-1)

def test_distancia_no_numerica_lanza_error():
    with pytest.raises(ValueError):
        ViajeNormal(1, normal(), conductora(), "Centro", "Poblado", distancia_km="diez")

def test_la_distancia_se_puede_leer():
    v = ViajeNormal(1, normal(), conductora(), "Centro", "Poblado", distancia_km=4.5)
    assert v.distancia_km == 4.5