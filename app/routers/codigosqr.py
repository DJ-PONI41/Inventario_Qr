# app/routers/codigosqr.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import SessionLocal
from app.schemas.codigosqr import CodigoQRCreate, CodigoQRRead
from app.crud import codigosqr as crud_codigosqr

router = APIRouter()

# Dependencia de conexión a la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/codigosqr", response_model=CodigoQRRead)
def crear_codigo_qr(qr: CodigoQRCreate, db: Session = Depends(get_db)):
    existente = crud_codigosqr.obtener_activo_por_lote(db, qr.IdLote)
    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un código QR activo para este lote."
        )
    return crud_codigosqr.crear_codigo_qr(db, qr)


@router.get("/codigosqr/{id_qr}", response_model=CodigoQRRead)
def obtener_codigo_qr(id_qr: int, db: Session = Depends(get_db)):
    qr = crud_codigosqr.obtener_por_id(db, id_qr)
    if not qr:
        raise HTTPException(status_code=404, detail="Código QR no encontrado.")
    return qr

@router.get("/codigosqr")
def listar_codigos_qr(
    skip: int = 0,
    limit: int = 10,
    id_lote: Optional[int] = Query(default=None),
    estado: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db)
):
    total, resultados = crud_codigosqr.obtener_codigos_qr(
        db,
        skip=skip,
        limit=limit,
        id_lote=id_lote,
        estado=estado
    )

    return {
        "Cantidad": total,
        "Data": [CodigoQRRead.from_orm(qr) for qr in resultados]
    }

@router.delete("/codigosqr/{id_qr}")
def eliminar_codigo_qr(id_qr: int, db: Session = Depends(get_db)):
    desactivado = crud_codigosqr.desactivar_codigo_qr(db, id_qr)
    if not desactivado:
        raise HTTPException(status_code=404, detail="Código QR no encontrado.")
    return {"mensaje": "Código QR desactivado correctamente."}
