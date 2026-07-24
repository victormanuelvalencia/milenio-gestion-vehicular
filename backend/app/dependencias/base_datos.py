from typing import Generator
from app.base_datos.conexion import SesionLocal

def obtener_bd() -> Generator:
    bd = SesionLocal()
    try:
        yield bd
    finally:
        bd.close()