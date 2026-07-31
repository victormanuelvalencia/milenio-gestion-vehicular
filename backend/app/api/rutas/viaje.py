from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.viaje import ViajeRespuesta, ViajeCrear, ViajeActualizar
from app.esquemas.gasto import GastoRespuesta
from app.servicios import viaje as servicio_viaje
from app.servicios import gasto as servicio_gasto
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual

enrutador = APIRouter(
    prefix="/viajes",
    tags=["Viajes"],
    dependencies=[Depends(obtener_usuario_actual)]
)


@enrutador.get("/", response_model=List[ViajeRespuesta])
def obtener_viajes(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_viaje.obtener_todos(bd, skip=skip, limit=limit)


@enrutador.get("/{id_viaje}", response_model=ViajeRespuesta)
def obtener_viaje(id_viaje: int, bd: Session = Depends(obtener_bd)):
    return servicio_viaje.obtener_por_id(bd, id_viaje=id_viaje)


@enrutador.get("/{id_viaje}/gastos", response_model=List[GastoRespuesta])
def obtener_gastos_de_viaje(id_viaje: int, bd: Session = Depends(obtener_bd)):
    """Retorna todos los gastos asociados a un viaje específico."""
    servicio_viaje.obtener_por_id(bd, id_viaje=id_viaje)  # valida existencia
    return servicio_gasto.obtener_por_viaje(bd, id_viaje=id_viaje)


@enrutador.post("/", response_model=ViajeRespuesta, status_code=status.HTTP_201_CREATED)
def crear_viaje(viaje: ViajeCrear, bd: Session = Depends(obtener_bd)):
    return servicio_viaje.crear(bd, viaje_crear=viaje)


@enrutador.put("/{id_viaje}", response_model=ViajeRespuesta)
def actualizar_viaje(id_viaje: int, viaje: ViajeActualizar, bd: Session = Depends(obtener_bd)):
    return servicio_viaje.actualizar(bd, id_viaje=id_viaje, viaje_actualizar=viaje)


@enrutador.delete("/{id_viaje}")
def eliminar_viaje(id_viaje: int, bd: Session = Depends(obtener_bd)):
    return servicio_viaje.eliminar(bd, id_viaje=id_viaje)
