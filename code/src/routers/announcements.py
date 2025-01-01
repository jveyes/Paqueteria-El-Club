# ========================================
# PAQUETES EL CLUB v3.1 - Router de Anuncios de Paquetes
# ========================================

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import random
import logging

from ..database.database import get_db
from ..models.announcement import PackageAnnouncement
from ..models.package import Package, PackageStatus
from ..schemas.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from ..dependencies import get_current_active_user
from ..utils.rate_limiter import check_rate_limit, get_rate_limit_info, reset_rate_limit
from ..utils.datetime_utils import get_colombia_datetime, format_colombia_datetime, get_colombia_now

logger = logging.getLogger(__name__)

router = APIRouter()

def generate_tracking_code(db: Session) -> str:
    """Generar código de guía único de 4 caracteres - CORREGIDO"""
    import random
    import string
    
    # Caracteres permitidos (excluyendo 0, o, O para evitar confusión)
    chars = string.ascii_uppercase.replace('O', '') + string.digits.replace('0', '')
    
    # Generar código de 4 caracteres
    while True:
        code = ''.join(random.choice(chars) for _ in range(4))
        
        # Verificar que no exista
        existing = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.tracking_code == code
        ).first()
        
        if not existing:
            return code

@router.post("/", response_model=AnnouncementResponse)
async def create_announcement(
    request: Request,
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db)
):
    """Crear nuevo anuncio de paquete con SMS automático"""
    # Verificar rate limit (máximo 5 anuncios por minuto por IP)
    check_rate_limit(request, max_requests=5, window=60, endpoint="announcements")
    
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
    
    # Crear anuncio con fecha explícita en Colombia
    db_announcement = PackageAnnouncement(
        **announcement_data.dict(),
        tracking_code=tracking_code,
        announced_at=get_colombia_now(),
        created_at=get_colombia_now(),
        updated_at=get_colombia_now()
    )
    
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    
    # SMS DESHABILITADO TEMPORALMENTE - Solo se envía desde el frontend
    # Esto evita el retraso en la creación del anuncio
    logger.info(f"Anuncio creado exitosamente para {announcement_data.customer_name}")
    logger.info(f"SMS se enviará desde el frontend para evitar retrasos")
    
    return db_announcement

@router.get("/test-timing")
async def test_timing(db: Session = Depends(get_db)):
    """Endpoint de prueba para medir timing"""
    import time
    start_time = time.time()
    
    # Simular operaciones básicas
    time.sleep(0.1)  # 100ms de delay artificial
    
    # Consulta simple a la BD
    db_start = time.time()
    count = db.query(PackageAnnouncement).count()
    db_time = time.time() - db_start
    
    # Función de tracking
    tracking_start = time.time()
    tracking_code = generate_tracking_code(db)
    tracking_time = time.time() - tracking_start
    
    end_time = time.time()
    total_time = end_time - start_time
    
    return {
        "message": "Test completado",
        "total_time": total_time,
        "db_query_time": db_time,
        "tracking_code_time": tracking_time,
        "db_count": count,
        "tracking_code": tracking_code,
        "timestamp": get_colombia_now().isoformat()
    }

@router.get("/test-simple")
async def test_simple():
    """Endpoint simple sin base de datos"""
    import time
    start_time = time.time()
    
    # Simular operaciones básicas
    time.sleep(0.1)  # 100ms de delay artificial
    
    end_time = time.time()
    total_time = end_time - start_time
    
    return {
        "message": "Test simple completado",
        "total_time": total_time,
        "timestamp": get_colombia_now().isoformat()
    }

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

