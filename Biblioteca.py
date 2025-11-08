# -parcial-programacion
# BIBLIOTECA DIGITAL - SISTEMA DE GESTIÓN
# Autores: Miguel Angel Mancera Palomares, Camilo Alexander Clavijo Marin
# Descripción:Programa de consola que administra el inventario de una biblioteca.Permite registrar préstamos, devoluciones, calcular multas y guardar datos.

import json
from datetime import date, timedelta

# Valor de la multa por día de retraso
TARIFA_POR_DIA = 1000

# 1️⃣ CLASES PRINCIPALES

class Material:
    # Representa un material bibliográfico (libro, revista, etc.)

    def __init__(self, id, titulo, autor, tipo, copias_totales):
        # Atributos básicos
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.tipo = tipo
        self.copias_totales = copias_totales
        self.copias_disponibles = copias_totales

    def __str__(self):
        # Retorna una representación legible del material
        return f"ID: {self.id} | {self.titulo} | {self.autor} | Tipo: {self.tipo} | Copias: {self.copias_disponibles}/{self.copias_totales}"


class Prestamo:
    # Representa un préstamo realizado por un usuario.

    def __init__(self, id, material_id, usuario, fecha_prestamo, dias_prestamo=14):
        self.id = id
        self.material_id = material_id
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo
        # Fecha límite = fecha de préstamo + días permitidos
        self.fecha_vencimiento = fecha_prestamo + timedelta(days=dias_prestamo)
        # La devolución y multa se asignan luego
        self.fecha_devolucion = None
        self.multa = 0.0

    def esta_devuelto(self):
        # Devuelve True si el préstamo ya fue devuelto.
        return self.fecha_devolucion is not None

    def __str__(self):
        # Muestra un resumen del préstamo.
        estado = "Devuelto" if self.esta_devuelto() else "Activo"
        return (f"ID Préstamo: {self.id} | Usuario: {self.usuario} | "
                f"Material ID: {self.material_id} | Vence: {self.fecha_vencimiento} | Estado: {estado}")


class Inventario:
    # Administra la lista de materiales bibliográficos disponibles.

    def __init__(self):
        self.materiales = []  # lista de objetos Material

    def agregar(self, material):
        # Agrega un material nuevo al inventario.
        self.materiales.append(material)

    def listar(self):
        # Muestra todos los materiales disponibles.
        if not self.materiales:
            print("Inventario vacío.")
            return
        for m in self.materiales:
            print(m)

    def buscar_por_id(self, id):
        # Busca un material por su ID y lo retorna si existe.
        for m in self.materiales:
            if m.id == id:
                return m
        return None

# FUNCIONES DE GUARDAR Y CARGAR DATOS

def guardar_datos(inventario, prestamos, archivo="biblioteca.json"):
    
    # Guarda los datos del inventario y los préstamos en un archivo JSON. Se ejecuta al salir del programa.
    
    datos = {
        "materiales": [
            {
                "id": m.id,
                "titulo": m.titulo,
                "autor": m.autor,
                "tipo": m.tipo,
                "copias_totales": m.copias_totales,
                "copias_disponibles": m.copias_disponibles
            }
            for m in inventario.materiales
        ],
        "prestamos": [
            {
                "id": p.id,
                "material_id": p.material_id,
                "usuario": p.usuario,
                "fecha_prestamo": p.fecha_prestamo.isoformat(),
                "fecha_vencimiento": p.fecha_vencimiento.isoformat(),
                "fecha_devolucion": p.fecha_devolucion.isoformat() if p.fecha_devolucion else None,
                "multa": p.multa
            }
            for p in prestamos
        ]
    }

    # Guarda los datos en formato legible (indent=4)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(" Datos guardados correctamente.")


def cargar_datos(archivo="biblioteca.json"):
    
    # Carga los datos del archivo JSON si existe. Si no existe, crea inventario y préstamos vacíos.
    
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # Reconstruir objetos de inventario
        inventario = Inventario()
        for m in datos["materiales"]:
            material = Material(m["id"], m["titulo"], m["autor"], m["tipo"], m["copias_totales"])
            material.copias_disponibles = m["copias_disponibles"]
            inventario.agregar(material)

        # Reconstruir objetos de préstamo
        prestamos = []
        for p in datos["prestamos"]:
            prestamo = Prestamo(
                p["id"],
                p["material_id"],
                p["usuario"],
                date.fromisoformat(p["fecha_prestamo"])
            )
            prestamo.fecha_vencimiento = date.fromisoformat(p["fecha_vencimiento"])
            if p["fecha_devolucion"]:
                prestamo.fecha_devolucion = date.fromisoformat(p["fecha_devolucion"])
            prestamo.multa = p["multa"]
            prestamos.append(prestamo)

        print(" Datos cargados correctamente.")
        return inventario, prestamos

    except FileNotFoundError:
        # Si el archivo no existe, se empieza desde cero
        print(" No se encontró archivo de datos, iniciando desde cero.")
        return Inventario(), []

# MENÚ PRINCIPAL (INTERFAZ DE USUARIO)

