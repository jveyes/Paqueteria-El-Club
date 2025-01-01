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

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, or_
import logging
import uuid
from datetime import datetime

# Importar configuración y utilidades
from .config import settings
from .utils.exceptions import PaqueteriaException
from .utils.auth_context import get_auth_context, get_auth_context_from_request

# Importar routers
from .routers import auth, packages, customers, rates, notifications, messages, files, admin, announcements, profile
from .database.database import engine, get_db, init_db
from .models import base
from .models.user import User
from .dependencies import get_current_active_user, get_current_active_user_from_cookies
from .utils.auth import verify_token

# Configurar logging optimizado
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Solo usar StreamHandler por ahora
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando PAQUETES EL CLUB v3.1...")
    
    # Inicializar base de datos con timezone configurado
    try:
        init_db()
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
# Las funciones get_auth_context y get_auth_context_from_request
# han sido movidas a utils/auth_context.py para evitar imports circulares

# ========================================
# MANEJO DE EXCEPCIONES PERSONALIZADAS
# ========================================

def handle_paqueteria_exception(request: Request, exc: PaqueteriaException):
    """Maneja las excepciones personalizadas de la aplicación"""
    logger.error(f"PaqueteriaException: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

def handle_http_exception(request: Request, exc: HTTPException):
    """Maneja las excepciones HTTP de manera personalizada"""
    if exc.status_code == 401:
        # Solo cambiar el mensaje para rutas que NO sean de login
        if "/api/auth/login" not in str(request.url):
            headers = dict(exc.headers) if exc.headers else {}
            headers["Location"] = "/auth/login"
            headers["Content-Type"] = "application/json"
            
            return JSONResponse(
                status_code=401,
                content={"detail": "No autenticado"},
                headers=headers
            )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Manejo de excepciones personalizadas
app.add_exception_handler(PaqueteriaException, handle_paqueteria_exception)
app.add_exception_handler(HTTPException, handle_http_exception)

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
app.include_router(profile.router, tags=["Perfil"])

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
            payload = verify_token(token)
            if payload and payload.get("username"):
                return {
                    "is_authenticated": True,
                    "user_name": payload.get("username")
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
    context = await get_auth_context_from_request(request)
    context["package_announcements"] = []
    return templates.TemplateResponse("customers/announce.html", context)

@app.get("/customers")
async def customers_page(request: Request):
    """Página de anunciar paquetes - Redirige a la página principal"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/", status_code=302)

@app.get("/announce")
async def announce_page(request: Request):
    """Página de anunciar paquetes - Ruta alternativa"""
    context = await get_auth_context_from_request(request)
    context["package_announcements"] = []
    return templates.TemplateResponse("customers/announce.html", context)

@app.get("/search")
async def search_page(request: Request):
    """Página de consulta de paquetes - Pública"""
    context = await get_auth_context_from_request(request)
    return templates.TemplateResponse("customers/search.html", context)

@app.get("/messages")
async def messages_page(request: Request):
    """Página de mensajes - Solo para usuarios autenticados"""
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        return RedirectResponse(url="/auth/login?redirect=/messages", status_code=302)
    
    return templates.TemplateResponse("messages/messages.html", context)



@app.get("/login")
async def login_page(request: Request):
    """Página de login - Pública"""
    context = await get_auth_context_from_request(request)
    return templates.TemplateResponse("auth/login.html", context)

@app.get("/auth/login")
async def auth_login_page(request: Request):
    """Página de login - Pública (ruta alternativa)"""
    # Obtener parámetro de redirección
    redirect_url = request.query_params.get("redirect", "/dashboard")
    context = await get_auth_context_from_request(request)
    context["redirect_url"] = redirect_url
    return templates.TemplateResponse("auth/login.html", context)

@app.get("/auth/register")
async def auth_register_page(request: Request):
    """Página de registro - Pública"""
    context = await get_auth_context_from_request(request)
    return templates.TemplateResponse("auth/register.html", context)

@app.get("/auth/forgot-password")
async def auth_forgot_password_page(request: Request):
    """Página de recuperación de contraseña - Pública"""
    context = await get_auth_context_from_request(request)
    return templates.TemplateResponse("auth/forgot-password.html", context)

@app.get("/auth/reset-password")
async def auth_reset_password_page(request: Request):
    """Página de restablecimiento de contraseña - Pública"""
    context = await get_auth_context_from_request(request)
    return templates.TemplateResponse("auth/reset-password.html", context)

@app.get("/settings")
async def settings_page(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Página de configuración - Solo para usuarios autenticados"""
    context = await get_auth_context_from_request(request)
    context["user"] = current_user
    return templates.TemplateResponse("profile/settings.html", context)

@app.get("/admin/users")
async def admin_users_page(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Página de gestión de usuarios - Solo para administradores"""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden acceder a esta página."
        )
    
    context = await get_auth_context_from_request(request)
    context["user"] = current_user
    
    # Obtener todos los usuarios del sistema
    from .database.database import get_db
    from .models.user import User
    from sqlalchemy.orm import Session
    
    db = next(get_db())
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        context["users"] = users
    finally:
        db.close()
    
    return templates.TemplateResponse("admin/users.html", context)

@app.get("/admin/users/search")
async def search_users(
    request: Request,
    q: str = None,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """API endpoint para búsqueda de usuarios - Solo para administradores"""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo los administradores pueden acceder a esta función."
        )
    
    if not q or q.strip() == "":
        # Si no hay término de búsqueda, devolver todos los usuarios
        users = db.query(User).order_by(User.created_at.desc()).all()
    else:
        search_term = f"%{q.strip()}%"
        # Buscar en todos los campos: username, full_name, email, phone, role, is_active
        users = db.query(User).filter(
            or_(
                User.email.ilike(search_term),
                User.phone.ilike(search_term),
                User.role.ilike(search_term),
                User.full_name.ilike(search_term),
                User.username.ilike(search_term),
                # Búsqueda por estado activo/inactivo
                User.is_active == (q.strip().lower() in ['activo', 'active', 'true', '1']),
                User.is_active == (q.strip().lower() in ['inactivo', 'inactive', 'false', '0'])
            )
        ).order_by(User.created_at.desc()).all()
    
    # Convertir usuarios a formato JSON
    users_data = []
    for user in users:
        users_data.append({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "role": user.role.value if user.role else None,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        })
    
    return {
        "users": users_data,
        "total": len(users_data),
        "search_term": q
    }

@app.post("/admin/users/create")
async def create_user(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Crear un nuevo usuario - Solo para administradores"""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden crear usuarios."
        )
    
    try:
        # Obtener datos del JSON
        data = await request.json()
        
        username = data.get("username")
        email = data.get("email")
        full_name = data.get("full_name")
        phone = data.get("phone", "")
        role = data.get("role", "operator")  # Permitir "operator" o "user"
        password = data.get("password")
        
        # Validar que el rol sea válido
        if role not in ["operator", "user", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rol inválido. Solo se permiten roles 'operator', 'user' o 'admin'"
            )
        
        # Validaciones básicas
        required_fields = [username, email, full_name]
        if role in ["operator", "admin"]:
            required_fields.append(password)
        
        if not all(required_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos obligatorios deben ser completados"
            )
        
        # Verificar si el usuario ya existe
        from .models.user import User
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario o email ya existe"
            )
        
        # Crear nuevo usuario
        from .utils.auth import get_password_hash
        from .models.user import UserRole
        
        # Hashear la contraseña solo si se proporciona (roles operator y admin)
        hashed_password = None
        if role in ["operator", "admin"] and password:
            hashed_password = get_password_hash(password)
        
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone if phone else None,
            role=UserRole(role),
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Usuario creado exitosamente",
                "user_id": str(new_user.id)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )

