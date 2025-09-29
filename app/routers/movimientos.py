# app/routers/movimientos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import SessionLocal
from app.schemas.movimientos import MovimientoCreate, MovimientoRead
from app.crud import movimientos as crud_movimientos

router = APIRouter()

# Dependencia de conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/movimientos", response_model=MovimientoRead)
def crear_movimiento(movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    return crud_movimientos.crear_movimiento(db, movimiento)

@router.get("/movimientos/{id_movimiento}", response_model=MovimientoRead)
def obtener_movimiento(id_movimiento: int, db: Session = Depends(get_db)):
    m = crud_movimientos.obtener_por_id(db, id_movimiento)
    if not m:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")
    return m

@router.get("/movimientos")
def listar_movimientos(
    skip: int = 0,
    limit: int = 10,
    tipo: Optional[str] = Query(default=None),
    id_lote: Optional[int] = Query(default=None),
    fecha: Optional[date] = Query(default=None),
    db: Session = Depends(get_db)
):
    total, resultados = crud_movimientos.obtener_movimientos(
        db,
        skip=skip,
        limit=limit,
        tipo=tipo,
        id_lote=id_lote,
        fecha=fecha
    )

    return {
        "Cantidad": total,
        "Data": [MovimientoRead.from_orm(m) for m in resultados]
    }

@router.delete("/movimientos/{id_movimiento}", response_model=MovimientoRead)
def anular_movimiento(id_movimiento: int, db: Session = Depends(get_db)):
    reverso = crud_movimientos.anular_movimiento(db, id_movimiento)
    if not reverso:
        raise HTTPException(status_code=404, detail="Movimiento original no encontrado.")
    return reverso
