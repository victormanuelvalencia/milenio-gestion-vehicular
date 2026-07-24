from app.base_datos.conexion import SesionLocal
from app.modelos.usuario import Usuario
from app.seguridad.contrasenas import obtener_hash_contrasena

db = SesionLocal()

usuario = db.query(Usuario).filter(
    Usuario.correo == "admin@milenio.com"
).first()

if usuario:
    print("El administrador ya existe")
else:
    admin = Usuario(
        nombre="Administrador",
        correo="admin@milenio.com",
        contrasena_hash=obtener_hash_contrasena("123456"),
        activo=True
    )

    db.add(admin)
    db.commit()

    print("Administrador creado correctamente")