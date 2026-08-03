from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.tipo_gasto import TipoGastoRespuesta, TipoGastoCrear, TipoGastoActualizar
from app.servicios import tipo_gasto as servicio_tipo_gasto
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual, requerir_superadmin
from app.modelos.usuario import Usuario

enrutador = APIRouter(
    prefix="/tipos-gasto",
    tags=["Tipos de Gasto"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/", response_model=List[TipoGastoRespuesta])
def obtener_tipos_gasto(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_tipo_gasto.obtener_todos(bd, skip=skip, limit=limit)

@enrutador.get("/{id_tipo}", response_model=TipoGastoRespuesta)
def obtener_tipo_gasto(id_tipo: int, bd: Session = Depends(obtener_bd)):
    return servicio_tipo_gasto.obtener_por_id(bd, id_tipo=id_tipo)

@enrutador.post("/", response_model=TipoGastoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_tipo_gasto(tipo: TipoGastoCrear, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_tipo_gasto.crear(bd, tipo_crear=tipo)

@enrutador.put("/{id_tipo}", response_model=TipoGastoRespuesta)
def actualizar_tipo_gasto(id_tipo: int, tipo: TipoGastoActualizar, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_tipo_gasto.actualizar(bd, id_tipo=id_tipo, tipo_actualizar=tipo)

@enrutador.delete("/{id_tipo}")
def eliminar_tipo_gasto(id_tipo: int, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_tipo_gasto.eliminar(bd, id_tipo=id_tipo)