# ========================================
# PAQUETES EL CLUB v3.1 - Utilidades de Autenticación
# ========================================

from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
import uuid

from ..config import settings

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verifica y decodifica un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user_from_token(token: str) -> Optional[dict]:
    """Obtiene la información del usuario desde un token"""
    payload = verify_token(token)
    if payload is None:
        return None
    
    user_id: str = payload.get("sub")
    if user_id is None:
        return None
    
    return {
        "user_id": user_id,
        "username": payload.get("username"),
        "role": payload.get("role"),
        "exp": payload.get("exp")
    }

def authenticate_user(username: str, password: str, db_user) -> bool:
    """Autentica un usuario con username y contraseña"""
    if not db_user:
        return False
    
    if not verify_password(password, db_user.hashed_password):
        return False
    
    if not db_user.is_active:
        return False
    
    return True

def create_user_token(user_id: Union[str, uuid.UUID], username: str, role: str) -> str:
    """Crea un token JWT para un usuario específico"""
    user_id_str = str(user_id) if isinstance(user_id, uuid.UUID) else user_id
    
    data = {
        "sub": user_id_str,
        "username": username,
        "role": role,
        "type": "access"
    }
    
    return create_access_token(data)

def validate_password_strength(password: str) -> bool:
    """Valida la fortaleza de una contraseña"""
    if len(password) < 8:
        return False
    
    # Al menos una letra mayúscula, una minúscula y un número
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit

def generate_secure_password() -> str:
    """Genera una contraseña segura aleatoria"""
    import random
    import string
    
    # Caracteres disponibles
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*"
    
    # Generar contraseña con al menos un carácter de cada tipo
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]
    
    # Completar con caracteres aleatorios
    all_chars = lowercase + uppercase + digits + symbols
    password.extend(random.choice(all_chars) for _ in range(8))
    
    # Mezclar la contraseña
    random.shuffle(password)
    
    return ''.join(password)
