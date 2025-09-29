# app/schemas/codigosqr.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import base64

# Custom encoder para convertir bytes a base64
def encode_qr(bin_data: bytes) -> str:
    return base64.b64encode(bin_data).decode("utf-8")

class CodigoQRBase(BaseModel):
    IdLote: int
    Estado: Optional[bool] = True

class CodigoQRCreate(CodigoQRBase):
    CodigoQR: bytes  # recibido como base64 (decodificado automáticamente por FastAPI)

class CodigoQRRead(CodigoQRBase):
    IdQR: int
    CodigoQR: str
    FechaGeneracion: datetime

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            bytes: encode_qr
        }
    }
