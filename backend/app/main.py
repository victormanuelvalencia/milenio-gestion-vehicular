from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI

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

from app.api.rutas import autenticacion, vehiculo, tipo_gasto, proveedor, gasto, reporte, usuario, conductor, viaje

app.include_router(autenticacion.enrutador, prefix="/api/v1")
app.include_router(vehiculo.enrutador, prefix="/api/v1")
app.include_router(tipo_gasto.enrutador, prefix="/api/v1")
app.include_router(proveedor.enrutador, prefix="/api/v1")
app.include_router(gasto.enrutador, prefix="/api/v1")
app.include_router(reporte.enrutador, prefix="/api/v1")
app.include_router(usuario.enrutador, prefix="/api/v1")
app.include_router(conductor.enrutador, prefix="/api/v1")
app.include_router(viaje.enrutador, prefix="/api/v1")

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Milenio Gestión Vehicular"
    }
