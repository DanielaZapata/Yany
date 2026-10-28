import pytest
from yany.pasajera import Pasajera

def test_leer_contacto_emergencia():
    p = Pasajera(1011, "jime", "3148445544", "3000000000")
    assert p.contacto_emergencia == "3000000000"

def test_mostrar_info_contiene_contacto():
    p = Pasajera(1011, "jime", "3148445544", "3000000000")
    texto = p.mostrar_info()
    assert "3000000000" in texto

def test_calcular_descuento_pasajera():
    p = Pasajera(1011, "jime", "3148445544", "3000000000")
    # Para un viaje de $20.000 COP, el 2% de descuento son $400 COP
    assert p.calcular_descuento(20000.0) == 400.0

def test_contacto_emergencia_vacio():
    with pytest.raises(ValueError):
        Pasajera(1011, "jime", "3148445544", "")