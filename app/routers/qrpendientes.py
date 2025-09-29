from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.qrpendientes import QRPendienteCreate, QRPendienteRead
from app.crud import qrpendientes as crud_qrpendientes

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/qrpendientes", response_model=QRPendienteRead)
def registrar_qr_pendiente(data: QRPendienteCreate, db: Session = Depends(get_db)):
    return crud_qrpendientes.crear_qr_pendiente(db, data)
