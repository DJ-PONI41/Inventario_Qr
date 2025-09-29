from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Boolean
from datetime import datetime
from app.database import Base

class QRPendiente(Base):
    __tablename__ = "QRPendientes"

    Id = Column(Integer, primary_key=True, index=True)
    NumeroLote = Column(String(50), nullable=False)
    CodigoQR = Column(LargeBinary, nullable=False)
    FechaGeneracion = Column(DateTime, default=datetime.now)
    Estado = Column(Boolean, default=True)
