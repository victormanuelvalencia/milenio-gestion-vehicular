from pydantic import BaseModel, EmailStr

class CredencialesLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class Token(BaseModel):
    token_acceso: str
    tipo_token: str

class DatosToken(BaseModel):
    correo: str | None = None