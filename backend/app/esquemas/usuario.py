from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from app.modelos.usuario import RolUsuario


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str = RolUsuario.USUARIO
    activo: bool = True

    @field_validator("rol")
    @classmethod
    def validar_rol(cls, v: str) -> str:
        if v not in RolUsuario.VALORES:
            raise ValueError(f"Rol inválido. Los valores permitidos son: {RolUsuario.VALORES}")
        return v


class UsuarioCrear(UsuarioBase):
    contrasena: str
    confirmar_contrasena: str

    @field_validator("confirmar_contrasena")
    @classmethod
    def contrasenas_deben_coincidir(cls, v: str, info) -> str:
        if "contrasena" in info.data and v != info.data["contrasena"]:
            raise ValueError("Las contraseñas no coinciden")
        return v


class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

    @field_validator("rol")
    @classmethod
    def validar_rol(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in RolUsuario.VALORES:
            raise ValueError(f"Rol inválido. Los valores permitidos son: {RolUsuario.VALORES}")
        return v


class CambiarContrasena(BaseModel):
    contrasena_nueva: str
    confirmar_contrasena: str

    @field_validator("confirmar_contrasena")
    @classmethod
    def contrasenas_deben_coincidir(cls, v: str, info) -> str:
        if "contrasena_nueva" in info.data and v != info.data["contrasena_nueva"]:
            raise ValueError("Las contraseñas no coinciden")
        return v


class CambiarEstado(BaseModel):
    activo: bool


class CambiarRol(BaseModel):
    rol: str

    @field_validator("rol")
    @classmethod
    def validar_rol(cls, v: str) -> str:
        if v not in RolUsuario.VALORES:
            raise ValueError(f"Rol inválido. Los valores permitidos son: {RolUsuario.VALORES}")
        return v


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str
    activo: bool
    fecha_creacion: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
