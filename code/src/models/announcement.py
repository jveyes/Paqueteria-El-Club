# ========================================
# PAQUETES EL CLUB v3.1 - Modelo de Anuncio de Paquetes
# ========================================

from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import BaseModel

class PackageAnnouncement(BaseModel):
    """Modelo para anuncios de paquetes"""
    __tablename__ = "package_announcements"
    
    # Información del cliente
    customer_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    
    # Información del paquete
    guide_number = Column(String(50), unique=True, nullable=False, index=True)
    tracking_code = Column(String(4), unique=True, nullable=False, index=True)
    
    # Estado del anuncio
    is_active = Column(Boolean, default=True, nullable=False)
    is_processed = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    announced_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    
    # Relaciones (opcional)
    customer_id = Column(UUID(as_uuid=True), nullable=True)
    package_id = Column(UUID(as_uuid=True), nullable=True)
    
    def __repr__(self):
        return f"<PackageAnnouncement {self.guide_number} - {self.customer_name}>"
    
    @property
    def status(self):
        """Estado del anuncio"""
        if not self.is_active:
            return "inactivo"
        elif self.is_processed:
            return "procesado"
        else:
            return "pendiente"
