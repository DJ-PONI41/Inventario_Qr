# app/crud/lotes.py
from sqlalchemy.orm import Session
from app.models.lotes import Lote
from app.schemas.lotes import LoteCreate
from datetime import date
from typing import Optional

from app.schemas.lotes import LoteUpdate

from sqlalchemy import cast, Date

def crear_lote(db: Session, lote: LoteCreate):
    nuevo = Lote(**lote.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_por_id(db: Session, id_lote: int):
    return db.query(Lote).filter(Lote.IdLote == id_lote).first()


def obtener_lotes(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    numero_lote: Optional[str] = None,
    estado: Optional[str] = None,
    idProducto: Optional[str] = None,
    vencimiento: Optional[date] = None
):
    query = db.query(Lote)

    if numero_lote:
        query = query.filter(Lote.NumeroLote.ilike(f"%{numero_lote}%"))
    if estado:
        query = query.filter(Lote.Estado == estado)
    if idProducto:
        query = query.filter(Lote.IdProducto == idProducto)
    if vencimiento:
        query = query.filter(cast(Lote.FechaVencimiento, Date) == vencimiento)

    total = query.count()
    resultados = query.order_by(Lote.IdLote).offset(skip).limit(limit).all()
    return total, resultados

def obtener_por_numero_lote(db: Session, id_producto: int, numero_lote: str):
    return db.query(Lote).filter(
        Lote.IdProducto == id_producto,
        Lote.NumeroLote == numero_lote
    ).first()

def actualizar_lote(db: Session, id_lote: int, datos: LoteUpdate):
    lote = db.query(Lote).filter(Lote.IdLote == id_lote).first()
    if not lote:
        return None

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(lote, campo, valor)

    db.commit()
    db.refresh(lote)
    return lote

def desactivar_lote(db: Session, id_lote: int):
    lote = db.query(Lote).filter(Lote.IdLote == id_lote).first()
    if not lote:
        return None
    lote.Estado = "AGOTADO"
    db.commit()
    return lote


def obtener_lotes_por_rango(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    numero_lote: Optional[str] = None,
    estado: Optional[str] = None,
    idProducto: Optional[str] = None,
    vencimiento_inicio: Optional[date] = None,
    vencimiento_fin: Optional[date] = None
):
    query = db.query(Lote)

    if numero_lote:
        query = query.filter(Lote.NumeroLote.ilike(f"%{numero_lote}%"))
    if estado:
        query = query.filter(Lote.Estado == estado)
    if idProducto:
        query = query.filter(Lote.IdProducto == idProducto)
    if vencimiento_inicio and vencimiento_fin:
        # FechaVencimiento entre inicio y fin (inclusive)
        query = query.filter(
            cast(Lote.FechaVencimiento, Date) >= vencimiento_inicio,
            cast(Lote.FechaVencimiento, Date) <= vencimiento_fin
        )

    total = query.count()
    resultados = query.order_by(Lote.IdLote).offset(skip).limit(limit).all()
    return total, resultados