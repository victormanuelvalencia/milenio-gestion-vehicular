from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.esquemas.usuario import (
    UsuarioRespuesta, 
    UsuarioCrear, 
    UsuarioActualizar,
    CambiarContrasena,
    CambiarEstado,
    CambiarRol
)
from app.servicios import usuario as servicio_usuario
from app.dependencias.base_datos import obtener_bd
from app.dependencias.seguridad import obtener_usuario_actual, requerir_superadmin
from app.modelos.usuario import Usuario

enrutador = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    dependencies=[Depends(obtener_usuario_actual)]
)

@enrutador.get("/", response_model=List[UsuarioRespuesta])
def obtener_usuarios(skip: int = 0, limit: int = 1000, bd: Session = Depends(obtener_bd)):
    return servicio_usuario.obtener_todos(bd, skip=skip, limit=limit)

@enrutador.get("/{id_usuario}", response_model=UsuarioRespuesta)
def obtener_usuario(id_usuario: int, bd: Session = Depends(obtener_bd)):
    return servicio_usuario.obtener_por_id(bd, id_usuario=id_usuario)

@enrutador.post("/", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCrear, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_usuario.crear(bd, usuario_crear=usuario)

@enrutador.put("/{id_usuario}", response_model=UsuarioRespuesta)
def actualizar_usuario(id_usuario: int, usuario: UsuarioActualizar, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_usuario.actualizar(bd, id_usuario=id_usuario, usuario_actualizar=usuario)

@enrutador.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_usuario.eliminar(bd, id_usuario=id_usuario)

@enrutador.patch("/{id_usuario}/estado", response_model=UsuarioRespuesta)
def cambiar_estado(id_usuario: int, estado: CambiarEstado, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_usuario.cambiar_estado(bd, id_usuario=id_usuario, activo=estado.activo)

@enrutador.patch("/{id_usuario}/rol", response_model=UsuarioRespuesta)
def cambiar_rol(id_usuario: int, rol: CambiarRol, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_usuario.cambiar_rol(bd, id_usuario=id_usuario, nuevo_rol=rol.rol)

@enrutador.patch("/{id_usuario}/contrasena")
def cambiar_contrasena(id_usuario: int, contrasenas: CambiarContrasena, bd: Session = Depends(obtener_bd), _: Usuario = Depends(requerir_superadmin)):
    return servicio_usuario.cambiar_contrasena(bd, id_usuario=id_usuario, nueva_contrasena=contrasenas.contrasena_nueva)
