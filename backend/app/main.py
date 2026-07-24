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
    version="1.0.0"
)

from app.api.rutas import autenticacion, vehiculo, tipo_gasto, proveedor, gasto

app.include_router(autenticacion.enrutador, prefix="/api/v1")
app.include_router(vehiculo.enrutador, prefix="/api/v1")
app.include_router(tipo_gasto.enrutador, prefix="/api/v1")
app.include_router(proveedor.enrutador, prefix="/api/v1")
app.include_router(gasto.enrutador, prefix="/api/v1")

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Milenio Gestión Vehicular"
    }