# ========================================
# PAQUETES EL CLUB v3.1 - Modelo de Cliente
# ========================================

from sqlalchemy import Column, String, Index
from sqlalchemy.orm import relationship

from .base import BaseModel
from ..database.database import Base

class Customer(BaseModel, Base):
    """Modelo de cliente simplificado"""
    __tablename__ = "customers"
    
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relaciones
    packages = relationship("Package", back_populates="customer")
    
    # Índices
    __table_args__ = (
        Index('idx_customer_phone', 'phone'),
        Index('idx_customer_name', 'name'),
    )
    
    def __repr__(self):
        return f"<Customer {self.name} - {self.tracking_number}>"