@app.post("/admin/users/update")
async def update_user(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Actualizar un usuario existente - Solo para administradores"""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden actualizar usuarios."
        )
    
    try:
        # Obtener datos del JSON
        data = await request.json()
        
        user_id_str = data.get("user_id")
        username = data.get("username")
        email = data.get("email")
        full_name = data.get("full_name")
        phone = data.get("phone", "")
        role = data.get("role")
        is_active = data.get("is_active", True)  # Default true
        
        # Validaciones básicas
        if not all([user_id_str, username, email, full_name, role]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos obligatorios deben ser completados"
            )
        
        # Convertir string a UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario inválido"
            )
        
        # Verificar que el rol sea válido
        if role not in ["operator", "user", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rol inválido. Solo se permiten roles 'operator', 'user' o 'admin'"
            )
        
        # Buscar el usuario a actualizar
        from .models.user import User
        user_to_update = db.query(User).filter(User.id == user_id).first()
        
        if not user_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Permitir cambios de rol, pero con validaciones de seguridad
        # No permitir que un admin se degrade a sí mismo si es el único admin
        if user_to_update.role.value == "admin" and role != "admin" and user_to_update.id == current_user.id:
            admin_count = db.query(User).filter(User.role == "admin").count()
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No puedes cambiar tu propio rol de administrador si eres el único admin del sistema"
                )
        
        # Verificar si el username o email ya existen en otros usuarios
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email),
            User.id != user_id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario o email ya existe en otro usuario"
            )
        
        # Actualizar el usuario
        from .models.user import UserRole
        
        user_to_update.username = username
        user_to_update.email = email
        user_to_update.full_name = full_name
        user_to_update.phone = phone if phone else None
        user_to_update.role = UserRole(role)
        user_to_update.is_active = is_active
        
        db.commit()
        db.refresh(user_to_update)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Usuario actualizado exitosamente",
                "user_id": str(user_to_update.id)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}"
        )

@app.post("/profile/update")
async def update_current_user_profile(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Actualizar perfil del usuario actual"""
    try:
        # Obtener datos del request JSON
        data = await request.json()
        
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        full_name = data.get("full_name", "").strip()
        phone = data.get("phone", "").strip() or None
        
        # Validaciones básicas
        if not all([username, email, full_name]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los campos username, email y full_name son obligatorios"
            )
        
        # Verificar username único si se está cambiando
        if username.lower() != current_user.username:
            existing = db.query(User).filter(
                and_(
                    User.username == username.lower(),
                    User.id != current_user.id
                )
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre de usuario '{username}' ya existe"
                )
        
        # Verificar email único si se está cambiando
        if email.lower() != current_user.email:
            existing = db.query(User).filter(
                and_(
                    User.email == email.lower(),
                    User.id != current_user.id
                )
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El email '{email}' ya está registrado"
                )
        
        # Actualizar usuario
        current_user.username = username.lower()
        current_user.email = email.lower()
        current_user.full_name = full_name
        current_user.phone = phone
        
        # Separar nombre completo en first_name y last_name
        # Nota: first_name y last_name son propiedades calculadas del full_name
        # No necesitamos asignarlas ya que se calculan automáticamente
        
        current_user.updated_at = get_colombia_now()
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "message": "Perfil actualizado exitosamente",
            "user": {
                "id": str(current_user.id),
                "username": current_user.username,
                "email": current_user.email,
                "full_name": current_user.full_name,
                "phone": current_user.phone
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar perfil: {str(e)}"
        )

@app.post("/admin/users/delete")
async def delete_user(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Eliminar un usuario - Solo para administradores"""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden eliminar usuarios."
        )
    
    try:
        # Obtener datos del JSON
        data = await request.json()
        user_id_str = data.get("user_id")
        
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario requerido"
            )
        
        # Convertir string a UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario inválido"
            )
        
        # Buscar el usuario a eliminar
        from .models.user import User
        user_to_delete = db.query(User).filter(User.id == user_id).first()
        
        if not user_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # No permitir eliminar el propio usuario
        if user_to_delete.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar tu propio usuario"
            )
        
        # Eliminar el usuario
        db.delete(user_to_delete)
        db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Usuario eliminado exitosamente"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}"
        )

@app.post("/admin/users/toggle-status")
async def toggle_user_status(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Activar/Desactivar un usuario - Solo para administradores"""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden cambiar el estado de usuarios."
        )
    
    try:
        # Obtener datos del JSON
        data = await request.json()
        user_id_str = data.get("user_id")
        is_active = data.get("is_active")
        
        if not user_id_str or is_active is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario y estado requeridos"
            )
        
        # Convertir string a UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario inválido"
            )
        
        # Buscar el usuario
        from .models.user import User
        user_to_update = db.query(User).filter(User.id == user_id).first()
        
        if not user_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # No permitir desactivar el propio usuario
        if user_to_update.id == current_user.id and not is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes desactivar tu propio usuario"
            )
        
        # Actualizar el estado
        user_to_update.is_active = is_active
        db.commit()
        db.refresh(user_to_update)
        
        status_text = "activado" if is_active else "desactivado"
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Usuario {status_text} exitosamente"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar estado del usuario: {str(e)}"
        )