@router.post("/send-sms-browser", response_model=Dict[str, Any])
async def send_sms_from_browser(
    request: Request,
    db: Session = Depends(get_db)
):
    """ENDPOINT ESPECIAL PARA ENVIAR SMS DESDE EL NAVEGADOR"""
    
    # Verificar que venga del navegador (no de API)
    user_agent = request.headers.get("user-agent", "")
    referer = request.headers.get("referer", "")
    
    # Solicitud de SMS desde navegador
    
    # Solo permitir desde navegador
    if not user_agent or "Mozilla" not in user_agent:
        logger.warning(f"Intento de SMS desde API - BLOQUEADO")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="SMS solo disponible desde navegador"
        )
    
    try:
        # Obtener datos del body
        body = await request.json()
        customer_name = body.get("customer_name")
        phone_number = body.get("phone_number")
        guide_number = body.get("guide_number")
        tracking_code = body.get("tracking_code")
        
        # Validar datos de entrada
        
        # Validar que todos los campos estén presentes
        if not customer_name or not phone_number or not guide_number or not tracking_code:
            missing_fields = []
            if not customer_name: missing_fields.append("customer_name")
            if not phone_number: missing_fields.append("phone_number")
            if not guide_number: missing_fields.append("guide_number")
            if not tracking_code: missing_fields.append("tracking_code")
            
            logger.error(f"Campos faltantes: {missing_fields}")
            return {
                "success": False,
                "error": f"Campos requeridos faltantes: {', '.join(missing_fields)}",
                "error_code": "MISSING_FIELDS",
                "missing_fields": missing_fields
            }
        
        # Validar formato del teléfono
        if not phone_number.isdigit() or len(phone_number) < 10:
            logger.error(f"Formato de teléfono inválido: {phone_number}")
            return {
                "success": False,
                "error": "Formato de teléfono inválido. Debe contener solo números y al menos 10 dígitos",
                "error_code": "INVALID_PHONE_FORMAT",
                "phone_number": phone_number
            }
        
        # Validar longitud del nombre
        if len(customer_name) < 2 or len(customer_name) > 100:
            logger.error(f"Longitud del nombre inválida: {len(customer_name)}")
            return {
                "success": False,
                "error": "El nombre debe tener entre 2 y 100 caracteres",
                "error_code": "INVALID_NAME_LENGTH",
                "name_length": len(customer_name)
            }
        
        # Importar y usar servicio de SMS
        try:
            from ..services.sms_service import SMSService
            sms_service = SMSService()
        except ImportError as import_error:
            logger.error(f"❌ Error importando servicio SMS: {import_error}")
            return {
                "success": False,
                "error": "Error interno: No se pudo cargar el servicio de SMS",
                "error_code": "SMS_SERVICE_IMPORT_ERROR",
                "error_type": "ImportError"
            }
        except Exception as service_error:
            logger.error(f"❌ Error creando servicio SMS: {service_error}")
            return {
                "success": False,
                "error": "Error interno: No se pudo inicializar el servicio de SMS",
                "error_code": "SMS_SERVICE_INIT_ERROR",
                "error_type": type(service_error).__name__
            }
        
        # Enviar SMS
        logger.info(f"📱 Llamando al servicio de SMS...")
        try:
            sms_result = await sms_service.send_tracking_sms(
                phone=phone_number,
                customer_name=customer_name,
                tracking_code=tracking_code,
                guide_number=guide_number
            )
            logger.info(f"📱 Llamada al servicio SMS completada")
        except Exception as sms_call_error:
            logger.error(f"❌ Error en llamada al servicio SMS: {sms_call_error}")
            logger.error(f"❌ Tipo de error: {type(sms_call_error).__name__}")
            
            # Categorizar errores de llamada
            if "timeout" in str(sms_call_error).lower():
                error_msg = "Timeout: El servicio de SMS tardó demasiado en responder"
                error_code = "SMS_CALL_TIMEOUT"
            elif "connection" in str(sms_call_error).lower():
                error_msg = "Error de conexión: No se pudo conectar al servicio de SMS"
                error_code = "SMS_CONNECTION_ERROR"
            else:
                error_msg = f"Error en llamada al servicio SMS: {str(sms_call_error)}"
                error_code = "SMS_CALL_ERROR"
            
            return {
                "success": False,
                "error": error_msg,
                "error_code": error_code,
                "error_type": type(sms_call_error).__name__
            }
        
        logger.info(f"📱 Resultado del servicio SMS: {sms_result}")
        
        # Verificar que sms_result no sea None
        if sms_result is None:
            logger.error(f"❌ El servicio de SMS retornó None")
            return {
                "success": False,
                "error": "El servicio de SMS no retornó respuesta"
            }
        
        # Verificar que sms_result sea un diccionario
        if not isinstance(sms_result, dict):
            logger.error(f"❌ El servicio de SMS retornó tipo incorrecto: {type(sms_result)}")
            return {
                "success": False,
                "error": f"Tipo de respuesta incorrecto: {type(sms_result)}"
            }
        
        if sms_result.get("success"):
            logger.info(f"✅ SMS enviado exitosamente desde navegador a {phone_number}")
            return {
                "success": True,
                "message": "SMS enviado exitosamente",
                "phone": phone_number,
                "tracking_code": tracking_code,
                "guide_number": guide_number,
                "customer_name": customer_name
            }
        else:
            error_msg = sms_result.get("error", "Error desconocido del servicio SMS")
            logger.error(f"❌ Error enviando SMS desde navegador: {error_msg}")
            
            # Categorizar errores del servicio SMS
            error_code = "SMS_SERVICE_ERROR"
            if "quota" in error_msg.lower():
                error_code = "SMS_QUOTA_EXCEEDED"
            elif "authentication" in error_msg.lower():
                error_code = "SMS_AUTH_ERROR"
            elif "phone" in error_msg.lower() or "invalid" in error_msg.lower():
                error_code = "SMS_INVALID_PHONE"
            elif "timeout" in error_msg.lower():
                error_code = "SMS_TIMEOUT"
            
            return {
                "success": False,
                "error": error_msg,
                "error_code": error_code,
                "phone_number": phone_number,
                "tracking_code": tracking_code
            }
            
    except Exception as e:
        logger.error(f"❌ Excepción enviando SMS desde navegador: {e}")
        logger.error(f"❌ Tipo de excepción: {type(e).__name__}")
        logger.error(f"❌ Detalles completos: {str(e)}")
        
        # Retornar error detallado
        error_message = f"Error interno del servidor: {str(e)}"
        
        # Categorizar errores comunes
        if "timeout" in str(e).lower():
            error_message = "Error de timeout: El servicio de SMS tardó demasiado en responder"
        elif "connection" in str(e).lower():
            error_message = "Error de conexión: No se pudo conectar al servicio de SMS"
        elif "authentication" in str(e).lower():
            error_message = "Error de autenticación: Problema con las credenciales del servicio SMS"
        elif "quota" in str(e).lower():
            error_message = "Error de cuota: Se ha agotado la cuota de SMS disponible"
        elif "invalid" in str(e).lower() or "phone" in str(e).lower():
            error_message = "Error de validación: Número de teléfono inválido o no soportado"
        
        return {
            "success": False,
            "error": error_message,
            "error_code": "INTERNAL_ERROR",
            "error_type": type(e).__name__
        }

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

