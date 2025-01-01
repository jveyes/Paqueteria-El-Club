# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Paquete
# ========================================

from sqlalchemy import Column, String, Text, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import BaseModel
from ..database.database import Base
from .customer import Customer
from .file import File

class PackageStatus(str, enum.Enum):
    """Estados del paquete"""
    ANUNCIADO = "anunciado"
    RECIBIDO = "recibido"
    EN_TRANSITO = "en_transito"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class PackageType(str, enum.Enum):
    """Tipos de paquete"""
    NORMAL = "normal"
    EXTRA_DIMENSIONADO = "extra_dimensionado"

class PackageCondition(str, enum.Enum):
    """Condición del paquete"""
    BUENO = "bueno"
    REGULAR = "regular"
    MALO = "malo"

class Package(BaseModel, Base):
    """Modelo de paquete"""
    __tablename__ = "packages"
    
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    status = Column(Enum(PackageStatus), default=PackageStatus.ANUNCIADO)
    package_type = Column(Enum(PackageType), default=PackageType.NORMAL)
    package_condition = Column(Enum(PackageCondition), default=PackageCondition.BUENO)
    storage_cost = Column(Numeric(10, 2), default=0)
    delivery_cost = Column(Numeric(10, 2), default=0)
    total_cost = Column(Numeric(10, 2), default=0)
    observations = Column(Text, nullable=True)
    
    # Timestamps específicos
    announced_at = Column(DateTime, nullable=True)
    received_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    
    # Relaciones - Solo UUID para PostgreSQL AWS RDS
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    customer = relationship("Customer", back_populates="packages")
    notifications = relationship("Notification", back_populates="package")
    files = relationship("File", back_populates="package")
    
    def __repr__(self):
        return f"<Package {self.tracking_number} - {self.status}>"
