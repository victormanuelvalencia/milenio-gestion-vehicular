from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date


class ViajeBase(BaseModel):
    vehiculo_id: int
    conductor_id: int
    empresa_id: int
    origen: str
    destino: str
    numero_manifiesto: str
    flete: float
    anticipo: float = 0.0
    fecha: Optional[date] = None


class ViajeCrear(ViajeBase):
    pass


class ViajeActualizar(BaseModel):
    vehiculo_id: Optional[int] = None
    conductor_id: Optional[int] = None
    empresa_id: Optional[int] = None
    origen: Optional[str] = None
    destino: Optional[str] = None
    numero_manifiesto: Optional[str] = None
    flete: Optional[float] = None
    anticipo: Optional[float] = None
    fecha: Optional[date] = None


from app.esquemas.vehiculo import VehiculoRespuesta
from app.esquemas.conductor import ConductorRespuesta
from app.esquemas.gasto import GastoRespuesta
from app.esquemas.empresa import EmpresaRespuesta


class ViajeRespuesta(ViajeBase):
    id: int
    vehiculo: Optional[VehiculoRespuesta] = None
    conductor: Optional[ConductorRespuesta] = None
    empresa: Optional[EmpresaRespuesta] = None
    gastos: Optional[List[GastoRespuesta]] = []
    model_config = ConfigDict(from_attributes=True)
