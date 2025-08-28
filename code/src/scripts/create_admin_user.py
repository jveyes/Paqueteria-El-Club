#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Script de Creación de Usuario Administrador
# ========================================

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent.parent))

from database.database import SessionLocal, engine
from models.user import User, UserRole
from utils.helpers import get_password_hash
from models import base

def create_admin_user():
    """Crear usuario administrador por defecto"""
    
    # Crear tablas si no existen
    base.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existe un admin
        existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        
        if existing_admin:
            print("✅ Ya existe un usuario administrador en el sistema")
            print(f"   Usuario: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            return
        
        # Crear usuario administrador por defecto
        admin_user = User(
            username="admin",
            email="admin@papyrus.com.co",
            hashed_password=get_password_hash("Admin2025!"),
            first_name="Administrador",
            last_name="Sistema",
            phone="3334004007",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Usuario administrador creado exitosamente")
        print(f"   Usuario: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Contraseña: Admin2025!")
        print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
