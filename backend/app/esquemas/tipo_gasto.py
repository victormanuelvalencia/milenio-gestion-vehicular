from pydantic import BaseModel, ConfigDict
from typing import Optional

class TipoGastoBase(BaseModel):
    nombre: str

class TipoGastoCrear(TipoGastoBase):
    pass

class TipoGastoActualizar(BaseModel):
    nombre: Optional[str] = None

class TipoGastoRespuesta(TipoGastoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)