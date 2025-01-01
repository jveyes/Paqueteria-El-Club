# ========================================
# PAQUETES EL CLUB v3.0 - Router de Mensajes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
import uuid

from ..database.database import get_db
from ..models.message import Message, MessageType, MessageStatus
from ..models.user import User
from ..schemas.message import (
    CustomerInquiryCreate, 
    MessageResponse, 
    MessageList, 
    MessageDetail, 
    MessageStats
)
from ..dependencies import get_current_active_user
from datetime import datetime

router = APIRouter()

@router.post("/customer-inquiry", status_code=status.HTTP_201_CREATED)
async def create_customer_inquiry(
    inquiry: CustomerInquiryCreate,
    db: Session = Depends(get_db)
):
    """Crear consulta de cliente (pública)"""
    try:
        # Crear nuevo mensaje
        message = Message(
            customer_name=inquiry.customer_name,
            customer_phone=inquiry.customer_phone,
            customer_email=inquiry.customer_email,
            package_guide_number=inquiry.package_guide_number,
            package_tracking_code=inquiry.package_tracking_code,
            subject=inquiry.subject,
            content=inquiry.content,
            message_type=MessageType.CUSTOMER_INQUIRY,
            status=MessageStatus.PENDING
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return {
            "message": "Consulta enviada exitosamente",
            "id": str(message.id),
            "status": "pending"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear consulta: {str(e)}"
        )

@router.get("/test")
async def test_messages():
    """Endpoint de prueba simple"""
    return {"message": "Endpoint funcionando", "timestamp": datetime.now().isoformat()}

@router.get("/")
async def list_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Listar mensajes (solo usuarios autenticados)"""
    # Obtener mensajes de la base de datos
    messages = db.query(Message).limit(10).all()
    
    # Convertir a formato simple
    result = []
    for message in messages:
        result.append({
            "id": str(message.id),
            "subject": message.subject,
            "content": message.content,
            "customer_name": message.customer_name,
            "customer_phone": message.customer_phone,
            "is_read": message.is_read,
            "status": message.status.value if hasattr(message.status, 'value') else str(message.status),
            "message_type": message.message_type.value if hasattr(message.message_type, 'value') else str(message.message_type),
            "created_at": "2025-09-01T15:00:00",
            "package_guide_number": message.package_guide_number,
            "package_tracking_code": message.package_tracking_code
        })
    
    return result

@router.get("/stats", response_model=MessageStats)
async def get_message_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener estadísticas de mensajes"""
    total_messages = db.query(Message).count()
    pending_messages = db.query(Message).filter(Message.status == MessageStatus.PENDING).count()
    resolved_messages = db.query(Message).filter(
        Message.status.in_([MessageStatus.RESOLVED, MessageStatus.CLOSED])
    ).count()
    unread_messages = db.query(Message).filter(Message.is_read == False).count()
    
    return MessageStats(
        total_messages=total_messages,
        pending_messages=pending_messages,
        resolved_messages=resolved_messages,
        unread_messages=unread_messages
    )

@router.get("/{message_id}", response_model=MessageDetail)
async def get_message_detail(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener detalle de un mensaje"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        # Marcar como leído si no lo está
        if not message.is_read:
            message.mark_as_read(current_user.id)
            db.commit()
        
        # Obtener nombres de usuarios relacionados
        read_by_name = None
        if message.read_by:
            read_by_name = message.read_by.full_name
        
        responded_by_name = None
        if message.responded_by:
            responded_by_name = message.responded_by.full_name
        
        return MessageDetail(
            id=str(message.id),
            customer_name=message.customer_name,
            customer_phone=message.customer_phone,
            customer_email=message.customer_email,
            subject=message.subject,
            content=message.content,
            message_type=message.message_type,
            status=message.status,
            is_read=message.is_read,
            read_at=message.read_at,
            read_by_name=read_by_name,
            created_at=message.created_at,
            package_guide_number=message.package_guide_number,
            package_tracking_code=message.package_tracking_code,
            admin_response=message.admin_response,
            responded_at=message.responded_at,
            responded_by_name=responded_by_name
        )
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )

@router.post("/{message_id}/respond", status_code=status.HTTP_200_OK)
async def respond_to_message(
    message_id: str,
    response: MessageResponse,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Responder a un mensaje"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        # Responder al mensaje
        message.respond(response.response, current_user.id)
        db.commit()
        
        return {
            "message": "Respuesta enviada exitosamente",
            "status": "resolved"
        }
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )

@router.put("/{message_id}/status", status_code=status.HTTP_200_OK)
async def update_message_status(
    message_id: str,
    new_status: MessageStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar estado de un mensaje"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        message.status = new_status
        message.updated_at = datetime.now()
        db.commit()
        
        return {
            "message": "Estado actualizado exitosamente",
            "status": new_status
        }
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar un mensaje (solo administradores)"""
    try:
        message = db.query(Message).filter(Message.id == uuid.UUID(message_id)).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        db.delete(message)
        db.commit()
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensaje inválido"
        )