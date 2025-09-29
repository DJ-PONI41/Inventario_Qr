# app/crud/ubicaciones.py
from sqlalchemy.orm import Session
from app.models.ubicaciones import Ubicacion
from app.schemas.ubicaciones import UbicacionCreate
from typing import Optional

def crear_ubicacion(db: Session, ubicacion: UbicacionCreate):
    nueva = Ubicacion(**ubicacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_por_id(db: Session, id_ubicacion: int):
    return db.query(Ubicacion).filter(Ubicacion.IdUbicacion == id_ubicacion).first()

def obtener_ubicaciones(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    ciudad: Optional[str] = None,
    tipo: Optional[str] = None,
    estado: Optional[bool] = None
):
    query = db.query(Ubicacion)

    if ciudad:
        query = query.filter(Ubicacion.Ciudad.ilike(f"%{ciudad}%"))
    if tipo:
        query = query.filter(Ubicacion.TipoUbicacion == tipo)
    if estado is not None:
        query = query.filter(Ubicacion.Estado == estado)

    total = query.count()
    resultados = query.order_by(Ubicacion.IdUbicacion).offset(skip).limit(limit).all()
    return total, resultados

def actualizar_ubicacion(db: Session, id_ubicacion: int, datos):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.IdUbicacion == id_ubicacion).first()
    if not ubicacion:
        return None

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(ubicacion, campo, valor)

    db.commit()
    db.refresh(ubicacion)
    return ubicacion

def desactivar_ubicacion(db: Session, id_ubicacion: int):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.IdUbicacion == id_ubicacion).first()
    if not ubicacion:
        return None
    ubicacion.Estado = False
    db.commit()
    return ubicacion
