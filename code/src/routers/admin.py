# ========================================
# PAQUETES EL CLUB v3.0 - Router de Administración
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..dependencies import require_admin

router = APIRouter()

@router.get("/dashboard")
async def admin_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Dashboard de administración"""
    return {
        "message": "Dashboard de administración",
        "user": current_user.username,
        "role": current_user.role
    }
