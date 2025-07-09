# -*- coding: utf-8 -*-
import json

import os
from tabulate import tabulate
from datetime import datetime
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

ARCHIVO_AUTOS = "autos.json"
ARCHIVO_HISTORIAL = "historial.json"
MAX_AUTOS = 10

def encabezado(titulo):
    print("\n" + "=" * 50)
    print(f"\U0001F697 {titulo.center(40)} \U0001F697")
    print("=" * 50 + "\n")

def cargar_archivo(nombre):
    if os.path.exists(nombre):
        with open(nombre, "r") as f:
            return json.load(f)
    return []

def guardar_archivo(nombre, datos):
    with open(nombre, "w") as f:
        json.dump(datos, f, indent=4)


autos = cargar_archivo(ARCHIVO_AUTOS)
historial = cargar_archivo(ARCHIVO_HISTORIAL)

def mostrar_menu():
    print("\n" + "=" * 50)
    print(Fore.MAGENTA + "      🛠️  TALLER MECÁNICO - MENÚ PRINCIPAL  🛠️")
    print("=" * 50)
    print("1️⃣  Ingresar auto")
    print("2️⃣  Ver autos en el taller")
    print("3️⃣  Despachar auto")
    print("4️⃣  Historial")
    print("5️⃣  🚪 Salir del sistema")
    print("=" * 50)
    return input("👉 Selecciona una opción (1-5): ").strip()

def submenu_historial():
    while True:
        encabezado("📜 Historial del Taller")
        print("1️⃣  🔍 Buscar auto por patente")
        print("2️⃣  📚 Ver historial completo")
        print("3️⃣  💰 Ver ganancias del taller")
        print("4️⃣  🔙 Volver al menú principal")
        print("=" * 50)
        opcion = input("👉 Selecciona una opción (1-4): ").strip()
        if opcion == '1':
            encabezado("🔎 Buscar por Patente")
            buscar_por_patente()
        elif opcion == '2':
            encabezado("📋 Historial de Autos")
            ver_historial()
        elif opcion == '3':
            encabezado("💵 Ganancias del Taller")
            ver_ganancias()
        elif opcion == '4':
            print(Fore.CYAN + "🔙 Volviendo al menú principal...\n")
            break
        else:
            print(Fore.RED + "❌ Opción inválida. Por favor, intenta nuevamente.\n")

def ingresar_auto():
    encabezado("🆕 Ingreso de Auto")
    if len(autos) >= MAX_AUTOS:
        print(Fore.YELLOW + "⚠️ Capacidad máxima del taller alcanzada. No se pueden ingresar más autos.\n")
        return
    marca = input("Marca del auto: ").strip()
    modelo = input("Modelo del auto: ").strip()
    while True:
        try:
            anio = int(input("Año del auto: ").strip())
            if 1886 <= anio <= datetime.now().year:
                break
            else:
                print(Fore.YELLOW + f"⚠️ Ingresa un año válido entre 1886 y {datetime.now().year}.")
        except ValueError:
            print(Fore.RED + "❌ Por favor, ingresa un número válido para el año.")
    patente = input("Patente del auto: ").strip().upper()
    falla = input("Falla reportada: ").strip()
    ingreso = datetime.now().strftime("%Y-%m-%d %H:%M")
    auto = {
        "marca": marca,
        "modelo": modelo,
        "anio": anio,
        "patente": patente,
        "falla": falla,
        "procedimiento": "",
        "fecha_ingreso": ingreso,
        "reparado": False,
        "costo": 0
    }
    autos.append(auto)
    guardar_archivo(ARCHIVO_AUTOS, autos)
    print(Fore.GREEN + "✅ Auto ingresado correctamente.\n")

def ver_autos():
    encabezado("🚗 Autos en el Taller")
    if not autos:
        print(Fore.YELLOW + "ℹ️ No hay autos en el taller actualmente.\n")
        return
    tabla = []
    for i, auto in enumerate(autos, 1):
        estado = "✅ Listo" if auto["reparado"] else "En reparación"
        tabla.append([
            i, auto["marca"], auto["modelo"], auto["anio"],
            auto["patente"], auto["falla"], auto["procedimiento"] or "Pendiente", estado
        ])
    print(tabulate(tabla, headers=["#", "Marca", "Modelo", "Año", "Patente", "Falla", "Procedimiento", "Estado"], tablefmt="fancy_grid"))
    print(f"\nTotal de autos en taller: {len(autos)} / {MAX_AUTOS}\n")

