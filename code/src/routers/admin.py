# ========================================
# PAQUETES EL CLUB v3.0 - Router de Administración
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
import uuid
from ..database.database import get_db
from ..models.user import User, UserRole
from ..schemas.user import UserCreate, UserUpdate, UserResponse, UserActivityLogResponse
from ..dependencies import get_current_user, get_current_admin_user, get_current_admin_user_from_cookies
from ..utils.auth import verify_password, get_password_hash
from ..services.user_service import UserService

router = APIRouter(tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user_from_cookies)
):
    """Obtener lista de usuarios - Solo para administradores"""
    users = db.query(User).all()
    return [UserResponse.from_orm(user) for user in users]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user_from_cookies)
):
    """Obtener usuario específico - Solo para administradores"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserResponse.from_orm(user)

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user_from_cookies)
):
    """Crear nuevo usuario - Solo para administradores"""
    
    # Verificar si el username ya existe
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe"
        )
    
    # Verificar si el email ya existe
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya existe"
        )
    
    # Verificar restricción de admin único
    if user_data.role == UserRole.ADMIN:
        existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario administrador en el sistema. Solo puede haber un admin."
            )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password,
        role=user_data.role,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user_from_cookies)
):
    """Actualizar usuario - Solo para administradores"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden acceder a esta función."
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar si el username ya existe (excluyendo el usuario actual)
    if user_data.username != user.username:
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe"
            )
    
    # Verificar si el email ya existe (excluyendo el usuario actual)
    if user_data.email != user.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya existe"
            )
    
    # Verificar restricción de admin único (solo si se está cambiando a admin)
    if user_data.role == UserRole.ADMIN and user.role != UserRole.ADMIN:
        existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario administrador en el sistema. Solo puede haber un admin."
            )
    
    # Actualizar campos (first_name y last_name se calculan automáticamente desde full_name)
    user.username = user_data.username
    user.email = user_data.email
    # Construir full_name si tenemos first_name y last_name separados
    if user_data.first_name and user_data.last_name:
        user.full_name = f"{user_data.first_name} {user_data.last_name}"
    elif user_data.first_name:
        user.full_name = user_data.first_name
    user.role = user_data.role
    
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/users/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user_from_cookies)
):
    """Activar/desactivar usuario - Solo para administradores"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden acceder a esta función."
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir desactivar al propio usuario
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta"
        )
    
    # Cambiar estado
    user.is_active = not user.is_active
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": f"Usuario {'activado' if user.is_active else 'desactivado'} correctamente",
        "is_active": user.is_active
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user_from_cookies)
):
    """Eliminar usuario - Solo para administradores"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo administradores pueden acceder a esta función."
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir eliminar al propio usuario
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    # No permitir eliminar al único admin
    if user.role == UserRole.ADMIN:
        admin_count = db.query(User).filter(User.role == UserRole.ADMIN).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar al único administrador del sistema"
            )
    
    db.delete(user)
    db.commit()
    
    return {"message": "Usuario eliminado correctamente"}

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: uuid.UUID,
    role_data: dict,
    current_user: User = Depends(get_current_admin_user_from_cookies),
    user_service: UserService = Depends(lambda: UserService(db)),
    request: Request = None
):
    """Actualizar rol de usuario (solo admin)"""
    try:
        new_role = UserRole(role_data.get("role"))
        updated_user = user_service.update_user_role(
            user_id=user_id,
            new_role=new_role,
            admin_user=current_user,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        return {
            "message": f"Rol actualizado exitosamente para {updated_user.username}",
            "user": UserResponse.from_orm(updated_user)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: uuid.UUID,
    status_data: dict,
    current_user: User = Depends(get_current_admin_user_from_cookies),
    user_service: UserService = Depends(lambda: UserService(db)),
    request: Request = None
):
    """Actualizar estado de usuario (solo admin)"""
    try:
        is_active = status_data.get("is_active", True)
        updated_user = user_service.update_user_status(
            user_id=user_id,
            is_active=is_active,
            admin_user=current_user,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        return {
            "message": f"Estado actualizado exitosamente para {updated_user.username}",
            "user": UserResponse.from_orm(updated_user)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/users/{user_id}/activity-logs")
async def get_user_activity_logs_admin(
    user_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_admin_user_from_cookies),
    user_service: UserService = Depends(lambda: UserService(db))
):
    """Obtener logs de actividad de un usuario (solo admin)"""
    try:
        logs = user_service.get_user_activity_logs(user_id, limit, offset)
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

@router.get("/package-management")
async def package_management_page(
    request: Request,
    current_user: User = Depends(get_current_admin_user_from_cookies)
):
    """Página de gestión de paquetes - Solo para administradores"""
    from fastapi.templating import Jinja2Templates
    from pathlib import Path
    
    templates = Jinja2Templates(directory=str(Path(__file__).parent.parent.parent / "templates"))
    
    return templates.TemplateResponse(
        "admin/package_management.html",
        {
            "request": request,
            "user": current_user
        }
    )
