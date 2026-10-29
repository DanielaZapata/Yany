import pytest
from yany.persona import Persona 

def test_leer_nombre():
    p = Persona(1011, "jime", "3148445554")
    assert p.nombre == "jime"

def test_mostrar_info_contiene_nombre():
    p = Persona(1011, "jime", "3148445554")
    texto = p.mostrar_info()
    assert "jime" in texto

def test_nombre_vacio():
    with pytest.raises(ValueError):
         Persona(1011, "", "3148445554")