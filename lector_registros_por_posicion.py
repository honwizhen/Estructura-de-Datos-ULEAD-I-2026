import struct
from datetime import date

COUNT_STRUCT = struct.Struct(">I")

NAME_LEN = 40
PROV_LEN = 20
CANT_LEN = 20
DIST_LEN = 20

RECORD_STRUCT = struct.Struct(f">{NAME_LEN}s B I {PROV_LEN}s {CANT_LEN}s {DIST_LEN}s")
RECORD_SIZE = RECORD_STRUCT.size


def unpack_fixed_str(b: bytes) -> str:
    return b.split(b"\0", 1)[0].decode("utf-8", errors="replace")


def read_record_at(filename: str, position_1based: int):
    with open(filename, "rb") as f:
        (n,) = COUNT_STRUCT.unpack(f.read(COUNT_STRUCT.size))

        if position_1based < 1 or position_1based > n:
            raise ValueError(f"Posición inválida: {position_1based}. Debe estar entre 1 y {n}.")

        header_size = COUNT_STRUCT.size
        offset = header_size + (position_1based - 1) * RECORD_SIZE
        f.seek(offset)

        data = f.read(RECORD_SIZE)
        if len(data) != RECORD_SIZE:
            raise IOError("No se pudo leer el registro completo (archivo corrupto o truncado).")

        nombre_b, edad, fecha_ord, prov_b, canton_b, dist_b = RECORD_STRUCT.unpack(data)

        # Reconstruir date (objeto real)
        fecha_nacimiento = date.fromordinal(fecha_ord)

        return {
            "nombre": unpack_fixed_str(nombre_b),
            "edad": int(edad),
            "fecha_nacimiento": fecha_nacimiento,  # <-- objeto date
            "provincia": unpack_fixed_str(prov_b),
            "canton": unpack_fixed_str(canton_b),
            "distrito": unpack_fixed_str(dist_b),
        }


def main():
    filename = input("Archivo: ").strip()
    pos = int(input("Posición del registro (1-based): "))

    record = read_record_at(filename, pos)

    print("\nRegistro encontrado:\n")
    for k, v in record.items():
        # Para imprimir bonito, date se muestra como YYYY-MM-DD por defecto
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
