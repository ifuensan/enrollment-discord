# functions
from datetime import datetime
import re

def es_correo_valido(correo: str) -> bool:
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(patron, correo) is not None

def obtener_todos_cursos(client):
    try:
        hoja = client.open("Master Calendar Courses 2025 ").worksheet("Courses ready")
        filas = hoja.get_all_values()
        nombres_cursos = list({fila[3].strip() for fila in filas[1:] if fila[3].strip() != ""})  # columna 3 = "Course Name"
        return sorted(nombres_cursos)  # orden alfabético opcional
    except Exception as e:
        print(f"⚠️ Error al leer los cursos: {e}")
        return []

def obtener_cursos_abiertos(client):
    try:
        hoja = client.open("Master Calendar Courses 2025 ").worksheet("Courses ready")
        filas = hoja.get_all_values()
        hoy = datetime.now()

        cursos_abiertos = []

        for fila in filas[1:]:  # Ignorar encabezado
            nombre = fila[3].strip()
            fecha_open = fila[4].strip()
            fecha_close = fila[5].strip()

            if not nombre or not fecha_open or not fecha_close:
                continue  # Saltar si hay campos vacíos

            try:
                fecha_open_dt = datetime.strptime(fecha_open, "%A, %B %d")
                fecha_close_dt = datetime.strptime(fecha_close, "%A, %B %d")

                # Asume el año actual si no hay año
                fecha_open_dt = fecha_open_dt.replace(year=hoy.year)
                fecha_close_dt = fecha_close_dt.replace(year=hoy.year)

                if fecha_open_dt <= hoy <= fecha_close_dt:
                    cursos_abiertos.append(nombre)

            except ValueError as e:
                print(f"❌ Error al parsear fechas: {e} → {fecha_open} / {fecha_close}")
                continue

        return sorted(set(cursos_abiertos))

    except Exception as e:
        print(f"⚠️ Error al leer los cursos: {e}")
        return []