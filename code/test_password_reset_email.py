#!/usr/bin/env python3
"""
Script para probar el envío de email de restablecimiento de contraseña
"""

import asyncio
import sys
import os
import uuid
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.append('/app/src')

from src.services.notification_service import NotificationService
from src.database.database import get_db
from src.models.user import User
from src.config import settings

async def test_password_reset_email():
    """Probar envío de email de restablecimiento de contraseña"""
    
    print("🚀 INICIANDO PRUEBA DE EMAIL DE RESTABLECIMIENTO DE CONTRASEÑA")
    print("=" * 70)
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Crear instancia del servicio de notificaciones
        notification_service = NotificationService(db)
        
        # Buscar un usuario existente o crear uno de prueba
        user = db.query(User).first()
        
        if not user:
            print("⚠️  No se encontraron usuarios en la base de datos")
            print("   Creando usuario de prueba...")
            
            # Crear usuario de prueba
            user = User(
                id=str(uuid.uuid4()),
                username="test_user",
                email="jveyes@gmail.com",
                hashed_password="test_hash",
                first_name="Test",
                last_name="User",
                phone="3001234567",
                is_active=True,
                role="USER"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("✅ Usuario de prueba creado")
        
        print(f"🔍 USUARIO DE PRUEBA:")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Nombre: {user.first_name} {user.last_name}")
        print()
        
        # Generar token de restablecimiento
        reset_token = str(uuid.uuid4())
        print(f"🔑 TOKEN DE RESTABLECIMIENTO: {reset_token}")
        print()
        
        print("📧 ENVIANDO EMAIL DE RESTABLECIMIENTO...")
        
        # Enviar email de restablecimiento
        success = await notification_service.send_password_reset_email(user, reset_token)
        
        if success:
            print("✅ Email de restablecimiento enviado exitosamente")
            print()
            print("📋 RESUMEN:")
            print(f"   Email enviado a: {user.email}")
            print(f"   Token generado: {reset_token}")
            print(f"   URL de restablecimiento: http://localhost/auth/reset-password?token={reset_token}")
            return True
        else:
            print("❌ Error al enviar email de restablecimiento")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = asyncio.run(test_password_reset_email())
    
    print("=" * 70)
    if success:
        print("🎉 PRUEBA EXITOSA: El envío de email de restablecimiento funciona")
    else:
        print("💥 PRUEBA FALLIDA: Hay problemas con el envío de email de restablecimiento")
    print("=" * 70)