def mostrar_menu():
    # Imprime el menú principal del sistema.
    print("\n Menú Biblioteca ")
    print("1. Inventario")
    print("2. Préstamo")
    print("3. Devolución")
    print("4. Multas")
    print("5. Salir")

# 4️⃣ FUNCIÓN PRINCIPAL DEL PROGRAMA

def main():
    # Cargar datos guardados (si existen)
    inventario, prestamos = cargar_datos()

    # Si el inventario está vacío, agregar materiales por defecto
    if not inventario.materiales:
        inventario.agregar(Material(1, "Fundamentos de Programación", "A. Autor", "Libro", 3))
        inventario.agregar(Material(2, "Estructuras de Datos", "B. Autor", "Libro", 2))
        inventario.agregar(Material(3, "Revista Ciencia Hoy", "Varios", "Revista", 1))

    salir = False
    while not salir:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        # OPCIÓN 1: INVENTARIO 
        if opcion == "1":
            print("\n Inventario ")
            inventario.listar()

        # OPCIÓN 2: PRÉSTAMO 
        elif opcion == "2":
            print("\n Registrar Préstamo ")
            inventario.listar()
            id_str = input("Ingrese el ID del material que desea prestar: ")

            # Validar entrada
            if not id_str.isdigit():
                print("ID inválido.")
                continue

            id_material = int(id_str)
            material = inventario.buscar_por_id(id_material)
            if not material:
                print("Material no encontrado.")
                continue
            if material.copias_disponibles <= 0:
                print("No hay copias disponibles de ese material.")
                continue

            # Registrar préstamo
            usuario = input("Ingrese el nombre del usuario: ")
            fecha_prestamo = date.today()
            nuevo_prestamo = Prestamo(len(prestamos) + 1, id_material, usuario, fecha_prestamo)
            prestamos.append(nuevo_prestamo)
            material.copias_disponibles -= 1

            print(f" Préstamo registrado correctamente para {usuario}.")
            print(f"Fecha de vencimiento: {nuevo_prestamo.fecha_vencimiento}")

        # OPCIÓN 3: DEVOLUCIÓN 
        elif opcion == "3":
            print("\n Registrar Devolución ")
            activos = [p for p in prestamos if not p.esta_devuelto()]
            if not activos:
                print("No hay préstamos activos.")
                continue

            # Mostrar préstamos activos
            for p in activos:
                print(p)

            id_str = input("Ingrese el ID del préstamo que desea devolver: ")
            if not id_str.isdigit():
                print("ID inválido.")
                continue

            id_prestamo = int(id_str)
            prestamo = next((p for p in prestamos if p.id == id_prestamo), None)
            if not prestamo:
                print("Préstamo no encontrado.")
                continue

            # Registrar la devolución
            fecha_devolucion = date.today()
            prestamo.fecha_devolucion = fecha_devolucion

            # Calcular multa si hay retraso
            dias_retraso = (fecha_devolucion - prestamo.fecha_vencimiento).days
            if dias_retraso > 0:
                prestamo.multa = dias_retraso * TARIFA_POR_DIA
                print(f" Devolución tardía ({dias_retraso} días). Multa: ${prestamo.multa:.2f}")
            else:
                print(" Devolución a tiempo. No hay multa.")

            # Aumentar las copias disponibles
            material = inventario.buscar_por_id(prestamo.material_id)
            if material:
                material.copias_disponibles += 1

        # OPCIÓN 4: MULTAS 
        elif opcion == "4":
            print("\n Multas y Préstamos ")
            if not prestamos:
                print("No hay préstamos registrados.")
                continue

            # Submenú
            print("1. Ver todas las multas")
            print("2. Ver préstamos activos")
            print("3. Ver préstamos devueltos")
            print("4. Volver al menú principal")
            subop = input("Seleccione una opción: ")

            if subop == "1":
                print("\n--- Multas registradas ---")
                hay_multas = False
                for p in prestamos:
                    if p.multa > 0:
                        hay_multas = True
                        material = inventario.buscar_por_id(p.material_id)
                        print(f"Usuario: {p.usuario} | Material: {material.titulo} | Multa: ${p.multa:.2f}")
                if not hay_multas:
                    print("No hay multas registradas.")

            elif subop == "2":
                print("\n--- Préstamos activos ---")
                for p in prestamos:
                    if not p.esta_devuelto():
                        material = inventario.buscar_por_id(p.material_id)
                        print(f"{p} | Material: {material.titulo}")

            elif subop == "3":
                print("\n--- Préstamos devueltos ---")
                for p in prestamos:
                    if p.esta_devuelto():
                        material = inventario.buscar_por_id(p.material_id)
                        print(f"{p} | Material: {material.titulo} | Multa: ${p.multa:.2f}")

            elif subop == "4":
                continue
            else:
                print("Opción inválida.")

        # OPCIÓN 5: SALIR 
        elif opcion == "5":
            guardar_datos(inventario, prestamos)
            print("Saliendo... ¡Hasta pronto!")
            salir = True

        # OPCIÓN INVÁLIDA 
        else:
            print("Opción inválida, intente de nuevo.")

# EJECUCIÓN DEL PROGRAMA

if __name__ == "__main__":
    main()
