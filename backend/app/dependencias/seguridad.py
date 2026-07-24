from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.dependencias.base_datos import obtener_bd
from app.configuracion.config import configuraciones
from app.modelos.usuario import Usuario
from app.esquemas.token import DatosToken

esquema_seguridad = HTTPBearer()

def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(esquema_seguridad),
    bd: Session = Depends(obtener_bd)
) -> Usuario:
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credenciales.credentials
        payload = jwt.decode(token, configuraciones.CLAVE_SECRETA, algorithms=[configuraciones.ALGORITMO])
        correo: str = payload.get("sub")
        if correo is None:
            raise excepcion_credenciales
        datos_token = DatosToken(correo=correo)
    except JWTError:
        raise excepcion_credenciales
        
    usuario = bd.query(Usuario).filter(Usuario.correo == datos_token.correo).first()
    if usuario is None:
        raise excepcion_credenciales
    if not usuario.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
        
    return usuario