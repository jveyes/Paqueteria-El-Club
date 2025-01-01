# ========================================
# PAQUETES EL CLUB v3.1 - Modelo de Token de Restablecimiento
# ========================================

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

from .base import BaseModel
from ..database.database import Base
from ..utils.datetime_utils import get_colombia_now
from ..config import settings

class PasswordResetToken(BaseModel, Base):
    """Modelo para tokens de restablecimiento de contraseña"""
    __tablename__ = "password_reset_tokens"
    
    # ID (usar UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Token único
    token = Column(String(255), unique=True, nullable=False, index=True)
    
    # Relación con usuario
    if settings.database_url.startswith("sqlite"):
        user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    else:
        user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Estado del token
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=get_colombia_now, nullable=False)
    used_at = Column(DateTime, nullable=True)
    
    # Relación
    user = relationship("User", back_populates="password_reset_tokens")
    
    def __repr__(self):
        return f"<PasswordResetToken {self.token[:8]}... - {self.user_id}>"
    
    @property
    def is_expired(self) -> bool:
        """Verifica si el token ha expirado"""
        from datetime import datetime
        now = datetime.now()
        return now > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Verifica si el token es válido (no expirado y no usado)"""
        return not self.is_expired and not self.is_used
    
    @classmethod
    def create_token(cls, user_id: uuid.UUID, expires_in_hours: int = 24) -> "PasswordResetToken":
        """Crea un nuevo token de restablecimiento"""
        token = str(uuid.uuid4())
        expires_at = get_colombia_now() + timedelta(hours=expires_in_hours)
        
        return cls(
            token=token,
            user_id=user_id,
            expires_at=expires_at
        )
    
    def mark_as_used(self):
        """Marca el token como usado"""
        self.is_used = True
        self.used_at = get_colombia_now()
