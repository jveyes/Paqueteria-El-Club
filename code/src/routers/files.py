# ========================================
# PAQUETES EL CLUB v3.0 - Router de Archivos
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..models.file import File
from ..dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_files(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar archivos"""
    files = db.query(File).all()
    return [{"id": f.id, "filename": f.filename, "size": f.file_size} for f in files]
