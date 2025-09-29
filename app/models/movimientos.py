# app/models/movimientos.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Movimiento(Base):
    __tablename__ = "Movimientos"

    IdMovimiento = Column(Integer, primary_key=True, index=True)
    IdLote = Column(Integer, ForeignKey("Lotes.IdLote"), nullable=False)
    TipoMovimiento = Column(String(10), nullable=False)  # ENTRADA / SALIDA
    Cantidad = Column(Integer, nullable=False)
    FechaMovimiento = Column(DateTime, default=datetime.now)
    Motivo = Column(String(100))
    DocumentoReferencia = Column(String(50))
    Responsable = Column(String(50), nullable=False)
    Observaciones = Column(String(255))
    FueAnulado = Column(String(2), default="No")