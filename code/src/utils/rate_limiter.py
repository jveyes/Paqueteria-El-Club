# ========================================
# PAQUETES EL CLUB v3.1 - Rate Limiting Utility
# ========================================

import redis
import time
from fastapi import HTTPException, Request
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Configuración de Redis
redis_client = None
try:
    redis_client = redis.Redis(
        host='redis',  # Nombre del servicio en docker-compose
        port=6379,
        db=0,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2
    )
    # Verificar conexión
    redis_client.ping()
    logger.info("✅ Conexión a Redis establecida para rate limiting")
except Exception as e:
    logger.warning(f"⚠️ Redis no disponible para rate limiting: {e}")
    redis_client = None

def check_rate_limit(
    request: Request, 
    max_requests: int = 5, 
    window: int = 60,
    endpoint: str = "announcements"
) -> None:
    """
    Verifica el rate limit para una IP específica
    
    Args:
        request: Request de FastAPI
        max_requests: Máximo número de requests permitidos
        window: Ventana de tiempo en segundos
        endpoint: Nombre del endpoint para diferenciar límites
        
    Raises:
        HTTPException: Si se excede el límite
    """
    if not redis_client:
        logger.warning("⚠️ Redis no disponible, saltando rate limiting")
        return
    
    try:
        # Obtener IP del cliente
        client_ip = request.client.host
        
        # Para desarrollo local, usar IP real si está disponible
        if client_ip in ['127.0.0.1', 'localhost']:
            forwarded_for = request.headers.get('X-Forwarded-For')
            if forwarded_for:
                client_ip = forwarded_for.split(',')[0].strip()
        
        # Crear clave única para esta IP y endpoint
        key = f"rate_limit:{endpoint}:{client_ip}"
        
        # Incrementar contador usando pipeline para atomicidad
        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        result = pipe.execute()
        
        # Obtener el nuevo valor del contador
        current_requests = result[0]  # El resultado del INCR
        
        if current_requests > max_requests:
            # Calcular tiempo restante
            ttl = redis_client.ttl(key)
            minutes = ttl // 60
            seconds = ttl % 60
            
            error_message = f"Demasiadas solicitudes. Máximo {max_requests} por minuto. "
            if minutes > 0:
                error_message += f"Intenta nuevamente en {minutes} minuto{'s' if minutes > 1 else ''} y {seconds} segundo{'s' if seconds != 1 else ''}."
            else:
                error_message += f"Intenta nuevamente en {seconds} segundo{'s' if seconds != 1 else ''}."
            
            logger.warning(f"🚫 Rate limit excedido para IP {client_ip}: {current_requests}/{max_requests}")
            raise HTTPException(
                status_code=429, 
                detail=error_message
            )
        
        # Log para monitoreo
        new_count = redis_client.get(key)
        logger.info(f"📊 Rate limit para IP {client_ip}: {new_count}/{max_requests}")
        
    except redis.RedisError as e:
        logger.error(f"❌ Error de Redis en rate limiting: {e}")
        # En caso de error de Redis, permitir la request
        return
    except HTTPException:
        # Re-lanzar HTTPException para que FastAPI la maneje
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado en rate limiting: {e}")
        # En caso de error inesperado, permitir la request
        return

def get_rate_limit_info(request: Request, endpoint: str = "announcements") -> dict:
    """
    Obtiene información del rate limit para una IP
    
    Args:
        request: Request de FastAPI
        endpoint: Nombre del endpoint
        
    Returns:
        dict: Información del rate limit
    """
    if not redis_client:
        return {"error": "Redis no disponible"}
    
    try:
        client_ip = request.client.host
        if client_ip in ['127.0.0.1', 'localhost']:
            forwarded_for = request.headers.get('X-Forwarded-For')
            if forwarded_for:
                client_ip = forwarded_for.split(',')[0].strip()
        
        key = f"rate_limit:{endpoint}:{client_ip}"
        current_requests = redis_client.get(key)
        ttl = redis_client.ttl(key)
        
        return {
            "ip": client_ip,
            "current_requests": int(current_requests) if current_requests else 0,
            "max_requests": 5,
            "window_seconds": 60,
            "time_remaining": ttl if ttl > 0 else 0,
            "limit_exceeded": int(current_requests) >= 5 if current_requests else False
        }
    except Exception as e:
        logger.error(f"❌ Error obteniendo info de rate limit: {e}")
        return {"error": str(e)}

def reset_rate_limit(request: Request, endpoint: str = "announcements") -> bool:
    """
    Resetea el rate limit para una IP (útil para testing)
    
    Args:
        request: Request de FastAPI
        endpoint: Nombre del endpoint
        
    Returns:
        bool: True si se reseteó exitosamente
    """
    if not redis_client:
        return False
    
    try:
        client_ip = request.client.host
        if client_ip in ['127.0.0.1', 'localhost']:
            forwarded_for = request.headers.get('X-Forwarded-For')
            if forwarded_for:
                client_ip = forwarded_for.split(',')[0].strip()
        
        key = f"rate_limit:{endpoint}:{client_ip}"
        redis_client.delete(key)
        logger.info(f"🔄 Rate limit reseteado para IP {client_ip}")
        return True
    except Exception as e:
        logger.error(f"❌ Error reseteando rate limit: {e}")
        return False
