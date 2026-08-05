from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.base_datos.base import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True, index=True)

    # Relaciones
    viajes: Mapped[List["Viaje"]] = relationship(back_populates="empresa")
