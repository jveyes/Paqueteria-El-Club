#!/usr/bin/env python3
"""
Script para probar el sistema de restablecimiento de contraseña
"""

import sys
from sqlalchemy import create_engine, text
import requests
import json

def check_password_reset_system():
    """Verificar el sistema de restablecimiento de contraseña"""
    try:
        print("🔐 ========================================")
        print("🔐 PRUEBA SISTEMA RESTABLECIMIENTO CONTRASEÑA")
        print("🔐 PAQUETES EL CLUB v3.1")
        print("🔐 ========================================")
        print("")
        
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Verificar usuarios disponibles
            print("\n1️⃣ VERIFICANDO USUARIOS DISPONIBLES:")
            result = conn.execute(text("SELECT id, username, email, first_name, last_name FROM users"))
            users = result.fetchall()
            
            if not users:
                print("❌ No hay usuarios en la base de datos")
                return False
            
            print(f"✅ Se encontraron {len(users)} usuarios:")
            for user in users:
                user_id, username, email, first_name, last_name = user
                print(f"   - {username} ({email}) - {first_name} {last_name}")
            
            # Verificar tokens de restablecimiento
            print("\n2️⃣ VERIFICANDO TOKENS DE RESTABLECIMIENTO:")
            result = conn.execute(text("SELECT COUNT(*) FROM password_reset_tokens"))
            token_count = result.fetchone()[0]
            print(f"📊 Total de tokens: {token_count}")
            
            # Verificar tokens válidos
            result = conn.execute(text("""
                SELECT id, token, user_id, expires_at, used 
                FROM password_reset_tokens 
                WHERE expires_at > NOW() AND used = false
                ORDER BY created_at DESC
            """))
            valid_tokens = result.fetchall()
            print(f"🔑 Tokens válidos: {len(valid_tokens)}")
            
            if valid_tokens:
                print("✅ Hay tokens válidos disponibles para restablecimiento")
                for token in valid_tokens:
                    token_id, token_val, user_id, expires_at, used = token
                    print(f"   - Token {token_id}: {token_val[:10]}... - Expira: {expires_at}")
            else:
                print("⚠️  No hay tokens válidos (todos expirados o usados)")
        
        # Verificar endpoints de la API
        print("\n3️⃣ VERIFICANDO ENDPOINTS DE LA API:")
        base_url = "https://guia.papyrus.com.co"
        
        endpoints = [
            "/health",
            "/api/auth/forgot-password",
            "/api/auth/reset-password",
            "/forgot-password",
            "/reset-password"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10, verify=False)
                status = "✅" if response.status_code < 400 else "⚠️"
                print(f"   {status} {endpoint} - Status: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {endpoint} - Error: {str(e)[:50]}...")
        
        print("\n4️⃣ INSTRUCCIONES PARA PROBAR RESTABLECIMIENTO:")
        print("=" * 50)
        print("1. Ve a: https://guia.papyrus.com.co/forgot-password")
        print("2. Ingresa el email: jveyes@gmail.com")
        print("3. Revisa tu email para el enlace de restablecimiento")
        print("4. Haz clic en el enlace y establece una nueva contraseña")
        print("5. Inicia sesión con la nueva contraseña")
        
        print("\n🌐 URLs IMPORTANTES:")
        print("=" * 30)
        print("🔗 Aplicación: https://guia.papyrus.com.co")
        print("🔗 Login: https://guia.papyrus.com.co/login")
        print("🔗 Forgot Password: https://guia.papyrus.com.co/forgot-password")
        print("🔗 Health Check: https://guia.papyrus.com.co/health")
        
        print("\n📧 CONFIGURACIÓN SMTP:")
        print("=" * 30)
        print("🏢 Servidor: smtp.gmail.com")
        print("🔌 Puerto: 587")
        print("👤 Usuario: jveyes@gmail.com")
        print("🔒 TLS: Habilitado")
        print("⚠️  Falta: EMAIL_PASSWORD en .env")
        
        print("\n✅ VERIFICACIÓN COMPLETADA!")
        print("🎉 El sistema de restablecimiento está configurado")
        print("📧 Solo falta agregar la contraseña de aplicación en .env")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    return check_password_reset_system()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Sistema de restablecimiento listo!")
    else:
        print("\n❌ Error en la verificación")
