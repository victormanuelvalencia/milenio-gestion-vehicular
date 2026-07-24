from app.base_datos.base import Base
from app.base_datos.conexion import motor

# Importar TODOS los modelos
from app.modelos.usuario import Usuario
from app.modelos.vehiculo import Vehiculo
from app.modelos.gasto import Gasto
from app.modelos.tipo_gasto import TipoGasto
from app.modelos.proveedor import Proveedor


def inicializar_base_datos():
    print("Creando tablas...")
    Base.metadata.create_all(bind=motor)
    print("Tablas creadas correctamente")


if __name__ == "__main__":
    inicializar_base_datos()