# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Mensajería
# ========================================

from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import BaseModel
from ..database.database import Base

class MessageType(str, enum.Enum):
    """Tipos de mensaje"""
    INTERNAL = "internal"
    SUPPORT = "support"
    SYSTEM = "system"

class Message(BaseModel, Base):
    """Modelo de mensajes internos"""
    __tablename__ = "messages"
    
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType), default=MessageType.INTERNAL)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # Relaciones
    sender = relationship("User", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.subject} - {self.message_type}>"
