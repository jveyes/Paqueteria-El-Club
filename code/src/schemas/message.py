# ========================================
# PAQUETES EL CLUB v3.0 - Schemas de Mensajes
# ========================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """Tipos de mensaje"""
    INTERNAL = "internal"
    SUPPORT = "support"
    SYSTEM = "system"
    CUSTOMER_INQUIRY = "customer_inquiry"

class MessageStatus(str, Enum):
    """Estados de mensaje"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class CustomerInquiryCreate(BaseModel):
    """Schema para crear consulta de cliente"""
    customer_name: str = Field(..., min_length=2, max_length=100, description="Nombre del cliente")
    customer_phone: str = Field(..., min_length=7, max_length=20, description="Teléfono del cliente")
    customer_email: str = Field(..., max_length=100, description="Email del cliente")
    package_guide_number: Optional[str] = Field(None, max_length=50, description="Número de guía del paquete")
    package_tracking_code: Optional[str] = Field(None, max_length=10, description="Código de tracking del paquete")
    subject: str = Field(..., min_length=5, max_length=200, description="Asunto de la consulta")
    content: str = Field(..., min_length=10, max_length=2000, description="Contenido de la consulta")

class MessageResponse(BaseModel):
    """Schema para respuesta de mensaje"""
    response: str = Field(..., min_length=5, max_length=2000, description="Respuesta del administrador")

class MessageList(BaseModel):
    """Schema para listar mensajes"""
    id: str
    customer_name: Optional[str]
    customer_phone: Optional[str]
    subject: str
    content: str
    message_type: MessageType
    status: MessageStatus
    is_read: bool
    created_at: datetime
    package_guide_number: Optional[str]
    package_tracking_code: Optional[str]
    
    class Config:
        from_attributes = True

class MessageDetail(BaseModel):
    """Schema para detalle de mensaje"""
    id: str
    customer_name: Optional[str]
    customer_phone: Optional[str]
    customer_email: Optional[str]
    subject: str
    content: str
    message_type: MessageType
    status: MessageStatus
    is_read: bool
    read_at: Optional[datetime]
    read_by_name: Optional[str]
    created_at: datetime
    package_guide_number: Optional[str]
    package_tracking_code: Optional[str]
    admin_response: Optional[str]
    responded_at: Optional[datetime]
    responded_by_name: Optional[str]
    
    class Config:
        from_attributes = True

class MessageStats(BaseModel):
    """Schema para estadísticas de mensajes"""
    total_messages: int
    pending_messages: int
    resolved_messages: int
    unread_messages: int
