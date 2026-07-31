from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from decimal import Decimal

class GastoBase(BaseModel):
    fecha: date
    valor: float
    vehiculo_id: Optional[int] = None
    tipo_gasto_id: int
    proveedor_id: Optional[int] = None
    proveedor_manual: Optional[str] = None
    observaciones: Optional[str] = None
    verificado_dian: Optional[bool] = False
    viaje_id: Optional[int] = None

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
    verificado_dian: Optional[bool] = None
    viaje_id: Optional[int] = None

from app.esquemas.vehiculo import VehiculoRespuesta
from app.esquemas.tipo_gasto import TipoGastoRespuesta
from app.esquemas.proveedor import ProveedorRespuesta

class GastoRespuesta(GastoBase):
    id: int
    vehiculo: Optional[VehiculoRespuesta] = None
    tipo_gasto: Optional[TipoGastoRespuesta] = None
    proveedor: Optional[ProveedorRespuesta] = None
    model_config = ConfigDict(from_attributes=True)