# app/schemas/lotes.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class LoteBase(BaseModel):
    IdProducto: int
    NumeroLote: str
    FechaFabricacion: Optional[date]
    FechaVencimiento: Optional[date]
    FechaRecepcion: Optional[datetime]
    CantidadInicial: int
    CantidadActual: int
    Estado: Optional[str] = "DISPONIBLE"

class LoteCreate(LoteBase):
    pass

class LoteRead(LoteBase):
    IdLote: int

    model_config = {
        "from_attributes": True
    }

class LoteUpdate(BaseModel):
    FechaFabricacion: Optional[date]
    FechaVencimiento: Optional[date]
    FechaRecepcion: Optional[datetime]
    Estado: Optional[str]

    model_config = {
        "from_attributes": True
    }
