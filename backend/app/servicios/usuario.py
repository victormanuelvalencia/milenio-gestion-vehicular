from sqlalchemy.orm import Session
from app.modelos.usuario import Usuario
from app.esquemas.usuario import UsuarioCrear, UsuarioActualizar
from app.seguridad.contrasenas import obtener_hash_contrasena
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def obtener_todos(bd: Session, skip: int = 0, limit: int = 1000):
    return bd.query(Usuario).offset(skip).limit(limit).all()

def obtener_por_id(bd: Session, id_usuario: int):
    usuario = bd.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

def crear(bd: Session, usuario_crear: UsuarioCrear):
    db_usuario = bd.query(Usuario).filter(Usuario.correo == usuario_crear.correo).first()
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado.")
    
    hash_contrasena = obtener_hash_contrasena(usuario_crear.contrasena)
    
    nuevo_usuario = Usuario(
        nombre=usuario_crear.nombre,
        correo=usuario_crear.correo,
        contrasena_hash=hash_contrasena,
        rol=usuario_crear.rol,
        activo=usuario_crear.activo
    )
    
    try:
        bd.add(nuevo_usuario)
        bd.commit()
        bd.refresh(nuevo_usuario)
        return nuevo_usuario
    except IntegrityError:
        bd.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el usuario.")

def actualizar(bd: Session, id_usuario: int, usuario_actualizar: UsuarioActualizar):
    db_usuario = obtener_por_id(bd, id_usuario)
    
    datos_actualizar = usuario_actualizar.model_dump(exclude_unset=True)
    
    if "correo" in datos_actualizar and datos_actualizar["correo"] != db_usuario.correo:
        usuario_existente = bd.query(Usuario).filter(Usuario.correo == datos_actualizar["correo"]).first()
        if usuario_existente:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado por otro usuario.")

    for clave, valor in datos_actualizar.items():
        setattr(db_usuario, clave, valor)
        
    try:
        bd.commit()
        bd.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        bd.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el usuario.")

def eliminar(bd: Session, id_usuario: int):
    db_usuario = obtener_por_id(bd, id_usuario)
    bd.delete(db_usuario)
    bd.commit()
    return {"mensaje": "Usuario eliminado exitosamente"}

def cambiar_contrasena(bd: Session, id_usuario: int, nueva_contrasena: str):
    db_usuario = obtener_por_id(bd, id_usuario)
    db_usuario.contrasena_hash = obtener_hash_contrasena(nueva_contrasena)
    bd.commit()
    return {"mensaje": "Contraseña actualizada exitosamente"}

def cambiar_estado(bd: Session, id_usuario: int, activo: bool):
    db_usuario = obtener_por_id(bd, id_usuario)
    db_usuario.activo = activo
    bd.commit()
    bd.refresh(db_usuario)
    return db_usuario

def cambiar_rol(bd: Session, id_usuario: int, nuevo_rol: str):
    db_usuario = obtener_por_id(bd, id_usuario)
    db_usuario.rol = nuevo_rol
    bd.commit()
    bd.refresh(db_usuario)
    return db_usuario
