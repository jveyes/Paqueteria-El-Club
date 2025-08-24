# ========================================
# PAQUETES EL CLUB v3.0 - Router de Paquetes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import uuid
from datetime import datetime

from ..database.database import get_db
from ..models.package import Package, PackageStatus, PackageType
from ..models.customer import Customer
from ..models.rate import Rate
from ..schemas.package import PackageCreate, PackageResponse, PackageUpdate, PackageAnnounce, PackageTracking
from ..dependencies import get_current_active_user, require_operator

router = APIRouter()

def generate_tracking_number() -> str:
    """Generar número de tracking único"""
    return f"PAP{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"

@router.post("/announce", response_model=PackageResponse)
async def announce_package(
    package_data: PackageAnnounce,
    db: Session = Depends(get_db)
):
    """Anunciar nuevo paquete"""
    # Generar número de tracking único
    tracking_number = generate_tracking_number()
    
    # Calcular tarifas automáticamente (simplificado por ahora)
    storage_cost = 1000  # Tarifa base
    delivery_cost = 1500  # Tarifa base
    total_cost = storage_cost + delivery_cost
    
    # Crear paquete
    db_package = Package(
        tracking_number=tracking_number,
        customer_name=package_data.customer_name,
        customer_phone=package_data.customer_phone,
        package_type=package_data.package_type,
        package_condition=package_data.package_condition,
        observations=package_data.observations,
        storage_cost=storage_cost,
        delivery_cost=delivery_cost,
        total_cost=total_cost,
        status=PackageStatus.ANUNCIADO,
        announced_at=datetime.now()
    )
    
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    
    # Crear o actualizar cliente
    customer = db.query(Customer).filter(
        Customer.tracking_number == tracking_number
    ).first()
    
    if not customer:
        customer = Customer(
            name=package_data.customer_name,
            phone=package_data.customer_phone,
            tracking_number=tracking_number
        )
        db.add(customer)
        db.commit()
    
    return db_package

@router.get("/{tracking_number}", response_model=PackageResponse)
async def get_package_by_tracking(
    tracking_number: str,
    db: Session = Depends(get_db)
):
    """Obtener paquete por número de tracking"""
    package = db.query(Package).filter(Package.tracking_number == tracking_number).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    return package

@router.get("/", response_model=List[PackageResponse])
async def list_packages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[PackageStatus] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar paquetes con filtros"""
    query = db.query(Package)
    
    # Aplicar filtros
    if status_filter:
        query = query.filter(Package.status == status_filter)
    
    if search:
        query = query.filter(
            or_(
                Package.tracking_number.ilike(f"%{search}%"),
                Package.customer_name.ilike(f"%{search}%"),
                Package.customer_phone.ilike(f"%{search}%")
            )
        )
    
    # Aplicar paginación
    packages = query.offset(skip).limit(limit).all()
    
    return packages

@router.put("/{package_id}/receive", response_model=PackageResponse)
async def receive_package(
    package_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(require_operator)
):
    """Recibir paquete en instalaciones"""
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    if package.status != PackageStatus.ANUNCIADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El paquete no está en estado anunciado"
        )
    
    # Actualizar estado
    package.status = PackageStatus.RECIBIDO
    package.received_at = datetime.now()
    db.commit()
    db.refresh(package)
    
    return package

@router.put("/{package_id}/deliver", response_model=PackageResponse)
async def deliver_package(
    package_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(require_operator)
):
    """Entregar paquete al cliente"""
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    if package.status not in [PackageStatus.RECIBIDO, PackageStatus.EN_TRANSITO]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El paquete no está listo para entrega"
        )
    
    # Actualizar estado
    package.status = PackageStatus.ENTREGADO
    package.delivered_at = datetime.now()
    db.commit()
    db.refresh(package)
    
    return package

@router.delete("/{package_id}")
async def cancel_package(
    package_id: uuid.UUID,
    reason: str = Query(..., description="Motivo de cancelación"),
    db: Session = Depends(get_db),
    current_user = Depends(require_operator)
):
    """Cancelar paquete"""
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    if package.status == PackageStatus.ENTREGADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede cancelar un paquete entregado"
        )
    
    # Actualizar estado
    package.status = PackageStatus.CANCELADO
    package.observations = f"CANCELADO: {reason}"
    db.commit()
    
    return {"message": "Paquete cancelado exitosamente"}

@router.get("/stats/summary")
async def get_package_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener estadísticas de paquetes"""
    total_packages = db.query(Package).count()
    announced_packages = db.query(Package).filter(Package.status == PackageStatus.ANUNCIADO).count()
    received_packages = db.query(Package).filter(Package.status == PackageStatus.RECIBIDO).count()
    delivered_packages = db.query(Package).filter(Package.status == PackageStatus.ENTREGADO).count()
    cancelled_packages = db.query(Package).filter(Package.status == PackageStatus.CANCELADO).count()
    
    # Calcular ingresos
    total_revenue = db.query(Package).filter(
        Package.status == PackageStatus.ENTREGADO
    ).with_entities(Package.total_cost).all()
    total_revenue = sum([r[0] or 0 for r in total_revenue])
    
    return {
        "total_packages": total_packages,
        "announced_packages": announced_packages,
        "received_packages": received_packages,
        "delivered_packages": delivered_packages,
        "cancelled_packages": cancelled_packages,
        "total_revenue": total_revenue,
        "currency": "COP"
    }
