# app/models/ubicaciones.py
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from app.database import Base

class Ubicacion(Base):
    __tablename__ = "Ubicaciones"

    IdUbicacion = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(50), nullable=False)
    Descripcion = Column(String(100))
    Responsable = Column(String(50))
    Latitud = Column(DECIMAL(10, 8), nullable=False)
    Longitud = Column(DECIMAL(11, 8), nullable=False)
    Direccion = Column(String(255))
    Ciudad = Column(String(50))
    Zona = Column(String(50))
    TipoUbicacion = Column(String(30))  # BODEGA, PUNTO_VENTA, PLANTA, etc.
    Estado = Column(Boolean, default=True)
