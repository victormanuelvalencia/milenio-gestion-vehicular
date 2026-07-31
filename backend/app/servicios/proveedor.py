from sqlalchemy.orm import Session
from app.modelos.proveedor import Proveedor
from app.esquemas.proveedor import ProveedorCrear, ProveedorActualizar
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def obtener_todos(bd: Session, skip: int = 0, limit: int = 10):
    return bd.query(Proveedor).offset(skip).limit(limit).all()

def obtener_por_id(bd: Session, id_proveedor: int):
    proveedor = bd.query(Proveedor).filter(Proveedor.id == id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor

def crear(bd: Session, proveedor_crear: ProveedorCrear):
    db_proveedor = Proveedor(**proveedor_crear.model_dump())
    try:
        bd.add(db_proveedor)
        bd.commit()
        bd.refresh(db_proveedor)
        return db_proveedor
    except IntegrityError:
        bd.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un proveedor registrado con este NIT.")

def actualizar(bd: Session, id_proveedor: int, proveedor_actualizar: ProveedorActualizar):
    db_proveedor = obtener_por_id(bd, id_proveedor)
    datos_actualizar = proveedor_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_proveedor, clave, valor)
    try:
        bd.commit()
        bd.refresh(db_proveedor)
        return db_proveedor
    except IntegrityError:
        bd.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un proveedor registrado con este NIT.")

def eliminar(bd: Session, id_proveedor: int):
    db_proveedor = obtener_por_id(bd, id_proveedor)
    try:
        bd.delete(db_proveedor)
        bd.commit()
        return {"mensaje": "Proveedor eliminado exitosamente"}
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar este proveedor porque está asociado a uno o más gastos o mantenimientos en el sistema."
        )