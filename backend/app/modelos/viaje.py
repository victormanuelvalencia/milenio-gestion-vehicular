from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, ForeignKey, Date
from app.base_datos.base import Base


class Viaje(Base):
    __tablename__ = "viajes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"))
    conductor_id: Mapped[int] = mapped_column(ForeignKey("conductores.id"))
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    origen: Mapped[str] = mapped_column(String(150))
    destino: Mapped[str] = mapped_column(String(150))
    numero_manifiesto: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    flete: Mapped[float] = mapped_column(Numeric(12, 2))
    anticipo: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    fecha: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relaciones
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="viajes")
    conductor: Mapped["Conductor"] = relationship(back_populates="viajes")
    empresa: Mapped["Empresa"] = relationship(back_populates="viajes")
    gastos: Mapped[List["Gasto"]] = relationship(back_populates="viaje")
