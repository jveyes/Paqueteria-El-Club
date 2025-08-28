# ========================================
# PAQUETES EL CLUB v3.0 - Validadores
# ========================================

import re
from typing import Optional, Dict, Any
from ..utils.exceptions import RateCalculationException

def validate_international_phone_number(phone: str) -> Dict[str, Any]:
    """
    Valida números de teléfono internacionales con soporte especial para Colombia
    
    Args:
        phone (str): Número de teléfono a validar
        
    Returns:
        dict: {
            "is_valid": bool,
            "country_code": str,
            "national_number": str,
            "formatted_number": str,
            "country": str,
            "error_message": str (si hay error)
        }
    """
    if not phone:
        return {
            "is_valid": False,
            "country_code": "",
            "national_number": "",
            "formatted_number": "",
            "country": "",
            "error_message": "El número de teléfono es requerido"
        }
    
    # Limpiar el número de espacios y caracteres especiales
    clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone.strip())
    
    # Si tiene exactamente 10 dígitos, asumir que es Colombia (celular)
    if len(clean_phone) == 10 and clean_phone.isdigit():
        # Validar formato colombiano (celular debe empezar con 3)
        if clean_phone.startswith('3'):
            formatted = f"+57 {clean_phone[:3]} {clean_phone[3:6]} {clean_phone[6:]}"
            return {
                "is_valid": True,
                "country_code": "+57",
                "national_number": clean_phone,
                "formatted_number": formatted,
                "country": "Colombia",
                "error_message": ""
            }
        else:
            return {
                "is_valid": False,
                "country_code": "",
                "national_number": "",
                "formatted_number": "",
                "country": "",
                "error_message": "Número colombiano inválido. Los celulares deben empezar con 3"
            }
    
    # Si tiene exactamente 7 dígitos, asumir que es Colombia (fijo)
    if len(clean_phone) == 7 and clean_phone.isdigit():
        # Validar formato colombiano (fijo debe empezar con 60X)
        if clean_phone.startswith('60') and clean_phone[2] in '123456789':
            formatted = f"+57 {clean_phone[:3]} {clean_phone[3:5]} {clean_phone[5:]}"
            return {
                "is_valid": True,
                "country_code": "+57",
                "national_number": clean_phone,
                "formatted_number": formatted,
                "country": "Colombia",
                "error_message": ""
            }
        else:
            return {
                "is_valid": False,
                "country_code": "",
                "national_number": "",
                "formatted_number": "",
                "country": "",
                "error_message": "Número fijo colombiano inválido. Debe empezar con 601, 602, 603, etc."
            }
    
    # Si empieza con +, es un número internacional
    if clean_phone.startswith('+'):
        # Extraer código de país (1-4 dígitos después del +)
        country_code_match = re.match(r'^\+(\d{1,4})(.+)$', clean_phone)
        if not country_code_match:
            return {
                "is_valid": False,
                "country_code": "",
                "national_number": "",
                "formatted_number": "",
                "country": "",
                "error_message": "Formato de código de país inválido"
            }
        
        country_code = "+" + country_code_match.group(1)
        national_number = country_code_match.group(2)
        
        # Caso especial: Colombia (+57)
        if country_code == "+57":
            # Validar formato colombiano (celular - 10 dígitos)
            if len(national_number) == 10 and national_number.isdigit():
                if national_number.startswith('3'):
                    formatted = f"+57 {national_number[:3]} {national_number[3:6]} {national_number[6:]}"
                    return {
                        "is_valid": True,
                        "country_code": "+57",
                        "national_number": national_number,
                        "formatted_number": formatted,
                        "country": "Colombia",
                        "error_message": ""
                    }
                else:
                    return {
                        "is_valid": False,
                        "country_code": "+57",
                        "national_number": national_number,
                        "formatted_number": "",
                        "country": "",
                        "error_message": "Número colombiano inválido. Los celulares deben empezar con 3"
                    }
            # Validar formato colombiano (fijo - 7 dígitos)
            elif len(national_number) == 7 and national_number.isdigit():
                if national_number.startswith('60') and national_number[2] in '123456789':
                    formatted = f"+57 {national_number[:3]} {national_number[3:5]} {national_number[5:]}"
                    return {
                        "is_valid": True,
                        "country_code": "+57",
                        "national_number": national_number,
                        "formatted_number": formatted,
                        "country": "Colombia",
                        "error_message": ""
                    }
                else:
                    return {
                        "is_valid": False,
                        "country_code": "+57",
                        "national_number": national_number,
                        "formatted_number": "",
                        "country": "",
                        "error_message": "Número fijo colombiano inválido. Debe empezar con 601, 602, 603, etc."
                    }
            else:
                return {
                    "is_valid": False,
                    "country_code": "+57",
                    "national_number": national_number,
                    "formatted_number": "",
                    "country": "",
                    "error_message": "Número colombiano debe tener 7 dígitos (fijo) o 10 dígitos (celular)"
                }
        
        # Validar longitud mínima (al menos 7 dígitos para números internacionales)
        if len(national_number) < 7:
            return {
                "is_valid": False,
                "country_code": country_code,
                "national_number": national_number,
                "formatted_number": "",
                "country": "",
                "error_message": "Número demasiado corto para ser un número internacional válido"
            }
        
        # Validar longitud máxima (máximo 15 dígitos total según estándar ITU-T)
        if len(clean_phone) > 16:  # +1 + hasta 15 dígitos
            return {
                "is_valid": False,
                "country_code": country_code,
                "national_number": national_number,
                "formatted_number": "",
                "country": "",
                "error_message": "Número demasiado largo"
            }
        
        # Formatear número internacional
        formatted = f"{country_code} {national_number}"
        
        # Detectar país común por código
        country_map = {
            "+1": "Estados Unidos/Canadá",
            "+44": "Reino Unido",
            "+33": "Francia",
            "+49": "Alemania",
            "+34": "España",
            "+39": "Italia",
            "+81": "Japón",
            "+86": "China",
            "+91": "India",
            "+52": "México",
            "+54": "Argentina",
            "+55": "Brasil",
            "+56": "Chile",
            "+57": "Colombia",
            "+58": "Venezuela",
            "+593": "Ecuador",
            "+51": "Perú",
            "+591": "Bolivia",
            "+595": "Paraguay",
            "+598": "Uruguay"
        }
        
        country = country_map.get(country_code, "Internacional")
        
        return {
            "is_valid": True,
            "country_code": country_code,
            "national_number": national_number,
            "formatted_number": formatted,
            "country": country,
            "error_message": ""
        }
    
    # Si no empieza con + y no tiene 7 o 10 dígitos, es inválido
    return {
        "is_valid": False,
        "country_code": "",
        "national_number": "",
        "formatted_number": "",
        "country": "",
        "error_message": "Formato inválido. Use 7 dígitos (fijo) o 10 dígitos (celular) para Colombia, o +código para otros países"
    }

