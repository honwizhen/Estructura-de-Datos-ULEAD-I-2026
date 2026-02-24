import random
import struct
import time
from datetime import date

# --------- Estructura binaria ----------
COUNT_STRUCT = struct.Struct(">I")  # un entero de 32 bits sin signo

# tamaños (bytes)
NAME_LEN = 40
PROV_LEN = 20
CANT_LEN = 20
DIST_LEN = 20

# estructura de registros ACTUALIZADA con numero_empleado al final
# nombre(40s), edad(B), fecha_ordinal(I), provincia(20s), canton(20s), distrito(20s), numero_empleado(I)
RECORD_STRUCT = struct.Struct(f">{NAME_LEN}s B I {PROV_LEN}s {CANT_LEN}s {DIST_LEN}s I")
RECORD_SIZE = RECORD_STRUCT.size

# --------- DATOS MEJORADOS (más opciones) ----------
NOMBRES = [
    "Mario", "Ana", "Luis", "Sofía", "Carlos", "María", "Jorge", 
    "Laura", "Pedro", "Andrea", "José", "Gabriela", "Juan", "Fernanda",
    "Diego", "Valeria", "Ricardo", "Monica", "Francisco", "Elena"
]

PROVINCIAS = [
    ("San José", ["San José", "Escazú", "Desamparados", "Puriscal", "Pérez Zeledón"]),
    ("Alajuela", ["Alajuela", "San Ramón", "Grecia", "Quesada", "Atenas"]),
    ("Cartago", ["Cartago", "Paraíso", "La Unión", "Turrialba", "Jiménez"]),
    ("Guanacaste", ["Liberia", "Nicoya", "Santa Cruz", "Bagaces", "Carrillo"]),  # Nuevo
    ("Puntarenas", ["Puntarenas", "Esparza", "Buenos Aires", "Quepos", "Golfito"]),  # Nuevo
    ("Limón", ["Limón", "Pococí", "Guápiles", "Talamanca", "Siquirres"]),  # Nuevo
    ("Isla del Coco", ["Bahía Wafer", "Bahía Chatham", "Cerro Iglesias"]),  # Nueva provincia inventada
    ("Nueva Cartago", ["Ciudad Real", "Puerto Limonal", "Valle Central"])  # Nueva provincia inventada
]

DISTRITOS = ["Centro", "Norte", "Sur", "Este", "Oeste", "Nordeste", "Noroeste", "Sureste", "Suroeste"]


def pack_fixed_str(text: str, size: int) -> bytes:
    """Convierte un string a bytes con tamaño fijo"""
    b = text.encode("utf-8")
    if len(b) > size:
        b = b[:size]
    return b.ljust(size, b"\0")


def random_birthdate(rng: random.Random) -> date:
    """Genera una fecha de nacimiento aleatoria"""
    y = rng.randint(1950, 2010)
    m = rng.randint(1, 12)
    d = rng.randint(1, 28)
    return date(y, m, d)


def generar_lista_registros(n: int, rng: random.Random) -> list:
    """Genera n registros como lista de diccionarios con numeros de empleado unicos"""
    lista = []
    numeros_empleado_generados = set()
    
    for i in range(1, n + 1):
        # Generar datos aleatorios
        prov, cantones = rng.choice(PROVINCIAS)
        canton = rng.choice(cantones)
        distrito = rng.choice(DISTRITOS)
        
        nac = random_birthdate(rng)
        today = date.today()
        edad = today.year - nac.year - ((today.month, today.day) < (nac.month, nac.day))
        edad = max(0, min(255, edad))
        
        nombre = f"{rng.choice(NOMBRES)} {i}"
        fecha_ordinal = nac.toordinal()
        
        # Generar numero de empleado UNICO
        while True:
            num_empleado = rng.randint(1, 100000)  # Entero positivo
            if num_empleado not in numeros_empleado_generados:
                numeros_empleado_generados.add(num_empleado)
                break
        
        registro = {
            'nombre': nombre,
            'edad': edad,
            'fecha_ordinal': fecha_ordinal,
            'provincia': prov,
            'canton': canton,
            'distrito': distrito,
            'num_empleado': num_empleado
        }
        lista.append(registro)
    
    return lista


def guardar_registros(filename: str, registros: list):
    """Guarda los registros ordenados en el archivo binario"""
    with open(filename, "wb") as f:
        # Escribir cabecera con cantidad de registros
        f.write(COUNT_STRUCT.pack(len(registros)))
        
        # Escribir cada registro
        for reg in registros:
            packed = RECORD_STRUCT.pack(
                pack_fixed_str(reg['nombre'], NAME_LEN),
                reg['edad'],
                reg['fecha_ordinal'],
                pack_fixed_str(reg['provincia'], PROV_LEN),
                pack_fixed_str(reg['canton'], CANT_LEN),
                pack_fixed_str(reg['distrito'], DIST_LEN),
                reg['num_empleado']
            )
            f.write(packed)


def main():
    """Función principal del generador"""
    print("=== GENERADOR DE ARCHIVO DE EMPLEADOS ===")
    
    n = int(input("Cantidad de registros a generar: "))
    filename = input("Nombre del archivo (se agregará .bin si no lo tiene): ").strip()
    
    # Asegurar extensión .bin
    if not filename.endswith('.bin'):
        filename += '.bin'
    
    seed = int(time.time())
    rng = random.Random(seed)
    
    print(f"Seed usada: {seed}")
    print(f"Tamaño del registro: {RECORD_SIZE} bytes")
    print(f"Tamaño total del archivo: {COUNT_STRUCT.size + (n * RECORD_SIZE)} bytes")
    
    print("\nGenerando registros aleatorios...")
    registros = generar_lista_registros(n, rng)
    
    print("Ordenando por número de empleado (ascendente)...")
    registros.sort(key=lambda r: r['num_empleado'])
    
    print("Guardando en archivo...")
    guardar_registros(filename, registros)
    
    print(f"\n¡OK! {n} registros escritos en '{filename}'")
    print("Los registros están ordenados por número de empleado.")
    
    # Mostrar primeros 5 registros como ejemplo
    print("\nPrimeros 5 registros (ya ordenados):")
    for i, reg in enumerate(registros[:5]):
        print(f"  {i+1}. Empleado #{reg['num_empleado']}: {reg['nombre']}")


if __name__ == "__main__":
    main()