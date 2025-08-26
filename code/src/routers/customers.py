# ========================================
# PAQUETES EL CLUB v3.0 - Router de Clientes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from ..database.database import get_db
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate, CustomerSearch
from ..dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crear nuevo cliente"""
    # Verificar si ya existe un cliente con ese tracking number
    existing_customer = db.query(Customer).filter(
        Customer.tracking_number == customer_data.tracking_number
    ).first()
    
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con ese número de tracking"
        )
    
    # Crear cliente
    db_customer = Customer(**customer_data.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer

@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar clientes con filtros"""
    query = db.query(Customer)
    
    if search:
        query = query.filter(
            or_(
                Customer.name.ilike(f"%{search}%"),
                Customer.phone.ilike(f"%{search}%"),
                Customer.tracking_number.ilike(f"%{search}%")
            )
        )
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.get("/{tracking_number}", response_model=CustomerResponse)
async def get_customer_by_tracking(
    tracking_number: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener cliente por número de tracking"""
    customer = db.query(Customer).filter(Customer.tracking_number == tracking_number).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return customer
