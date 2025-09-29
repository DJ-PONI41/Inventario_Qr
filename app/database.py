# app/database.py
import os, urllib.parse, certifi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SERVER = os.getenv("AZURE_SQL_SERVER", "bd-inventario.database.windows.net")
DB     = os.getenv("AZURE_SQL_DB", "db_Inventario_Pil_v2")
USER   = os.getenv("AZURE_SQL_USER", "")  # usar usuario@servidor
PASS   = os.getenv("AZURE_SQL_PASSWORD", "")
PORT   = int(os.getenv("AZURE_SQL_PORT", "1433"))

USER_Q = urllib.parse.quote_plus(USER)
PASS_Q = urllib.parse.quote_plus(PASS)

DATABASE_URL = f"mssql+pytds://{USER_Q}:{PASS_Q}@{SERVER}:{PORT}/{DB}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    connect_args={
        "cafile": certifi.where(),   # <- habilita TLS
        "validate_host": True,       # valida CN del cert (si falla, pon False temporalmente)
        "login_timeout": 30,
        "timeout": 30,
        # "tds_version": "7.4",      # opcional
    },
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
