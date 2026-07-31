from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.conductor import ConductorRespuesta, ConductorCrear, ConductorActualizar
from app.servicios import conductor as servicio_conductor
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual

enrutador = APIRouter(
    prefix="/conductores",
    tags=["Conductores"],
    dependencies=[Depends(obtener_usuario_actual)]
)


@enrutador.get("/", response_model=List[ConductorRespuesta])
def obtener_conductores(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_conductor.obtener_todos(bd, skip=skip, limit=limit)


@enrutador.get("/{id_conductor}", response_model=ConductorRespuesta)
def obtener_conductor(id_conductor: int, bd: Session = Depends(obtener_bd)):
    return servicio_conductor.obtener_por_id(bd, id_conductor=id_conductor)


@enrutador.post("/", response_model=ConductorRespuesta, status_code=status.HTTP_201_CREATED)
def crear_conductor(conductor: ConductorCrear, bd: Session = Depends(obtener_bd)):
    return servicio_conductor.crear(bd, conductor_crear=conductor)


@enrutador.put("/{id_conductor}", response_model=ConductorRespuesta)
def actualizar_conductor(id_conductor: int, conductor: ConductorActualizar, bd: Session = Depends(obtener_bd)):
    return servicio_conductor.actualizar(bd, id_conductor=id_conductor, conductor_actualizar=conductor)


@enrutador.delete("/{id_conductor}")
def eliminar_conductor(id_conductor: int, bd: Session = Depends(obtener_bd)):
    return servicio_conductor.eliminar(bd, id_conductor=id_conductor)
