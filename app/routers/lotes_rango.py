from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.database import SessionLocal
from app.schemas.lotes import LoteRead
from app.crud import lotes as crud_lotes

router = APIRouter(prefix="/lotes/rango", tags=["lotes-rango"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=dict)
def listar_lotes_por_rango(
    fecha_inicio: date = Query(..., description="Fecha mínima de vencimiento (YYYY-MM-DD)"),
    fecha_fin: date    = Query(..., description="Fecha máxima de vencimiento (YYYY-MM-DD)"),
    skip: int         = Query(0, ge=0),
    limit: int        = Query(10, ge=1),
    db: Session       = Depends(get_db),
):
    """
    Retorna lotes cuya FechaVencimiento esté
    entre `fecha_inicio` y `fecha_fin`.
    """
    total, resultados = crud_lotes.obtener_lotes_por_rango(
        db,
        skip=skip,
        limit=limit,
        vencimiento_inicio=fecha_inicio,
        vencimiento_fin=fecha_fin,
    )
    if resultados is None:
        raise HTTPException(status_code=404, detail="No se encontraron lotes en ese rango.")
    return {
        "Cantidad": total,
        "Data": [LoteRead.from_orm(l) for l in resultados]
    }
