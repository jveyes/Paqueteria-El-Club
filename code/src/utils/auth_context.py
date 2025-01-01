# ========================================
# PAQUETES EL CLUB v3.1 - Utilidades de Contexto de Autenticación
# ========================================

from fastapi import Request
from typing import Dict, Any, Optional
import logging
from .auth import verify_token

logger = logging.getLogger(__name__)

def get_auth_context(request: Request, is_authenticated: bool = False, user_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Genera el contexto de autenticación para los templates.
    
    Args:
        request (Request): Objeto request de FastAPI
        is_authenticated (bool): Estado de autenticación
        user_name (Optional[str]): Nombre del usuario autenticado
    
    Returns:
        Dict[str, Any]: Contexto de autenticación
    """
    context = {
        "request": request,
        "is_authenticated": is_authenticated,
        "user_name": user_name,
        "user_role": None,
        "user_id": None,
        "first_name": None
    }
    
    if is_authenticated and user_name:
        # Extraer información adicional de las cookies si está disponible
        user_role = request.cookies.get("user_role")
        user_id = request.cookies.get("user_id")
        
        context.update({
            "user_role": user_role,
            "user_id": user_id,
            "first_name": user_name.split()[0] if user_name and " " in user_name else user_name
        })
    
    return context

async def get_auth_context_from_request(request: Request) -> Dict[str, Any]:
    """
    Obtiene el contexto de autenticación desde las cookies o headers del request.
    
    Esta función verifica si existe un token JWT válido en las cookies
    o en el header Authorization y retorna el contexto de autenticación correspondiente.
    
    Args:
        request (Request): Objeto request de FastAPI
    
    Returns:
        dict: Contexto de autenticación basado en las cookies o headers
    """
    try:
        logger.debug(f"Obteniendo contexto de autenticación para {request.url}")
        # Verificar si hay user_name en cookies (indicador de autenticación)
        user_name = request.cookies.get("user_name")
        if user_name and user_name.strip():
            return get_auth_context(request, is_authenticated=True, user_name=user_name)
        
        # Si no hay user_name, verificar token
        token = request.cookies.get("access_token")
        if token and token.strip():
            payload = verify_token(token)
            if payload and payload.get("username"):
                return get_auth_context(request, is_authenticated=True, user_name=payload.get("username"))
        
        # Verificar también user_id como indicador adicional
        user_id = request.cookies.get("user_id")
        if user_id and user_id.strip():
            # Si hay user_id pero no user_name, intentar obtener el nombre del token
            token = request.cookies.get("access_token")
            if token:
                payload = verify_token(token)
                if payload and payload.get("username"):
                    return get_auth_context(request, is_authenticated=True, user_name=payload.get("username"))
        
        return get_auth_context(request, is_authenticated=False)
        
    except Exception as e:
        logger.error(f"Error obteniendo contexto de autenticación: {e}")
        return get_auth_context(request, is_authenticated=False)