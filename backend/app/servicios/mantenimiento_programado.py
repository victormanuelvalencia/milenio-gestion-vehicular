from sqlalchemy.orm import Session
from app.modelos.mantenimiento_programado import MantenimientoProgramado
from app.esquemas.mantenimiento_programado import MantenimientoProgramadoCrear, MantenimientoProgramadoActualizar
from fastapi import HTTPException, status

def obtener_todos(bd: Session, skip: int = 0, limit: int = 1000):
    return bd.query(MantenimientoProgramado).order_by(MantenimientoProgramado.fecha_programada.asc()).offset(skip).limit(limit).all()

def obtener_por_id(bd: Session, id_mantenimiento: int):
    mantenimiento = bd.query(MantenimientoProgramado).filter(MantenimientoProgramado.id == id_mantenimiento).first()
    if not mantenimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento programado no encontrado")
    return mantenimiento

def crear(bd: Session, mantenimiento_crear: MantenimientoProgramadoCrear):
    db_mantenimiento = MantenimientoProgramado(**mantenimiento_crear.model_dump())
    bd.add(db_mantenimiento)
    bd.commit()
    bd.refresh(db_mantenimiento)
    return db_mantenimiento

def actualizar(bd: Session, id_mantenimiento: int, mantenimiento_actualizar: MantenimientoProgramadoActualizar):
    db_mantenimiento = obtener_por_id(bd, id_mantenimiento)
    datos_actualizar = mantenimiento_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_mantenimiento, clave, valor)
    bd.commit()
    bd.refresh(db_mantenimiento)
    return db_mantenimiento

def eliminar(bd: Session, id_mantenimiento: int):
    db_mantenimiento = obtener_por_id(bd, id_mantenimiento)
    bd.delete(db_mantenimiento)
    bd.commit()
    return {"mensaje": "Mantenimiento programado eliminado exitosamente"}
