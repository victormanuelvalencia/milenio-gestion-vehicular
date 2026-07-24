from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.sql import func
from app.base_datos.base import Base


class RolUsuario:
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"

    VALORES = [SUPERADMIN, ADMIN, USUARIO]


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    correo: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    contrasena_hash: Mapped[str] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    rol: Mapped[str] = mapped_column(String(20), default=RolUsuario.USUARIO)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())