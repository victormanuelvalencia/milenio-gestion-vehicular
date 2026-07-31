from pydantic import BaseModel, ConfigDict
from typing import Optional


class ConductorBase(BaseModel):
    nombre: str
    cedula: str
    estado: bool = True


class ConductorCrear(ConductorBase):
    pass


class ConductorActualizar(BaseModel):
    nombre: Optional[str] = None
    cedula: Optional[str] = None
    estado: Optional[bool] = None


class ConductorRespuesta(ConductorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
