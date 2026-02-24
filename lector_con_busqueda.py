import struct
from datetime import date

COUNT_STRUCT = struct.Struct(">I")

NAME_LEN = 40
PROV_LEN = 20
CANT_LEN = 20
DIST_LEN = 20

RECORD_STRUCT = struct.Struct(f">{NAME_LEN}s B I {PROV_LEN}s {CANT_LEN}s {DIST_LEN}s I")
RECORD_SIZE = RECORD_STRUCT.size


def unpack_fixed_str(b: bytes) -> str:
    """Convierte bytes a string, eliminando caracteres nulos"""
    return b.split(b"\0", 1)[0].decode("utf-8", errors="replace")


def leer_cabecera(filename: str) -> int:
    """Lee la cabecera del archivo y retorna el número de registros"""
    try:
        with open(filename, "rb") as f:
            f.seek(0)
            (n,) = COUNT_STRUCT.unpack(f.read(COUNT_STRUCT.size))
            return n
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo '{filename}' no encontrado.")
    except Exception as e:
        raise Exception(f"Error al leer cabecera: {e}")


def leer_por_posicion(filename: str, posicion_1based: int) -> dict:
    """
    Lee un registro del archivo por su posición (1-based)
    Retorna un diccionario con los datos del registro
    """
    # Leer cabecera para obtener cantidad de registros
    n = leer_cabecera(filename)
    
    if posicion_1based < 1 or posicion_1based > n:
        raise ValueError(f"Posición inválida: {posicion_1based}. Debe estar entre 1 y {n}.")
    
    with open(filename, "rb") as f:
        # Calcular offset (cabecera + (posicion-1) * tamaño_registro)
        header_size = COUNT_STRUCT.size
        offset = header_size + (posicion_1based - 1) * RECORD_SIZE
        f.seek(offset)
        
        # Leer el registro
        data = f.read(RECORD_SIZE)
        if len(data) != RECORD_SIZE:
            raise IOError("No se pudo leer el registro completo (archivo corrupto o truncado).")
        
        # Desempaquetar todos los campos (incluyendo el nuevo numero_empleado)
        nombre_b, edad, fecha_ord, prov_b, canton_b, dist_b, num_empleado = RECORD_STRUCT.unpack(data)
        
        # Reconstruir fecha
        fecha_nacimiento = date.fromordinal(fecha_ord)
        
        return {
            'nombre': unpack_fixed_str(nombre_b),
            'edad': int(edad),
            'fecha_nacimiento': fecha_nacimiento,
            'provincia': unpack_fixed_str(prov_b),
            'canton': unpack_fixed_str(canton_b),
            'distrito': unpack_fixed_str(dist_b),
            'num_empleado': num_empleado
        }


def buscar_por_empleado(filename: str, num_empleado_buscado: int) -> dict or None:
    """
    Realiza búsqueda binaria por número de empleado
    Retorna el registro si lo encuentra, None si no existe
    """
    try:
        # Leer cabecera
        n = leer_cabecera(filename)
        
        inferior = 1
        superior = n
        
        with open(filename, "rb") as f:
            header_size = COUNT_STRUCT.size
            
            while inferior <= superior:
                pos_media = (inferior + superior) // 2
                
                # Calcular offset y leer registro en posición media
                offset = header_size + (pos_media - 1) * RECORD_SIZE
                f.seek(offset)
                data = f.read(RECORD_SIZE)
                
                if len(data) != RECORD_SIZE:
                    return None  # Archivo corrupto
                
                # Desempaquetar (el último campo es num_empleado)
                nombre_b, edad, fecha_ord, prov_b, canton_b, dist_b, num_emp = RECORD_STRUCT.unpack(data)
                
                print(f"  Comparando con posición {pos_media}: empleado #{num_emp}")  # Debug opcional
                
                if num_emp == num_empleado_buscado:
                    # Encontrado, construir diccionario completo
                    return {
                        'nombre': unpack_fixed_str(nombre_b),
                        'edad': edad,
                        'fecha_nacimiento': date.fromordinal(fecha_ord),
                        'provincia': unpack_fixed_str(prov_b),
                        'canton': unpack_fixed_str(canton_b),
                        'distrito': unpack_fixed_str(dist_b),
                        'num_empleado': num_emp,
                        'posicion': pos_media  # Guardamos la posición donde se encontró
                    }
                elif num_emp > num_empleado_buscado:
                    superior = pos_media - 1
                else:  # num_emp < num_empleado_buscado
                    inferior = pos_media + 1
        
        return None  # No encontrado
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo '{filename}' no encontrado.")
    except Exception as e:
        raise Exception(f"Error durante la búsqueda: {e}")


def mostrar_registro(registro: dict):
    """Muestra un registro formateado"""
    print("\n" + "="*50)
    print("REGISTRO ENCONTRADO:")
    print("="*50)
    for key, value in registro.items():
        if key == 'fecha_nacimiento':
            print(f"{key.replace('_', ' ').title()}: {value.strftime('%d/%m/%Y')}")
        elif key == 'posicion':
            print(f"Encontrado en posición: {value}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    print("="*50)


# Funciones para ser usadas por el controlador
def obtener_info_archivo(filename: str) -> dict:
    """Obtiene información básica del archivo"""
    n = leer_cabecera(filename)
    return {
        'num_registros': n,
        'tamano_registro': RECORD_SIZE,
        'tamano_total': COUNT_STRUCT.size + (n * RECORD_SIZE)
    }


if __name__ == "__main__":
    # Modo de prueba directa
    print("=== LECTOR DE REGISTROS (MODO PRUEBA) ===")
    filename = input("Archivo a leer: ").strip()
    
    try:
        info = obtener_info_archivo(filename)
        print(f"Archivo contiene {info['num_registros']} registros")
        print(f"Tamaño del registro: {info['tamano_registro']} bytes")
        
        opcion = input("\n¿Buscar por (1) Posición o (2) Número de empleado? ").strip()
        
        if opcion == '1':
            pos = int(input("Posición: "))
            registro = leer_por_posicion(filename, pos)
            mostrar_registro(registro)
        elif opcion == '2':
            num = int(input("Número de empleado: "))
            print("\nRealizando búsqueda binaria...")
            registro = buscar_por_empleado(filename, num)
            if registro:
                mostrar_registro(registro)
            else:
                print(f"\nNo existe empleado con número {num}")
        else:
            print("Opción no válida")
            
    except Exception as e:
        print(f"Error: {e}")