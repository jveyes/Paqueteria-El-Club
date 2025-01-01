# ========================================
# PAQUETES EL CLUB v3.1 - Servicio de Logs de Actividad
# ========================================

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from ..models.user_activity_log import UserActivityLog, ActivityType
from ..models.user import User
from ..utils.datetime_utils import get_colombia_now

class ActivityLogService:
    """Servicio para manejo de logs de actividad de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_activity(
        self,
        user_id: uuid.UUID,
        activity_type: ActivityType,
        description: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        activity_metadata: Optional[dict] = None
    ) -> UserActivityLog:
        """Registrar una nueva actividad del usuario"""
        activity_log = UserActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            activity_metadata=activity_metadata or {}
        )
        
        self.db.add(activity_log)
        self.db.commit()
        self.db.refresh(activity_log)
        
        return activity_log
    
    def get_user_activity_logs(
        self,
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0,
        activity_type: Optional[ActivityType] = None
    ) -> List[UserActivityLog]:
        """Obtener logs de actividad de un usuario"""
        query = self.db.query(UserActivityLog).filter(
            UserActivityLog.user_id == user_id
        )
        
        if activity_type:
            query = query.filter(UserActivityLog.activity_type == activity_type)
        
        return query.order_by(desc(UserActivityLog.created_at)).offset(offset).limit(limit).all()
    
    def get_recent_activity_logs(self, days: int = 7) -> List[UserActivityLog]:
        """Obtener logs de actividad recientes de todos los usuarios"""
        cutoff_date = get_colombia_now() - timedelta(days=days)
        
        return self.db.query(UserActivityLog).filter(
            UserActivityLog.created_at >= cutoff_date
        ).order_by(desc(UserActivityLog.created_at)).all()
    
    def get_activity_stats(self, user_id: uuid.UUID, days: int = 30) -> dict:
        """Obtener estadísticas de actividad de un usuario"""
        cutoff_date = get_colombia_now() - timedelta(days=days)
        
        # Total de actividades
        total_activities = self.db.query(UserActivityLog).filter(
            UserActivityLog.user_id == user_id,
            UserActivityLog.created_at >= cutoff_date
        ).count()
        
        # Actividades por tipo
        activities_by_type = {}
        for activity_type in ActivityType:
            count = self.db.query(UserActivityLog).filter(
                UserActivityLog.user_id == user_id,
                UserActivityLog.activity_type == activity_type,
                UserActivityLog.created_at >= cutoff_date
            ).count()
            if count > 0:
                activities_by_type[activity_type.value] = count
        
        return {
            "total_activities": total_activities,
            "activities_by_type": activities_by_type,
            "period_days": days
        }
