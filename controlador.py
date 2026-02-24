#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controlador principal para el Sistema de Gestión de Empleados
Tarea Programada 1 - Estructuras de Datos
"""

import os
import sys
import generador_ordenado as generador
import lector_con_busqueda as lector


def limpiar_pantalla():
    """Limpia la pantalla según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")


def mostrar_banner():
    """Muestra el banner del programa"""
    print("="*60)
    print("     SISTEMA DE GESTIÓN DE EMPLEADOS v1.0")
    print("     Tarea Programada 1 - Estructuras de Datos")
    print("="*60)


def mostrar_menu():
    """Muestra el menú principal y retorna la opción seleccionada"""
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Generar nuevo archivo de empleados")
    print("2. Leer registro por posición")
    print("3. Buscar empleado por número")
    print("4. Ver información del archivo")
    print("5. Salir")
    return input("\nSeleccione una opción (1-5): ").strip()


def opcion_generar_archivo():
    """Opción 1: Generar nuevo archivo"""
    print("\n--- GENERAR NUEVO ARCHIVO ---")
    try:
        generador.main()
    except ValueError as e:
        print(f"Error: Ingrese un número válido. {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    pausar()


def opcion_leer_por_posicion():
    """Opción 2: Leer registro por posición"""
    print("\n--- LEER REGISTRO POR POSICIÓN ---")
    archivo = input("Nombre del archivo .bin: ").strip()
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        pausar()
        return
    
    try:
        # Mostrar información del archivo
        info = lector.obtener_info_archivo(archivo)
        print(f"El archivo contiene {info['num_registros']} registros.")
        
        pos = int(input("Posición del registro a leer (1-based): "))
        registro = lector.leer_por_posicion(archivo, pos)
        
        # Mostrar el registro
        print("\n" + "="*50)
        print("REGISTRO ENCONTRADO:")
        print("="*50)
        print(f"Nombre: {registro['nombre']}")
        print(f"Edad: {registro['edad']} años")
        print(f"Fecha de Nacimiento: {registro['fecha_nacimiento'].strftime('%d/%m/%Y')}")
        print(f"Provincia: {registro['provincia']}")
        print(f"Cantón: {registro['canton']}")
        print(f"Distrito: {registro['distrito']}")
        print(f"Número de Empleado: {registro['num_empleado']}")
        print("="*50)
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error al leer el registro: {e}")
    
    pausar()


def opcion_buscar_por_empleado():
    """Opción 3: Buscar empleado por número (búsqueda binaria)"""
    print("\n--- BUSCAR EMPLEADO POR NÚMERO ---")
    archivo = input("Nombre del archivo .bin: ").strip()
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        pausar()
        return
    
    try:
        # Mostrar información del archivo
        info = lector.obtener_info_archivo(archivo)
        print(f"Buscando en {info['num_registros']} registros...")
        
        num_empleado = int(input("Número de empleado a buscar: "))
        
        print("\nRealizando búsqueda binaria...")
        registro = lector.buscar_por_empleado(archivo, num_empleado)
        
        if registro:
            print("\n" + "="*50)
            print("¡EMPLEADO ENCONTRADO!")
            print("="*50)
            print(f"Nombre: {registro['nombre']}")
            print(f"Edad: {registro['edad']} años")
            print(f"Fecha de Nacimiento: {registro['fecha_nacimiento'].strftime('%d/%m/%Y')}")
            print(f"Provincia: {registro['provincia']}")
            print(f"Cantón: {registro['canton']}")
            print(f"Distrito: {registro['distrito']}")
            print(f"Número de Empleado: {registro['num_empleado']}")
            if 'posicion' in registro:
                print(f"Encontrado en la posición: {registro['posicion']}")
            print("="*50)
        else:
            print(f"\nNo existe un empleado con el número {num_empleado}.")
            
    except ValueError:
        print("Error: Ingrese un número de empleado válido.")
    except Exception as e:
        print(f"Error durante la búsqueda: {e}")
    
    pausar()


def opcion_info_archivo():
    """Opción 4: Ver información del archivo"""
    print("\n--- INFORMACIÓN DEL ARCHIVO ---")
    archivo = input("Nombre del archivo .bin: ").strip()
    
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        pausar()
        return
    
    try:
        info = lector.obtener_info_archivo(archivo)
        tamano_real = os.path.getsize(archivo)
        
        print(f"\nInformación del archivo: {archivo}")
        print("-" * 30)
        print(f"Número de registros: {info['num_registros']}")
        print(f"Tamaño del registro: {info['tamano_registro']} bytes")
        print(f"Tamaño de cabecera: {lector.COUNT_STRUCT.size} bytes")
        print(f"Tamaño total (calculado): {info['tamano_total']} bytes")
        print(f"Tamaño real en disco: {tamano_real} bytes")
        print(f"Rango de posiciones: 1 - {info['num_registros']}")
        
        # Verificar integridad básica
        if tamano_real == info['tamano_total']:
            print("\n✅ El archivo parece estar intacto.")
        else:
            print("\n⚠️  El tamaño del archivo no coincide con el esperado.")
            
    except Exception as e:
        print(f"Error al leer información: {e}")
    
    pausar()


def main():
    """Función principal del controlador"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        opcion = mostrar_menu()
        
        if opcion == '1':
            opcion_generar_archivo()
        elif opcion == '2':
            opcion_leer_por_posicion()
        elif opcion == '3':
            opcion_buscar_por_empleado()
        elif opcion == '4':
            opcion_info_archivo()
        elif opcion == '5':
            print("\nGracias por usar el sistema. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("\nOpción no válida. Intente de nuevo.")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario. ¡Hasta luego!")
        sys.exit(0)