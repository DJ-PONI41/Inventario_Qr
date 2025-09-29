from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class MovimientoBase(BaseModel):
    IdLote: int
    TipoMovimiento: Literal["ENTRADA", "SALIDA"]
    Cantidad: int = Field(gt=0, description="Debe ser mayor a 0")
    Motivo: Optional[str] = None
    DocumentoReferencia: Optional[str] = None
    Responsable: str
    Observaciones: Optional[str] = None

class MovimientoCreate(MovimientoBase):
    pass

class MovimientoRead(MovimientoBase):
    IdMovimiento: int
    FechaMovimiento: datetime
    FueAnulado: str

    model_config = {
        "from_attributes": True
    }
