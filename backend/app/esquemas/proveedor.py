from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProveedorBase(BaseModel):
    nombre: str
    nit: str
    direccion: Optional[str] = None

class ProveedorCrear(ProveedorBase):
    pass

class ProveedorActualizar(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorRespuesta(ProveedorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)