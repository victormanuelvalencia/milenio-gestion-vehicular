from sqlalchemy.orm import Session
from app.modelos.mantenimiento import Mantenimiento
from app.esquemas.mantenimiento import MantenimientoCrear, MantenimientoActualizar
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def obtener_todos(bd: Session, skip: int = 0, limit: int = 1000):
    return bd.query(Mantenimiento).order_by(Mantenimiento.fecha.desc()).offset(skip).limit(limit).all()

def obtener_por_id(bd: Session, id_mantenimiento: int):
    mantenimiento = bd.query(Mantenimiento).filter(Mantenimiento.id == id_mantenimiento).first()
    if not mantenimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
    return mantenimiento

def crear(bd: Session, mantenimiento_crear: MantenimientoCrear):
    db_mantenimiento = Mantenimiento(**mantenimiento_crear.model_dump())
    bd.add(db_mantenimiento)
    bd.commit()
    bd.refresh(db_mantenimiento)
    return db_mantenimiento

def actualizar(bd: Session, id_mantenimiento: int, mantenimiento_actualizar: MantenimientoActualizar):
    db_mantenimiento = obtener_por_id(bd, id_mantenimiento)
    datos_actualizar = mantenimiento_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_mantenimiento, clave, valor)
    bd.commit()
    bd.refresh(db_mantenimiento)
    return db_mantenimiento

def eliminar(bd: Session, id_mantenimiento: int):
    db_mantenimiento = obtener_por_id(bd, id_mantenimiento)
    try:
        bd.delete(db_mantenimiento)
        bd.commit()
        return {"mensaje": "Mantenimiento eliminado exitosamente"}
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar este mantenimiento porque está referenciado en otros registros del sistema."
        )
