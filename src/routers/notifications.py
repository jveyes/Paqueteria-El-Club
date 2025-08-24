# ========================================
# PAQUETES EL CLUB v3.0 - Router de Notificaciones
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..models.notification import Notification
from ..dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar notificaciones"""
    notifications = db.query(Notification).all()
    return [{"id": n.id, "type": n.notification_type, "status": n.status} for n in notifications]
