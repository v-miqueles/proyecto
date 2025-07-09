# modelos.py
import json
import os
from datetime import datetime

ARCHIVO_AUTOS = "autos.json"
ARCHIVO_HISTORIAL = "historial.json"

class Auto:
    def __init__(self, marca, modelo, anio, patente, falla):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.patente = patente.upper()
        self.falla = falla
        self.procedimiento = ""
        self.fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.fecha_salida = None
        self.reparado = False
        self.costo = 0

    def marcar_como_reparado(self, procedimiento, costo):
        self.procedimiento = procedimiento
        self.costo = costo
        self.reparado = True
        self.fecha_salida = datetime.now().strftime("%Y-%m-%d %H:%M")

    def a_dict(self):
        return self.__dict__

    @staticmethod
    def desde_dict(datos):
        auto = Auto(datos['marca'], datos['modelo'], datos['anio'], datos['patente'], datos['falla'])
        auto.procedimiento = datos.get('procedimiento', '')
        auto.fecha_ingreso = datos.get('fecha_ingreso')
        auto.fecha_salida = datos.get('fecha_salida')
        auto.reparado = datos.get('reparado', False)
        auto.costo = datos.get('costo', 0)
        return auto

class Taller:
    def __init__(self, capacidad, archivo_autos=ARCHIVO_AUTOS):
        self.capacidad = capacidad
        self.archivo_autos = archivo_autos
        self.autos = self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo_autos):
            with open(self.archivo_autos, 'r') as f:
                return [Auto.desde_dict(a) for a in json.load(f)]
        return []

    def guardar(self):
        with open(self.archivo_autos, 'w') as f:
            json.dump([a.a_dict() for a in self.autos], f, indent=4)

    def ingresar_auto(self, auto):
        if len(self.autos) >= self.capacidad:
            return False
        self.autos.append(auto)
        self.guardar()
        return True

    def listar_autos(self):
        return self.autos

    def despachar_auto(self, indice, procedimiento, costo):
        if 0 <= indice < len(self.autos):
            auto = self.autos[indice]
            auto.marcar_como_reparado(procedimiento, costo)
            auto_despachado = self.autos.pop(indice)
            self.guardar()
            return auto_despachado
        return None

class Historial:
    def __init__(self, archivo_historial=ARCHIVO_HISTORIAL):
        self.archivo_historial = archivo_historial
        self.autos = self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo_historial):
            with open(self.archivo_historial, 'r') as f:
                return [Auto.desde_dict(a) for a in json.load(f)]
        return []

    def guardar(self):
        with open(self.archivo_historial, 'w') as f:
            json.dump([a.a_dict() for a in self.autos], f, indent=4)

    def agregar(self, auto):
        self.autos.append(auto)
        self.guardar()

    def buscar_por_patente(self, patente):
        return [a for a in self.autos if a.patente == patente.upper()]

    def listar(self):
        return self.autos

    def calcular_ganancias(self):
        return sum(a.costo for a in self.autos)
