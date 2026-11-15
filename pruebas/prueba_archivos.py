from estructuras.lista import Lista
from gestores.gestor_archivos import GestorArchivos
from yany.pasajera import Pasajera

archivos = GestorArchivos()

# lista con dos pasajeras de prueba
lista = Lista()
lista.agregar(Pasajera(1, "Ana", "3001112233", "Maria 3004445566"))
lista.agregar(Pasajera(2, "Sofia", "3007778899", "Laura 3001230000"))

# se guardan en el json
archivos.guardar_pasajeras(lista)
print("Pasajeras guardadas")

# se cargan otra vez desde el archivo
lista_cargada = archivos.cargar_pasajeras()

# se muestra lo que se cargó
for p in lista_cargada.mostrar():
    print(p.mostrar_info())