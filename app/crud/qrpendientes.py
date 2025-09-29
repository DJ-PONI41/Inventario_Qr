from sqlalchemy.orm import Session
from app.models.qrpendientes import QRPendiente
from app.schemas.qrpendientes import QRPendienteCreate
from typing import Optional

def crear_qr_pendiente(db: Session, data: QRPendienteCreate):
    nuevo = QRPendiente(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_por_numero_lote(db: Session, numero_lote: str) -> Optional[QRPendiente]:
    return db.query(QRPendiente).filter(QRPendiente.NumeroLote == numero_lote, QRPendiente.Estado == True).first()

def eliminar_qr_pendiente(db: Session, id: int):
    qr = db.query(QRPendiente).filter(QRPendiente.Id == id).first()
    if qr:
        db.delete(qr)
        db.commit()
