# Este archivo se encarga de guardar y cargar los datos en archivos JSON

import json
import os
from estructuras.lista import Lista
from yany.pasajera import Pasajera
from yany.conductora import Conductora
from yany.vehiculo import Vehiculo
from yany.resena import Resena
from yany.zona import Zona
from estructuras.arbol import Arbol
from yany.pasajeraPremium import PasajeraPremium
from yany.mantenimiento import Mantenimiento
from yany.viajeNormal import ViajeNormal
from yany.ViajeConAcompanante import ViajeConAcompanante
from yany.excepciones import ArchivoInvalidoError


class GestorArchivos:
    def __init__(self, ruta_datos="datos"):
        self.__ruta_datos = ruta_datos
        # si la carpeta datos no existe, se crea
        os.makedirs(self.__ruta_datos, exist_ok=True)

    # GUARDAR una lista en un archivo json
    def __guardar_json(self, nombre_archivo, datos):
        ruta = os.path.join(self.__ruta_datos, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    # CARGAR un archivo json y devolver lo que tiene adentro
    def __cargar_json(self, nombre_archivo):
        ruta = os.path.join(self.__ruta_datos, nombre_archivo)
        # si el archivo todavia no existe, devuelve una lista vacia
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except json.JSONDecodeError:
            raise ArchivoInvalidoError(f"El archivo '{nombre_archivo}' está dañado o no es válido.")

    # BUSCAR en una lista el objeto que tenga ese id
    def __buscar_por_id(self, lista, id):
        for x in lista.mostrar():
            if x.id == id:
                return x
        return None


    # PASAJERAS
    def guardar_pasajeras(self, lista):
        datos = []
        for p in lista.mostrar():
            if isinstance(p, PasajeraPremium):
                datos.append({"tipo": "premium", "id": p.id, "nombre": p.nombre,
                              "telefono": p.telefono,
                              "contacto_emergencia": p.contacto_emergencia,
                              "porcentaje_descuento": p.porcentaje_descuento})
            else:
                datos.append({"tipo": "normal", "id": p.id, "nombre": p.nombre,
                              "telefono": p.telefono,
                              "contacto_emergencia": p.contacto_emergencia})
        self.__guardar_json("pasajeras.json", datos)

    def cargar_pasajeras(self):
        lista = Lista()
        datos = self.__cargar_json("pasajeras.json")
        for d in datos:
            if d.get("tipo") == "premium":
                pasajera = PasajeraPremium(d["id"], d["nombre"], d["telefono"],
                                           d["contacto_emergencia"], d["porcentaje_descuento"])
            else:
                pasajera = Pasajera(d["id"], d["nombre"], d["telefono"], d["contacto_emergencia"])
            lista.agregar(pasajera)
        return lista


    # CONDUCTORAS
    def guardar_conductoras(self, lista):
        datos = []
        for c in lista.mostrar():
            vehiculo = None
            if c.vehiculo is not None:
                mantenimientos = []
                for m in c.vehiculo.mantenimientos:
                    mantenimientos.append({"fecha": m.fecha,
                                           "descripcion": m.descripcion})

                vehiculo = {"placa": c.vehiculo.placa,
                            "color": c.vehiculo.color,
                            "anio": c.vehiculo.anio,
                            "mantenimientos": mantenimientos}

            resenas = []
            for r in c.resenas:
                resenas.append({"id": r.id,
                                "calificacion": r.calificacion,
                                "comentario": r.comentario})

            datos.append({"id": c.id, "nombre": c.nombre,
                          "telefono": c.telefono,
                          "certificada": c.certificada,
                          "disponible": c.disponible,
                          "vehiculo": vehiculo,
                          "resenas": resenas})
        self.__guardar_json("conductoras.json", datos)

    def cargar_conductoras(self):
        lista = Lista()
        datos = self.__cargar_json("conductoras.json")
        for d in datos:
            vehiculo = None
            if d["vehiculo"] is not None:
                v = d["vehiculo"]
                vehiculo = Vehiculo(v["placa"], v["color"], v["anio"])
                for m in v.get("mantenimientos", []):
                    vehiculo.registrar_mantenimiento(Mantenimiento(m["fecha"], m["descripcion"]))

            resenas = []
            for r in d["resenas"]:
                resenas.append(Resena(r["id"], r["calificacion"],
                                      r["comentario"]))

            conductora = Conductora(d["id"], d["nombre"], d["telefono"],
                                    d["certificada"], d["disponible"],
                                    vehiculo, resenas)
            lista.agregar(conductora)
        return lista


    # VIAJES
    def guardar_viajes(self, lista):
        datos = []
        for v in lista.mostrar():
            # un viaje puede no tener conductora todavia
            conductora_id = None
            if v.conductora is not None:
                conductora_id = v.conductora.id

            if isinstance(v, ViajeConAcompanante):
                datos.append({"tipo": "acompanante", "id": v.id,
                              "pasajera_id": v.pasajera.id,
                              "conductora_id": conductora_id,
                              "origen": v.origen,
                              "destino": v.destino,
                              "estado": v.estado,
                              "num_acompanantes": v.num_acompanantes,
                              "lleva_mascota": v.lleva_mascota})
            else:
                datos.append({"tipo": "normal", "id": v.id,
                              "pasajera_id": v.pasajera.id,
                              "conductora_id": conductora_id,
                              "origen": v.origen,
                              "destino": v.destino,
                              "estado": v.estado})
        self.__guardar_json("viajes.json", datos)

    def cargar_viajes(self, lista_pasajeras, lista_conductoras):
        lista = Lista()
        datos = self.__cargar_json("viajes.json")
        for d in datos:
            # buscar la pasajera y la conductora por su id
            pasajera = self.__buscar_por_id(lista_pasajeras, d["pasajera_id"])
            conductora = None
            if d["conductora_id"] is not None:
                conductora = self.__buscar_por_id(lista_conductoras,
                                                  d["conductora_id"])

            if d.get("tipo") == "acompanante":
                viaje = ViajeConAcompanante(d["id"], pasajera, conductora,
                                            d["origen"], d["destino"],
                                            d["num_acompanantes"], d["lleva_mascota"],
                                            d["estado"])
            else:
                viaje = ViajeNormal(d["id"], pasajera, conductora,
                                    d["origen"], d["destino"], d["estado"])
            lista.agregar(viaje)
        return lista

      # ZONAS
    def guardar_zonas(self, arbol):
        datos = []
        # se recorre en preorden: asi, al cargar, el arbol queda con la misma forma
        for z in arbol.preorden():
            datos.append({"id": z.id, "nombre": z.nombre})
        self.__guardar_json("zonas.json", datos)

    def cargar_zonas(self):
        arbol = Arbol()
        datos = self.__cargar_json("zonas.json")
        for d in datos:
            arbol.insertar(Zona(d["id"], d["nombre"]))
        return arbol

    