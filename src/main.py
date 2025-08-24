# ========================================
# PAQUETES EL CLUB v3.0 - Aplicación Principal FastAPI
# ========================================

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Importar configuración y utilidades
from .config import settings
from .utils.exceptions import PaqueteriaException, handle_paqueteria_exception

# Importar routers
from .routers import auth, packages, customers, rates, notifications, messages, files, admin
from .database.database import engine
from .models import base

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando PAQUETES EL CLUB v3.0...")
    
    # Crear tablas si no existen
    base.Base.metadata.create_all(bind=engine)
    
    logger.info("✅ Base de datos inicializada")
    logger.info("✅ Aplicación lista para recibir requests")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando PAQUETES EL CLUB v3.0...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Sistema de gestión de paquetería con tarifas automáticas",
    version=settings.app_version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Manejo de excepciones personalizadas
@app.exception_handler(PaqueteriaException)
async def paqueteria_exception_handler(request: Request, exc: PaqueteriaException):
    return handle_paqueteria_exception(exc)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(packages.router, prefix="/api/packages", tags=["Paquetes"])
app.include_router(customers.router, prefix="/api/customers", tags=["Clientes"])
app.include_router(rates.router, prefix="/api/rates", tags=["Tarifas"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notificaciones"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensajería"])
app.include_router(files.router, prefix="/api/files", tags=["Archivos"])
app.include_router(admin.router, prefix="/api/admin", tags=["Administración"])

@app.get("/")
async def root(request: Request):
    """Página principal"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "service": settings.app_name,
        "environment": settings.environment
    }

@app.get("/metrics")
async def metrics():
    """Endpoint para métricas de Prometheus"""
    # Aquí se agregarían métricas personalizadas
    return {"status": "metrics_endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