@router.get("/tracking/{tracking_code}")
async def get_tracking_info(
    tracking_code: str,
    db: Session = Depends(get_db)
):
    """Obtener información de tracking de un paquete"""
    # Buscar anuncio por código de tracking
    announcement = db.query(PackageAnnouncement).filter(
        PackageAnnouncement.tracking_code == tracking_code.upper()
    ).first()
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de guía no encontrado"
        )
    
    # Buscar paquete relacionado
    package = db.query(Package).filter(
        Package.tracking_number == announcement.guide_number
    ).first()
    
    # Construir historial
    history = []
    
    # 1. Estado inicial: ANUNCIADO
    history.append({
        "status": "ANUNCIADO",
        "description": "Paquete anunciado",
        "timestamp": announcement.announced_at,
        "timestamp_colombia": format_colombia_datetime(announcement.announced_at, "%Y-%m-%d %H:%M:%S") if announcement.announced_at else None,
        "timestamp_formatted": format_colombia_datetime(announcement.announced_at, "%A, %d de %B de %Y, %I:%M %p") if announcement.announced_at else None,
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
        "YDBS": ["RECIBIDO", "ENTREGADO"],  # Flujo completo
        
        # Nuevos códigos de muestra con diferentes flujos (creados el 28/08/2025)
        # Flujos completos
        "2Z2B": ["RECIBIDO", "ENTREGADO"],  # Flujo Completo Rápido
        "C77H": ["RECIBIDO", "ENTREGADO"],  # Flujo Completo Normal
        "XS6B": ["RECIBIDO", "ENTREGADO"],  # Flujo Completo Lento
        
        # Flujos parciales
        "LCDR": ["RECIBIDO"],  # Solo Recibido Rápido
        "GV98": ["RECIBIDO"],  # Solo Recibido Normal
        
        # Cancelaciones
        "CIBY": ["CANCELADO"],  # Cancelación Temprana
        "QDIA": ["RECIBIDO", "CANCELADO"],  # Cancelación Tardía
        
        # Estados especiales
        "6DR2": ["RECIBIDO"],  # En Proceso
        "7K3N": ["RECIBIDO"],  # Pendiente de Entrega
        "TE19": ["RECIBIDO"],  # Retrasado
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
                    "timestamp_colombia": format_colombia_datetime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    "timestamp_formatted": format_colombia_datetime(timestamp, "%A, %d de %B de %Y, %I:%M %p"),
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
                    "timestamp_colombia": format_colombia_datetime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    "timestamp_formatted": format_colombia_datetime(timestamp, "%A, %d de %B de %Y, %I:%M %p"),
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
                    "timestamp_colombia": format_colombia_datetime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    "timestamp_formatted": format_colombia_datetime(timestamp, "%A, %d de %B de %Y, %I:%M %p"),
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
                "timestamp_colombia": format_colombia_datetime(package.received_at, "%Y-%m-%d %H:%M:%S"),
                "timestamp_formatted": format_colombia_datetime(package.received_at, "%A, %d de %B de %Y, %I:%M %p"),
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
                "timestamp_colombia": format_colombia_datetime(package.delivered_at, "%Y-%m-%d %H:%M:%S"),
                "timestamp_formatted": format_colombia_datetime(package.delivered_at, "%A, %d de %B de %Y, %I:%M %p"),
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
                "timestamp_colombia": format_colombia_datetime(package.updated_at, "%Y-%m-%d %H:%M:%S"),
                "timestamp_formatted": format_colombia_datetime(package.updated_at, "%A, %d de %B de %Y, %I:%M %p"),
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
            "announced_at": format_colombia_datetime(announcement.announced_at, "%Y-%m-%d %H:%M:%S") if announcement.announced_at else None,
            "announced_at_formatted": format_colombia_datetime(announcement.announced_at, "%A, %d de %B de %Y, %I:%M %p") if announcement.announced_at else None,
            "processed_at": format_colombia_datetime(announcement.processed_at, "%Y-%m-%d %H:%M:%S") if announcement.processed_at else None
        },
        "package": {
            "id": str(package.id) if package else None,
            "tracking_number": package.tracking_number if package else announcement.guide_number,
            "customer_name": package.customer_name if package else announcement.customer_name,
            "customer_phone": package.customer_phone if package else announcement.phone_number,
            "status": package.status.value if package else current_status,
            "announced_at": format_colombia_datetime(package.announced_at, "%Y-%m-%d %H:%M:%S") if package and package.announced_at else format_colombia_datetime(announcement.announced_at, "%Y-%m-%d %H:%M:%S"),
            "received_at": format_colombia_datetime(package.received_at, "%Y-%m-%d %H:%M:%S") if package and package.received_at else None,
            "delivered_at": format_colombia_datetime(package.delivered_at, "%Y-%m-%d %H:%M:%S") if package and package.delivered_at else None,
            "total_cost": str(package.total_cost) if package and package.total_cost else "25,000.00"
        } if package or announcement.tracking_code in simulated_states else None,
        "history": history,
        "current_status": current_status,
        "search_query": tracking_code
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

@router.get("/search/package")
async def search_package_by_guide_number(
    query: str = Query(..., description="Número de guía o código de tracking"),
    db: Session = Depends(get_db)
):
    """Buscar paquete por número de guía o código de tracking"""
    # Normalizar la consulta
    query = query.strip().upper()
    
    # Buscar anuncio por número de guía o código de tracking
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
    
    # 1. Estado inicial: ANUNCIADO
    history.append({
        "status": "ANUNCIADO",
        "description": "Paquete anunciado",
        "timestamp": announcement.announced_at,
        "timestamp_colombia": format_colombia_datetime(announcement.announced_at, "%Y-%m-%d %H:%M:%S") if announcement.announced_at else None,
        "timestamp_formatted": format_colombia_datetime(announcement.announced_at, "%A, %d de %B de %Y, %I:%M %p") if announcement.announced_at else None,
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
        "YDBS": ["RECIBIDO", "ENTREGADO"],  # Flujo completo
        
        # Nuevos códigos de muestra con diferentes flujos (creados el 28/08/2025)
        # Flujos completos
        "2Z2B": ["RECIBIDO", "ENTREGADO"],  # Flujo Completo Rápido
        "C77H": ["RECIBIDO", "ENTREGADO"],  # Flujo Completo Normal
        "XS6B": ["RECIBIDO", "ENTREGADO"],  # Flujo Completo Lento
        
        # Flujos parciales
        "LCDR": ["RECIBIDO"],  # Solo Recibido Rápido
        "GV98": ["RECIBIDO"],  # Solo Recibido Normal
        
        # Cancelaciones
        "CIBY": ["CANCELADO"],  # Cancelación Temprana
        "QDIA": ["RECIBIDO", "CANCELADO"],  # Cancelación Tardía
        
        # Estados especiales
        "6DR2": ["RECIBIDO"],  # En Proceso
        "7K3N": ["RECIBIDO"],  # Pendiente de Entrega
        "TE19": ["RECIBIDO"],  # Retrasado
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
                    "timestamp_colombia": format_colombia_datetime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    "timestamp_formatted": format_colombia_datetime(timestamp, "%A, %d de %B de %Y, %I:%M %p"),
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
                    "timestamp_colombia": format_colombia_datetime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    "timestamp_formatted": format_colombia_datetime(timestamp, "%A, %d de %B de %Y, %I:%M %p"),
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
                    "timestamp_colombia": format_colombia_datetime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    "timestamp_formatted": format_colombia_datetime(timestamp, "%A, %d de %B de %Y, %I:%M %p"),
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
                "timestamp_colombia": format_colombia_datetime(package.received_at, "%Y-%m-%d %H:%M:%S"),
                "timestamp_formatted": format_colombia_datetime(package.received_at, "%A, %d de %B de %Y, %I:%M %p"),
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
                "timestamp_colombia": format_colombia_datetime(package.delivered_at, "%Y-%m-%d %H:%M:%S"),
                "timestamp_formatted": format_colombia_datetime(package.delivered_at, "%A, %d de %B de %Y, %I:%M %p"),
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
                "timestamp_colombia": format_colombia_datetime(package.updated_at, "%Y-%m-%d %H:%M:%S"),
                "timestamp_formatted": format_colombia_datetime(package.updated_at, "%A, %d de %B de %Y, %I:%M %p"),
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
            "announced_at": format_colombia_datetime(announcement.announced_at, "%Y-%m-%d %H:%M:%S") if announcement.announced_at else None,
            "announced_at_formatted": format_colombia_datetime(announcement.announced_at, "%A, %d de %B de %Y, %I:%M %p") if announcement.announced_at else None,
            "processed_at": format_colombia_datetime(announcement.processed_at, "%Y-%m-%d %H:%M:%S") if announcement.processed_at else None
        },
        "package": {
            "id": str(package.id) if package else None,
            "tracking_number": package.tracking_number if package else announcement.guide_number,
            "customer_name": package.customer_name if package else announcement.customer_name,
            "customer_phone": package.customer_phone if package else announcement.phone_number,
            "status": package.status.value if package else current_status,
            "announced_at": format_colombia_datetime(package.announced_at, "%Y-%m-%d %H:%M:%S") if package and package.announced_at else format_colombia_datetime(announcement.announced_at, "%Y-%m-%d %H:%M:%S"),
            "received_at": format_colombia_datetime(package.received_at, "%Y-%m-%d %H:%M:%S") if package and package.received_at else None,
            "delivered_at": format_colombia_datetime(package.delivered_at, "%Y-%m-%d %H:%M:%S") if package and package.delivered_at else None,
            "total_cost": str(package.total_cost) if package and package.total_cost else "25,000.00"
        } if package or announcement.tracking_code in simulated_states else None,
        "history": history,
        "current_status": current_status,
        "search_query": query
    }

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

@router.get("/rate-limit/info")
async def get_rate_limit_info_endpoint(request: Request):
    """Obtener información del rate limit para la IP actual"""
    return get_rate_limit_info(request, endpoint="announcements")

@router.post("/rate-limit/reset")
async def reset_rate_limit_endpoint(request: Request):
    """Resetear rate limit para la IP actual (solo para desarrollo/testing)"""
    success = reset_rate_limit(request, endpoint="announcements")
    if success:
        return {"message": "Rate limit reseteado exitosamente"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error reseteando rate limit"
        )
