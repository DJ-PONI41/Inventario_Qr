# app/models/lotes.py
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from app.database import Base
from datetime import datetime

class Lote(Base):
    __tablename__ = "Lotes"

    IdLote = Column(Integer, primary_key=True, index=True)
    IdProducto = Column(Integer, ForeignKey("Productos.IdProducto"), nullable=False)
    NumeroLote = Column(String(50), nullable=False)
    FechaVencimiento = Column(Date)
    FechaFabricacion = Column(Date)
    FechaRecepcion = Column(DateTime, default=datetime.now)
    CantidadInicial = Column(Integer, nullable=False)
    CantidadActual = Column(Integer, nullable=False)
    Estado = Column(String(20), default="DISPONIBLE")  # DISPONIBLE, VENCIDO, AGOTADO
