# app/routers/ubicaciones.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import SessionLocal
from app.schemas.ubicaciones import UbicacionCreate, UbicacionRead
from app.crud import ubicaciones as crud_ubicaciones

from app.schemas.ubicaciones import UbicacionUpdate

router = APIRouter()

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ubicaciones", response_model=UbicacionRead)
def crear_ubicacion(ubicacion: UbicacionCreate, db: Session = Depends(get_db)):
    return crud_ubicaciones.crear_ubicacion(db, ubicacion)

@router.get("/ubicaciones/{id_ubicacion}", response_model=UbicacionRead)
def obtener_ubicacion(id_ubicacion: int, db: Session = Depends(get_db)):
    u = crud_ubicaciones.obtener_por_id(db, id_ubicacion)
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada.")
    return u

@router.get("/ubicaciones")
def listar_ubicaciones(
    skip: int = 0,
    limit: int = 10,
    ciudad: Optional[str] = Query(default=None),
    tipo: Optional[str] = Query(default=None),
    estado: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db)
):
    total, resultados = crud_ubicaciones.obtener_ubicaciones(
        db,
        skip=skip,
        limit=limit,
        ciudad=ciudad,
        tipo=tipo,
        estado=estado
    )

    return {
        "Cantidad": total,
        "Data": [UbicacionRead.from_orm(u) for u in resultados]
    }



@router.put("/ubicaciones/{id_ubicacion}", response_model=UbicacionRead)
def editar_ubicacion(id_ubicacion: int, datos: UbicacionUpdate, db: Session = Depends(get_db)):
    actualizada = crud_ubicaciones.actualizar_ubicacion(db, id_ubicacion, datos)
    if not actualizada:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada.")
    return actualizada

@router.delete("/ubicaciones/{id_ubicacion}")
def eliminar_ubicacion(id_ubicacion: int, db: Session = Depends(get_db)):
    desactivada = crud_ubicaciones.desactivar_ubicacion(db, id_ubicacion)
    if not desactivada:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada.")
    return {"mensaje": "Ubicación desactivada correctamente."}
