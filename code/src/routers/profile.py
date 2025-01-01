# ========================================
# PAQUETES EL CLUB v3.1 - Router de Perfiles
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from ..database.database import get_db
from ..models.user import User
from ..schemas.user import UserUpdate, UserChangePassword, UserProfile, UserActivityLogResponse
from ..services.user_service import UserService
from ..dependencies import get_user_service
from ..dependencies import get_current_active_user_from_cookies, get_current_active_user
from fastapi.templating import Jinja2Templates
from ..utils.auth_context import get_auth_context_from_request
from ..utils.datetime_utils import get_colombia_now
router = APIRouter(prefix="/profile", tags=["profile"])

# Configurar templates
templates = Jinja2Templates(directory="templates")

def get_auth_context(request: Request, is_authenticated: bool = False, user_name: str = None):
    """Función helper para contexto de autenticación"""
    return {
        "request": request,
        "is_authenticated": is_authenticated,
        "user_name": user_name
    }

# ========================================
# VISTAS DE PERFIL
# ========================================

@router.get("/", response_class=HTMLResponse)
async def profile_page(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Página principal del perfil de usuario"""
    context = await get_auth_context_from_request(request)
    context["user"] = current_user
    return templates.TemplateResponse("profile/profile.html", context)

@router.get("", response_class=HTMLResponse)
async def profile_page_no_slash(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Página principal del perfil de usuario (sin barra final)"""
    context = await get_auth_context_from_request(request)
    context["user"] = current_user
    return templates.TemplateResponse("profile/profile.html", context)

@router.get("/edit", response_class=HTMLResponse)
async def edit_profile_page(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Página para editar perfil"""
    context = await get_auth_context_from_request(request)
    context["user"] = current_user
    return templates.TemplateResponse("profile/edit.html", context)

@router.get("/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Página para cambiar contraseña"""
    context = await get_auth_context_from_request(request)
    context["user"] = current_user
    return templates.TemplateResponse("profile/change-password.html", context)

# ========================================
# API ENDPOINTS
# ========================================

@router.get("/api/profile", response_model=UserProfile)
async def get_profile(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Obtener información del perfil del usuario actual"""
    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        full_name=current_user.full_name,
        phone=current_user.phone,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.get("/api/profile/test")
async def test_profile_auth(request: Request, current_user: User = Depends(get_current_active_user_from_cookies)):
    """Endpoint de prueba para verificar autenticación"""
    return {
        "message": "Autenticación exitosa desde router",
        "user_id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email
    }

@router.put("/api/profile/update-simple")
async def update_profile_simple(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Actualizar perfil de usuario - Versión simple"""
    try:
        # Obtener datos del request
        data = await request.json()
        
        # Validar datos básicos
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        full_name = data.get("full_name", "").strip()
        phone = data.get("phone", "").strip() or None
        
        if not username or not email or not full_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los campos username, email y full_name son obligatorios"
            )
        
        # Actualizar usuario directamente
        current_user.username = username.lower()
        current_user.email = email.lower()
        current_user.full_name = full_name
        current_user.phone = phone
        
        # Nota: first_name y last_name son propiedades calculadas del full_name
        # No necesitamos asignarlas ya que se calculan automáticamente
        
        current_user.updated_at = get_colombia_now()
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "message": "Perfil actualizado exitosamente desde router",
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

@router.put("/api/profile")
async def update_profile(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    user_service: UserService = Depends(get_user_service)
):
    """Actualizar información del perfil"""
    try:
        # Obtener datos del request JSON
        data = await request.json()
        
        # Crear UserUpdate desde los datos JSON
        user_data = UserUpdate(
            username=data.get("username"),
            email=data.get("email"),
            full_name=data.get("full_name"),
            phone=data.get("phone")
        )
        
        updated_user = user_service.update_user_profile(
            user_id=current_user.id,
            user_data=user_data,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        return {
            "message": "Perfil actualizado exitosamente",
            "user": UserProfile(
                id=updated_user.id,
                username=updated_user.username,
                email=updated_user.email,
                first_name=updated_user.first_name,
                last_name=updated_user.last_name,
                full_name=updated_user.full_name,
                phone=updated_user.phone,
                role=updated_user.role,
                is_active=updated_user.is_active,
                profile_photo=updated_user.profile_photo,
                created_at=updated_user.created_at,
                updated_at=updated_user.updated_at
            )
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/api/change-password")
async def change_password(
    password_data: UserChangePassword,
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    user_service: UserService = Depends(get_user_service)
):
    """Cambiar contraseña del usuario"""
    try:
        user_service.change_password(
            user_id=current_user.id,
            current_password=password_data.current_password,
            new_password=password_data.new_password,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        return {"message": "Contraseña cambiada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/api/profile/activity")
async def get_user_activity(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    db: Session = Depends(get_db)
):
    """Obtener actividad reciente del usuario"""
    try:
        # Obtener anuncios creados por el usuario
        try:
            from ..models.package_announcement import PackageAnnouncement
            recent_announcements = db.query(PackageAnnouncement).filter(
                PackageAnnouncement.created_by_id == current_user.id
            ).order_by(PackageAnnouncement.created_at.desc()).limit(10).all()
        except ImportError:
            recent_announcements = []
        
        # Por ahora, no incluimos archivos para evitar errores
        recent_files = []
        
        return {
            "announcements": [
                {
                    "id": str(ann.id),
                    "tracking_code": ann.tracking_code,
                    "customer_name": ann.customer_name,
                    "created_at": ann.created_at.isoformat() if ann.created_at else None,
                    "status": ann.status
                } for ann in recent_announcements
            ],
            "files": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener actividad: {str(e)}"
        )

@router.get("/api/profile/activity-logs")
async def get_user_activity_logs(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_active_user_from_cookies),
    user_service: UserService = Depends(get_user_service)
):
    """Obtener logs de actividad del usuario actual"""
    try:
        logs = user_service.get_user_activity_logs(current_user.id, limit, offset)
        return [
            UserActivityLogResponse(
                id=log.id,
                activity_type=log.activity_type.value,
                description=log.description,
                ip_address=log.ip_address,
                created_at=log.created_at,
                activity_metadata=log.activity_metadata
            ) for log in logs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener logs de actividad: {str(e)}"
        )

@router.get("/api/profile/activity-stats")
async def get_user_activity_stats(
    request: Request,
    days: int = 30,
    current_user: User = Depends(get_current_active_user_from_cookies),
    user_service: UserService = Depends(get_user_service)
):
    """Obtener estadísticas de actividad del usuario actual"""
    try:
        return user_service.get_user_activity_stats(current_user.id, days)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

@router.put("/api/profile/upload-photo")
async def upload_profile_photo(
    request: Request,
    current_user: User = Depends(get_current_active_user_from_cookies),
    user_service: UserService = Depends(get_user_service)
):
    """Subir foto de perfil"""
    try:
        # Aquí implementarías la lógica de subida de archivos
        # Por ahora, simulamos la actualización
        form_data = await request.form()
        photo_url = form_data.get("photo_url", "")
        
        user_data = UserUpdate(profile_photo=photo_url)
        updated_user = user_service.update_user_profile(
            user_id=current_user.id,
            user_data=user_data,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        
        return {
            "message": "Foto de perfil actualizada exitosamente",
            "profile_photo": updated_user.profile_photo
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
