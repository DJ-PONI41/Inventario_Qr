from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QRPendienteCreate(BaseModel):
    NumeroLote: str
    CodigoQR: bytes

class QRPendienteRead(QRPendienteCreate):
    Id: int
    FechaGeneracion: datetime
    Estado: bool

    model_config = {
        "from_attributes": True
    }
