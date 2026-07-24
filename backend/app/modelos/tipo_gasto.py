from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.base_datos.base import Base

class TipoGasto(Base):
    __tablename__ = "tipos_gasto"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))

    # Relación uno a muchos con Gastos
    gastos: Mapped[List["Gasto"]] = relationship(back_populates="tipo_gasto")