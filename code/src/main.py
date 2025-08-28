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
from fastapi.responses import RedirectResponse, JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
import logging
from datetime import datetime

# Importar configuración y utilidades
from .config import settings
from .utils.exceptions import PaqueteriaException, handle_paqueteria_exception

# Importar routers
from .routers import auth, packages, customers, rates, notifications, messages, files, admin, announcements
from .database.database import engine, get_db
from .models import base
from .dependencies import get_current_active_user, verify_token

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
app.include_router(announcements.router, prefix="/api/announcements", tags=["Anuncios"])
app.include_router(customers.router, prefix="/api/customers", tags=["Clientes"])
app.include_router(rates.router, prefix="/api/rates", tags=["Tarifas"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notificaciones"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensajes"])
app.include_router(files.router, prefix="/api/files", tags=["Archivos"])
app.include_router(admin.router, prefix="/api/admin", tags=["Administración"])

# ========================================
# ENDPOINT ADICIONAL PARA VERIFICACIÓN DE AUTENTICACIÓN
# ========================================

@app.get("/api/auth/check")
async def check_auth(request: Request):
    """Verificar estado de autenticación desde frontend"""
    try:
        # Intentar obtener el token desde las cookies
        token = request.cookies.get("access_token")
        if token:
            username = verify_token(token)
            if username:
                return {
                    "is_authenticated": True,
                    "user_name": username
                }
    except Exception:
        pass
    
    return {
        "is_authenticated": False,
        "user_name": None
    }

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

@app.get("/track")
async def track_package_page(request: Request):
    """Página de consulta de paquetes por código de guía - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("customers/track-package.html", context)

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
    """Página de registro - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("auth/register.html", context)

@app.get("/auth/forgot-password")
async def auth_forgot_password_page(request: Request):
    """Página de recuperación de contraseña - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("auth/forgot-password.html", context)

@app.get("/auth/reset-password")
async def auth_reset_password_page(request: Request):
    """Página de restablecimiento de contraseña - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("auth/reset-password.html", context)

@app.get("/logout")
async def logout_page(request: Request):
    """Página de logout - Redirige a la página de login"""
    # Limpiar cookies de autenticación
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie("access_token")
    response.delete_cookie("user_id")
    response.delete_cookie("user_name")
    response.delete_cookie("user_role")
    return response

@app.get("/help")
async def help_page(request: Request):
    """Página de ayuda - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("customers/help.html", context)

@app.get("/cookies")
async def cookies_page(request: Request):
    """Página de política de cookies - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("customers/cookies.html", context)

@app.get("/policies")
async def policies_page(request: Request):
    """Página de políticas - Pública"""
    context = get_auth_context(request, is_authenticated=False)
    return templates.TemplateResponse("customers/policies.html", context)

@app.get("/dashboard")
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    """Dashboard administrativo - Solo para usuarios autenticados"""
    # Verificar autenticación
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        # Redirigir a login si no está autenticado
        return RedirectResponse(url="/auth/login?redirect=/dashboard", status_code=302)
    
    try:
        # Obtener estadísticas reales de la base de datos
        from .models.package import Package, PackageStatus
        from .models.announcement import PackageAnnouncement
        from .models.customer import Customer
        
        # Estadísticas de paquetes
        total_packages = db.query(Package).count()
        pending_packages = db.query(Package).filter(Package.status == PackageStatus.ANUNCIADO).count()
        delivered_packages = db.query(Package).filter(Package.status == PackageStatus.ENTREGADO).count()
        total_customers = db.query(Customer).count()
        
        # Estadísticas de anuncios
        total_announcements = db.query(PackageAnnouncement).count()
        pending_announcements = db.query(PackageAnnouncement).filter(
            and_(PackageAnnouncement.is_active == True, PackageAnnouncement.is_processed == False)
        ).count()
        processed_announcements = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_processed == True
        ).count()
        
        # Anuncios recientes (últimos 5)
        recent_announcements = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_active == True
        ).order_by(desc(PackageAnnouncement.announced_at)).limit(5).all()
        
        # Paquetes recientes (últimos 5)
        recent_packages = db.query(Package).order_by(desc(Package.created_at)).limit(5).all()
        
        stats = {
            "total_packages": total_packages,
            "pending_packages": pending_packages,
            "delivered_packages": delivered_packages,
            "total_customers": total_customers,
            "total_announcements": total_announcements,
            "pending_announcements": pending_announcements,
            "processed_announcements": processed_announcements
        }
        
        # Agregar información del usuario al contexto
        context.update({
            "stats": stats,
            "recent_announcements": recent_announcements,
            "recent_packages": recent_packages
        })
        
        return templates.TemplateResponse("dashboard.html", context)
        
    except Exception as e:
        logger.error(f"Error en dashboard: {e}")
        # En caso de error, mostrar dashboard básico
        context.update({
            "stats": {
                "total_packages": 0,
                "pending_packages": 0,
                "delivered_packages": 0,
                "total_customers": 0,
                "total_announcements": 0,
                "pending_announcements": 0,
                "processed_announcements": 0
            },
            "recent_announcements": [],
            "recent_packages": []
        })
        return templates.TemplateResponse("dashboard.html", context)

# ========================================
# RUTAS PROTEGIDAS - REQUIEREN AUTENTICACIÓN
# ========================================

@app.get("/admin")
async def admin_page(request: Request):
    """Página de administración - Solo para administradores"""
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        return RedirectResponse(url="/auth/login?redirect=/admin", status_code=302)
    
    return templates.TemplateResponse("admin/admin.html", context)

@app.get("/packages")
async def packages_page(request: Request):
    """Página de gestión de paquetes - Solo para usuarios autenticados"""
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        return RedirectResponse(url="/auth/login?redirect=/packages", status_code=302)
    
    return templates.TemplateResponse("packages/packages.html", context)

@app.get("/customers-management")
async def customers_management_page(request: Request):
    """Página de gestión de clientes - Solo para usuarios autenticados"""
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        return RedirectResponse(url="/auth/login?redirect=/customers-management", status_code=302)
    
    return templates.TemplateResponse("customers/customers-management.html", context)

# ========================================
# HEALTH CHECKS Y UTILIDADES
# ========================================

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version
    }

@app.get("/api/health")
async def api_health_check():
    """Health check para API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
