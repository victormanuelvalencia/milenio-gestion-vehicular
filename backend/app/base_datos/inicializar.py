from app.base_datos.base import Base
from app.base_datos.conexion import motor

# Importar TODOS los modelos
from app.modelos.usuario import Usuario
from app.modelos.vehiculo import Vehiculo
from app.modelos.gasto import Gasto
from app.modelos.tipo_gasto import TipoGasto
from app.modelos.proveedor import Proveedor
from app.modelos.conductor import Conductor

from app.base_datos.conexion import SesionLocal
from app.modelos.usuario import Usuario, RolUsuario
from app.seguridad.contrasenas import obtener_hash_contrasena

def sembrar_usuario_inicial(bd):
    correo_admin = "desarrollo@mileniotransportadora.com"
    usuario_existente = bd.query(Usuario).filter(Usuario.correo == correo_admin).first()
    if not usuario_existente:
        print(f"Creando usuario inicial: {correo_admin}...")
        usuario = Usuario(
            nombre="Equipo de Desarrollo",
            correo=correo_admin,
            contrasena_hash=obtener_hash_contrasena("231020Aa#"),
            activo=True,
            rol=RolUsuario.SUPERADMIN
        )
        bd.add(usuario)
        bd.commit()
        print("Usuario inicial creado correctamente.")
    else:
        print(f"El usuario {correo_admin} ya existe.")

def inicializar_base_datos():
    print("Creando tablas...")
    Base.metadata.create_all(bind=motor)
    print("Tablas creadas correctamente")
    
    bd = SesionLocal()
    try:
        sembrar_usuario_inicial(bd)
    finally:
        bd.close()

if __name__ == "__main__":
    inicializar_base_datos()