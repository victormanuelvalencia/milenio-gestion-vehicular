from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.base_datos.base import Base

class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    nit: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    # Relación uno a muchos con Gastos
    gastos: Mapped[List["Gasto"]] = relationship(back_populates="proveedor")