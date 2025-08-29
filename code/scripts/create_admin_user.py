#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Script de Creación de Usuario Admin
# ========================================

import sys
import os
import uuid
from datetime import datetime

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sqlalchemy.orm import Session
from src.database.database import SessionLocal, engine
from src.models.user import User, UserRole
from src.models.password_reset import PasswordResetToken
from src.utils.auth import get_password_hash
from src.utils.datetime_utils import get_colombia_now

def create_admin_user():
    """Crear usuario administrador inicial"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe un admin
        existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if existing_admin:
            print(f"✅ Ya existe un administrador: {existing_admin.username}")
            return existing_admin
        
        # Datos del admin por defecto
        admin_data = {
            "username": "admin",
            "email": "admin@paqueteselclub.com",
            "full_name": "Administrador del Sistema",
            "password": "Admin123!",
            "role": UserRole.ADMIN,
            "is_active": True,
            "is_verified": True,
            "phone": "3001234567",
            "notes": "Usuario administrador creado automáticamente"
        }
        
        # Crear hash de la contraseña
        hashed_password = get_password_hash(admin_data["password"])
        
        # Crear usuario admin
        admin_user = User(
            username=admin_data["username"],
            email=admin_data["email"],
            full_name=admin_data["full_name"],
            hashed_password=hashed_password,
            role=admin_data["role"],
            is_active=admin_data["is_active"],
            is_verified=admin_data["is_verified"],
            phone=admin_data["phone"],
            notes=admin_data["notes"]
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Usuario administrador creado exitosamente!")
        print(f"   Username: {admin_data['username']}")
        print(f"   Email: {admin_data['email']}")
        print(f"   Contraseña: {admin_data['password']}")
        print(f"   Rol: {admin_data['role']}")
        print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creando usuario admin: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def create_operator_user():
    """Crear usuario operador de ejemplo"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe el operador
        existing_operator = db.query(User).filter(
            User.username == "operador"
        ).first()
        
        if existing_operator:
            print(f"✅ Ya existe el operador: {existing_operator.username}")
            return existing_operator
        
        # Datos del operador
        operator_data = {
            "username": "operador",
            "email": "operador@paqueteselclub.com",
            "full_name": "Operador del Sistema",
            "password": "Operador123!",
            "role": UserRole.OPERATOR,
            "is_active": True,
            "is_verified": True,
            "phone": "3009876543",
            "notes": "Usuario operador de ejemplo"
        }
        
        # Crear hash de la contraseña
        hashed_password = get_password_hash(operator_data["password"])
        
        # Crear usuario operador
        operator_user = User(
            username=operator_data["username"],
            email=operator_data["email"],
            full_name=operator_data["full_name"],
            hashed_password=hashed_password,
            role=operator_data["role"],
            is_active=operator_data["is_active"],
            is_verified=operator_data["is_verified"],
            phone=operator_data["phone"],
            notes=operator_data["notes"]
        )
        
        db.add(operator_user)
        db.commit()
        db.refresh(operator_user)
        
        print("✅ Usuario operador creado exitosamente!")
        print(f"   Username: {operator_data['username']}")
        print(f"   Email: {operator_data['email']}")
        print(f"   Contraseña: {operator_data['password']}")
        print(f"   Rol: {operator_data['role']}")
        
        return operator_user
        
    except Exception as e:
        print(f"❌ Error creando usuario operador: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 PAQUETES EL CLUB v3.1 - Creación de Usuarios Iniciales")
    print("=" * 60)
    
    # Crear admin
    print("\n📋 Creando usuario administrador...")
    admin = create_admin_user()
    
    # Crear operador
    print("\n📋 Creando usuario operador...")
    operator = create_operator_user()
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado!")
    print("\n🔐 Credenciales de acceso:")
    print("   Admin: admin / Admin123!")
    print("   Operador: operador / Operador123!")
    print("\n⚠️  RECUERDA: Cambiar las contraseñas después del primer login")

if __name__ == "__main__":
    main()
