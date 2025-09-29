# app/crud/inventario_ubicaciones.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.inventario_ubicaciones import InventarioUbicacion
from app.schemas.inventario_ubicaciones import InventarioUbicacionCreate
from typing import Optional

def crear_inventario(db: Session, inventario: InventarioUbicacionCreate):
    nuevo = InventarioUbicacion(**inventario.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_por_id(db: Session, id_inventario: int):
    return db.query(InventarioUbicacion).filter(
        InventarioUbicacion.IdInventarioUbicacion == id_inventario
    ).first()

def obtener_inventario(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    id_ubicacion: Optional[int] = None,
    id_lote: Optional[int] = None,
    seccion: Optional[str] = None,
    posicion: Optional[str] = None
):
    query = db.query(InventarioUbicacion)

    if id_ubicacion is not None:
        query = query.filter(InventarioUbicacion.IdUbicacion == id_ubicacion)
    if id_lote is not None:
        query = query.filter(InventarioUbicacion.IdLote == id_lote)
    if seccion:
        query = query.filter(InventarioUbicacion.Seccion.ilike(f"%{seccion}%"))
    if posicion:
        query = query.filter(InventarioUbicacion.Posicion.ilike(f"%{posicion}%"))

    total = query.count()
    resultados = query.order_by(InventarioUbicacion.FechaUltimaActualizacion.desc()).offset(skip).limit(limit).all()
    return total, resultados

def actualizar_inventario(db: Session, id_inventario: int, datos):
    inventario = db.query(InventarioUbicacion).filter(
        InventarioUbicacion.IdInventarioUbicacion == id_inventario
    ).first()

    if not inventario:
        return None

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(inventario, campo, valor)

    inventario.FechaUltimaActualizacion = datetime.now()

    db.commit()
    db.refresh(inventario)
    return inventario

def eliminar_inventario(db: Session, id_inventario: int):
    inv = db.query(InventarioUbicacion).filter(
        InventarioUbicacion.IdInventarioUbicacion == id_inventario
    ).first()

    if not inv:
        return None

    db.delete(inv)
    db.commit()
    return True
