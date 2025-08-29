# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Notificaciones
# ========================================

from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import BaseModel
from ..database.database import Base
from ..config import settings

class NotificationType(str, enum.Enum):
    """Tipos de notificación"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

class NotificationStatus(str, enum.Enum):
    """Estados de notificación"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"

class Notification(BaseModel, Base):
    """Modelo de notificaciones"""
    __tablename__ = "notifications"
    
    if settings.database_url.startswith("sqlite"):
        package_id = Column(String(36), ForeignKey("packages.id"), nullable=True)
        user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    else:
        package_id = Column(UUID(as_uuid=True), ForeignKey("packages.id"), nullable=True)
        user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    notification_type = Column(Enum(NotificationType), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    sent_at = Column(DateTime, nullable=True)
    delivery_confirmation = Column(JSON, default=dict)
    
    # Relaciones
    package = relationship("Package", back_populates="notifications")
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.notification_type} - {self.status}>"