@app.post("/admin/users/reset-password")
async def reset_user_password(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Restablecer contraseña de un usuario - Solo para administradores"""
    # Verificar que el usuario sea administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden restablecer contraseñas."
        )
    
    try:
        # Obtener datos del JSON
        data = await request.json()
        user_id_str = data.get("user_id")
        
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario requerido"
            )
        
        # Convertir string a UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario inválido"
            )
        
        # Buscar el usuario
        from .models.user import User
        user_to_reset = db.query(User).filter(User.id == user_id).first()
        
        if not user_to_reset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Solo restablecer contraseña para usuarios con rol operator o admin
        if user_to_reset.role.value not in ["admin", "operator"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden restablecer contraseñas de usuarios con rol Administrador u Operador"
            )
        
        # Generar nueva contraseña temporal
        import secrets
        import string
        new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        # Actualizar la contraseña
        from .utils.auth import get_password_hash
        user_to_reset.hashed_password = get_password_hash(new_password)
        db.commit()
        
        # Aquí se podría enviar un email con la nueva contraseña
        # Por ahora, solo retornamos un mensaje de éxito
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Contraseña restablecida exitosamente",
                "new_password": new_password  # En producción, esto debería enviarse por email
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al restablecer contraseña: {str(e)}"
        )

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
    context = await get_auth_context_from_request(request)
    return templates.TemplateResponse("customers/help.html", context)

@app.get("/test-search")
async def test_search_page(request: Request):
    """Página de prueba de búsqueda - Pública"""
    return templates.TemplateResponse("testing/test_search.html", context={"request": request})

@app.get("/cookies")
async def cookies_page(request: Request):
    """Página de política de cookies - Pública"""
    context = await get_auth_context_from_request(request)
    return templates.TemplateResponse("customers/cookies.html", context)

@app.get("/policies")
async def policies_page(request: Request):
    """Página de políticas - Pública"""
    context = await get_auth_context_from_request(request)
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
        
        return templates.TemplateResponse("dashboard/dashboard.html", context)
        
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
        return templates.TemplateResponse("dashboard/dashboard.html", context)

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

@app.get("/test-simple")
async def test_simple():
    """Ruta de prueba simple"""
    return {"message": "Test simple funcionando"}

@app.get("/test-packages")
async def test_packages():
    """Ruta de prueba para paquetes"""
    return {"message": "Test paquetes funcionando"}

@app.get("/package-management")
async def package_management_page(request: Request):
    """Página de gestión de paquetes - Solo para administradores"""
    return {"message": "Ruta de gestión de paquetes funcionando"}

@app.get("/test-final")
async def test_final():
    """Ruta de prueba final"""
    return {"message": "Test final funcionando"}

@app.get("/test-very-simple")
async def test_very_simple():
    """Ruta de prueba muy simple"""
    return {"message": "Test muy simple funcionando"}

@app.get("/test-very-very-simple")
async def test_very_very_simple():
    """Ruta de prueba muy muy simple"""
    return {"message": "Test muy muy simple funcionando"}

@app.get("/test-very-very-very-simple")
async def test_very_very_very_simple():
    """Ruta de prueba muy muy muy simple"""
    return {"message": "Test muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-simple")
async def test_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-simple")
async def test_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-very-simple")
async def test_very_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-very-very-simple")
async def test_very_very_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-very-very-very-simple")
async def test_very_very_very_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-very-very-very-very-simple")
async def test_very_very_very_very_very_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-very-very-very-very-very-simple")
async def test_very_very_very_very_very_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy muy muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-very-very-very-very-very-very-simple")
async def test_very_very_very_very_very_very_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy muy muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy muy muy muy muy muy muy simple funcionando"}

@app.get("/test-very-very-very-very-very-very-very-very-very-very-very-very-simple")
async def test_very_very_very_very_very_very_very_very_very_very_very_very_simple():
    """Ruta de prueba muy muy muy muy muy muy muy muy muy muy muy muy simple"""
    return {"message": "Test muy muy muy muy muy muy muy muy muy muy muy muy simple funcionando"}

@app.get("/packages")
async def packages_page(request: Request):
    """Página de gestión de paquetes - Solo para usuarios autenticados"""
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        return RedirectResponse(url="/auth/login?redirect=/packages", status_code=302)
    
    return templates.TemplateResponse("packages/list.html", context)

@app.get("/packages/detail")
async def package_detail_page(request: Request):
    """Página de detalle del paquete - Solo para usuarios autenticados"""
    context = await get_auth_context_from_request(request)
    
    if not context["is_authenticated"]:
        return RedirectResponse(url="/auth/login?redirect=/packages/detail", status_code=302)
    
    return templates.TemplateResponse("packages/detail.html", context)

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

@app.get("/test-profile-auth")
async def test_profile_auth(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies)
):
    """Endpoint de prueba para verificar autenticación"""
    return {
        "message": "Autenticación exitosa",
        "user_id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email
    }

@app.post("/profile/update")
async def update_profile_simple(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Actualizar perfil - Usando el mismo patrón que admin/users/update"""
    try:
        # Obtener datos del request JSON
        data = await request.json()
        
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        full_name = data.get("full_name", "").strip()
        phone = data.get("phone", "").strip() or None
        
        # Validaciones básicas
        if not all([username, email, full_name]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los campos username, email y full_name son obligatorios"
            )
        
        # Verificar username único si se está cambiando
        if username.lower() != current_user.username:
            existing = db.query(User).filter(
                and_(
                    User.username == username.lower(),
                    User.id != current_user.id
                )
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre de usuario '{username}' ya existe"
                )
        
        # Verificar email único si se está cambiando
        if email.lower() != current_user.email:
            existing = db.query(User).filter(
                and_(
                    User.email == email.lower(),
                    User.id != current_user.id
                )
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El email '{email}' ya está registrado"
                )
        
        # Actualizar usuario
        current_user.username = username.lower()
        current_user.email = email.lower()
        current_user.full_name = full_name
        current_user.phone = phone
        
        # Separar nombre completo en first_name y last_name
        # Nota: first_name y last_name son propiedades calculadas del full_name
        # No necesitamos asignarlas ya que se calculan automáticamente
        
        current_user.updated_at = get_colombia_now()
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "message": "Perfil actualizado exitosamente",
            "user": {
                "id": str(current_user.id),
                "username": current_user.username,
                "email": current_user.email,
                "full_name": current_user.full_name,
                "phone": current_user.phone
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar perfil: {str(e)}"
        )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
