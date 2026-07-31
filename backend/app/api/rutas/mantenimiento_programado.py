from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.mantenimiento_programado import MantenimientoProgramadoRespuesta, MantenimientoProgramadoCrear, MantenimientoProgramadoActualizar
from app.servicios import mantenimiento_programado as servicio_mantenimiento_programado
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual

enrutador = APIRouter(
    prefix="/mantenimientos-programados",
    tags=["Mantenimientos Programados"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/", response_model=List[MantenimientoProgramadoRespuesta])
def obtener_mantenimientos_programados(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_mantenimiento_programado.obtener_todos(bd, skip=skip, limit=limit)

@enrutador.get("/{id_mantenimiento}", response_model=MantenimientoProgramadoRespuesta)
def obtener_mantenimiento_programado(id_mantenimiento: int, bd: Session = Depends(obtener_bd)):
    return servicio_mantenimiento_programado.obtener_por_id(bd, id_mantenimiento=id_mantenimiento)

@enrutador.post("/", response_model=MantenimientoProgramadoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_mantenimiento_programado(mantenimiento: MantenimientoProgramadoCrear, bd: Session = Depends(obtener_bd)):
    return servicio_mantenimiento_programado.crear(bd, mantenimiento_crear=mantenimiento)

@enrutador.put("/{id_mantenimiento}", response_model=MantenimientoProgramadoRespuesta)
def actualizar_mantenimiento_programado(id_mantenimiento: int, mantenimiento: MantenimientoProgramadoActualizar, bd: Session = Depends(obtener_bd)):
    return servicio_mantenimiento_programado.actualizar(bd, id_mantenimiento=id_mantenimiento, mantenimiento_actualizar=mantenimiento)

@enrutador.delete("/{id_mantenimiento}")
def eliminar_mantenimiento_programado(id_mantenimiento: int, bd: Session = Depends(obtener_bd)):
    return servicio_mantenimiento_programado.eliminar(bd, id_mantenimiento=id_mantenimiento)
