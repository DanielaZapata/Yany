from estructuras.arbol import Arbol
from gestores.gestor_archivos import GestorArchivos
from yany.zona import Zona

fallos = []


# muestra OK o FALLO segun se cumpla la condicion
def comprobar(descripcion, condicion):
    if condicion:
        print("OK     ", descripcion)
    else:
        print("FALLO  ", descripcion)
        fallos.append(descripcion)


archivos = GestorArchivos("datos_prueba_zonas")

print("--- 1. Armar el arbol ---")
arbol = Arbol()
zonas = [(4, "Centro"), (2, "Norte"), (6, "Sur"), (1, "Oriente"),
         (3, "Occidente"), (5, "Aeropuerto"), (7, "Terminal")]
for id, nombre in zonas:
    arbol.insertar(Zona(id, nombre))
comprobar("buscar la zona 3 en el arbol", arbol.buscar(3).nombre == "Occidente")
comprobar("buscar una zona que no existe devuelve None", arbol.buscar(99) is None)

print("--- 2. Guardar y cargar ---")
archivos.guardar_zonas(arbol)
cargado = archivos.cargar_zonas()
comprobar("las 7 zonas se cargaron ordenadas por id",
          [z.id for z in cargado.inorden()] == [1, 2, 3, 4, 5, 6, 7])
comprobar("los nombres se conservaron",
          all(cargado.buscar(id).nombre == nombre for id, nombre in zonas))
comprobar("el arbol conserva su forma",
          [z.id for z in cargado.preorden()] == [z.id for z in arbol.preorden()])

print("--- 3. Cargar sin archivo ---")
vacio = GestorArchivos("datos_prueba_zonas_vacia").cargar_zonas()
comprobar("sin archivo se obtiene un arbol vacio", vacio.raiz is None)

print()
if fallos:
    print("Fallaron", len(fallos), "comprobaciones:")
    for f in fallos:
        print(" -", f)
else:
    print("Todo OK: no hubo ningun FALLO.")