from datetime import datetime, timedelta, timezone
from jose import jwt
from app.configuracion.config import configuraciones

def crear_token_acceso(datos: dict, tiempo_expiracion: timedelta | None = None):
    datos_a_codificar = datos.copy()
    if tiempo_expiracion:
        expira = datetime.now(timezone.utc) + tiempo_expiracion
    else:
        expira = datetime.now(timezone.utc) + timedelta(minutes=configuraciones.MINUTOS_EXPIRACION_TOKEN)
    
    datos_a_codificar.update({"exp": expira})
    token_jwt = jwt.encode(
        datos_a_codificar, 
        configuraciones.CLAVE_SECRETA, 
        algorithm=configuraciones.ALGORITMO
    )
    return token_jwt