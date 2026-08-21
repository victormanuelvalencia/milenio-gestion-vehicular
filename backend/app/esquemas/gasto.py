from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
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
    factura: Optional[str] = None
    viaje_id: Optional[int] = None

class GastoCrear(GastoBase):
    pass


class GastoMasivoItem(BaseModel):
    """Un gasto individual dentro de una operación de registro masivo."""
    tipo_gasto_id: int
    valor: float
    proveedor_id: Optional[int] = None
    proveedor_manual: Optional[str] = None
    observaciones: Optional[str] = None
    factura: Optional[str] = None

    @field_validator('valor')
    @classmethod
    def valor_positivo(cls, v):
        if v <= 0:
            raise ValueError('El valor del gasto debe ser mayor que cero')
        return v


class GastosMasivosCrear(BaseModel):
    """Payload para registrar múltiples gastos asociados a un mismo viaje."""
    gastos: List[GastoMasivoItem]

class GastoActualizar(BaseModel):
    fecha: Optional[date] = None
    valor: Optional[float] = None
    vehiculo_id: Optional[int] = None
    tipo_gasto_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    proveedor_manual: Optional[str] = None
    observaciones: Optional[str] = None
    verificado_dian: Optional[bool] = None
    factura: Optional[str] = None
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