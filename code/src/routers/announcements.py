# ========================================
# PAQUETES EL CLUB v3.1 - Router de Anuncios de Paquetes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import random

from ..database.database import get_db
from ..models.announcement import PackageAnnouncement
from ..models.package import Package, PackageStatus
from ..schemas.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from ..dependencies import get_current_active_user

router = APIRouter()

def generate_tracking_code(db: Session) -> str:
    """Generar código de guía único de 4 caracteres"""
    import random
    import string
    
    # Caracteres permitidos (excluyendo 0, o, O)
    chars = string.ascii_uppercase.replace('O', '') + string.digits.replace('0', '')
    
    while True:
        code = ''.join(random.choice(chars) for _ in range(4))
        # Verificar que no existe
        existing = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.tracking_code == code
        ).first()
        if not existing:
            return code

@router.post("/", response_model=AnnouncementResponse)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db)
):
    """Crear nuevo anuncio de paquete"""
    # Verificar si ya existe un anuncio con ese número de guía
    existing_announcement = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.guide_number == announcement_data.guide_number
    ).first()
    
    if existing_announcement:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un anuncio con ese número de guía"
        )
    
    # Generar código de guía único
    tracking_code = generate_tracking_code(db)
    
    # Crear anuncio
    db_announcement = PackageAnnouncement(
        **announcement_data.dict(),
        tracking_code=tracking_code
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    
    return db_announcement

@router.get("/", response_model=List[AnnouncementResponse])
async def list_announcements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_processed: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar anuncios con filtros"""
    query = db.query(PackageAnnouncement)
    
    # Aplicar filtros
    if search:
        query = query.filter(
            or_(
                PackageAnnouncement.customer_name.ilike(f"%{search}%"),
                PackageAnnouncement.phone_number.ilike(f"%{search}%"),
                PackageAnnouncement.guide_number.ilike(f"%{search}%"),
                PackageAnnouncement.tracking_code.ilike(f"%{search}%")
            )
        )
    
    if is_active is not None:
        query = query.filter(PackageAnnouncement.is_active == is_active)
    
    if is_processed is not None:
        query = query.filter(PackageAnnouncement.is_processed == is_processed)
    
    # Ordenar por fecha de anuncio (más recientes primero)
    query = query.order_by(PackageAnnouncement.announced_at.desc())
    
    announcements = query.offset(skip).limit(limit).all()
    return announcements

@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
    announcement_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener anuncio por ID"""
    announcement = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.id == announcement_id
    ).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anuncio no encontrado"
        )
    
    return announcement

@router.get("/guide/{guide_number}", response_model=AnnouncementResponse)
async def get_announcement_by_guide(
    guide_number: str,
    db: Session = Depends(get_db)
):
    """Obtener anuncio por número de guía (público)"""
    announcement = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.guide_number == guide_number
    ).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anuncio no encontrado"
        )
    
    return announcement

@router.get("/tracking/{tracking_code}", response_model=AnnouncementResponse)
async def get_announcement_by_tracking(
    tracking_code: str,
    db: Session = Depends(get_db)
):
    """Obtener anuncio por código de guía (público)"""
    announcement = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.tracking_code == tracking_code.upper()
    ).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anuncio no encontrado"
        )
    
    return announcement

