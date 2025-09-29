# app/crud/movimientos.py
from sqlalchemy.orm import Session
from app.models.movimientos import Movimiento
from app.schemas.movimientos import MovimientoCreate
from typing import Optional
from datetime import date

from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime
from app.models.lotes import Lote
from app.schemas.movimientos import MovimientoCreate

from sqlalchemy import cast, Date


def crear_movimiento(db: Session, movimiento: MovimientoCreate):
    try:
        lote = db.query(Lote).filter(Lote.IdLote == movimiento.IdLote).first()
        if not lote:
            raise HTTPException(status_code=404, detail="Lote no encontrado.")

        if movimiento.TipoMovimiento.upper() == "ENTRADA":
            lote.CantidadActual += movimiento.Cantidad

        elif movimiento.TipoMovimiento.upper() == "SALIDA":
            if lote.CantidadActual < movimiento.Cantidad:
                raise HTTPException(
                    status_code=400,
                    detail="Stock insuficiente para realizar la salida."
                )
            lote.CantidadActual -= movimiento.Cantidad

        # Actualizar fecha de modificación del lote
        lote.FechaModificacion = datetime.now()

        # Registrar movimiento
        nuevo = Movimiento(**movimiento.dict())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar movimiento: {str(e)}")

def obtener_por_id(db: Session, id_movimiento: int):
    return db.query(Movimiento).filter(Movimiento.IdMovimiento == id_movimiento).first()

def obtener_movimientos(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    tipo: Optional[str] = None,
    id_lote: Optional[int] = None,
    fecha: Optional[date] = None
):
    query = db.query(Movimiento)

    if tipo:
        query = query.filter(Movimiento.TipoMovimiento == tipo.upper())
    if id_lote:
        query = query.filter(Movimiento.IdLote == id_lote)
    if fecha:
        query = query.filter(cast(Movimiento.FechaMovimiento, Date) == fecha)

    total = query.count()
    resultados = query.order_by(Movimiento.FechaMovimiento.desc()).offset(skip).limit(limit).all()
    return total, resultados

def anular_movimiento(db: Session, id_movimiento: int):
    original = db.query(Movimiento).filter(Movimiento.IdMovimiento == id_movimiento).first()
    if not original:
        return None

    lote = db.query(Lote).filter(Lote.IdLote == original.IdLote).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado.")

    # Evitar anular dos veces
    if original.FueAnulado == "Si":
        raise HTTPException(status_code=400, detail="Este movimiento ya fue anulado.")

    # Determinar tipo inverso
    tipo_inverso = "SALIDA" if original.TipoMovimiento == "ENTRADA" else "ENTRADA"

    # Validar stock si es una SALIDA inversa
    if tipo_inverso == "SALIDA" and lote.CantidadActual < original.Cantidad:
        raise HTTPException(
            status_code=400,
            detail="No hay suficiente stock para anular este movimiento."
        )

    # Ajustar stock
    if tipo_inverso == "ENTRADA":
        lote.CantidadActual += original.Cantidad
    else:
        lote.CantidadActual -= original.Cantidad

    lote.FechaModificacion = datetime.now()

    # Marcar original como anulado
    original.FueAnulado = "Si"

    # Crear movimiento reverso
    reverso = Movimiento(
        IdLote=original.IdLote,
        TipoMovimiento=tipo_inverso,
        Cantidad=original.Cantidad,
        Motivo="ANULACIÓN",
        DocumentoReferencia=f"Reverso de ID {id_movimiento}",
        Responsable=original.Responsable,
        Observaciones=f"Anulación automática del movimiento ID {id_movimiento}"
    )

    db.add(reverso)
    db.commit()
    db.refresh(reverso)
    return reverso
