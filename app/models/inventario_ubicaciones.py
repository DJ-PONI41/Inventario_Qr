# app/models/inventario_ubicaciones.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class InventarioUbicacion(Base):
    __tablename__ = "InventarioUbicaciones"

    IdInventarioUbicacion = Column(Integer, primary_key=True, index=True)
    IdLote = Column(Integer, ForeignKey("Lotes.IdLote"), nullable=False)
    IdUbicacion = Column(Integer, ForeignKey("Ubicaciones.IdUbicacion"), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    Seccion = Column(String(50))
    Posicion = Column(String(50))
    FechaUltimaActualizacion = Column(DateTime, default=datetime.now)
