from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.empresa import EmpresaRespuesta, EmpresaCrear, EmpresaActualizar
from app.servicios import empresa as servicio_empresa
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual, requerir_superadmin
from app.modelos.usuario import Usuario

enrutador = APIRouter(
    prefix="/empresas",
    tags=["Empresas"],
    dependencies=[Depends(obtener_usuario_actual)]
)


@enrutador.get("/", response_model=List[EmpresaRespuesta])
def obtener_empresas(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_empresa.obtener_todos(bd, skip=skip, limit=limit)


@enrutador.get("/{id_empresa}", response_model=EmpresaRespuesta)
def obtener_empresa(id_empresa: int, bd: Session = Depends(obtener_bd)):
    return servicio_empresa.obtener_por_id(bd, id_empresa=id_empresa)


@enrutador.post("/", response_model=EmpresaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_empresa(empresa: EmpresaCrear, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_empresa.crear(bd, empresa_crear=empresa)


@enrutador.put("/{id_empresa}", response_model=EmpresaRespuesta)
def actualizar_empresa(id_empresa: int, empresa: EmpresaActualizar, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_empresa.actualizar(bd, id_empresa=id_empresa, empresa_actualizar=empresa)


@enrutador.delete("/{id_empresa}")
def eliminar_empresa(id_empresa: int, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_empresa.eliminar(bd, id_empresa=id_empresa)
