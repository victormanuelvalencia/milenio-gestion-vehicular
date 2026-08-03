from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract

from app.modelos.gasto import Gasto
from app.modelos.tipo_gasto import TipoGasto
from app.modelos.viaje import Viaje
from app.modelos.vehiculo import Vehiculo

class ServicioReportes:
    @staticmethod
    def _obtener_query_base_gastos(bd: Session):
        """Retorna una consulta base de Gasto con todas sus relaciones cargadas."""
        return bd.query(Gasto).options(
            joinedload(Gasto.vehiculo),
            joinedload(Gasto.tipo_gasto),
            joinedload(Gasto.proveedor)
        )

    @staticmethod
    def obtener_gastos_por_vehiculo(bd: Session, vehiculo_id: Optional[int], fecha_inicio: Optional[date], fecha_fin: Optional[date]):
        q = ServicioReportes._obtener_query_base_gastos(bd)
        if vehiculo_id:
            q = q.filter(Gasto.vehiculo_id == vehiculo_id)
        if fecha_inicio:
            q = q.filter(Gasto.fecha >= fecha_inicio)
        if fecha_fin:
            q = q.filter(Gasto.fecha <= fecha_fin)
        return q.order_by(Gasto.fecha.desc()).all()

    @staticmethod
    def obtener_gastos_por_mes(bd: Session, anio: int):
        meses_nombres = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        resultados = (
            bd.query(
                extract('month', Gasto.fecha).label('mes'),
                func.count(Gasto.id).label('cantidad'),
                func.sum(Gasto.valor).label('total')
            )
            .filter(extract('year', Gasto.fecha) == anio)
            .group_by(extract('month', Gasto.fecha))
            .order_by(extract('month', Gasto.fecha))
            .all()
        )
        return [
            {
                "mes": int(r.mes),
                "mes_nombre": meses_nombres.get(int(r.mes), str(r.mes)),
                "cantidad": r.cantidad,
                "total": float(r.total or 0)
            }
            for r in resultados
        ]

    @staticmethod
    def obtener_utilidad_por_vehiculo(bd: Session, vehiculo_id: Optional[int], fecha_inicio: Optional[date], fecha_fin: Optional[date]):
        q_vehiculos = bd.query(Vehiculo)
        if vehiculo_id:
            q_vehiculos = q_vehiculos.filter(Vehiculo.id == vehiculo_id)
        
        vehiculos = q_vehiculos.all()
        resultados = []
        
        for v in vehiculos:
            # Calcular ingresos (viajes)
            q_viajes = bd.query(func.sum(Viaje.flete)).filter(Viaje.vehiculo_id == v.id)
            if fecha_inicio:
                q_viajes = q_viajes.filter(Viaje.fecha >= fecha_inicio)
            if fecha_fin:
                q_viajes = q_viajes.filter(Viaje.fecha <= fecha_fin)
            
            ingresos = q_viajes.scalar() or 0.0
            
            # Calcular gastos
            q_gastos = bd.query(func.sum(Gasto.valor)).filter(Gasto.vehiculo_id == v.id)
            if fecha_inicio:
                q_gastos = q_gastos.filter(Gasto.fecha >= fecha_inicio)
            if fecha_fin:
                q_gastos = q_gastos.filter(Gasto.fecha <= fecha_fin)
                
            gastos = q_gastos.scalar() or 0.0
            
            utilidad = float(ingresos) - float(gastos)
            
            if ingresos > 0 or gastos > 0:
                resultados.append({
                    "vehiculo": v.placa,
                    "ingresos": float(ingresos),
                    "gastos": float(gastos),
                    "utilidad": utilidad
                })
                
        resultados.sort(key=lambda x: x["utilidad"], reverse=True)
        return resultados

    @staticmethod
    def obtener_historial_vehiculo(bd: Session, vehiculo_id: Optional[int]):
        q = ServicioReportes._obtener_query_base_gastos(bd)
        if vehiculo_id:
            q = q.filter(Gasto.vehiculo_id == vehiculo_id)
        return q.order_by(Gasto.fecha.desc()).all()

    @staticmethod
    def obtener_costos_entre_fechas(bd: Session, fecha_inicio: Optional[date], fecha_fin: Optional[date]):
        q = ServicioReportes._obtener_query_base_gastos(bd)
        if fecha_inicio:
            q = q.filter(Gasto.fecha >= fecha_inicio)
        if fecha_fin:
            q = q.filter(Gasto.fecha <= fecha_fin)
        return q.order_by(Gasto.fecha.desc()).all()

    @staticmethod
    def obtener_gastos_por_proveedor(bd: Session, proveedor_id: Optional[str]):
        q = ServicioReportes._obtener_query_base_gastos(bd)
        if proveedor_id == "null":
            q = q.filter(Gasto.proveedor_id == None)
        elif proveedor_id and proveedor_id.isdigit():
            q = q.filter(Gasto.proveedor_id == int(proveedor_id))
        return q.order_by(Gasto.fecha.desc()).all()
