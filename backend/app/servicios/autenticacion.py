from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modelos.usuario import Usuario
from app.esquemas.token import Token
from app.seguridad.contrasenas import verificar_contrasena
from app.seguridad.tokens import crear_token_acceso
from app.configuracion.config import configuraciones

def autenticar_usuario(bd: Session, correo: str, contrasena: str) -> Token:
    usuario = bd.query(Usuario).filter(Usuario.correo == correo).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    if not verificar_contrasena(contrasena, usuario.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )

    tiempo_expiracion_acceso = timedelta(minutes=configuraciones.MINUTOS_EXPIRACION_TOKEN)
    token_acceso = crear_token_acceso(
        datos={"sub": usuario.correo, "rol": usuario.rol, "nombre": usuario.nombre},
        tiempo_expiracion=tiempo_expiracion_acceso
    )
    
    return Token(token_acceso=token_acceso, tipo_token="bearer")