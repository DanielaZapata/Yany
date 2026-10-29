import pytest
from yany.conductora import Conductora

#CLASE FALSA SOLO PARA PROBAR EL PROMEDIO, MIENTRAS NO EXISTA RESEÑA 
class ResenaFalsa:
    def __init__(self, calificacion):
        self.calificacion = calificacion

def test_crear_conductora():
    c = Conductora(1, "Ana", "3001234567", True, True)
    assert c.nombre == "Ana"
    assert c.certificada is True

def test_resenas_empieza_vacia():
    c = Conductora(1, "Ana", "3001234567", True, True)
    assert len(c.resenas) == 0

def test_mostrar_info_contiene_nombre():
    c = Conductora(1, "Ana", "3001234567", True, True)
    assert "Ana" in c.mostrar_info()

def test_certificada_no_booleana_falla():
    with pytest.raises(ValueError):
        Conductora(1, "Ana", "3001234567", "si", True)

def test_promedio_sin_resenas():
    c = Conductora(1, "Ana", "3001234567", True, True)
    assert c.calificacion_promedio() == 0.0

def test_promedio_con_resenas():
    c = Conductora(1, "Ana", "3001234567", True, True)
    c.agregar_resena(ResenaFalsa(4))
    c.agregar_resena(ResenaFalsa(5))
    #EL PROMEDIO ENTRE 4 Y 5 ES 4.5
    assert c.calificacion_promedio() == pytest.approx(4.5)