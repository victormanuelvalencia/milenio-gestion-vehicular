from passlib.context import CryptContext

contexto_contrasenas = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    return contexto_contrasenas.verify(contrasena_plana, contrasena_hasheada)

def obtener_hash_contrasena(contrasena: str) -> str:
    return contexto_contrasenas.hash(contrasena)