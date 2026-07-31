from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from app.base_datos.base import Base


class Conductor(Base):
    __tablename__ = "conductores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    cedula: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)
