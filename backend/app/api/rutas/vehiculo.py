from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.vehiculo import VehiculoRespuesta, VehiculoCrear, VehiculoActualizar
from app.servicios import vehiculo as servicio_vehiculo
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual
from app.modelos.usuario import Usuario

enrutador = APIRouter(
    prefix="/vehiculos",
    tags=["Vehículos"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/", response_model=List[VehiculoRespuesta])
def obtener_vehiculos(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_vehiculo.obtener_todos(bd, skip=skip, limit=limit)

@enrutador.get("/{id_vehiculo}", response_model=VehiculoRespuesta)
def obtener_vehiculo(id_vehiculo: int, bd: Session = Depends(obtener_bd)):
    return servicio_vehiculo.obtener_por_id(bd, id_vehiculo=id_vehiculo)

@enrutador.post("/", response_model=VehiculoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_vehiculo(vehiculo: VehiculoCrear, bd: Session = Depends(obtener_bd)):
    return servicio_vehiculo.crear(bd, vehiculo_crear=vehiculo)

@enrutador.put("/{id_vehiculo}", response_model=VehiculoRespuesta)
def actualizar_vehiculo(id_vehiculo: int, vehiculo: VehiculoActualizar, bd: Session = Depends(obtener_bd)):
    return servicio_vehiculo.actualizar(bd, id_vehiculo=id_vehiculo, vehiculo_actualizar=vehiculo)

@enrutador.delete("/{id_vehiculo}")
def eliminar_vehiculo(id_vehiculo: int, bd: Session = Depends(obtener_bd)):
    return servicio_vehiculo.eliminar(bd, id_vehiculo=id_vehiculo)