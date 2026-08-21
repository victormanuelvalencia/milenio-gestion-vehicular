from typing import List
from sqlalchemy.orm import Session
from app.modelos.gasto import Gasto
from app.modelos.viaje import Viaje
from app.esquemas.gasto import GastoCrear, GastoActualizar, GastoMasivoItem
from fastapi import HTTPException, status


def _resolver_vehiculo_desde_viaje(bd: Session, datos: dict) -> dict:
    """
    Si se proporciona viaje_id pero no vehiculo_id,
    deduce automáticamente el vehiculo_id desde el viaje asociado.
    """
    if datos.get("viaje_id") and not datos.get("vehiculo_id"):
        viaje = bd.query(Viaje).filter(Viaje.id == datos["viaje_id"]).first()
        if not viaje:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El viaje especificado no existe"
            )
        datos["vehiculo_id"] = viaje.vehiculo_id
    return datos


def _forzar_fecha_desde_viaje(bd: Session, datos: dict) -> dict:
    """
    Si se proporciona viaje_id y el viaje tiene fecha registrada,
    la fecha del gasto se fuerza a coincidir con la del viaje.
    Esto garantiza que todos los gastos de un viaje tengan la misma fecha.
    """
    viaje_id = datos.get("viaje_id")
    if viaje_id:
        viaje = bd.query(Viaje).filter(Viaje.id == viaje_id).first()
        if viaje and viaje.fecha:
            datos["fecha"] = viaje.fecha
    return datos


def obtener_todos(bd: Session, skip: int = 0, limit: int = 10):
    return bd.query(Gasto).offset(skip).limit(limit).all()


def obtener_por_id(bd: Session, id_gasto: int):
    gasto = bd.query(Gasto).filter(Gasto.id == id_gasto).first()
    if not gasto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto no encontrado")
    return gasto


def obtener_por_viaje(bd: Session, id_viaje: int):
    return bd.query(Gasto).filter(Gasto.viaje_id == id_viaje).all()


def crear(bd: Session, gasto_crear: GastoCrear):
    datos = gasto_crear.model_dump()
    datos = _resolver_vehiculo_desde_viaje(bd, datos)
    datos = _forzar_fecha_desde_viaje(bd, datos)

    if not datos.get("vehiculo_id"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe especificar un viaje (número de manifiesto) o un vehículo directamente"
        )

    db_gasto = Gasto(**datos)
    bd.add(db_gasto)
    bd.commit()
    bd.refresh(db_gasto)
    return db_gasto


def actualizar(bd: Session, id_gasto: int, gasto_actualizar: GastoActualizar):
    db_gasto = obtener_por_id(bd, id_gasto)
    datos_actualizar = gasto_actualizar.model_dump(exclude_unset=True)

    # Si cambia el viaje y no se especifica vehiculo_id, re-derivar
    if "viaje_id" in datos_actualizar and "vehiculo_id" not in datos_actualizar:
        datos_actualizar = _resolver_vehiculo_desde_viaje(bd, datos_actualizar)

    # Forzar fecha del viaje (actual o nuevo) si hay viaje_id
    viaje_id = datos_actualizar.get("viaje_id", db_gasto.viaje_id)
    if viaje_id:
        datos_actualizar["viaje_id"] = viaje_id
        datos_actualizar = _forzar_fecha_desde_viaje(bd, datos_actualizar)

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


def crear_masivo(bd: Session, viaje_id: int, gastos_crear: List[GastoMasivoItem]) -> List[Gasto]:
    """
    Registra múltiples gastos asociados a un mismo viaje en una única transacción.
    Si falla cualquier gasto, se hace rollback de toda la operación.
    """
    if not gastos_crear:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe incluir al menos un gasto para registrar"
        )

    # Verificar que el viaje existe y obtener sus datos
    viaje = bd.query(Viaje).filter(Viaje.id == viaje_id).first()
    if not viaje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El viaje especificado no existe"
        )

    gastos_creados = []
    try:
        for item in gastos_crear:
            datos = {
                "viaje_id": viaje_id,
                "vehiculo_id": viaje.vehiculo_id,
                "fecha": viaje.fecha,
                "tipo_gasto_id": item.tipo_gasto_id,
                "valor": item.valor,
                "proveedor_id": item.proveedor_id,
                "proveedor_manual": item.proveedor_manual,
                "observaciones": item.observaciones,
                "verificado_dian": False,
            }
            db_gasto = Gasto(**datos)
            bd.add(db_gasto)
            gastos_creados.append(db_gasto)

        bd.commit()

        for g in gastos_creados:
            bd.refresh(g)

        return gastos_creados

    except HTTPException:
        bd.rollback()
        raise
    except Exception as e:
        bd.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar los gastos. No se guardó ningún gasto."
        ) from e