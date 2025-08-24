# ========================================
# PAQUETES EL CLUB v3.0 - Router de Mensajes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..models.message import Message
from ..dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_messages(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar mensajes"""
    messages = db.query(Message).all()
    return [{"id": m.id, "subject": m.subject, "type": m.message_type} for m in messages]
