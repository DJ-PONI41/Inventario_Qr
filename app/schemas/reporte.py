# app/schemas/lotes.py
from pydantic import BaseModel
from datetime import date

class LoteRead(BaseModel):
    IdLote: int
    NumeroLote: str
    IdProducto: int
    CantidadInicial: int
    CantidadActual: int
    FechaFabricacion: date
    FechaVencimiento: date

    class Config:
        orm_mode = True  # 🔁 para usar con SQLAlchemy
