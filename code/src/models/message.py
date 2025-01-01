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
from ..config import settings
from datetime import datetime

class MessageType(str, enum.Enum):
    """Tipos de mensaje"""
    INTERNAL = "internal"
    SUPPORT = "support"
    SYSTEM = "system"
    CUSTOMER_INQUIRY = "customer_inquiry"  # Nueva consulta de cliente

class MessageStatus(str, enum.Enum):
    """Estados de mensaje"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Message(BaseModel, Base):
    """Modelo de mensajes internos y consultas de clientes"""
    __tablename__ = "messages"
    
    if settings.database_url.startswith("sqlite"):
        sender_id = Column(String(36), ForeignKey("users.id"), nullable=True)  # Nullable para consultas de clientes
    else:
        sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Nullable para consultas de clientes
    
    # Campos para consultas de clientes
    customer_name = Column(String(100), nullable=True)
    customer_phone = Column(String(20), nullable=True)
    customer_email = Column(String(100), nullable=True)
    
    # Campos para referencia al paquete
    package_guide_number = Column(String(50), nullable=True)
    package_tracking_code = Column(String(10), nullable=True)
    
    # Campos del mensaje
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType), default=MessageType.CUSTOMER_INQUIRY)
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING)
    
    # Campos de timestamp
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Campos de seguimiento
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    read_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Respuesta del administrador
    admin_response = Column(Text, nullable=True)
    responded_at = Column(DateTime, nullable=True)
    responded_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relaciones
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages")
    read_by = relationship("User", foreign_keys=[read_by_id])
    responded_by = relationship("User", foreign_keys=[responded_by_id])
    
    def __repr__(self):
        return f"<Message {self.subject} - {self.message_type} - {self.status}>"
    
    @property
    def is_customer_inquiry(self):
        """Verifica si es una consulta de cliente"""
        return self.message_type == MessageType.CUSTOMER_INQUIRY
    
    @property
    def is_resolved(self):
        """Verifica si el mensaje está resuelto"""
        return self.status in [MessageStatus.RESOLVED, MessageStatus.CLOSED]
    
    def mark_as_read(self, user_id):
        """Marca el mensaje como leído"""
        self.is_read = True
        self.read_at = datetime.now()
        self.read_by_id = user_id
    
    def respond(self, response, user_id):
        """Responde al mensaje"""
        self.admin_response = response
        self.responded_at = datetime.now()
        self.responded_by_id = user_id
        self.status = MessageStatus.RESOLVED
