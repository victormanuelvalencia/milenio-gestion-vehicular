from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.proveedor import ProveedorRespuesta, ProveedorCrear, ProveedorActualizar
from app.servicios import proveedor as servicio_proveedor
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual
from app.modelos.usuario import Usuario

enrutador = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/", response_model=List[ProveedorRespuesta])
def obtener_proveedores(skip: int = 0, limit: int = 10, bd: Session = Depends(obtener_bd)):
    return servicio_proveedor.obtener_todos(bd, skip=skip, limit=limit)

@enrutador.get("/{id_proveedor}", response_model=ProveedorRespuesta)
def obtener_proveedor(id_proveedor: int, bd: Session = Depends(obtener_bd)):
    return servicio_proveedor.obtener_por_id(bd, id_proveedor=id_proveedor)

@enrutador.post("/", response_model=ProveedorRespuesta, status_code=status.HTTP_201_CREATED)
def crear_proveedor(proveedor: ProveedorCrear, bd: Session = Depends(obtener_bd)):
    return servicio_proveedor.crear(bd, proveedor_crear=proveedor)

@enrutador.put("/{id_proveedor}", response_model=ProveedorRespuesta)
def actualizar_proveedor(id_proveedor: int, proveedor: ProveedorActualizar, bd: Session = Depends(obtener_bd)):
    return servicio_proveedor.actualizar(bd, id_proveedor=id_proveedor, proveedor_actualizar=proveedor)

@enrutador.delete("/{id_proveedor}")
def eliminar_proveedor(id_proveedor: int, bd: Session = Depends(obtener_bd)):
    return servicio_proveedor.eliminar(bd, id_proveedor=id_proveedor)