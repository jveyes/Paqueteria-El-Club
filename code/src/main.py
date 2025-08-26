# ========================================
# PAQUETES EL CLUB v3.1 - Aplicación Principal FastAPI Optimizada
# ========================================
#
# Este archivo contiene la configuración principal de la aplicación FastAPI
# incluyendo rutas, middleware, templates y configuración de servicios.
#
# Características principales:
# - Sistema de autenticación con JWT
# - Templates HTML con Jinja2
# - Rutas públicas y protegidas
# - Configuración de CORS
# - Logging optimizado
# - Health checks
#
# Autor: JEMAVI
# Versión: 3.1.0
# Fecha: 2025-08-25
# ========================================

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
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
from .dependencies import get_current_active_user

# Configurar logging optimizado
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
    logger.info("Iniciando PAQUETES EL CLUB v3.1...")
    
    # Crear tablas de la base de datos
    try:
        base.Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
    
    yield
    
    # Shutdown
    logger.info("Cerrando PAQUETES EL CLUB v3.1...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema de gestión de paquetería optimizado para 50 usuarios simultáneos",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# ========================================
# FUNCIONES HELPER PARA AUTENTICACIÓN
# ========================================

def get_auth_context(request: Request, is_authenticated: bool = False, user_name: str = None):
    """
    Retorna el contexto de autenticación para las plantillas HTML.
    
    Args:
        request (Request): Objeto request de FastAPI
        is_authenticated (bool): Estado de autenticación del usuario
        user_name (str): Nombre del usuario autenticado
    
    Returns:
        dict: Contexto con información de autenticación para templates
    """
    return {
        "request": request,
        "is_authenticated": is_authenticated,
        "user_name": user_name
    }

async def get_auth_context_from_request(request: Request):
    """
    Obtiene el contexto de autenticación desde las cookies del request.
    
    Esta función verifica si existe un token JWT válido en las cookies
    y retorna el contexto de autenticación correspondiente.
    
    Args:
        request (Request): Objeto request de FastAPI
    
    Returns:
        dict: Contexto de autenticación basado en las cookies
    """
    try:
        # Intentar obtener el token desde las cookies
        token = request.cookies.get("access_token")
        if token:
            # Verificar el token usando la función de dependencias
            from .dependencies import verify_token
            username = verify_token(token)
            if username:
                return get_auth_context(request, is_authenticated=True, user_name=username)
    except Exception:
        # En caso de error, retornar contexto no autenticado
        pass
    
    return get_auth_context(request, is_authenticated=False)

# Manejo de excepciones personalizadas
app.add_exception_handler(PaqueteriaException, handle_paqueteria_exception)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(packages.router, prefix="/api/packages", tags=["Paquetes"])
app.include_router(customers.router, prefix="/api/customers", tags=["Clientes"])
app.include_router(rates.router, prefix="/api/rates", tags=["Tarifas"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notificaciones"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensajes"])
app.include_router(files.router, prefix="/api/files", tags=["Archivos"])
app.include_router(admin.router, prefix="/api/admin", tags=["Administración"])

# ========================================
# RUTAS PÚBLICAS - ACCESO SIN AUTENTICACIÓN
# ========================================

@app.get("/")
async def root(request: Request):
    """
    Página principal de la aplicación.
    
    Muestra el formulario de anuncio de paquetes para clientes.
    Esta es la página de entrada principal del sistema.
    
    Args:
        request (Request): Objeto request de FastAPI
    
    Returns:
        TemplateResponse: Página HTML con formulario de anuncio
    """
    context = get_auth_context(request, is_authenticated=False)
    context["package_announcements"] = []
    return templates.TemplateResponse("customers/announce.html", context)

@app.get("/customers")
async def customers_page(request: Request):
    """Página de anunciar paquetes - Redirige a la página principal"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/", status_code=302)

@app.get("/search")
async def search_page(request: Request):
    """Página de consulta de paquetes - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("customers/search.html", context)

@app.get("/login")
async def login_page(request: Request):
    """Página de login - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("auth/login.html", context)

@app.get("/auth/login")
async def auth_login_page(request: Request):
    """Página de login - Pública (ruta alternativa)"""
    # Obtener parámetro de redirección
    redirect_url = request.query_params.get("redirect", "/dashboard")
    context = get_auth_context(request, is_authenticated=False)
    context["redirect_url"] = redirect_url
    return templates.TemplateResponse("auth/login.html", context)

@app.get("/auth/register")
async def auth_register_page(request: Request):
    """Página de registro - Solo para usuarios autenticados"""
    # Verificar autenticación desde cookies
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        # Redirigir a login si no está autenticado
        return RedirectResponse(url="/auth/login?redirect=/auth/register", status_code=302)
    
    return templates.TemplateResponse("auth/register.html", context)

@app.get("/auth/forgot-password")
async def auth_forgot_password_page(request: Request):
    """Página de recuperación de contraseña - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("auth/forgot-password.html", context)

@app.get("/help")
async def help_page(request: Request):
    """Página de ayuda - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("customers/help.html", context)

@app.get("/dashboard")
async def dashboard_page(request: Request):
    """Dashboard administrativo"""
    # Datos de ejemplo para el dashboard
    stats = {
        "total_packages": 150,
        "pending_packages": 25,
        "delivered_packages": 120,
        "total_customers": 45
    }
    
    recent_packages = [
        {"id": 1, "tracking_number": "ABC123", "customer_name": "Juan Pérez", "status": "pending"},
        {"id": 2, "tracking_number": "XYZ789", "customer_name": "María García", "status": "delivered"}
    ]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "recent_packages": recent_packages
    })

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment
    }

@app.get("/api/auth/check")
async def check_auth(request: Request):
    """Verificar estado de autenticación"""
    context = await get_auth_context_from_request(request)
    return {
        "is_authenticated": context["is_authenticated"],
        "user_name": context["user_name"]
    }

@app.get("/api/docs")
async def api_docs():
    """Redirigir a la documentación de la API"""
    return {"docs_url": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
        limit_concurrency=50,
        limit_max_requests=1000
    )
