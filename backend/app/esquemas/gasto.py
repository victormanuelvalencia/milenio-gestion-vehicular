from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from decimal import Decimal

class GastoBase(BaseModel):
    fecha: date
    valor: float
    vehiculo_id: int
    tipo_gasto_id: int
    proveedor_id: Optional[int] = None
    proveedor_manual: Optional[str] = None
    observaciones: Optional[str] = None

class GastoCrear(GastoBase):
    pass

class GastoActualizar(BaseModel):
    fecha: Optional[date] = None
    valor: Optional[float] = None
    vehiculo_id: Optional[int] = None
    tipo_gasto_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    proveedor_manual: Optional[str] = None
    observaciones: Optional[str] = None

class GastoRespuesta(GastoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)