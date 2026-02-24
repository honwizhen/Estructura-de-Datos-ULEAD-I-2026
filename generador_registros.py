import random
import struct
import time
from datetime import date

# --------- Estructura binaria ----------
COUNT_STRUCT = struct.Struct(">I")  # un entero de 32 bits sin signo

# tamannios (bytes)
NAME_LEN = 40
PROV_LEN = 20
CANT_LEN = 20
DIST_LEN = 20

# estructura de registros
# nombre(40s), edad(B), fecha_ordinal(I), provincia(20s), canton(20s), distrito(20s)
RECORD_STRUCT = struct.Struct(f">{NAME_LEN}s B I {PROV_LEN}s {CANT_LEN}s {DIST_LEN}s")
RECORD_SIZE = RECORD_STRUCT.size

#datos aleatorios
NOMBRES = ["Mario", "Ana", "Luis", "Sofía", "Carlos", "María", "Jorge"]
PROVINCIAS = [
    ("San José", ["San José", "Escazú", "Desamparados"]),
    ("Alajuela", ["Alajuela", "San Ramón", "Grecia"]),
    ("Cartago", ["Cartago", "Paraíso", "La Unión"]),
]
DISTRITOS = ["Centro", "Norte", "Sur", "Este", "Oeste"]


def pack_fixed_str(text: str, size: int) -> bytes:
    # Nota: si el texto tiene caracteres UTF-8 multibyte, un corte a mitad puede producir reemplazos al decodificar.
    b = text.encode("utf-8")
    if len(b) > size:
        b = b[:size]
    return b.ljust(size, b"\0")


def random_birthdate(rng: random.Random) -> date:
    y = rng.randint(1950, 2010)
    m = rng.randint(1, 12)
    d = rng.randint(1, 28)
    return date(y, m, d)


def build_record(rng: random.Random, index: int):
    prov, cantones = rng.choice(PROVINCIAS)
    canton = rng.choice(cantones)
    distrito = rng.choice(DISTRITOS)

    nac = random_birthdate(rng)
    today = date.today()
    edad = today.year - nac.year - ((today.month, today.day) < (nac.month, nac.day))
    edad = max(0, min(255, edad))

    nombre = f"{rng.choice(NOMBRES)} {index}"
    fecha_ordinal = nac.toordinal()  # entero fijo

    return nombre, edad, fecha_ordinal, prov, canton, distrito


def main():
    n = int(input("Cantidad de registros a generar: "))
    filename = input("Nombre del archivo binario: ").strip()

    seed = int(time.time())  # segundos actuales
    rng = random.Random(seed)

    print(f"Seed usada: {seed}")
    print(f"RECORD_SIZE = {RECORD_SIZE} bytes")

    with open(filename, "wb") as f:
        f.write(COUNT_STRUCT.pack(n)) #se escribe la cantidad

        for i in range(1, n + 1):
            nombre, edad, fecha_ord, prov, canton, dist = build_record(rng, i)

            packed = RECORD_STRUCT.pack(
                pack_fixed_str(nombre, NAME_LEN),
                edad,
                fecha_ord,
                pack_fixed_str(prov, PROV_LEN),
                pack_fixed_str(canton, CANT_LEN),
                pack_fixed_str(dist, DIST_LEN),
            )
            f.write(packed)

    print(f"OK: {n} registros escritos en '{filename}'")


if __name__ == "__main__":
    main()
