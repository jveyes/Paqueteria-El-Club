# ========================================
# PAQUETES EL CLUB v3.1 - Router de Autenticación
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..database.database import get_db
from ..models.user import User, UserRole
from ..schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserLogin, 
    UserChangePassword, UserResetPassword, UserRequestReset,
    TokenResponse, PasswordResetTokenResponse
)
from ..services.user_service import UserService
from ..utils.auth import create_user_token
from ..dependencies import (
    get_current_user, get_current_active_user, 
    get_current_admin_user, get_user_service
)

router = APIRouter(tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Iniciar sesión de usuario"""
    user_service = UserService(db)
    
    # Autenticar usuario
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token = create_user_token(user.id, user.username, user.role.value)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Registrar nuevo usuario (solo admin puede crear usuarios)"""
    try:
        user = user_service.create_user(user_data)
        return UserResponse.from_orm(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Obtener información del usuario actual"""
    return UserResponse.from_orm(current_user)

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """Actualizar información del usuario actual"""
    try:
        # No permitir cambiar el rol desde aquí
        if user_data.role:
            user_data.role = None
        
        updated_user = user_service.update_user(current_user.id, user_data)
        return UserResponse.from_orm(updated_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/change-password")
async def change_password(
    password_data: UserChangePassword,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """Cambiar contraseña del usuario actual"""
    try:
        user_service.change_password(
            current_user.id,
            password_data.current_password,
            password_data.new_password
        )
        return {"message": "Contraseña cambiada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/request-reset", response_model=PasswordResetTokenResponse)
async def request_password_reset(
    reset_data: UserRequestReset,
    user_service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db)
):
    """Solicitar restablecimiento de contraseña"""
    reset_token = user_service.create_password_reset_token(reset_data.email)
    
    if not reset_token:
        # No revelar si el email existe o no
        return PasswordResetTokenResponse(
            message="Si el email existe, se enviará un enlace de restablecimiento",
            expires_at=None
        )
    
    # Enviar email con el token
    try:
        from ..services.notification_service import NotificationService
        notification_service = NotificationService(db)
        
        # Obtener el usuario
        user = user_service.get_user_by_email(reset_data.email)
        if user:
            email_sent = await notification_service.send_password_reset_email(user, reset_token.token)
            
            if email_sent:
                return PasswordResetTokenResponse(
                    message="Se ha enviado un enlace de restablecimiento a tu correo electrónico",
                    expires_at=reset_token.expires_at
                )
            else:
                # Si falla el envío de email, pero el token se creó correctamente
                return PasswordResetTokenResponse(
                    message="Se ha creado el enlace de restablecimiento, pero hubo un problema enviando el email. Contacta al administrador.",
                    expires_at=reset_token.expires_at
                )
        else:
            # Esto no debería pasar ya que el token se creó
            return PasswordResetTokenResponse(
                message="Error interno del sistema. Contacta al administrador.",
                expires_at=reset_token.expires_at
            )
            
    except Exception as e:
        # Log del error pero no revelar detalles al usuario
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error enviando email de reset: {e}")
        
        return PasswordResetTokenResponse(
            message="Si el email existe, se enviará un enlace de restablecimiento",
            expires_at=reset_token.expires_at
        )

@router.post("/reset-password")
async def reset_password(
    reset_data: UserResetPassword,
    user_service: UserService = Depends(get_user_service)
):
    """Restablecer contraseña usando token"""
    try:
        user_service.reset_password(reset_data.token, reset_data.new_password)
        return {"message": "Contraseña restablecida exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout")
async def logout():
    """Cerrar sesión (el token se invalida en el cliente)"""
    return {"message": "Sesión cerrada exitosamente"}

# Rutas de administración de usuarios (solo admin)

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Listar todos los usuarios (solo admin)"""
    users = user_service.get_all_users(skip=skip, limit=limit)
    return [UserResponse.from_orm(user) for user in users]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Obtener usuario específico (solo admin)"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return UserResponse.from_orm(user)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Actualizar usuario (solo admin)"""
    try:
        updated_user = user_service.update_user(user_id, user_data)
        return UserResponse.from_orm(updated_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Eliminar usuario (solo admin)"""
    try:
        user_service.delete_user(user_id)
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/users/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """Obtener estadísticas de usuarios (solo admin)"""
    return user_service.get_user_stats()
