from sqlalchemy.orm import Session
from app.modelos.vehiculo import Vehiculo
from app.esquemas.vehiculo import VehiculoCrear, VehiculoActualizar
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def obtener_todos(bd: Session, skip: int = 0, limit: int = 10):
    return bd.query(Vehiculo).offset(skip).limit(limit).all()

def obtener_por_id(bd: Session, id_vehiculo: int):
    vehiculo = bd.query(Vehiculo).filter(Vehiculo.id == id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado")
    return vehiculo

def crear(bd: Session, vehiculo_crear: VehiculoCrear):
    db_vehiculo = Vehiculo(**vehiculo_crear.model_dump())
    try:
        bd.add(db_vehiculo)
        bd.commit()
        bd.refresh(db_vehiculo)
        return db_vehiculo
    except IntegrityError as e:
        bd.rollback()
        print(e)
        raise

def actualizar(bd: Session, id_vehiculo: int, vehiculo_actualizar: VehiculoActualizar):
    db_vehiculo = obtener_por_id(bd, id_vehiculo)
    datos_actualizar = vehiculo_actualizar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_vehiculo, clave, valor)
    try:
        bd.commit()
        bd.refresh(db_vehiculo)
        return db_vehiculo
    except IntegrityError:
        bd.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un vehículo registrado con esta placa.")

def eliminar(bd: Session, id_vehiculo: int):
    db_vehiculo = obtener_por_id(bd, id_vehiculo)
    try:
        bd.delete(db_vehiculo)
        bd.commit()
        return {"mensaje": "Vehículo eliminado exitosamente"}
    except IntegrityError:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar este vehículo porque tiene viajes, gastos o mantenimientos asociados en el sistema."
        )