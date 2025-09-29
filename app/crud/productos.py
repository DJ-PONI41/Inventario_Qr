# app/crud/productos.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.productos import Producto
from app.schemas.productos import ProductoCreate

# Crear nuevo producto
def contar_productos_activos(db: Session) -> int:
    return db.query(Producto).filter(Producto.Estado == True).count()

def crear_producto(db: Session, producto: ProductoCreate):
    nuevo = Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Obtener todos los productos activos
def obtener_productos(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    nombre: str = None,
    unidad: str = None,
    codigo: str = None
):
    query = db.query(Producto).filter(Producto.Estado == True)

    if nombre:
        query = query.filter(Producto.Nombre.ilike(f"%{nombre}%"))
    if unidad:
        query = query.filter(Producto.UnidadMedida == unidad)
    if codigo:
        query = query.filter(Producto.CodigoProducto.ilike(f"%{codigo}%"))

    total = query.count()
    productos = (
        query.order_by(Producto.IdProducto)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return total, productos


def obtener_productos_total(
    db: Session
):
    query = db.query(Producto).filter(Producto.Estado == True)
    total = query.count()
    productos = (
        query.order_by(Producto.IdProducto)
        .all()
    )

    return total, productos


# Obtener producto por código
def obtener_por_codigo(db: Session, codigo: str):
    return db.query(Producto).filter(Producto.CodigoProducto == codigo).first()

# Obtener producto por ID
def obtener_por_id(db: Session, id_producto: int):
    return db.query(Producto).filter(Producto.IdProducto == id_producto).first()

# Para contar productos


def actualizar_producto(db: Session, id_producto: int, datos):
    producto = db.query(Producto).filter(Producto.IdProducto == id_producto).first()
    if not producto:
        return None

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(producto, campo, valor)

    producto.FechaModificacion = datetime.now()
    db.commit()
    db.refresh(producto)
    return producto

def desactivar_producto(db: Session, id_producto: int):
    producto = db.query(Producto).filter(Producto.IdProducto == id_producto).first()
    if not producto:
        return None
    producto.Estado = False
    producto.FechaModificacion = datetime.now()
    db.commit()
    return producto




