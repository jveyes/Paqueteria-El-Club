# ========================================
# PAQUETES EL CLUB v3.0 - Servicio de Paquetes
# ========================================

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from ..models.package import Package, PackageStatus, PackageType
from ..models.customer import Customer
from ..schemas.package import PackageCreate, PackageUpdate, PackageAnnounce
from ..utils.exceptions import (
    PackageNotFoundException,
    InvalidPackageStatusException,
    DuplicateTrackingNumberException
)
from ..utils.helpers import generate_tracking_number
from ..utils.validators import validate_package_dimensions, validate_package_weight
from ..utils.datetime_utils import get_colombia_now
from .rate_service import RateService
from .notification_service import NotificationService

class PackageService:
    """Servicio para la lógica de negocio de paquetes"""
    
    def __init__(self, db: Session):
        self.db = db
        self.rate_service = RateService(db)
        self.notification_service = NotificationService(db)
    
    def create_package(self, package_data: PackageAnnounce) -> Package:
        """Crear nuevo paquete"""
        # Generar tracking number único
        tracking_number = generate_tracking_number()
        
        # Verificar que no exista
        existing = self.db.query(Package).filter(
            Package.tracking_number == tracking_number
        ).first()
        
        if existing:
            raise DuplicateTrackingNumberException(tracking_number)
        
        # Calcular tarifas
        costs = self.rate_service.calculate_package_costs(
            package_type=package_data.package_type,
            storage_days=1,
            delivery_required=True
        )
        
        # Crear paquete
        db_package = Package(
            tracking_number=tracking_number,
            customer_name=package_data.customer_name,
            customer_phone=package_data.customer_phone,
            package_type=package_data.package_type,
            package_condition=package_data.package_condition,
            observations=package_data.observations,
            storage_cost=costs["storage_cost"],
            delivery_cost=costs["delivery_cost"],
            total_cost=costs["total_cost"],
            status=PackageStatus.ANUNCIADO,
            announced_at=get_colombia_now()
        )
        
        self.db.add(db_package)
        self.db.commit()
        self.db.refresh(db_package)
        
        # Crear o actualizar cliente
        self._create_or_update_customer(package_data, tracking_number)
        
        # Enviar notificación
        self.notification_service.send_package_announcement(db_package)
        
        return db_package
    
    def get_package_by_tracking(self, tracking_number: str) -> Package:
        """Obtener paquete por número de tracking"""
        package = self.db.query(Package).filter(
            Package.tracking_number == tracking_number
        ).first()
        
        if not package:
            raise PackageNotFoundException(tracking_number)
        
        return package
    
    def list_packages(
        self,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[PackageStatus] = None,
        search: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[Package]:
        """Listar paquetes con filtros"""
        query = self.db.query(Package)
        
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
        
        if date_from:
            query = query.filter(Package.created_at >= date_from)
        
        if date_to:
            query = query.filter(Package.created_at <= date_to)
        
        # Aplicar paginación
        packages = query.offset(skip).limit(limit).all()
        
        return packages
    
    def receive_package(self, package_id: uuid.UUID) -> Package:
        """Recibir paquete en instalaciones"""
        package = self.db.query(Package).filter(Package.id == package_id).first()
        
        if not package:
            raise PackageNotFoundException(str(package_id))
        
        if package.status != PackageStatus.ANUNCIADO:
            raise InvalidPackageStatusException(
                package.status.value,
                PackageStatus.ANUNCIADO.value,
                "recibir"
            )
        
        # Actualizar estado
        package.status = PackageStatus.RECIBIDO
        package.received_at = get_colombia_now()
        self.db.commit()
        self.db.refresh(package)
        
        # Enviar notificación
        self.notification_service.send_package_received(package)
        
        return package
    
    def deliver_package(self, package_id: uuid.UUID) -> Package:
        """Entregar paquete al cliente"""
        package = self.db.query(Package).filter(Package.id == package_id).first()
        
        if not package:
            raise PackageNotFoundException(str(package_id))
        
        valid_statuses = [PackageStatus.RECIBIDO, PackageStatus.EN_TRANSITO]
        if package.status not in valid_statuses:
            raise InvalidPackageStatusException(
                package.status.value,
                "recibido o en tránsito",
                "entregar"
            )
        
        # Actualizar estado
        package.status = PackageStatus.ENTREGADO
        package.delivered_at = get_colombia_now()
        self.db.commit()
        self.db.refresh(package)
        
        # Enviar notificación
        self.notification_service.send_package_delivered(package)
        
        return package
    
    def cancel_package(self, package_id: uuid.UUID, reason: str) -> Package:
        """Cancelar paquete"""
        package = self.db.query(Package).filter(Package.id == package_id).first()
        
        if not package:
            raise PackageNotFoundException(str(package_id))
        
        if package.status == PackageStatus.ENTREGADO:
            raise InvalidPackageStatusException(
                package.status.value,
                "cualquier estado excepto entregado",
                "cancelar"
            )
        
        # Actualizar estado
        package.status = PackageStatus.CANCELADO
        package.observations = f"CANCELADO: {reason}"
        self.db.commit()
        self.db.refresh(package)
        
        # Enviar notificación
        self.notification_service.send_package_cancelled(package, reason)
        
        return package
    
    def get_package_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de paquetes"""
        total_packages = self.db.query(Package).count()
        
        # Paquetes por estado
        status_counts = self.db.query(
            Package.status,
            func.count(Package.id)
        ).group_by(Package.status).all()
        
        status_stats = {status.value: count for status, count in status_counts}
        
        # Ingresos totales
        total_revenue = self.db.query(
            func.sum(Package.total_cost)
        ).filter(Package.status == PackageStatus.ENTREGADO).scalar() or 0
        
        # Paquetes entregados hoy
        today = get_colombia_now().date()
        delivered_today = self.db.query(Package).filter(
            and_(
                Package.status == PackageStatus.ENTREGADO,
                func.date(Package.delivered_at) == today
            )
        ).count()
        
        return {
            "total_packages": total_packages,
            "status_distribution": status_stats,
            "total_revenue": float(total_revenue),
            "delivered_today": delivered_today,
            "currency": "COP"
        }
    
    def _create_or_update_customer(self, package_data: PackageAnnounce, tracking_number: str):
        """Crear o actualizar cliente"""
        customer = self.db.query(Customer).filter(
            Customer.tracking_number == tracking_number
        ).first()
        
        if not customer:
            customer = Customer(
                name=package_data.customer_name,
                phone=package_data.customer_phone,
                tracking_number=tracking_number
            )
            self.db.add(customer)
            self.db.commit()
