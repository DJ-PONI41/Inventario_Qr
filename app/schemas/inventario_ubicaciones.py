from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InventarioUbicacionBase(BaseModel):
    IdLote: int
    IdUbicacion: int
    Cantidad: int = Field(gt=0, description="Debe ser mayor que cero")
    Seccion: Optional[str] = None
    Posicion: Optional[str] = None

class InventarioUbicacionCreate(InventarioUbicacionBase):
    pass

class InventarioUbicacionUpdate(BaseModel):
    Cantidad: Optional[int] = Field(default=None, gt=0)
    Seccion: Optional[str] = None
    Posicion: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class InventarioUbicacionRead(InventarioUbicacionBase):
    IdInventarioUbicacion: int
    FechaUltimaActualizacion: datetime

    model_config = {
        "from_attributes": True
    }
