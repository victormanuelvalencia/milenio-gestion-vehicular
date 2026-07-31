from pydantic import BaseModel, ConfigDict
from typing import Optional

class VehiculoBase(BaseModel):
    placa: str
    marca: str
    ano: int
    estado: bool = True

class VehiculoCrear(VehiculoBase):
    pass

class VehiculoActualizar(BaseModel):
    placa: Optional[str] = None
    marca: Optional[str] = None
    ano: Optional[int] = None
    estado: Optional[bool] = None

class VehiculoRespuesta(VehiculoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)