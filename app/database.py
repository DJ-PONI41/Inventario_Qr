# app/database.py
import os, urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SERVER = os.getenv("AZURE_SQL_SERVER", "bd-inventario.database.windows.net")  # sin 'tcp:'
DB     = os.getenv("AZURE_SQL_DB", "db_Inventario_Pil_v2")
USER   = os.getenv("AZURE_SQL_USER", "")
PASS   = os.getenv("AZURE_SQL_PASSWORD", "")
PORT   = int(os.getenv("AZURE_SQL_PORT", "1433"))

USER_Q = urllib.parse.quote_plus(USER)
PASS_Q = urllib.parse.quote_plus(PASS)

# URL base sin flags de TLS
DATABASE_URL = f"mssql+pytds://{USER_Q}:{PASS_Q}@{SERVER}:{PORT}/{DB}"

# >>> CLAVE: forzar TLS y validación de host <<<
CONNECT_ARGS = {
    "use_tls": True,
    "validate_host": True,   # si diera error de certificado/host, prueba False temporalmente
    "login_timeout": 30,
    "timeout": 30,
}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    connect_args=CONNECT_ARGS,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
