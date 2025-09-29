# app/schemas/ubicaciones.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class UbicacionBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    Responsable: Optional[str] = None
    Latitud: Decimal
    Longitud: Decimal
    Direccion: Optional[str] = None
    Ciudad: Optional[str] = None
    Zona: Optional[str] = None
    TipoUbicacion: Optional[str] = None
    Estado: Optional[bool] = True

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionRead(UbicacionBase):
    IdUbicacion: int

    model_config = {
        "from_attributes": True
    }

class UbicacionUpdate(BaseModel):
    Nombre: Optional[str] = None
    Descripcion: Optional[str] = None
    Responsable: Optional[str] = None
    Latitud: Optional[Decimal] = None
    Longitud: Optional[Decimal] = None
    Direccion: Optional[str] = None
    Ciudad: Optional[str] = None
    Zona: Optional[str] = None
    TipoUbicacion: Optional[str] = None
    Estado: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
