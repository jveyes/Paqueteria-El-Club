# ========================================
# PAQUETES EL CLUB v3.0 - Servicio de Tarifas
# ========================================

from sqlalchemy.orm import Session
from typing import Dict, Any
from decimal import Decimal

from ..models.rate import Rate, RateType
from ..models.package import PackageType
from ..utils.exceptions import RateCalculationException
from ..utils.validators import validate_rate_calculation_params
from ..config import settings

class RateService:
    """Servicio para la lógica de negocio de tarifas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_package_costs(
        self,
        package_type: PackageType,
        storage_days: int = 1,
        delivery_required: bool = True
    ) -> Dict[str, float]:
        """Calcular costos de un paquete"""
        # Validar parámetros
        validate_rate_calculation_params(
            package_type.value,
            storage_days,
            delivery_required
        )
        
        # Obtener tarifas activas
        storage_rate = self._get_active_rate(RateType.STORAGE)
        delivery_rate = self._get_active_rate(RateType.DELIVERY)
        package_type_rate = self._get_active_rate(RateType.PACKAGE_TYPE)
        
        # Calcular costos base
        base_storage = float(storage_rate.base_price) if storage_rate else settings.base_storage_rate
        base_delivery = float(delivery_rate.base_price) if delivery_rate else settings.base_delivery_rate
        
        # Aplicar multiplicadores por tipo de paquete
        if package_type == PackageType.EXTRA_DIMENSIONADO:
            multiplier = float(package_type_rate.package_type_multiplier) if package_type_rate else 1.5
            base_storage *= multiplier
            base_delivery *= multiplier
        
        # Calcular costos finales
        storage_cost = base_storage * storage_days
        delivery_cost = base_delivery if delivery_required else 0
        total_cost = storage_cost + delivery_cost
        
        return {
            "storage_cost": storage_cost,
            "delivery_cost": delivery_cost,
            "total_cost": total_cost,
            "currency": settings.currency
        }
    
    def get_active_rates(self) -> Dict[str, Rate]:
        """Obtener todas las tarifas activas"""
        rates = self.db.query(Rate).filter(Rate.is_active == True).all()
        return {rate.rate_type.value: rate for rate in rates}
    
    def create_rate(self, rate_data: Dict[str, Any]) -> Rate:
        """Crear nueva tarifa"""
        # Desactivar tarifas anteriores del mismo tipo
        existing_rates = self.db.query(Rate).filter(
            Rate.rate_type == rate_data["rate_type"],
            Rate.is_active == True
        ).all()
        
        for rate in existing_rates:
            rate.is_active = False
        
        # Crear nueva tarifa
        new_rate = Rate(**rate_data)
        self.db.add(new_rate)
        self.db.commit()
        self.db.refresh(new_rate)
        
        return new_rate
    
    def update_rate(self, rate_id: str, rate_data: Dict[str, Any]) -> Rate:
        """Actualizar tarifa existente"""
        rate = self.db.query(Rate).filter(Rate.id == rate_id).first()
        
        if not rate:
            raise RateCalculationException(f"Tarifa con ID {rate_id} no encontrada")
        
        # Actualizar campos
        for field, value in rate_data.items():
            if hasattr(rate, field):
                setattr(rate, field, value)
        
        self.db.commit()
        self.db.refresh(rate)
        
        return rate
    
    def get_rate_history(self, rate_type: RateType = None) -> list:
        """Obtener historial de cambios de tarifas"""
        query = self.db.query(Rate)
        
        if rate_type:
            query = query.filter(Rate.rate_type == rate_type)
        
        return query.order_by(Rate.created_at.desc()).all()
    
    def _get_active_rate(self, rate_type: RateType) -> Rate:
        """Obtener tarifa activa por tipo"""
        return self.db.query(Rate).filter(
            Rate.rate_type == rate_type,
            Rate.is_active == True
        ).first()
    
    def get_rate_summary(self) -> Dict[str, Any]:
        """Obtener resumen de tarifas actuales"""
        active_rates = self.get_active_rates()
        
        summary = {
            "active_rates": len(active_rates),
            "rates_by_type": {}
        }
        
        for rate_type, rate in active_rates.items():
            summary["rates_by_type"][rate_type] = {
                "base_price": float(rate.base_price),
                "daily_storage_rate": float(rate.daily_storage_rate) if rate.daily_storage_rate else 0,
                "delivery_rate": float(rate.delivery_rate) if rate.delivery_rate else 0,
                "package_type_multiplier": float(rate.package_type_multiplier) if rate.package_type_multiplier else 1.0,
                "valid_from": rate.valid_from.isoformat() if rate.valid_from else None
            }
        
        return summary
