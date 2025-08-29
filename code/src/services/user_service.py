# ========================================
# PAQUETES EL CLUB v3.1 - Servicio de Usuarios
# ========================================

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import uuid
import logging

from ..models.user import User, UserRole
from ..models.password_reset import PasswordResetToken
from ..schemas.user import UserCreate, UserUpdate
from ..utils.auth import get_password_hash, verify_password, generate_secure_password
from ..utils.exceptions import UserException
from ..utils.datetime_utils import get_colombia_now

logger = logging.getLogger(__name__)

class UserService:
    """Servicio para la lógica de negocio de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Crear nuevo usuario"""
        # Verificar que el username no exista
        existing_user = self.db.query(User).filter(
            User.username == user_data.username.lower()
        ).first()
        
        if existing_user:
            raise UserException(f"El nombre de usuario '{user_data.username}' ya existe")
        
        # Verificar que el email no exista
        existing_email = self.db.query(User).filter(
            User.email == user_data.email.lower()
        ).first()
        
        if existing_email:
            raise UserException(f"El email '{user_data.email}' ya está registrado")
        
        # Crear usuario
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            username=user_data.username.lower(),
            email=user_data.email.lower(),
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            phone=user_data.phone,
            notes=user_data.notes,
            role=user_data.role,
            is_active=user_data.is_active,
            is_verified=True  # Por defecto verificados
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        logger.info(f"Usuario creado: {db_user.username} ({db_user.role})")
        return db_user
    
    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Obtener usuario por ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        return self.db.query(User).filter(User.username == username.lower()).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email.lower()).first()
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtener todos los usuarios con paginación"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_active_users(self) -> List[User]:
        """Obtener usuarios activos"""
        return self.db.query(User).filter(User.is_active == True).all()
    
    def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        """Actualizar usuario"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise UserException("Usuario no encontrado")
        
        # Verificar username único si se está cambiando
        if user_data.username and user_data.username.lower() != user.username:
            existing = self.db.query(User).filter(
                and_(
                    User.username == user_data.username.lower(),
                    User.id != user_id
                )
            ).first()
            if existing:
                raise UserException(f"El nombre de usuario '{user_data.username}' ya existe")
        
        # Verificar email único si se está cambiando
        if user_data.email and user_data.email.lower() != user.email:
            existing = self.db.query(User).filter(
                and_(
                    User.email == user_data.email.lower(),
                    User.id != user_id
                )
            ).first()
            if existing:
                raise UserException(f"El email '{user_data.email}' ya está registrado")
        
        # Actualizar campos
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "username" and value:
                setattr(user, field, value.lower())
            elif field == "email" and value:
                setattr(user, field, value.lower())
            else:
                setattr(user, field, value)
        
        user.updated_at = get_colombia_now()
        
        self.db.commit()
        self.db.refresh(user)
        
        logger.info(f"Usuario actualizado: {user.username}")
        return user
    
    def delete_user(self, user_id: uuid.UUID) -> bool:
        """Eliminar usuario (desactivar)"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise UserException("Usuario no encontrado")
        
        # No permitir eliminar el último admin
        if user.role == UserRole.ADMIN:
            admin_count = self.db.query(User).filter(
                and_(
                    User.role == UserRole.ADMIN,
                    User.is_active == True
                )
            ).count()
            
            if admin_count <= 1:
                raise UserException("No se puede eliminar el último administrador")
        
        user.is_active = False
        user.updated_at = get_colombia_now()
        
        self.db.commit()
        
        logger.info(f"Usuario desactivado: {user.username}")
        return True
    
    def change_password(self, user_id: uuid.UUID, current_password: str, new_password: str) -> bool:
        """Cambiar contraseña de usuario"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise UserException("Usuario no encontrado")
        
        # Verificar contraseña actual
        if not verify_password(current_password, user.hashed_password):
            raise UserException("Contraseña actual incorrecta")
        
        # Actualizar contraseña
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = get_colombia_now()
        
        self.db.commit()
        
        logger.info(f"Contraseña cambiada para usuario: {user.username}")
        return True
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """Restablecer contraseña usando token"""
        # Buscar token válido
        reset_token = self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token
        ).first()
        
        if not reset_token:
            raise UserException("Token de restablecimiento inválido")
        
        if not reset_token.is_valid:
            raise UserException("Token de restablecimiento expirado o ya usado")
        
        # Obtener usuario
        user = self.get_user_by_id(reset_token.user_id)
        if not user:
            raise UserException("Usuario no encontrado")
        
        # Actualizar contraseña
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = get_colombia_now()
        
        # Marcar token como usado
        reset_token.mark_as_used()
        
        self.db.commit()
        
        logger.info(f"Contraseña restablecida para usuario: {user.username}")
        return True
    
    def create_password_reset_token(self, email: str) -> Optional[PasswordResetToken]:
        """Crear token de restablecimiento de contraseña"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        # Invalidar tokens anteriores del usuario
        self.db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id
        ).update({"is_used": True})
        
        # Crear nuevo token
        reset_token = PasswordResetToken.create_token(user.id)
        
        self.db.add(reset_token)
        self.db.commit()
        self.db.refresh(reset_token)
        
        logger.info(f"Token de restablecimiento creado para: {user.email}")
        return reset_token
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autenticar usuario por username o email"""
        # Primero intentar por username
        user = self.get_user_by_username(username)
        
        # Si no se encuentra por username, intentar por email
        if not user:
            user = self.get_user_by_email(username)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def get_user_stats(self) -> dict:
        """Obtener estadísticas de usuarios"""
        total_users = self.db.query(User).count()
        active_users = self.db.query(User).filter(User.is_active == True).count()
        admin_users = self.db.query(User).filter(
            and_(
                User.role == UserRole.ADMIN,
                User.is_active == True
            )
        ).count()
        operator_users = self.db.query(User).filter(
            and_(
                User.role == UserRole.OPERATOR,
                User.is_active == True
            )
        ).count()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "admin_users": admin_users,
            "operator_users": operator_users
        }
