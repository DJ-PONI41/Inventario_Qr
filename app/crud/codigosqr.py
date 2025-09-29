# app/crud/codigosqr.py
from sqlalchemy.orm import Session
from app.models.codigosqr import CodigoQR
from app.schemas.codigosqr import CodigoQRCreate
from typing import Optional

def crear_codigo_qr(db: Session, qr: CodigoQRCreate):
    nuevo = CodigoQR(**qr.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_por_id(db: Session, id_qr: int):
    return db.query(CodigoQR).filter(CodigoQR.IdQR == id_qr).first()

def obtener_codigos_qr(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    id_lote: Optional[int] = None,
    estado: Optional[bool] = None
):
    query = db.query(CodigoQR)

    if id_lote is not None:
        query = query.filter(CodigoQR.IdLote == id_lote)
    if estado is not None:
        query = query.filter(CodigoQR.Estado == estado)

    total = query.count()
    resultados = query.order_by(CodigoQR.FechaGeneracion.desc()).offset(skip).limit(limit).all()
    return total, resultados

def obtener_activo_por_lote(db: Session, id_lote: int):
    return db.query(CodigoQR).filter(
        CodigoQR.IdLote == id_lote,
        CodigoQR.Estado == True
    ).first()

def desactivar_codigo_qr(db: Session, id_qr: int):
    qr = db.query(CodigoQR).filter(CodigoQR.IdQR == id_qr).first()
    if not qr:
        return None
    qr.Estado = False
    db.commit()
    return qr
