from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Numeric, ForeignKey
from app.base_datos.base import Base

class Gasto(Base):
    __tablename__ = "gastos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fecha: Mapped[date] = mapped_column(Date)
    valor: Mapped[float] = mapped_column(Numeric(10, 2))
    
    # Llaves foráneas
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"))
    tipo_gasto_id: Mapped[int] = mapped_column(ForeignKey("tipos_gasto.id"))
    proveedor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("proveedores.id"), nullable=True)
    
    # Campos adicionales
    proveedor_manual: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    verificado_dian: Mapped[bool] = mapped_column(default=False)

    # Relaciones
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="gastos")
    tipo_gasto: Mapped["TipoGasto"] = relationship(back_populates="gastos")
    proveedor: Mapped[Optional["Proveedor"]] = relationship(back_populates="gastos")