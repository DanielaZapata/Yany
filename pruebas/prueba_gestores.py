# prueba_completa.py
# Prueba de punta a punta del GestorYANY con las clases reales
#
# OJO: esta prueba guarda en la carpeta datos los archivos pasajeras.json,
# conductoras.json y viajes.json, y reemplaza lo que ya tengan adentro.
#
# Ejecutar desde la carpeta Yany con:  python -m pruebas.prueba_completa

import os

from gestores.gestor_yany import GestorYANY
from yany.pasajera import Pasajera
from yany.conductora import Conductora
from yany.vehiculo import Vehiculo
from yany.resena import Resena
from yany.viaje import Viaje

fallos = []


# muestra OK o FALLO segun se cumpla la condicion
def comprobar(descripcion, condicion):
    if condicion:
        print("OK     ", descripcion)
    else:
        print("FALLO  ", descripcion)
        fallos.append(descripcion)


gestor = GestorYANY()

print("--- 1. Registrar ---")
ana = Pasajera(1, "Ana", "3001112233", "Maria 3004445566")
sofia = Pasajera(2, "Sofia", "3007778899", "Laura 3001230000")
laura = Conductora(10, "Laura", "3002223344", True, True,
                   Vehiculo("ABC123", "rojo", 2020),
                   [Resena(1, 5, "muy buen servicio")])
sara = Conductora(11, "Sara", "3005556677", True, True)

comprobar("registrar a Ana", gestor.registrar_pasajera(ana) is True)
comprobar("registrar a Sofia", gestor.registrar_pasajera(sofia) is True)
comprobar("Ana repetida no se registra", gestor.registrar_pasajera(ana) is False)
comprobar("registrar a Laura", gestor.registrar_conductora(laura) is True)
comprobar("registrar a Sara", gestor.registrar_conductora(sara) is True)
comprobar("Laura repetida no se registra", gestor.registrar_conductora(laura) is False)

print("--- 2. Solicitar y asignar viajes ---")
viaje1 = Viaje(100, ana, None, "Centro", "Poblado")
viaje2 = Viaje(101, sofia, None, "Laureles", "Envigado")
viaje3 = Viaje(102, ana, None, "Belen", "Centro")
for v in (viaje1, viaje2, viaje3):
    comprobar("solicitar el viaje " + str(v.id), gestor.solicitar_viaje(v) is True)

comprobar("hay 2 conductoras, se asignan 2 viajes", gestor.asignar_viajes() == 2)
comprobar("el viaje 100 quedo con Laura", viaje1.conductora is laura)
comprobar("el viaje 101 quedo con Sara", viaje2.conductora is sara)
comprobar("los viajes asignados estan En_curso",
          viaje1.estado == "En_curso" and viaje2.estado == "En_curso")
comprobar("el viaje 102 sigue esperando",
          viaje3.conductora is None and viaje3.estado == "Solicitado")
comprobar("Laura y Sara quedaron ocupadas",
          laura.disponible is False and sara.disponible is False)
comprobar("la tarifa con 2% de descuento es 7840", viaje1.calcular_tarifa() == 7840)

print("--- 3. Alertas ---")
alerta1 = gestor.activar_alerta(100, "Emergencia")
alerta2 = gestor.activar_alerta(101, "Acoso")
comprobar("alerta de un viaje que no existe devuelve None",
          gestor.activar_alerta(999, "Emergencia") is None)
comprobar("las alertas tienen id 1 y 2", alerta1.id == 1 and alerta2.id == 2)
try:
    gestor.activar_alerta(100, "Inventada")
    comprobar("un tipo invalido da error", False)
except ValueError:
    comprobar("un tipo invalido da error", True)

comprobar("se atiende primero la alerta mas antigua",
          gestor.atender_alerta() is alerta1 and alerta1.atendida is True)
comprobar("la segunda alerta sigue pendiente", alerta2.atendida is False)
comprobar("se atiende la segunda alerta", gestor.atender_alerta() is alerta2)
comprobar("sin alertas devuelve None", gestor.atender_alerta() is None)

print("--- 4. Finalizar viaje ---")
comprobar("finalizar un viaje que no existe devuelve False",
          gestor.finalizar_viaje(999) is False)
comprobar("finalizar el viaje 100", gestor.finalizar_viaje(100) is True)
comprobar("el viaje quedo Finalizado y Laura libre",
          viaje1.estado == "Finalizado" and laura.disponible is True)
try:
    gestor.finalizar_viaje(100)
    comprobar("finalizar dos veces el mismo viaje da error", False)
except ValueError:
    comprobar("finalizar dos veces el mismo viaje da error", True)
comprobar("con Laura libre se asigna el viaje 102",
          gestor.asignar_viajes() == 1 and viaje3.conductora is laura)

print("--- 5. Guardar ---")
gestor.guardar_todo()
for nombre in ("pasajeras.json", "conductoras.json", "viajes.json"):
    comprobar("existe datos/" + nombre,
              os.path.exists(os.path.join("datos", nombre)))

print("--- 6. Cargar en un gestor nuevo ---")
nuevo = GestorYANY()
nuevo.cargar_todo()
comprobar("Ana ya estaba cargada",
          nuevo.registrar_pasajera(Pasajera(1, "Ana", "3001112233", "Maria 3004445566")) is False)
comprobar("Laura ya estaba cargada",
          nuevo.registrar_conductora(Conductora(10, "Laura", "3002223344", True, True)) is False)
comprobar("el viaje 101 se cargo y se puede finalizar",
          nuevo.finalizar_viaje(101) is True)
comprobar("el viaje 102 se cargo y se puede finalizar",
          nuevo.finalizar_viaje(102) is True)
try:
    nuevo.finalizar_viaje(100)
    comprobar("el viaje 100 se cargo como Finalizado", False)
except ValueError:
    comprobar("el viaje 100 se cargo como Finalizado", True)

# las conductoras cargadas quedaron libres al finalizar, asi que reciben un viaje nuevo
nuevo.solicitar_viaje(Viaje(103, ana, None, "Centro", "Envigado"))
comprobar("con las conductoras libres se asigna un viaje nuevo",
          nuevo.asignar_viajes() == 1)

print()
if fallos:
    print("Fallaron", len(fallos), "comprobaciones:")
    for f in fallos:
        print(" -", f)
else:
    print("Todo OK: no hubo ningun FALLO.")