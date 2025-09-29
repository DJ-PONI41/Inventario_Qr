from fastapi import FastAPI
from sqlalchemy import text
from .database import engine

app = FastAPI()

@app.get("/debug/driver")
def driver():
    return {
        "dialect": str(engine.dialect.name),
        "dbapi": getattr(engine.dialect.dbapi, "__name__", "unknown"),
    }

@app.get("/debug/db-ping")
def db_ping():
    with engine.connect() as conn:
        row = conn.execute(text("SELECT DB_NAME() db, SUSER_SNAME() login")).mappings().first()
    return {"db": row["db"], "login": row["login"]}
