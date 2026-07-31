from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class MantenimientoProgramadoBase(BaseModel):
    vehiculo_id: int
    descripcion: str
    fecha_programada: date
    estado: Optional[str] = "Pendiente"

class MantenimientoProgramadoCrear(MantenimientoProgramadoBase):
    pass

class MantenimientoProgramadoActualizar(BaseModel):
    vehiculo_id: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_programada: Optional[date] = None
    estado: Optional[str] = None

from app.esquemas.vehiculo import VehiculoRespuesta

class MantenimientoProgramadoRespuesta(MantenimientoProgramadoBase):
    id: int
    vehiculo: Optional[VehiculoRespuesta] = None
    model_config = ConfigDict(from_attributes=True)
