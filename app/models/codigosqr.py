# app/models/codigosqr.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, LargeBinary, Boolean
from app.database import Base
from datetime import datetime

class CodigoQR(Base):
    __tablename__ = "CodigosQR"

    IdQR = Column(Integer, primary_key=True, index=True)
    IdLote = Column(Integer, ForeignKey("Lotes.IdLote"), nullable=False)
    CodigoQR = Column(LargeBinary)  # Binario QR
    FechaGeneracion = Column(DateTime, default=datetime.now)
    Estado = Column(Boolean, default=True)
