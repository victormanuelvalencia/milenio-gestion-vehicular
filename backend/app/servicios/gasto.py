from sqlalchemy.orm import Session
from app.modelos.gasto import Gasto
from app.esquemas.gasto import GastoCrear, GastoActualizar
from fastapi import HTTPException, status

def obtener_todos(bd: Session, skip: int = 0, limit: int = 10):
    return bd.query(Gasto).offset(skip).limit(limit).all()

def obtener_por_id(bd: Session, id_gasto: int):
    gasto = bd.query(Gasto).filter(Gasto.id == id_gasto).first()
    if not gasto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto no encontrado")
    return gasto

def crear(bd: Session, gasto_crear: GastoCrear):
    db_gasto = Gasto(**gasto_crear.model_dump())
    bd.add(db_gasto)
    bd.commit()
    bd.refresh(db_gasto)
    return db_gasto

def actualizar(bd: Session, id_gasto: int, gasto_actualizar: GastoActualizar):
    db_gasto = obtener_por_id(bd, id_gasto)
    datos_actualizar = gasto_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_gasto, clave, valor)
    bd.commit()
    bd.refresh(db_gasto)
    return db_gasto

def eliminar(bd: Session, id_gasto: int):
    db_gasto = obtener_por_id(bd, id_gasto)
    bd.delete(db_gasto)
    bd.commit()
    return {"mensaje": "Gasto eliminado exitosamente"}