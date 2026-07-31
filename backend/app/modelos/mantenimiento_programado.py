from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey
from app.base_datos.base import Base

class MantenimientoProgramado(Base):
    __tablename__ = "mantenimientos_programados"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"))
    descripcion: Mapped[str] = mapped_column(String(255))
    fecha_programada: Mapped[date] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(20), default="Pendiente")

    # Relaciones
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="mantenimientos_programados")
