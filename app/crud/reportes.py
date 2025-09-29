from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from app.crud.lotes import obtener_lotes, obtener_lotes_por_rango
from app.models.lotes import Lote
from app.crud.movimientos import obtener_movimientos
from app.models.movimientos import Movimiento
from app.models.productos import Producto
from app.crud.productos import obtener_productos_total 

def generar_reporte_lotes(
    db: Session,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None
) -> List[Lote]:
    """
    Obtiene todos los lotes que caen dentro del rango de fechas de vencimiento.
    Si no se especifica rango, devuelve todos los lotes.

    :param db: sesión de base de datos
    :param fecha_inicio: límite inferior (inclusive)
    :param fecha_fin: límite superior (inclusive)
    :return: lista de instancias de Lote
    """
    skip = 0
    limit = 10_000_000

    if fecha_inicio or fecha_fin:
        # Si solo uno de los extremos es None, asumimos fecha mínima o máxima
        fi = fecha_inicio or date.min
        ff = fecha_fin or date.max

        # ✅ Llamada corregida con nombres correctos
        _, resultados = obtener_lotes_por_rango(
            db=db,
            vencimiento_inicio=fi,
            vencimiento_fin=ff,
            skip=skip,
            limit=limit
        )
    else:
        # Sin rango usamos el CRUD genérico
        _, resultados = obtener_lotes(db, skip=skip, limit=limit)

    return resultados


def contar_lotes_stock_bajo(db: Session) -> dict:
    """
    Retorna un diccionario con la cantidad de lotes cuyo stock actual
    es menor al mínimo definido en su producto, y los datos de esos lotes.
    """
    _, lotes = obtener_lotes(db, skip=0, limit=10_000_000)
    _, productos = obtener_productos_total(db)

    mapa_productos = {p.IdProducto: p for p in productos}

    resultado = []
    for lote in lotes:
        producto = mapa_productos.get(lote.IdProducto)
        if producto and producto.StockMinimo is not None:
            if lote.CantidadActual < producto.StockMinimo:
                resultado.append({
                    "IdLote": lote.IdLote,
                    "NumeroLote": lote.NumeroLote,
                    "CantidadActual": lote.CantidadActual,
                    "StockMinimo": producto.StockMinimo,
                    "Producto": producto.Nombre,
                    "IdProducto": producto.IdProducto,
                })

    return {
        "count": len(resultado),
        "data": resultado
    }

def generar_reporte_movimientos(
    db: Session,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None
) -> List[dict]:
    """
    Devuelve una lista de movimientos con información enriquecida:
    - Nombre del lote y datos del lote como anotación
    - Datos del producto relacionado al lote
    - Indicación de si fue anulado
    """
    skip = 0
    limit = 10_000_000
    _, movimientos = obtener_movimientos(
        db,
        skip=skip,
        limit=limit,
        tipo=None,
        id_lote=None,
        fecha=None  # se filtra después si es necesario
    )

    if fecha_inicio or fecha_fin:
        fi = fecha_inicio or date.min
        ff = fecha_fin or date.max
        movimientos = [m for m in movimientos if fi <= m.FechaMovimiento.date() <= ff]

    _, lotes = obtener_lotes(db, skip=0, limit=limit)
    _, productos = obtener_productos_total(db)
    mapa_lotes = {l.IdLote: l for l in lotes}
    mapa_productos = {p.IdProducto: p for p in productos}

    resultado = []
    for mov in movimientos:
        lote = mapa_lotes.get(mov.IdLote)
        producto = mapa_productos.get(lote.IdProducto) if lote else None

        comentario = None
        if lote and producto:
            comentario = (
                f"Producto: {producto.Nombre}\n"
                f"Código: {producto.CodigoProducto}\n"
                f"Unidad: {producto.UnidadMedida}\n"
                f"Stock Mínimo: {producto.StockMinimo}\n"
                f"Lote: {lote.NumeroLote}\n"
                f"Cantidad Actual: {lote.CantidadActual}\n"
                f"Fecha Vencimiento: {lote.FechaVencimiento}"
            )

        resultado.append({
            "IdMovimiento": mov.IdMovimiento,
            "FechaMovimiento": mov.FechaMovimiento,
            "TipoMovimiento": mov.TipoMovimiento,
            "Cantidad": mov.Cantidad,
            "Motivo": mov.Motivo,
            "DocumentoReferencia": mov.DocumentoReferencia,
            "Responsable": mov.Responsable,
            "Observaciones": mov.Observaciones,
            "FueAnulado": mov.FueAnulado,
            "NombreLote": lote.NumeroLote if lote else f"[ID {mov.IdLote}]",
            "ComentarioLote": comentario
        })

    return resultado