def despachar_auto():
    ver_autos()
    if not autos:
        return
    try:
        indice = int(input("Selecciona el número del auto a despachar: ").strip()) - 1
        if 0 <= indice < len(autos):
            auto = autos[indice]
            procedimiento = input("Describe el procedimiento realizado: ").strip()
            while True:
                try:
                    costo = int(input("Costo de la reparación (en CLP): ").strip())
                    break
                except ValueError:
                    print(Fore.RED + "❌ Por favor, ingresa un número válido para el costo.")
            auto["procedimiento"] = procedimiento
            auto["reparado"] = True
            auto["costo"] = costo
            auto["fecha_salida"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            historial.append(auto)
            del autos[indice]
            guardar_archivo(ARCHIVO_AUTOS, autos)
            guardar_archivo(ARCHIVO_HISTORIAL, historial)
            print(Fore.GREEN + "✅ Auto despachado\n")
            print(Fore.CYAN + "📂 Datos guardados correctamente.\n")
        else:
            print(Fore.YELLOW + "⚠️ Número seleccionado no corresponde a ningún auto.\n")
    except ValueError:
        print(Fore.RED + "❌ Entrada inválida. Debes ingresar un número.\n")

def buscar_por_patente():
    consulta = input("Ingresa la patente a buscar: ").strip().upper()
    encontrados = [a for a in autos if a["patente"] == consulta]
    encontrados += [h for h in historial if h["patente"] == consulta]
    
    if not encontrados:
        print(Fore.YELLOW + f"ℹ️ No se encontraron autos con la patente '{consulta}'.\n")
        return

    tabla = []
    for auto in encontrados:
        tabla.append([
            auto.get("marca", ""),
            auto.get("modelo", ""),
            auto.get("anio", ""),
            auto.get("patente", ""),
            auto.get("falla", ""),
            auto.get("procedimiento", "Pendiente"),
            "✅ Listo" if auto.get("reparado", False) else "En reparación",
            f"${auto.get('costo', 0):,} CLP"
        ])

    headers = ["Marca", "Modelo", "Año", "Patente", "Falla", "Procedimiento", "Estado", "Costo"]
    print("\n" + "-"*50)
    print(Fore.CYAN + f"🔍 Resultados para patente: {consulta}\n" + Style.RESET_ALL)
    print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
    print("")

def ver_historial():
    if not historial:
        print(Fore.YELLOW + "ℹ️ No hay autos en el historial.\n")
        return
    tabla = []
    for i, auto in enumerate(historial, 1):
        tabla.append([
            i, auto["marca"], auto["modelo"], auto["anio"],
            auto["patente"], auto["falla"], auto["procedimiento"], f"${auto.get('costo', 0):,} CLP"
        ])
    print(tabulate(tabla, headers=["#", "Marca", "Modelo", "Año", "Patente", "Falla", "Procedimiento", "Costo"], tablefmt="fancy_grid"))
    print("")

def ver_ganancias():
    total = sum(auto.get("costo", 0) for auto in historial)
    print(Fore.GREEN + f"💰 Ganancia total acumulada del taller: ${total:,} CLP\n")

def borrar_todos_los_datos():
    encabezado("🗑️ Borrar Todos los Datos")
    confirmacion = input(Fore.RED + "⚠️ ¿Estás seguro que quieres borrar *todos* los datos? (sí/no): ").strip().lower()
    if confirmacion == "sí":
        guardar_archivo(ARCHIVO_AUTOS, [])
        guardar_archivo(ARCHIVO_HISTORIAL, [])
        autos.clear()
        historial.clear()
        print(Fore.RED + "🗑️ Todos los datos han sido borrados permanentemente.\n")
    else:
        print(Fore.CYAN + "❌ Operación cancelada. No se borraron los datos.\n")

def despedida():
    print("\n" + "=" * 50)
    print(Fore.GREEN + "👋 Gracias por usar el sistema del Taller Mecánico")
    print(Fore.GREEN + "      ¡Que tengas un excelente día! 🚗🛠️")
    print("=" * 50 + "\n")

# Ciclo principal del programa
while True:
    opcion = mostrar_menu()
    if opcion == '1':
        ingresar_auto()
    elif opcion == '2':
        ver_autos()
    elif opcion == '3':
        encabezado("🚚 Despachar Auto")
        despachar_auto()
    elif opcion == '4':
        submenu_historial()
    elif opcion == '5':
        despedida()
        break
    elif opcion == '00':
        borrar_todos_los_datos()
    else:
        print(Fore.RED + "❌ Opción inválida. Por favor, intenta nuevamente.\n")
        
