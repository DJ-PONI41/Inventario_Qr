# app/models/productos.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database import Base

class Producto(Base):
    __tablename__ = "Productos"

    IdProducto = Column(Integer, primary_key=True, index=True)
    CodigoProducto = Column(String(20), unique=True, nullable=False)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(255))
    StockMinimo = Column(Integer, default=0)
    UnidadMedida = Column(String(20), nullable=False)
    Estado = Column(Boolean, default=True)
    FechaCreacion = Column(DateTime, default=datetime.now)
    FechaModificacion = Column(DateTime, nullable=True)