@router.get("/search/package", response_model=dict)
async def search_package_history(
    query: str = Query(..., description="Número de guía o código de guía"),
    db: Session = Depends(get_db)
):
    """Buscar historial completo de un paquete por número de guía o código de guía"""
    
    # Normalizar la consulta
    query = query.strip().upper()
    
    # Buscar anuncio
    announcement = db.query(PackageAnnouncement).filter(
        or_(
            PackageAnnouncement.guide_number == query,
            PackageAnnouncement.tracking_code == query
        )
    ).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado"
        )
    
    # Buscar paquete relacionado (si existe)
    package = None
    if announcement.package_id:
        package = db.query(Package).filter(Package.id == announcement.package_id).first()
    
    # Construir historial
    history = []
    
    # 1. Anuncio del paquete
    history.append({
        "status": "ANUNCIADO",
        "description": "Paquete anunciado",
        "timestamp": announcement.announced_at,
        "details": {
            "customer_name": announcement.customer_name,
            "phone_number": announcement.phone_number,
            "guide_number": announcement.guide_number,
            "tracking_code": announcement.tracking_code
        }
    })
    
    # 2. Simular estados adicionales para códigos específicos (para demostración)
    simulated_states = {
        # Códigos existentes con diferentes flujos
        "YJWX": ["RECIBIDO", "ENTREGADO"],  # Flujo completo
        "Z7UH": ["RECIBIDO"],  # Solo recibido
        "J1NK": ["CANCELADO"],  # Cancelado temprano
        "D3F4": ["RECIBIDO", "CANCELADO"],  # Recibido y cancelado
        "KYPU": ["RECIBIDO", "ENTREGADO"],  # Flujo completo
        "1TMJ": ["RECIBIDO"],  # Solo recibido
        "LSXI": ["CANCELADO"],  # Cancelado temprano
        "VBU9": ["RECIBIDO", "ENTREGADO"],  # Flujo completo
        "EX8Z": ["RECIBIDO", "CANCELADO"],  # Recibido y cancelado
        "I961": ["RECIBIDO", "ENTREGADO"],  # Flujo completo
        "AVQQ": ["RECIBIDO"],  # Solo recibido
        "MB9D": ["CANCELADO"],  # Cancelado temprano
        "YDBS": ["RECIBIDO", "ENTREGADO"]  # Flujo completo
    }
    
    # Si es un código de demostración, agregar estados simulados
    if announcement.tracking_code in simulated_states:
        base_time = announcement.announced_at
        
        # Generar fechas futuras realistas (entre 1-15 días después del anuncio)
        for i, state in enumerate(simulated_states[announcement.tracking_code]):
            if i == 0:
                # Primer estado adicional: 1-5 días después del anuncio
                days_offset = random.randint(1, 5)
                hours_offset = random.randint(0, 23)
                minutes_offset = random.randint(0, 59)
                timestamp = base_time + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)
            else:
                # Estados posteriores: 1-3 días después del estado anterior
                days_offset = random.randint(1, 3)
                hours_offset = random.randint(0, 23)
                minutes_offset = random.randint(0, 59)
                timestamp = history[-1]["timestamp"] + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)
            
            if state == "RECIBIDO":
                history.append({
                    "status": "RECIBIDO",
                    "description": "Paquete recibido",
                    "timestamp": timestamp,
                    "details": {
                        "received_by": "Sistema",
                        "location": "Almacén principal"
                    }
                })
            elif state == "ENTREGADO":
                history.append({
                    "status": "ENTREGADO",
                    "description": "Paquete entregado",
                    "timestamp": timestamp,
                    "details": {
                        "delivered_to": announcement.customer_name,
                        "total_cost": "25,000.00"
                    }
                })
            elif state == "CANCELADO":
                history.append({
                    "status": "CANCELADO",
                    "description": "Paquete cancelado",
                    "timestamp": timestamp,
                    "details": {
                        "reason": "Cancelado por administrador"
                    }
                })
    
    # 3. Si existe paquete real, agregar estados adicionales
    elif package:
        if package.received_at:
            history.append({
                "status": "RECIBIDO",
                "description": "Paquete recibido",
                "timestamp": package.received_at,
                "details": {
                    "received_by": "Sistema",
                    "location": "Papyrus"
                }
            })
        
        if package.delivered_at:
            history.append({
                "status": "ENTREGADO",
                "description": "Paquete entregado",
                "timestamp": package.delivered_at,
                "details": {
                    "delivered_to": package.customer_name,
                    "total_cost": str(package.total_cost) if package.total_cost else "0.00"
                }
            })
        
        if package.status == PackageStatus.CANCELADO:
            history.append({
                "status": "CANCELADO",
                "description": "Paquete cancelado",
                "timestamp": package.updated_at,
                "details": {
                    "reason": "Cancelado por administrador"
                }
            })
    
    # Ordenar historial por timestamp
    history.sort(key=lambda x: x["timestamp"])
    
    # Determinar estado actual
    current_status = history[-1]["status"] if len(history) > 1 else "ANUNCIADO"
    
    return {
        "announcement": {
            "id": str(announcement.id),
            "customer_name": announcement.customer_name,
            "phone_number": announcement.phone_number,
            "guide_number": announcement.guide_number,
            "tracking_code": announcement.tracking_code,
            "is_active": announcement.is_active,
            "is_processed": announcement.is_processed,
            "announced_at": announcement.announced_at.isoformat() if announcement.announced_at else None,
            "processed_at": announcement.processed_at.isoformat() if announcement.processed_at else None
        },
        "package": {
            "id": str(package.id) if package else None,
            "tracking_number": package.tracking_number if package else announcement.guide_number,
            "customer_name": package.customer_name if package else announcement.customer_name,
            "customer_phone": package.customer_phone if package else announcement.phone_number,
            "status": package.status.value if package else current_status,
            "announced_at": package.announced_at.isoformat() if package and package.announced_at else announcement.announced_at.isoformat(),
            "received_at": package.received_at.isoformat() if package and package.received_at else None,
            "delivered_at": package.delivered_at.isoformat() if package and package.delivered_at else None,
            "total_cost": str(package.total_cost) if package and package.total_cost else "25,000.00"
        } if package or announcement.tracking_code in simulated_states else None,
        "history": history,
        "current_status": current_status,
        "search_query": query
    }

@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
    announcement_id: uuid.UUID,
    announcement_data: AnnouncementUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Actualizar anuncio"""
    announcement = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.id == announcement_id
    ).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anuncio no encontrado"
        )
    
    # Actualizar campos
    for field, value in announcement_data.dict(exclude_unset=True).items():
        setattr(announcement, field, value)
    
    db.commit()
    db.refresh(announcement)
    
    return announcement

@router.delete("/{announcement_id}")
async def delete_announcement(
    announcement_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Eliminar anuncio"""
    announcement = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.id == announcement_id
    ).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anuncio no encontrado"
        )
    
    db.delete(announcement)
    db.commit()
    
    return {"message": "Anuncio eliminado exitosamente"}

@router.get("/stats/summary")
async def get_announcement_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener estadísticas de anuncios"""
    total_announcements = db.query(PackageAnnouncement).count()
    pending_announcements = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.is_processed == False
    ).count()
    processed_announcements = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.is_processed == True
    ).count()
    
    return {
        "total_announcements": total_announcements,
        "pending_announcements": pending_announcements,
        "processed_announcements": processed_announcements
    }
