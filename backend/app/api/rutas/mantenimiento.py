from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.mantenimiento import MantenimientoRespuesta, MantenimientoCrear, MantenimientoActualizar
from app.servicios import mantenimiento as servicio_mantenimiento
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual, requerir_superadmin
from app.modelos.usuario import Usuario

enrutador = APIRouter(
    prefix="/mantenimientos",
    tags=["Mantenimientos"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/", response_model=List[MantenimientoRespuesta])
def obtener_mantenimientos(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_mantenimiento.obtener_todos(bd, skip=skip, limit=limit)

@enrutador.get("/{id_mantenimiento}", response_model=MantenimientoRespuesta)
def obtener_mantenimiento(id_mantenimiento: int, bd: Session = Depends(obtener_bd)):
    return servicio_mantenimiento.obtener_por_id(bd, id_mantenimiento=id_mantenimiento)

@enrutador.post("/", response_model=MantenimientoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_mantenimiento(mantenimiento: MantenimientoCrear, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_mantenimiento.crear(bd, mantenimiento_crear=mantenimiento)

@enrutador.put("/{id_mantenimiento}", response_model=MantenimientoRespuesta)
def actualizar_mantenimiento(id_mantenimiento: int, mantenimiento: MantenimientoActualizar, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_mantenimiento.actualizar(bd, id_mantenimiento=id_mantenimiento, mantenimiento_actualizar=mantenimiento)

@enrutador.delete("/{id_mantenimiento}")
def eliminar_mantenimiento(id_mantenimiento: int, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_mantenimiento.eliminar(bd, id_mantenimiento=id_mantenimiento)
