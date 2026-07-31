from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event, String

class Base(DeclarativeBase):
    pass

def uppercase_string_fields(mapper, connection, target):
    for col in mapper.columns:
        if isinstance(col.type, String):
            val = getattr(target, col.name)
            if isinstance(val, str):
                # Excluir campos que no deben ser mayúsculas (correos, contraseñas, roles)
                if col.name not in ('correo', 'contrasena_hash', 'rol'):
                    setattr(target, col.name, val.upper())

event.listen(Base, 'before_insert', uppercase_string_fields, propagate=True)
event.listen(Base, 'before_update', uppercase_string_fields, propagate=True)