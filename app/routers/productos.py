# app/routers/productos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import SessionLocal
from app.schemas.productos import ProductoCreate, ProductoRead
from app.crud import productos as crud_productos

from fastapi import Query

from app.models.productos import Producto

from app.schemas.productos import ProductoUpdate

router = APIRouter()

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    existente = crud_productos.obtener_por_codigo(db, producto.CodigoProducto)
    if existente:
        raise HTTPException(status_code=400, detail="El código de producto ya existe.")
    return crud_productos.crear_producto(db, producto)



@router.get("/productos")
def listar_productos(
    skip: int = 0,
    limit: int = 10,
    nombre: str = Query(default=None),
    unidad: str = Query(default=None),
    codigo: str = Query(default=None),
    db: Session = Depends(get_db)
):
    total, productos = crud_productos.obtener_productos(
        db, skip=skip, limit=limit, nombre=nombre, unidad=unidad, codigo=codigo
    )

    productos_serializados = [ProductoRead.from_orm(p) for p in productos]

    return {"Cantidad": total, "Data": productos_serializados}


@router.get("/productos/bajo-stock", response_model=List[ProductoRead])
def productos_bajo_stock(db: Session = Depends(get_db)):
    from app.models.lotes import Lote  # 👈 usamos join
    from sqlalchemy import func

    subquery = (
        db.query(
            Lote.IdProducto,
            func.sum(Lote.CantidadActual).label("stock_actual")
        )
        .group_by(Lote.IdProducto)
        .subquery()
    )

    productos = (
        db.query(Producto)
        .join(subquery, Producto.IdProducto == subquery.c.IdProducto)
        .filter(
            Producto.Estado == True,
            subquery.c.stock_actual < Producto.StockMinimo
        )
        .all()
    )

    return productos



@router.get("/productos/{id_producto}", response_model=ProductoRead)
def obtener_producto(id_producto: int, db: Session = Depends(get_db)):
    producto = crud_productos.obtener_por_id(db, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto


@router.get("/productos_all")
def listar_productos(
    db: Session = Depends(get_db)
):
    total, productos = crud_productos.obtener_productos_total(
        db
    )

    productos_serializados = [ProductoRead.from_orm(p) for p in productos]

    return {"Cantidad": total, "Data": productos_serializados}




@router.put("/productos/{id_producto}", response_model=ProductoRead)
def editar_producto(id_producto: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    actualizado = crud_productos.actualizar_producto(db, id_producto, datos)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return actualizado

@router.delete("/productos/{id_producto}")
def eliminar_producto(id_producto: int, db: Session = Depends(get_db)):
    eliminado = crud_productos.desactivar_producto(db, id_producto)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return {"mensaje": "Producto desactivado correctamente"}
