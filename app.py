# app.py
from modelos import Auto, Taller, Historial
from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)

MAX_AUTOS = 10

class TallerApp:
    def __init__(self):
        self.taller = Taller(MAX_AUTOS)
        self.historial = Historial()

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu()
            if opcion == '1':
                self.ingresar_auto()
            elif opcion == '2':
                self.ver_autos()
            elif opcion == '3':
                self.despachar_auto()
            elif opcion == '4':
                self.submenu_historial()
            elif opcion == '5':
                self.despedida()
                break
            else:
                print(Fore.RED + "❌ Opción inválida. Intenta nuevamente.")

    def mostrar_menu(self):
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

    def encabezado(self, titulo):
        print("\n" + "=" * 50)
        print(f"\U0001F697 {titulo.center(40)} \U0001F697")
        print("=" * 50 + "\n")

    def ingresar_auto(self):
        self.encabezado("🆕 Ingreso de Auto")
        if len(self.taller.autos) >= MAX_AUTOS:
            print(Fore.YELLOW + "⚠️ Capacidad máxima alcanzada.")
            return
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        try:
            anio = int(input("Año: "))
        except ValueError:
            print(Fore.RED + "❌ Año inválido.")
            return
        patente = input("Patente: ")
        falla = input("Falla reportada: ")
        auto = Auto(marca, modelo, anio, patente, falla)
        if self.taller.ingresar_auto(auto):
            print(Fore.GREEN + "✅ Auto ingresado correctamente.")
        else:
            print(Fore.RED + "❌ No se pudo ingresar el auto.")

    def ver_autos(self):
        self.encabezado("🚗 Autos en el Taller")
        autos = self.taller.listar_autos()
        if not autos:
            print(Fore.YELLOW + "ℹ️ No hay autos en el taller.")
            return
        tabla = []
        for i, a in enumerate(autos, 1):
            estado = "✅ Listo" if a.reparado else "En reparación"
            tabla.append([i, a.marca, a.modelo, a.anio, a.patente, a.falla, a.procedimiento or "Pendiente", estado])
        print(tabulate(tabla, headers=["#", "Marca", "Modelo", "Año", "Patente", "Falla", "Procedimiento", "Estado"], tablefmt="fancy_grid"))

    def despachar_auto(self):
        self.encabezado("🚚 Despachar Auto")
        autos = self.taller.listar_autos()
        if not autos:
            print(Fore.YELLOW + "ℹ️ No hay autos para despachar.")
            return
        self.ver_autos()
        try:
            indice = int(input("Selecciona el número del auto a despachar: ")) - 1
            procedimiento = input("Procedimiento realizado: ")
            costo = int(input("Costo (CLP): "))
        except ValueError:
            print(Fore.RED + "❌ Entrada inválida.")
            return
        auto = self.taller.despachar_auto(indice, procedimiento, costo)
        if auto:
            self.historial.agregar(auto)
            print(Fore.GREEN + "✅ Auto despachado exitosamente.")
        else:
            print(Fore.RED + "❌ Índice inválido.")

    def submenu_historial(self):
        while True:
            self.encabezado("📜 Historial del Taller")
            print("1️⃣  🔍 Buscar auto por patente")
            print("2️⃣  📚 Ver historial completo")
            print("3️⃣  💰 Ver ganancias del taller")
            print("4️⃣  🔙 Volver al menú principal")
            print("=" * 50)
            opcion = input("👉 Selecciona una opción (1-4): ").strip()
            if opcion == '1':
                patente = input("Ingresa la patente a buscar: ").strip().upper()
                resultados = self.historial.buscar_por_patente(patente)
                if resultados:
                    for auto in resultados:
                        print(f"\n{auto.marca} {auto.modelo} ({auto.anio}) - {auto.patente}")
                        print(f"Falla: {auto.falla}")
                        print(f"Procedimiento: {auto.procedimiento}")
                        print(f"Costo: ${auto.costo:,} CLP\n")
                else:
                    print(Fore.YELLOW + f"ℹ️ No se encontraron autos con la patente '{patente}'.")
            elif opcion == '2':
                self.encabezado("📋 Historial de Autos")
                autos = self.historial.listar()
                if not autos:
                    print(Fore.YELLOW + "ℹ️ No hay autos en el historial.")
                    continue
                tabla = []
                for i, a in enumerate(autos, 1):
                    tabla.append([i, a.marca, a.modelo, a.anio, a.patente, a.falla, a.procedimiento, f"${a.costo:,} CLP"])
                print(tabulate(tabla, headers=["#", "Marca", "Modelo", "Año", "Patente", "Falla", "Procedimiento", "Costo"], tablefmt="fancy_grid"))
            elif opcion == '3':
                self.encabezado("💵 Ganancias del Taller")
                ganancia = self.historial.calcular_ganancias()
                print(Fore.GREEN + f"Ganancia total: ${ganancia:,} CLP")
            elif opcion == '4':
                print(Fore.CYAN + "🔙 Volviendo al menú principal...")
                break
            else:
                print(Fore.RED + "❌ Opción inválida. Intenta nuevamente.")

    def despedida(self):
        print("\n" + "=" * 50)
        print(Fore.GREEN + "👋 Gracias por usar el sistema del Taller Mecánico")
        print(Fore.GREEN + "      ¡Que tengas un excelente día! 🚗🛠️")
        print("=" * 50 + "\n")

if __name__ == "__main__":
    app = TallerApp()
    app.ejecutar()
