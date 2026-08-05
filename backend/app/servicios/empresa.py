from sqlalchemy.orm import Session
from app.modelos.empresa import Empresa
from app.esquemas.empresa import EmpresaCrear, EmpresaActualizar
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def obtener_todos(bd: Session, skip: int = 0, limit: int = 1000):
    return bd.query(Empresa).offset(skip).limit(limit).all()


def obtener_por_id(bd: Session, id_empresa: int):
    empresa = bd.query(Empresa).filter(Empresa.id == id_empresa).first()
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa no encontrada")
    return empresa


def crear(bd: Session, empresa_crear: EmpresaCrear):
    db_empresa = Empresa(**empresa_crear.model_dump())
    try:
        bd.add(db_empresa)
        bd.commit()
        bd.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una empresa registrada con este nombre."
        )


def actualizar(bd: Session, id_empresa: int, empresa_actualizar: EmpresaActualizar):
    db_empresa = obtener_por_id(bd, id_empresa)
    datos_actualizar = empresa_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_empresa, clave, valor)
    try:
        bd.commit()
        bd.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una empresa registrada con este nombre."
        )


def eliminar(bd: Session, id_empresa: int):
    db_empresa = obtener_por_id(bd, id_empresa)
    try:
        bd.delete(db_empresa)
        bd.commit()
        return {"mensaje": "Empresa eliminada exitosamente"}
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar esta empresa porque está asociada a uno o más viajes en el sistema."
        )
