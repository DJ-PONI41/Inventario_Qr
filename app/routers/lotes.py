# app/routers/lotes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import SessionLocal
from app.schemas.lotes import LoteCreate, LoteRead
from app.crud import lotes as crud_lotes

from app.schemas.lotes import LoteUpdate

router = APIRouter()

# Dependencia de conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/lotes", response_model=LoteRead)
def crear_lote(lote: LoteCreate, db: Session = Depends(get_db)):
    existente = crud_lotes.obtener_por_numero_lote(db, lote.IdProducto, lote.NumeroLote)
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un lote con ese número para este producto.")
    return crud_lotes.crear_lote(db, lote)


@router.get("/lotes/{id_lote}", response_model=LoteRead)
def obtener_lote(id_lote: int, db: Session = Depends(get_db)):
    lote = crud_lotes.obtener_por_id(db, id_lote)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado.")
    return lote

@router.get("/lotes")
def listar_lotes(
    skip: int = 0,
    limit: int = 10,
    numero_lote: Optional[str] = Query(default=None),
    estado: Optional[str] = Query(default=None),
    idProducto: Optional[str] = Query(default=None),
    vencimiento: Optional[date] = Query(default=None),
    db: Session = Depends(get_db)
):
    total, resultados = crud_lotes.obtener_lotes(
        db,
        skip=skip,
        limit=limit,
        numero_lote=numero_lote,
        estado=estado,
        idProducto=idProducto,
        vencimiento=vencimiento
    )

    return {
        "Cantidad": total,
        "Data": [LoteRead.from_orm(l) for l in resultados]
    }


@router.put("/lotes/{id_lote}", response_model=LoteRead)
def editar_lote(id_lote: int, datos: LoteUpdate, db: Session = Depends(get_db)):
    lote = crud_lotes.actualizar_lote(db, id_lote, datos)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado.")
    return lote

@router.delete("/lotes/{id_lote}")
def eliminar_lote(id_lote: int, db: Session = Depends(get_db)):
    eliminado = crud_lotes.desactivar_lote(db, id_lote)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Lote no encontrado.")
    return {"mensaje": "Lote marcado como AGOTADO correctamente"}