def validate_phone_number(phone: str) -> bool:
    """Validar formato de número de teléfono (función legacy para compatibilidad)"""
    result = validate_international_phone_number(phone)
    return result["is_valid"]

def validate_tracking_number(tracking: str) -> bool:
    """Validar formato de número de tracking"""
    # Formato: PAP + YYYYMMDD + 8 caracteres alfanuméricos
    pattern = r'^PAP\d{8}[A-Z0-9]{8}$'
    return bool(re.match(pattern, tracking))

def validate_email(email: str) -> bool:
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_package_dimensions(length: float, width: float, height: float) -> bool:
    """Validar dimensiones de paquete"""
    if any(dim <= 0 for dim in [length, width, height]):
        return False
    if any(dim > 200 for dim in [length, width, height]):  # 200cm máximo
        return False
    return True

def validate_package_weight(weight: float) -> bool:
    """Validar peso del paquete"""
    if weight <= 0:
        return False
    if weight > 50:  # 50kg máximo
        return False
    return True

def validate_rate_calculation_params(
    package_type: str,
    storage_days: int,
    delivery_required: bool
) -> None:
    """Validar parámetros para cálculo de tarifas"""
    if storage_days < 1:
        raise RateCalculationException("Los días de almacenamiento deben ser al menos 1")
    
    if storage_days > 365:
        raise RateCalculationException("Los días de almacenamiento no pueden exceder 365")
    
    valid_package_types = ["normal", "extra_dimensionado"]
    if package_type not in valid_package_types:
        raise RateCalculationException(f"Tipo de paquete debe ser uno de: {valid_package_types}")

def sanitize_filename(filename: str) -> str:
    """Sanitizar nombre de archivo"""
    # Remover caracteres peligrosos
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limitar longitud
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:250] + '.' + ext
    return filename

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validar extensión de archivo"""
    if not filename:
        return False
    ext = filename.lower().split('.')[-1]
    return ext in [ext.lower() for ext in allowed_extensions]

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validar tamaño de archivo"""
    return file_size <= max_size
