# API de Inventario PIL

Este backend gestiona productos, lotes, movimientos, códigos QR, ubicaciones y su distribución física en una empresa de inventario. Diseñado para ser consumido por una aplicación móvil y de escritorio.

---

## 🚀 Tecnologías

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQL Server
- Uvicorn

---

## ⚙️ Instalación

```bash
# Clonar repositorio
git clone https://tu-repo/api-inventario-pil.git
cd api-inventario-pil

# Crear entorno virtual
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
uvicorn app.main:app --reload
```

---

## 📌 Estructura

```
app/
├── main.py
├── database.py
├── models/
├── schemas/
├── crud/
└── routers/
```

---

## 🔐 Conexión a SQL Server

Edita el archivo `app/database.py`:

```python
DATABASE_URL = "mssql+pyodbc://USUARIO:CONTRASENA@localhost/NOMBRE_DB?driver=ODBC+Driver+17+for+SQL+Server"
```

---

## 📡 Documentación Interactiva

- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📚 Endpoints disponibles

Ver tabla adjunta para lista completa por entidad, con parámetros y respuesta.

---

## 🛡️ Validaciones clave

- Control de stock (`CantidadActual`) automatizado desde movimientos
- Prevención de duplicados (`QR`, `Lote`)
- Eliminación lógica en productos, lotes, ubicaciones, QR
- Anulación segura de movimientos (con reverso automático)
- Filtros y paginación para todos los listados

---

## ✅ Estado del backend

✅ Listo para producción / integración con frontend móvil y escritorio.

---