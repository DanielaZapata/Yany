import pytest
from yany.vehiculo import Vehiculo

def test_crear_vehiculo():

    v = Vehiculo("ABC123", "Rojo", 2020, [])
    assert v.placa == "ABC123"
    assert v.color == "Rojo"
    assert v.anio == 2020
    assert v.mantenimientos == []

def test_obtener_placa():

    v = Vehiculo("ABC123", "Rojo", 2020)
    assert v.placa == "ABC123"

def test_obtener_color():
    v = Vehiculo("ABC123", "Rojo", 2020)
    assert v.color == "Rojo"

def test_obtener_anio():
    v = Vehiculo("ABC123", "Rojo", 2020)
    assert v.anio == 2020

def test_obtener_mantenimientos():
    v = Vehiculo("ABC123", "Rojo", 2020, ["Cambio de aceite"])
    assert v.mantenimientos == ["Cambio de aceite"]

def test_registrar_mantenimiento():
    v = Vehiculo("ABC123", "Rojo", 2020, [])
    v.registrar_mantenimiento("Cambio de aceite")
    assert "Cambio de aceite" in v.mantenimientos

def test_registrar_varios_mantenimientos():
    v = Vehiculo("ABC123", "Rojo", 2020, [])
    v.registrar_mantenimiento("Cambio de aceite")
    v.registrar_mantenimiento("Revisión de frenos")
    assert len(v.mantenimientos) == 2
    assert v.mantenimientos == ["Cambio de aceite", "Revisión de frenos"]

