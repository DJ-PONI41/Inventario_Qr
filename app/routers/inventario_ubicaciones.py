# app/routers/inventario_ubicaciones.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import SessionLocal
from app.schemas.inventario_ubicaciones import InventarioUbicacionCreate, InventarioUbicacionRead
from app.crud import inventario_ubicaciones as crud_inv

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/inventario", response_model=InventarioUbicacionRead)
def crear_inventario(inventario: InventarioUbicacionCreate, db: Session = Depends(get_db)):
    return crud_inv.crear_inventario(db, inventario)

@router.get("/inventario/{id_inventario}", response_model=InventarioUbicacionRead)
def obtener_inventario_por_id(id_inventario: int, db: Session = Depends(get_db)):
    inv = crud_inv.obtener_por_id(db, id_inventario)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado.")
    return inv

@router.get("/inventario")
def listar_inventario(
    skip: int = 0,
    limit: int = 10,
    id_ubicacion: Optional[int] = Query(default=None),
    id_lote: Optional[int] = Query(default=None),
    seccion: Optional[str] = Query(default=None),
    posicion: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
):
    total, resultados = crud_inv.obtener_inventario(
        db,
        skip=skip,
        limit=limit,
        id_ubicacion=id_ubicacion,
        id_lote=id_lote,
        seccion=seccion,
        posicion=posicion
    )

    return {
        "Cantidad": total,
        "Data": [InventarioUbicacionRead.from_orm(i) for i in resultados]
    }

from app.schemas.inventario_ubicaciones import InventarioUbicacionUpdate

@router.put("/inventario/{id_inventario}", response_model=InventarioUbicacionRead)
def editar_inventario(id_inventario: int, datos: InventarioUbicacionUpdate, db: Session = Depends(get_db)):
    actualizado = crud_inv.actualizar_inventario(db, id_inventario, datos)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado.")
    return actualizado

@router.delete("/inventario/{id_inventario}")
def eliminar_inventario(id_inventario: int, db: Session = Depends(get_db)):
    eliminado = crud_inv.eliminar_inventario(db, id_inventario)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado.")
    return {"mensaje": "Registro de inventario eliminado correctamente."}
