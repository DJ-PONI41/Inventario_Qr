# app/database.py
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Lee credenciales desde variables de entorno (Render/tu .env)
SERVER = os.getenv("AZURE_SQL_SERVER", "bd-inventario.database.windows.net")  # sin 'tcp:'
DB     = os.getenv("AZURE_SQL_DB", "db_Inventario_Pil_v2")
USER   = os.getenv("AZURE_SQL_USER", "")
PASS   = os.getenv("AZURE_SQL_PASSWORD", "")
PORT   = os.getenv("AZURE_SQL_PORT", "1433")

# Nota: en Azure SQL a veces el usuario debe ser 'usuario@nombre-servidor'
USER_Q = urllib.parse.quote_plus(USER)
PASS_Q = urllib.parse.quote_plus(PASS)

# Driver puro Python (no requiere ODBC del sistema)
DATABASE_URL = f"mssql+pytds://{USER_Q}:{PASS_Q}@{SERVER}:{PORT}/{DB}?autocommit=True"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

# (Opcional) dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
