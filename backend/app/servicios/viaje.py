from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modelos.viaje import Viaje
from app.esquemas.viaje import ViajeCrear, ViajeActualizar
from fastapi import HTTPException, status


def obtener_todos(bd: Session, skip: int = 0, limit: int = 1000):
    return bd.query(Viaje).offset(skip).limit(limit).all()


def obtener_por_id(bd: Session, id_viaje: int):
    viaje = bd.query(Viaje).filter(Viaje.id == id_viaje).first()
    if not viaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viaje no encontrado")
    return viaje


def crear(bd: Session, viaje_crear: ViajeCrear):
    db_viaje = Viaje(**viaje_crear.model_dump())
    bd.add(db_viaje)
    try:
        bd.commit()
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de manifiesto ya existe"
        )
    bd.refresh(db_viaje)
    return db_viaje


def actualizar(bd: Session, id_viaje: int, viaje_actualizar: ViajeActualizar):
    db_viaje = obtener_por_id(bd, id_viaje)
    datos_actualizar = viaje_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_viaje, clave, valor)
    try:
        bd.commit()
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de manifiesto ya existe"
        )
    bd.refresh(db_viaje)
    return db_viaje


def eliminar(bd: Session, id_viaje: int):
    db_viaje = obtener_por_id(bd, id_viaje)
    try:
        bd.delete(db_viaje)
        bd.commit()
        return {"mensaje": "Viaje eliminado exitosamente"}
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar este viaje porque tiene gastos u otros registros asociados en el sistema."
        )
