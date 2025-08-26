# ========================================
# PAQUETES EL CLUB v3.0 - Router de Autenticación
# ========================================

import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from jose import JWTError, jwt

from ..database.database import get_db
from ..models.user import User, PasswordResetToken
from ..schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, LoginResponse, LogoutResponse, AuthCheckResponse
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..utils.helpers import verify_password, get_password_hash
from ..services.notification_service import NotificationService
from ..config import settings
from ..dependencies import create_access_token, oauth2_scheme

router = APIRouter(prefix="/api/auth", tags=["authentication"])

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Obtener usuario actual desde token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario activo actual"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    # Verificar si ya existe un admin
    existing_admin = db.query(User).filter(User.role == "ADMIN").first()
    if existing_admin and user_data.role == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un administrador en el sistema"
        )
    
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o email ya existe"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = None,
    db: Session = Depends(get_db)
):
    """Iniciar sesión"""
    # Buscar usuario por username o email (case insensitive)
    username_or_email = form_data.username.lower()
    user = db.query(User).filter(
        (User.username.ilike(username_or_email)) | (User.email.ilike(username_or_email))
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Configurar cookies de autenticación
    if response:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,  # 30 minutos
            samesite="lax"
        )
        response.set_cookie(
            key="user_id",
            value=str(user.id),
            httponly=True,
            max_age=1800,
            samesite="lax"
        )
        response.set_cookie(
            key="user_name",
            value=user.first_name,
            httponly=False,
            max_age=1800,
            samesite="lax"
        )
        response.set_cookie(
            key="user_role",
            value=user.role,
            httponly=False,
            max_age=1800,
            samesite="lax"
        )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Cerrar sesión"""
    # En una implementación más robusta, se invalidaría el token
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Obtener información del usuario actual"""
    return current_user

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Solicitar recuperación de contraseña"""
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Por seguridad, no revelamos si el email existe o no
        return {
            "message": "Se ha enviado un enlace de recuperación a tu correo electrónico",
            "email": request.email
        }
    
    if not user.is_active:
        return {
            "message": "Se ha enviado un enlace de recuperación a tu correo electrónico",
            "email": request.email
        }
    
    # Generar token único
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Crear token de reset
    reset_token = PasswordResetToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at
    )
    
    db.add(reset_token)
    db.commit()
    
    # Enviar email
    notification_service = NotificationService(db)
    email_sent = await notification_service.send_password_reset_email(user, token)
    
    if email_sent:
        return {
            "message": "Se ha enviado un enlace de recuperación a tu correo electrónico",
            "email": request.email
        }
    else:
        # Si falla el envío, eliminar el token
        db.delete(reset_token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al enviar el email de recuperación"
        )

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Restablecer contraseña"""
    # Buscar token válido
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token
    ).first()
    
    if not reset_token or not reset_token.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    # Validar nueva contraseña
    if len(request.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres"
        )
    
    # Obtener usuario
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no encontrado"
        )
    
    # Actualizar contraseña
    user.hashed_password = get_password_hash(request.new_password)
    
    # Marcar token como usado
    reset_token.used = True
    
    db.commit()
    
    return {
        "message": "Contraseña actualizada exitosamente"
    }

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar perfil del usuario actual"""
    # Verificar si el username ya existe (excluyendo el usuario actual)
    if user_data.username != current_user.username:
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe"
            )
    
    # Verificar si el email ya existe (excluyendo el usuario actual)
    if user_data.email != current_user.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya existe"
            )
    
    # Actualizar campos
    current_user.username = user_data.username
    current_user.email = user_data.email
    current_user.first_name = user_data.first_name
    current_user.last_name = user_data.last_name
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.post("/change-password")
async def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cambiar contraseña del usuario actual"""
    # Verificar contraseña actual
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # Validar nueva contraseña
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe tener al menos 8 caracteres"
        )
    
    # Actualizar contraseña
    current_user.password_hash = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Contraseña cambiada exitosamente"}
