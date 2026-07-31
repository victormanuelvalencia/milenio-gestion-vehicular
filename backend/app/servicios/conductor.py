from sqlalchemy.orm import Session
from app.modelos.conductor import Conductor
from app.esquemas.conductor import ConductorCrear, ConductorActualizar
from fastapi import HTTPException, status


def obtener_todos(bd: Session, skip: int = 0, limit: int = 1000):
    return bd.query(Conductor).offset(skip).limit(limit).all()


def obtener_por_id(bd: Session, id_conductor: int):
    conductor = bd.query(Conductor).filter(Conductor.id == id_conductor).first()
    if not conductor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conductor no encontrado")
    return conductor


def crear(bd: Session, conductor_crear: ConductorCrear):
    db_conductor = Conductor(**conductor_crear.model_dump())
    bd.add(db_conductor)
    bd.commit()
    bd.refresh(db_conductor)
    return db_conductor


def actualizar(bd: Session, id_conductor: int, conductor_actualizar: ConductorActualizar):
    db_conductor = obtener_por_id(bd, id_conductor)
    datos_actualizar = conductor_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_conductor, clave, valor)
    bd.commit()
    bd.refresh(db_conductor)
    return db_conductor


def eliminar(bd: Session, id_conductor: int):
    db_conductor = obtener_por_id(bd, id_conductor)
    bd.delete(db_conductor)
    bd.commit()
    return {"mensaje": "Conductor eliminado exitosamente"}
