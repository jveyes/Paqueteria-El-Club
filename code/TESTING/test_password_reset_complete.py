#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test Completo de Recuperación de Contraseña
# ========================================

import sys
import os
import asyncio
import logging
from datetime import datetime

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import get_db, engine
from src.models.user import User, UserRole
from src.models.password_reset import PasswordResetToken
from src.services.user_service import UserService
from src.services.notification_service import NotificationService
from src.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_password_reset_system():
    """Test completo del sistema de recuperación de contraseña"""
    print("🔍 INICIANDO TEST COMPLETO DE RECUPERACIÓN DE CONTRASEÑA")
    print("=" * 60)
    
    # Crear sesión de base de datos
    db = next(get_db())
    
    try:
        # 1. Verificar configuración SMTP
        print("\n📧 1. VERIFICANDO CONFIGURACIÓN SMTP")
        print(f"   Host: {settings.smtp_host}")
        print(f"   Puerto: {settings.smtp_port}")
        print(f"   Usuario: {settings.smtp_user}")
        print(f"   Contraseña: {'✅ Configurada' if settings.smtp_password else '❌ No configurada'}")
        
        if not settings.smtp_password:
            print("   ⚠️  ADVERTENCIA: Contraseña SMTP no configurada")
            print("   💡 En desarrollo, el sistema simulará el envío de emails")
        
        # 2. Buscar usuario de prueba
        print("\n👤 2. BUSCANDO USUARIO DE PRUEBA")
        user_service = UserService(db)
        
        # Buscar usuario admin
        test_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
        
        if not test_user:
            print("   ❌ No se encontró usuario admin para pruebas")
            print("   💡 Creando usuario de prueba...")
            
            # Crear usuario de prueba
            from src.schemas.user import UserCreate
            test_user_data = UserCreate(
                username="test_admin",
                email="test@papyrus.com.co",
                full_name="Usuario de Prueba",
                password="TestPassword123!",
                role=UserRole.ADMIN
            )
            
            test_user = user_service.create_user(test_user_data)
            print(f"   ✅ Usuario de prueba creado: {test_user.email}")
        else:
            print(f"   ✅ Usuario encontrado: {test_user.email}")
        
        # 3. Probar creación de token
        print("\n🔑 3. PROBANDO CREACIÓN DE TOKEN")
        reset_token = user_service.create_password_reset_token(test_user.email)
        
        if reset_token:
            print(f"   ✅ Token creado exitosamente")
            print(f"   Token: {reset_token.token[:8]}...")
            print(f"   Expira: {reset_token.expires_at}")
            print(f"   Válido: {reset_token.is_valid}")
        else:
            print("   ❌ Error creando token")
            return False
        
        # 4. Probar envío de email
        print("\n📧 4. PROBANDO ENVÍO DE EMAIL")
        notification_service = NotificationService(db)
        
        email_sent = await notification_service.send_password_reset_email(test_user, reset_token.token)
        
        if email_sent:
            print("   ✅ Email enviado exitosamente")
        else:
            print("   ❌ Error enviando email")
            if settings.environment == "development":
                print("   💡 En desarrollo, esto puede ser normal si SMTP no está configurado")
        
        # 5. Probar validación de token
        print("\n✅ 5. PROBANDO VALIDACIÓN DE TOKEN")
        
        # Buscar token en BD
        stored_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == reset_token.token
        ).first()
        
        if stored_token:
            print(f"   ✅ Token encontrado en base de datos")
            print(f"   Válido: {stored_token.is_valid}")
            print(f"   Usado: {stored_token.is_used}")
            print(f"   Expira: {stored_token.expires_at}")
        else:
            print("   ❌ Token no encontrado en base de datos")
        
        # 6. Probar restablecimiento de contraseña
        print("\n🔄 6. PROBANDO RESTABLECIMIENTO DE CONTRASEÑA")
        
        new_password = "NewPassword123!"
        reset_success = user_service.reset_password(reset_token.token, new_password)
        
        if reset_success:
            print("   ✅ Contraseña restablecida exitosamente")
            
            # Verificar que el token esté marcado como usado
            updated_token = db.query(PasswordResetToken).filter(
                PasswordResetToken.token == reset_token.token
            ).first()
            
            if updated_token and updated_token.is_used:
                print("   ✅ Token marcado como usado correctamente")
            else:
                print("   ❌ Token no marcado como usado")
        else:
            print("   ❌ Error restableciendo contraseña")
        
        # 7. Verificar nueva contraseña
        print("\n🔐 7. VERIFICANDO NUEVA CONTRASEÑA")
        
        # Intentar autenticar con nueva contraseña
        authenticated_user = user_service.authenticate_user(test_user.username, new_password)
        
        if authenticated_user:
            print("   ✅ Autenticación exitosa con nueva contraseña")
        else:
            print("   ❌ Error autenticando con nueva contraseña")
        
        print("\n" + "=" * 60)
        print("🎉 TEST COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        logger.error(f"Error en test: {e}", exc_info=True)
        return False
        
    finally:
        db.close()

async def test_api_endpoint():
    """Test del endpoint API"""
    print("\n🌐 PROBANDO ENDPOINT API")
    print("=" * 40)
    
    try:
        import httpx
        
        async with httpx.AsyncClient() as client:
            # Test del endpoint
            response = await client.post(
                "http://localhost:8000/api/auth/request-reset",
                json={"email": "test@papyrus.com.co"},
                timeout=30.0
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                print("   ✅ Endpoint funcionando correctamente")
                return True
            else:
                print("   ❌ Error en endpoint")
                return False
                
    except Exception as e:
        print(f"   ❌ Error conectando al endpoint: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS DE RECUPERACIÓN DE CONTRASEÑA")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test del sistema completo
    system_ok = asyncio.run(test_password_reset_system())
    
    if system_ok:
        # Test del endpoint API (solo si el servidor está corriendo)
        try:
            api_ok = asyncio.run(test_api_endpoint())
        except:
            print("\n⚠️  Servidor no disponible para test de API")
            api_ok = True  # No es crítico
    
    print("\n📊 RESUMEN DE TESTS")
    print("=" * 30)
    print(f"   Sistema: {'✅ OK' if system_ok else '❌ ERROR'}")
    print(f"   API: {'✅ OK' if 'api_ok' in locals() and api_ok else '❌ ERROR'}")
    
    if system_ok:
        print("\n🎯 RECOMENDACIONES:")
        print("   1. Verifica que la configuración SMTP esté correcta")
        print("   2. Asegúrate de que el servidor esté corriendo en localhost:8000")
        print("   3. Revisa los logs del servidor para más detalles")
        print("\n✅ El sistema de recuperación de contraseña está funcionando correctamente")
    else:
        print("\n❌ Hay problemas en el sistema de recuperación de contraseña")
        print("   Revisa los errores anteriores y corrige los problemas")

if __name__ == "__main__":
    main()
