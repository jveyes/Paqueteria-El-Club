# ========================================
# PAQUETES EL CLUB v3.1 - Utilidades de Seguridad
# ========================================

import re
import html
import unicodedata


def sanitize_text(text: str) -> str:
    """
    Sanitiza texto removiendo caracteres peligrosos y normalizando Unicode
    
    Args:
        text: Texto a sanitizar
        
    Returns:
        Texto sanitizado
    """
    if not text:
        return text
    
    # Convertir a string si no lo es
    text = str(text)
    
    # Normalizar Unicode (remover caracteres de control y emojis)
    text = unicodedata.normalize('NFKD', text)
    
    # Remover caracteres de control (excepto espacios y saltos de línea)
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Remover emojis y caracteres Unicode especiales
    text = re.sub(r'[^\x00-\x7F\u00A0-\u00FF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\u2C60-\u2C7F\uA720-\uA7FF]', '', text)
    
    # Escapar HTML para prevenir XSS
    text = html.escape(text)
    
    # Remover caracteres potencialmente peligrosos
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', '[', ']', '\\', '/', '|', '`', '~', '!', '@', '#', '$', '%', '^', '*', '+', '=', '?']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    # Limpiar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def validate_phone_number(phone: str) -> str:
    """
    Valida y limpia número de teléfono colombiano
    
    Args:
        phone: Número de teléfono a validar
        
    Returns:
        Número de teléfono limpio
        
    Raises:
        ValueError: Si el número no es válido
    """
    if not phone:
        raise ValueError('El teléfono es requerido')
    
    # Remover todos los caracteres no numéricos
    digits = re.sub(r'[^\d]', '', phone)
    
    # Validar longitud mínima
    if len(digits) < 10:
        raise ValueError('El teléfono debe tener al menos 10 dígitos')
    
    # Validar longitud máxima
    if len(digits) > 15:
        raise ValueError('El teléfono no puede exceder 15 dígitos')
    
    # Validar que sea un número colombiano válido
    if not digits.startswith(('3', '6')):
        raise ValueError('El teléfono debe ser un número colombiano válido (celular o fijo)')
    
    return digits

def validate_guide_number(guide: str) -> str:
    """
    Valida y limpia número de guía
    
    Args:
        guide: Número de guía a validar
        
    Returns:
        Número de guía limpio
        
    Raises:
        ValueError: Si la guía no es válida
    """
    if not guide:
        raise ValueError('El número de guía es requerido')
    
    # Sanitizar texto
    guide = sanitize_text(guide)
    
    # Validar longitud mínima
    if len(guide) < 5:
        raise ValueError('El número de guía debe tener al menos 5 caracteres')
    
    # Validar longitud máxima
    if len(guide) > 50:
        raise ValueError('El número de guía no puede exceder 50 caracteres')
    
    # Solo permitir letras, números y guiones
    if not re.match(r'^[A-Za-z0-9\-]+$', guide):
        raise ValueError('El número de guía solo puede contener letras, números y guiones')
    
    return guide.upper()

def validate_customer_name(name: str) -> str:
    """
    Valida y limpia nombre del cliente
    
    Args:
        name: Nombre a validar
        
    Returns:
        Nombre limpio
        
    Raises:
        ValueError: Si el nombre no es válido
    """
    if not name:
        raise ValueError('El nombre del cliente es requerido')
    
    # Sanitizar texto
    name = sanitize_text(name)
    
    # Validar longitud mínima
    if len(name) < 2:
        raise ValueError('El nombre debe tener al menos 2 caracteres')
    
    # Validar longitud máxima
    if len(name) > 100:
        raise ValueError('El nombre no puede exceder 100 caracteres')
    
    # Solo permitir letras, espacios y algunos caracteres especiales seguros
    if not re.match(r'^[A-Za-zÀ-ÿ\s\.]+$', name):
        raise ValueError('El nombre solo puede contener letras, espacios y puntos')
    
    return name.strip()

def is_safe_input(text: str) -> bool:
    """
    Verifica si el texto es seguro (no contiene caracteres peligrosos)
    
    Args:
        text: Texto a verificar
        
    Returns:
        True si es seguro, False si no
    """
    if not text:
        return True
    
    # Verificar caracteres peligrosos
    dangerous_patterns = [
        r'<script',  # XSS
        r'javascript:',  # XSS
        r'on\w+\s*=',  # Event handlers
        r'<iframe',  # XSS
        r'<object',  # XSS
        r'<embed',  # XSS
        r'<form',  # XSS
        r'<input',  # XSS
        r'<textarea',  # XSS
        r'<select',  # XSS
        r'<button',  # XSS
        r'<link',  # XSS
        r'<meta',  # XSS
        r'<style',  # XSS
        r'<title',  # XSS
        r'<body',  # XSS
        r'<head',  # XSS
        r'<html',  # XSS
        r'<xml',  # XSS
        r'<svg',  # XSS
        r'<math',  # XSS
        r'<applet',  # XSS
        r'<base',  # XSS
        r'<bgsound',  # XSS
        r'<link',  # XSS
        r'<meta',  # XSS
        r'<title',  # XSS
        r'<xmp',  # XSS
        r'<listing',  # XSS
        r'<plaintext',  # XSS
        r'<marquee',  # XSS
        r'<isindex',  # XSS
        r'<nextid',  # XSS
        r'<spacer',  # XSS
        r'<wbr',  # XSS
        r'<nobr',  # XSS
        r'<noembed',  # XSS
        r'<noframes',  # XSS
        r'<noscript',  # XSS
        r'<noindex',  # XSS
        r'<noprint',  # XSS
        r'<nobr',  # XSS
        r'<wbr',  # XSS
        r'<spacer',  # XSS
        r'<isindex',  # XSS
        r'<nextid',  # XSS
        r'<marquee',  # XSS
        r'<plaintext',  # XSS
        r'<listing',  # XSS
        r'<xmp',  # XSS
        r'<title',  # XSS
        r'<meta',  # XSS
        r'<link',  # XSS
        r'<bgsound',  # XSS
        r'<base',  # XSS
        r'<applet',  # XSS
        r'<math',  # XSS
        r'<svg',  # XSS
        r'<xml',  # XSS
        r'<html',  # XSS
        r'<head',  # XSS
        r'<body',  # XSS
        r'<style',  # XSS
        r'<title',  # XSS
        r'<meta',  # XSS
        r'<link',  # XSS
        r'<button',  # XSS
        r'<select',  # XSS
        r'<textarea',  # XSS
        r'<input',  # XSS
        r'<form',  # XSS
        r'<embed',  # XSS
        r'<object',  # XSS
        r'<iframe',  # XSS
        r'on\w+\s*=',  # Event handlers
        r'javascript:',  # XSS
        r'<script',  # XSS
        r'DROP\s+TABLE',  # SQL Injection
        r'DELETE\s+FROM',  # SQL Injection
        r'UPDATE\s+.*\s+SET',  # SQL Injection
        r'INSERT\s+INTO',  # SQL Injection
        r'CREATE\s+TABLE',  # SQL Injection
        r'ALTER\s+TABLE',  # SQL Injection
        r'DROP\s+DATABASE',  # SQL Injection
        r'CREATE\s+DATABASE',  # SQL Injection
        r'USE\s+',  # SQL Injection
        r'SHOW\s+',  # SQL Injection
        r'DESCRIBE\s+',  # SQL Injection
        r'EXPLAIN\s+',  # SQL Injection
        r'UNION\s+',  # SQL Injection
        r'SELECT\s+.*\s+FROM',  # SQL Injection
        r'WHERE\s+.*\s*=\s*.*\s*--',  # SQL Injection
        r'OR\s+1\s*=\s*1',  # SQL Injection
        r'AND\s+1\s*=\s*1',  # SQL Injection
        r'OR\s+1\s*=\s*1\s*--',  # SQL Injection
        r'AND\s+1\s*=\s*1\s*--',  # SQL Injection
        r'OR\s+1\s*=\s*1\s*#',  # SQL Injection
        r'AND\s+1\s*=\s*1\s*#',  # SQL Injection
        r'OR\s+1\s*=\s*1\s*/*',  # SQL Injection
        r'AND\s+1\s*=\s*1\s*/*',  # SQL Injection
        r'OR\s+1\s*=\s*1\s*--',  # SQL Injection
        r'AND\s+1\s*=\s*1\s*--',  # SQL Injection
        r'OR\s+1\s*=\s*1\s*#',  # SQL Injection
        r'AND\s+1\s*=\s*1\s*#',  # SQL Injection
        r'OR\s+1\s*=\s*1\s*/*',  # SQL Injection
        r'AND\s+1\s*=\s*1\s*/*',  # SQL Injection
    ]
    
    text_lower = text.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return False
    
    return True
