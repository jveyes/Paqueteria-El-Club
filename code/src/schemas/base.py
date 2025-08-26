# ========================================
# PAQUETES EL CLUB v3.0 - Esquemas Base
# ========================================

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class BaseSchema(BaseModel):
    """Esquema base con configuración"""
    model_config = ConfigDict(from_attributes=True)

class BaseSchemaWithTimestamps(BaseSchema):
    """Esquema base con timestamps"""
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
