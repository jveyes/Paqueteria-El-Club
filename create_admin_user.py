#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Crear Usuario Administrador
# ========================================

import sys
import os
import uuid
from datetime import datetime

# Agregar el directorio code al path
sys.path.append('./code')

from src.database.database import SessionLocal, engine
from src.models.user import User, UserRole
from src.utils.auth import get_password_hash

def create_admin_user():
    """Crear usuario administrador por defecto"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe un usuario admin
        existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if existing_admin:
            print(f"✅ Ya existe un usuario administrador: {existing_admin.username}")
            return existing_admin
        
        # Crear usuario administrador
        admin_user = User(
            id=uuid.uuid4(),
            username="admin",
            email="admin@papyrus.com.co",
            full_name="Administrador Sistema",
            hashed_password=get_password_hash("Admin2025!"),
            phone="3334004007",
            role=UserRole.ADMIN,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Usuario administrador creado exitosamente:")
        print(f"   Username: admin")
        print(f"   Email: admin@papyrus.com.co")
        print(f"   Password: Admin2025!")
        print(f"   Role: {admin_user.role.value}")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def create_test_user():
    """Crear usuario de prueba"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe el usuario de prueba
        existing_user = db.query(User).filter(User.username == "jveyes").first()
        if existing_user:
            print(f"✅ Ya existe el usuario de prueba: {existing_user.username}")
            return existing_user
        
        # Crear usuario de prueba
        test_user = User(
            id=uuid.uuid4(),
            username="jveyes",
            email="jveyes@gmail.com",
            full_name="Juan Veyes",
            hashed_password=get_password_hash("Test2025!"),
            phone="3334004007",
            role=UserRole.OPERATOR,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Usuario de prueba creado exitosamente:")
        print(f"   Username: jveyes")
        print(f"   Email: jveyes@gmail.com")
        print(f"   Password: Test2025!")
        print(f"   Role: {test_user.role.value}")
        
        return test_user
        
    except Exception as e:
        print(f"❌ Error creando usuario de prueba: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Creando usuarios en la base de datos...")
    print("=" * 50)
    
    # Crear usuario administrador
    admin = create_admin_user()
    
    print()
    
    # Crear usuario de prueba
    test_user = create_test_user()
    
    print()
    print("=" * 50)
    print("🎉 Proceso completado!")
    print()
    print("📋 Credenciales de acceso:")
    print("   Admin: admin / Admin2025!")
    print("   Test:  jveyes / Test2025!")
    print()
    print("🌐 Accede a: http://localhost:80")
