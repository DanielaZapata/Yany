import pytest
from yany.mantenimiento import Mantenimiento


def test_crear_mantenimiento():
    m = Mantenimiento("2026-10-30", "Cambio de aceite")
    assert m.fecha == "2026-10-30"
    assert m.descripcion == "Cambio de aceite"


def test_descripcion_vacia_lanza_error():
    with pytest.raises(ValueError):
        Mantenimiento("2026-10-30", "   ")


def test_mostrar_info_contiene_fecha_y_descripcion():
    m = Mantenimiento("2026-10-30", "Cambio de aceite")
    assert "2026-10-30" in m.mostrar_info()
    assert "Cambio de aceite" in m.mostrar_info()


def test_cambiar_fecha_y_descripcion_no_se_pisan():
    m = Mantenimiento("2026-10-30", "Cambio de aceite")
    m.fecha = "2026-11-01"
    assert m.fecha == "2026-11-01"
    assert m.descripcion == "Cambio de aceite"