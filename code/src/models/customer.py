# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Cliente
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
    country_code = Column(String(5), default='+57')
    phone_formatted = Column(String(25), nullable=True)
    phone_country = Column(String(50), default='Colombia')
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relaciones
    packages = relationship("Package", back_populates="customer")
    
    # Índices
    __table_args__ = (
        Index('idx_customer_phone', 'phone'),
        Index('idx_customer_name', 'name'),
        Index('idx_customer_country', 'country_code'),
    )
    
    def __repr__(self):
        return f"<Customer {self.name} - {self.tracking_number}>"
