from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual
from app.esquemas.gasto import GastoRespuesta
from app.servicios.reporte import ServicioReportes

enrutador = APIRouter(
    prefix="/reportes",
    tags=["Reportes"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/gastos-por-vehiculo", response_model=List[GastoRespuesta])
def gastos_por_vehiculo(
    vehiculo_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    bd: Session = Depends(obtener_bd)
):
    return ServicioReportes.obtener_gastos_por_vehiculo(bd, vehiculo_id, fecha_inicio, fecha_fin)


@enrutador.get("/gastos-por-mes")
def gastos_por_mes(anio: int, bd: Session = Depends(obtener_bd)):
    return ServicioReportes.obtener_gastos_por_mes(bd, anio)


@enrutador.get("/gastos-por-tipo")
def gastos_por_tipo(
    vehiculo_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    bd: Session = Depends(obtener_bd)
):
    return ServicioReportes.obtener_gastos_por_tipo(bd, vehiculo_id, fecha_inicio, fecha_fin)


@enrutador.get("/historial-vehiculo", response_model=List[GastoRespuesta])
def historial_vehiculo(vehiculo_id: Optional[int] = None, bd: Session = Depends(obtener_bd)):
    return ServicioReportes.obtener_historial_vehiculo(bd, vehiculo_id)


@enrutador.get("/costos-entre-fechas", response_model=List[GastoRespuesta])
def costos_entre_fechas(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    bd: Session = Depends(obtener_bd)
):
    return ServicioReportes.obtener_costos_entre_fechas(bd, fecha_inicio, fecha_fin)


@enrutador.get("/gastos-por-proveedor", response_model=List[GastoRespuesta])
def gastos_por_proveedor(proveedor_id: Optional[str] = None, bd: Session = Depends(obtener_bd)):
    return ServicioReportes.obtener_gastos_por_proveedor(bd, proveedor_id)
