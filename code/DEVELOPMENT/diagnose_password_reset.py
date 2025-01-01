#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Diagnóstico de Recuperación de Contraseña
# ========================================

import sys
import os
import logging
from datetime import datetime

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import settings
from src.database.database import get_db
from src.models.user import User
from src.models.password_reset import PasswordResetToken

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def diagnose_password_reset():
    """Diagnóstico completo del sistema de recuperación de contraseña"""
    print("🔍 DIAGNÓSTICO DEL SISTEMA DE RECUPERACIÓN DE CONTRASEÑA")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    issues = []
    
    # 1. Verificar configuración SMTP
    print("\n📧 1. CONFIGURACIÓN SMTP")
    print("-" * 30)
    
    smtp_config = {
        "Host": settings.smtp_host,
        "Puerto": settings.smtp_port,
        "Usuario": settings.smtp_user,
        "Contraseña": "✅ Configurada" if settings.smtp_password else "❌ No configurada",
        "From Name": settings.smtp_from_name,
        "From Email": settings.smtp_from_email
    }
    
    for key, value in smtp_config.items():
        print(f"   {key}: {value}")
    
    if not settings.smtp_password:
        issues.append("Contraseña SMTP no configurada")
        print("   ⚠️  En desarrollo, el sistema simulará el envío de emails")
    
    # 2. Verificar base de datos
    print("\n🗄️  2. BASE DE DATOS")
    print("-" * 30)
    
    try:
        db = next(get_db())
        
        # Verificar conexión
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        print("   ✅ Conexión a base de datos: OK")
        
        # Verificar tablas
        tables = ["users", "password_reset_tokens"]
        for table in tables:
            try:
                db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                print(f"   ✅ Tabla {table}: OK")
            except Exception as e:
                issues.append(f"Tabla {table} no accesible: {e}")
                print(f"   ❌ Tabla {table}: ERROR")
        
        # Verificar usuarios
        user_count = db.query(User).count()
        print(f"   👥 Usuarios en BD: {user_count}")
        
        if user_count == 0:
            issues.append("No hay usuarios en la base de datos")
            print("   ⚠️  No hay usuarios para probar")
        
        # Verificar tokens existentes
        token_count = db.query(PasswordResetToken).count()
        print(f"   🔑 Tokens de reset: {token_count}")
        
        # Verificar tokens válidos
        valid_tokens = db.query(PasswordResetToken).filter(
            PasswordResetToken.is_used == False
        ).count()
        print(f"   ✅ Tokens válidos: {valid_tokens}")
        
        db.close()
        
    except Exception as e:
        issues.append(f"Error conectando a BD: {e}")
        print(f"   ❌ Error de base de datos: {e}")
    
    # 3. Verificar configuración de la aplicación
    print("\n⚙️  3. CONFIGURACIÓN DE LA APLICACIÓN")
    print("-" * 30)
    
    app_config = {
        "Entorno": settings.environment,
        "Debug": settings.debug,
        "Secret Key": "✅ Configurada" if settings.secret_key else "❌ No configurada",
        "Algoritmo": settings.algorithm,
        "Expiración Token": f"{settings.access_token_expire_minutes} minutos"
    }
    
    for key, value in app_config.items():
        print(f"   {key}: {value}")
    
    if not settings.secret_key:
        issues.append("Secret key no configurada")
    
    # 4. Verificar archivos críticos
    print("\n📁 4. ARCHIVOS CRÍTICOS")
    print("-" * 30)
    
    critical_files = [
        "src/routers/auth.py",
        "src/services/user_service.py", 
        "src/services/notification_service.py",
        "src/models/password_reset.py",
        "templates/auth/forgot-password.html"
    ]
    
    for file_path in critical_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}")
        else:
            issues.append(f"Archivo faltante: {file_path}")
            print(f"   ❌ {file_path}")
    
    # 5. Verificar endpoints
    print("\n🌐 5. ENDPOINTS")
    print("-" * 30)
    
    endpoints = [
        "/api/auth/request-reset",
        "/auth/forgot-password",
        "/auth/reset-password"
    ]
    
    for endpoint in endpoints:
        print(f"   📍 {endpoint}")
    
    # 6. Resumen de problemas
    print("\n📊 RESUMEN DE DIAGNÓSTICO")
    print("=" * 60)
    
    if issues:
        print("❌ PROBLEMAS ENCONTRADOS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 SOLUCIONES RECOMENDADAS:")
        
        if "Contraseña SMTP no configurada" in issues:
            print("   1. Configura SMTP_PASSWORD en env.development")
            print("      SMTP_PASSWORD=tu_contraseña_aqui")
        
        if "No hay usuarios en la base de datos" in issues:
            print("   2. Crea al menos un usuario admin")
            print("      python code/create_admin_user.py")
        
        if "Secret key no configurada" in issues:
            print("   3. Configura SECRET_KEY en env.development")
        
        print("\n💡 CONSEJOS ADICIONALES:")
        print("   - Ejecuta: python code/test_password_reset_complete.py")
        print("   - Revisa los logs del servidor")
        print("   - Verifica que el servidor esté corriendo en localhost:8000")
        
    else:
        print("✅ NO SE ENCONTRARON PROBLEMAS")
        print("   El sistema de recuperación de contraseña debería funcionar correctamente")
        print("\n🧪 Para verificar completamente, ejecuta:")
        print("   python code/test_password_reset_complete.py")
    
    print("\n" + "=" * 60)

def quick_test():
    """Test rápido del endpoint"""
    print("\n⚡ TEST RÁPIDO DEL ENDPOINT")
    print("=" * 40)
    
    try:
        import requests
        
        response = requests.post(
            "http://localhost:8000/api/auth/request-reset",
            json={"email": "test@papyrus.com.co"},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Endpoint funcionando")
        else:
            print("   ❌ Error en endpoint")
            
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Servidor no disponible")
        print("   💡 Asegúrate de que el servidor esté corriendo")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Función principal"""
    diagnose_password_reset()
    
    # Preguntar si hacer test rápido
    try:
        response = input("\n¿Quieres hacer un test rápido del endpoint? (s/n): ").lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            quick_test()
    except KeyboardInterrupt:
        print("\n\n👋 Diagnóstico cancelado")

if __name__ == "__main__":
    main()
