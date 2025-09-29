# app/main.py
from fastapi import FastAPI
from app.routers import (
    productos,
    lotes,
    movimientos,
    codigosqr,
    ubicaciones,
    inventario_ubicaciones,
    lotes_rango,
    reportes  # 👈 añadimos esta línea
)

from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    title="API de Inventario PIL",
    version="1.0.0",
    description="Backend para la gestión de inventario (versión móvil y escritorio)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o restringido: ["https://86c8-xxx.ngrok-free.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Registro de endpoints
app.include_router(productos.router, prefix="/api", tags=["Productos"])
app.include_router(lotes.router, prefix="/api", tags=["Lotes"])
app.include_router(movimientos.router, prefix="/api", tags=["Movimientos"])
app.include_router(codigosqr.router, prefix="/api", tags=["Codigos QR"])
app.include_router(ubicaciones.router, prefix="/api", tags=["Ubicaciones"])
app.include_router(inventario_ubicaciones.router, prefix="/api", tags=["Inventario Ubicaciones"])  
app.include_router(lotes_rango.router)
app.include_router(reportes.router)# 👈 nuevo




