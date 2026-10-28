import pytest
from yany.pasajeraPremium import PasajeraPremium

def test_leer_porcentaje_descuento():
    pp = PasajeraPremium(1012, "ana", "3001234567", "3000000000", 0.05)
    assert pp.porcentaje_descuento == 0.05

def test_calcular_descuento_premium():
    #CON UN 5% (0.05) DE DESCUENTO DE UN VIAJE DE $20.000 COP, EL DESCUENTO DEBE SER DE $1.000 COP
    pp = PasajeraPremium(1012, "ana", "3001234567", "3000000000", 0.05)
    assert pp.calcular_descuento(20000.0) == pytest.approx(1000.0)

def test_mostrar_info_contiene_porcentaje():
    pp = PasajeraPremium(1012, "ana", "3001234567", "3000000000", 0.05)
    texto = pp.mostrar_info()
    assert "0.05" in texto

def test_porcentaje_descuento_negativo():
    with pytest.raises(ValueError):
        PasajeraPremium(1012, "ana", "3001234567", "3000000000", -0.05)

def test_porcentaje_descuento_mayor_a_uno():
    with pytest.raises(ValueError):
        PasajeraPremium(1012, "ana", "3001234567", "3000000000", 1.5)

def test_porcentaje_por_defecto():
    pp = PasajeraPremium(1012, "ana", "3001234567", "3000000000")
    assert pp.porcentaje_descuento == 0.05