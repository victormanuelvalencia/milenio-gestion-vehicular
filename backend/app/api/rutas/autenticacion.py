from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.esquemas.token import Token, CredencialesLogin
from app.servicios.autenticacion import autenticar_usuario
from app.dependencias.base_datos import obtener_bd

enrutador = APIRouter()

@enrutador.post("/login", response_model=Token)
def login(credenciales: CredencialesLogin, bd: Session = Depends(obtener_bd)):
    """
    Inicia sesión con correo y contraseña.
    Retorna un JWT de acceso.
    """
    return autenticar_usuario(bd=bd, correo=credenciales.correo, contrasena=credenciales.contrasena)