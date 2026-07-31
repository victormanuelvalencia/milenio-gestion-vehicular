from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Numeric, ForeignKey, Integer
from app.base_datos.base import Base

class Mantenimiento(Base):
    __tablename__ = "mantenimientos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fecha: Mapped[date] = mapped_column(Date)
    kilometraje: Mapped[int] = mapped_column(Integer)
    valor: Mapped[float] = mapped_column(Numeric(10, 2))
    
    # Llaves foráneas
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"))
    proveedor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("proveedores.id", ondelete="SET NULL"), nullable=True)
    
    # Campos adicionales
    descripcion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    proveedor_manual: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    # Relaciones
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="mantenimientos")
    proveedor: Mapped[Optional["Proveedor"]] = relationship(back_populates="mantenimientos")
