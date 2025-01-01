# ========================================
# PAQUETES EL CLUB v3.0 - Router de Tarifas
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database.database import get_db
from ..models.rate import Rate, RateType
from ..schemas.rate import RateCreate, RateResponse, RateUpdate, RateCalculation
from ..dependencies import get_current_active_user, get_current_admin_user
from ..utils.datetime_utils import get_colombia_now

router = APIRouter()

@router.get("/", response_model=List[RateResponse])
async def list_rates(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar tarifas"""
    rates = db.query(Rate).filter(Rate.is_active == True).all()
    return rates

@router.post("/", response_model=RateResponse)
async def create_rate(
    rate_data: RateCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Crear nueva tarifa"""
    # Desactivar tarifas anteriores del mismo tipo
    existing_rates = db.query(Rate).filter(
        Rate.rate_type == rate_data.rate_type,
        Rate.is_active == True
    ).all()
    
    for rate in existing_rates:
        rate.is_active = False
        rate.valid_to = get_colombia_now()
    
    # Crear nueva tarifa
    db_rate = Rate(**rate_data.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    
    return db_rate

@router.post("/calculate")
async def calculate_rate(
    calculation_data: RateCalculation,
    db: Session = Depends(get_db)
):
    """Calcular tarifa para un paquete"""
    # Cálculo simplificado
    base_storage = 1000
    base_delivery = 1500
    
    if calculation_data.package_type.value == "extra_dimensionado":
        base_storage *= 1.5
        base_delivery *= 1.5
    
    storage_cost = base_storage * calculation_data.storage_days
    delivery_cost = base_delivery if calculation_data.delivery_required else 0
    total_cost = storage_cost + delivery_cost
    
    return {
        "package_type": calculation_data.package_type,
        "storage_days": calculation_data.storage_days,
        "delivery_required": calculation_data.delivery_required,
        "storage_cost": storage_cost,
        "delivery_cost": delivery_cost,
        "total_cost": total_cost,
        "currency": "COP"
    }
