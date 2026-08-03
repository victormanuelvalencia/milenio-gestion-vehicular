from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.gasto import GastoRespuesta, GastoCrear, GastoActualizar
from app.servicios import gasto as servicio_gasto
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual, requerir_superadmin
from app.modelos.usuario import Usuario

enrutador = APIRouter(
    prefix="/gastos",
    tags=["Gastos"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/", response_model=List[GastoRespuesta])
def obtener_gastos(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_gasto.obtener_todos(bd, skip=skip, limit=limit)

@enrutador.get("/{id_gasto}", response_model=GastoRespuesta)
def obtener_gasto(id_gasto: int, bd: Session = Depends(obtener_bd)):
    return servicio_gasto.obtener_por_id(bd, id_gasto=id_gasto)

@enrutador.post("/", response_model=GastoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_gasto(gasto: GastoCrear, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_gasto.crear(bd, gasto_crear=gasto)

@enrutador.put("/{id_gasto}", response_model=GastoRespuesta)
def actualizar_gasto(id_gasto: int, gasto: GastoActualizar, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_gasto.actualizar(bd, id_gasto=id_gasto, gasto_actualizar=gasto)

@enrutador.delete("/{id_gasto}")
def eliminar_gasto(id_gasto: int, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_gasto.eliminar(bd, id_gasto=id_gasto)