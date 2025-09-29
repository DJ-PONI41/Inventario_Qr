# app/database.py
import os, urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SERVER = os.getenv("AZURE_SQL_SERVER", "bd-inventario.database.windows.net")
DB     = os.getenv("AZURE_SQL_DB", "db_Inventario_Pil_v2")
USER   = os.getenv("AZURE_SQL_USER", "")
PASS   = os.getenv("AZURE_SQL_PASSWORD", "")
PORT   = os.getenv("AZURE_SQL_PORT", "1433")

USER_Q = urllib.parse.quote_plus(USER)
PASS_Q = urllib.parse.quote_plus(PASS)

# TLS obligatorio en Azure SQL
DATABASE_URL = (
    f"mssql+pytds://{USER_Q}:{PASS_Q}@{SERVER}:{PORT}/{DB}"
    "?autocommit=True&use_tls=True&validate_host=True&login_timeout=30&timeout=30"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
