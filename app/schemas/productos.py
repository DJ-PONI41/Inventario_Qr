# app/schemas/productos.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductoBase(BaseModel):
    CodigoProducto: str
    Nombre: str
    Descripcion: Optional[str] = None
    StockMinimo: int
    UnidadMedida: str

class ProductoCreate(ProductoBase):
    """Usado al crear un producto nuevo."""
    pass

class ProductoRead(ProductoBase):
    """Usado al devolver datos de productos existentes."""
    IdProducto: int
    Estado: bool
    FechaCreacion: datetime
    FechaModificacion: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class ProductoUpdate(BaseModel):
    Nombre: Optional[str]
    Descripcion: Optional[str]
    StockMinimo: Optional[int]
    UnidadMedida: Optional[str]
    Estado: Optional[bool]

    model_config = {
        "from_attributes": True
    }
