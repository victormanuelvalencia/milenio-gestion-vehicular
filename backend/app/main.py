from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager

from app.base_datos.inicializar import inicializar_base_datos

@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_base_datos()
    yield

app = FastAPI(
    title="Milenio Gestión Vehicular",
    description="API para el control de gastos y administración de vehículos.",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc).lower()
    if "foreign key" in error_msg or "violates foreign key constraint" in error_msg or "foreign_key" in error_msg or "fk_" in error_msg:
        return JSONResponse(
            status_code=400,
            content={"detail": "No se puede eliminar este registro porque está asociado a uno o más viajes, gastos u otros registros en el sistema."}
        )
    elif "unique constraint" in error_msg or "violates unique constraint" in error_msg:
        return JSONResponse(
            status_code=400,
            content={"detail": "Ya existe un registro con estos datos (valor duplicado)."}
        )
    
    return JSONResponse(
        status_code=400,
        content={"detail": "Error de integridad en la base de datos. Verifica la información enviada."}
    )

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vehiculos.mileniotransportadora.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.rutas import autenticacion, vehiculo, tipo_gasto, proveedor, gasto, reporte, usuario, conductor, viaje, mantenimiento, mantenimiento_programado

app.include_router(autenticacion.enrutador, prefix="/api/v1")
app.include_router(vehiculo.enrutador, prefix="/api/v1")
app.include_router(tipo_gasto.enrutador, prefix="/api/v1")
app.include_router(proveedor.enrutador, prefix="/api/v1")
app.include_router(gasto.enrutador, prefix="/api/v1")
app.include_router(reporte.enrutador, prefix="/api/v1")
app.include_router(usuario.enrutador, prefix="/api/v1")
app.include_router(conductor.enrutador, prefix="/api/v1")
app.include_router(viaje.enrutador, prefix="/api/v1")
app.include_router(mantenimiento.enrutador, prefix="/api/v1")
app.include_router(mantenimiento_programado.enrutador, prefix="/api/v1")

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Milenio Gestión Vehicular"
    }
