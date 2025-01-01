# ========================================
# PAQUETES EL CLUB v3.1 - Dependencias de Autenticación
# ========================================

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from .database.database import get_db
from .models.user import User, UserRole
from .services.user_service import UserService
from .utils.auth import get_current_user_from_token

# Configuración del esquema de autenticación
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario actual desde token JWT"""
    token = credentials.credentials
    
    # Verificar token
    user_data = get_current_user_from_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener usuario de la base de datos
    user_service = UserService(db)
    user = user_service.get_user_by_id(uuid.UUID(user_data["user_id"]))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario activo actual"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario administrador actual"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador"
        )
    return current_user

def get_current_admin_user_from_cookies(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario administrador actual desde cookies (para páginas web)"""
    user = get_current_user_from_cookies(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={
                "Location": "/auth/login",
                "Content-Type": "application/json"
            },
        )
    
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador"
        )
    return user

def get_current_operator_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario operador actual"""
    if not current_user.is_operator and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de operador"
        )
    return current_user

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Obtener servicio de usuarios"""
    return UserService(db)

def get_current_user_from_cookies(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Obtener usuario actual desde cookies (para páginas web)"""
    try:
        # Verificar si hay token en cookies
        token = request.cookies.get("access_token")
        if not token:
            return None
        
        # Verificar token
        user_data = get_current_user_from_token(token)
        if not user_data:
            return None
        
        # Obtener usuario de la base de datos
        user_service = UserService(db)
        user = user_service.get_user_by_id(uuid.UUID(user_data["user_id"]))
        
        if not user or not user.is_active:
            return None
        
        return user
    except Exception:
        return None

def get_current_active_user_from_cookies(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario activo actual desde cookies (para páginas web)"""
    user = get_current_user_from_cookies(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={
                "Location": "/auth/login",
                "Content-Type": "application/json"
            },
        )
    return user

def verify_token_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Verificar token opcionalmente (para rutas que pueden ser públicas o privadas)"""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    user_data = get_current_user_from_token(token)
    
    if not user_data:
        return None
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(uuid.UUID(user_data["user_id"]))
    
    if not user or not user.is_active:
        return None
    
    return user

def require_admin_or_self(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user)
) -> User:
    """Verificar que el usuario sea admin o el propietario del recurso"""
    if current_user.is_admin:
        return current_user
    
    if current_user.id == user_id:
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado. Solo puedes acceder a tus propios recursos"
    )
