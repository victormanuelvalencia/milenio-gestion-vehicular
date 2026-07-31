from sqlalchemy.orm import Session
from app.modelos.tipo_gasto import TipoGasto
from app.esquemas.tipo_gasto import TipoGastoCrear, TipoGastoActualizar
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def obtener_todos(bd: Session, skip: int = 0, limit: int = 10):
    return bd.query(TipoGasto).offset(skip).limit(limit).all()

def obtener_por_id(bd: Session, id_tipo: int):
    tipo = bd.query(TipoGasto).filter(TipoGasto.id == id_tipo).first()
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de gasto no encontrado")
    return tipo

def crear(bd: Session, tipo_crear: TipoGastoCrear):
    db_tipo = TipoGasto(**tipo_crear.model_dump())
    bd.add(db_tipo)
    bd.commit()
    bd.refresh(db_tipo)
    return db_tipo

def actualizar(bd: Session, id_tipo: int, tipo_actualizar: TipoGastoActualizar):
    db_tipo = obtener_por_id(bd, id_tipo)
    datos_actualizar = tipo_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_tipo, clave, valor)
    bd.commit()
    bd.refresh(db_tipo)
    return db_tipo

def eliminar(bd: Session, id_tipo: int):
    db_tipo = obtener_por_id(bd, id_tipo)
    try:
        bd.delete(db_tipo)
        bd.commit()
        return {"mensaje": "Tipo de gasto eliminado exitosamente"}
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar este tipo de gasto porque está asociado a uno o más gastos registrados en el sistema."
        )