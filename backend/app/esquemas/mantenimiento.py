from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class MantenimientoBase(BaseModel):
    fecha: date
    kilometraje: int
    vehiculo_id: int
    proveedor_id: Optional[int] = None
    proveedor_manual: Optional[str] = None
    descripcion: Optional[str] = None
    valor: float

class MantenimientoCrear(MantenimientoBase):
    pass

class MantenimientoActualizar(BaseModel):
    fecha: Optional[date] = None
    kilometraje: Optional[int] = None
    vehiculo_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    proveedor_manual: Optional[str] = None
    descripcion: Optional[str] = None
    valor: Optional[float] = None

from app.esquemas.vehiculo import VehiculoRespuesta
from app.esquemas.proveedor import ProveedorRespuesta

class MantenimientoRespuesta(MantenimientoBase):
    id: int
    vehiculo: Optional[VehiculoRespuesta] = None
    proveedor: Optional[ProveedorRespuesta] = None
    model_config = ConfigDict(from_attributes=True)
