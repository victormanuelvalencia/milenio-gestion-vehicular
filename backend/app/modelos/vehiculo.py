from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean
from app.base_datos.base import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    placa: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    marca: Mapped[str] = mapped_column(String(50))
    ano: Mapped[int] = mapped_column(Integer)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación uno a muchos con Gastos
    gastos: Mapped[List["Gasto"]] = relationship(back_populates="vehiculo", cascade="all, delete-orphan")