import pytest
from yany.resena import Resena


def test_crear_resena_valida():
    r = Resena(1, 5, "Muy buen servicio")
    assert r.id == 1
    assert r.calificacion == 5
    assert r.comentario == "Muy buen servicio"


def test_calificacion_cero_lanza_error():
    with pytest.raises(ValueError):
        Resena(1, 0, "Mala")


def test_calificacion_mayor_a_cinco_lanza_error():
    with pytest.raises(ValueError):
        Resena(1, 6, "Excelente")


def test_calificacion_no_entera_lanza_error():
    with pytest.raises(ValueError):
        Resena(1, 4.5, "Buena")


def test_mostrar_info_contiene_comentario():
    r = Resena(1, 4, "Conductora amable")
    assert "Conductora amable" in r.mostrar_info()
    assert "4" in r.mostrar_info()


def test_cambiar_calificacion_invalida_lanza_error():
    r = Resena(1, 3, "Normal")
    with pytest.raises(ValueError):
        r.calificacion = 10