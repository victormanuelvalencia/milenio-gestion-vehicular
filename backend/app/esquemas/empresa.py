from pydantic import BaseModel, ConfigDict
from typing import Optional


class EmpresaBase(BaseModel):
    nombre: str


class EmpresaCrear(EmpresaBase):
    pass


class EmpresaActualizar(BaseModel):
    nombre: Optional[str] = None


class EmpresaRespuesta(EmpresaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
