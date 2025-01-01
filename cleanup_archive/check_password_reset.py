#!/usr/bin/env python3
"""
Script para verificar el estado del sistema de restablecimiento de contraseña
"""

import sys
from sqlalchemy import create_engine, text

def main():
    try:
        print("🔐 ========================================")
        print("🔐 VERIFICACIÓN SISTEMA RESTABLECIMIENTO")
        print("🔐 PAQUETES EL CLUB v3.1")
        print("🔐 ========================================")
        print("")
        
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos AWS RDS...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a AWS RDS establecida")
        
        print("\n📋 VERIFICANDO SISTEMA DE RESTABLECIMIENTO:")
        print("=" * 50)
        
        with engine.connect() as conn:
            # 1. Verificar tabla password_reset_tokens
            print("\n1️⃣ TABLA PASSWORD_RESET_TOKENS:")
            result = conn.execute(text("SELECT COUNT(*) FROM password_reset_tokens"))
            token_count = result.fetchone()[0]
            print(f"   🔑 Total de tokens: {token_count}")
            
            if token_count > 0:
                result = conn.execute(text("""
                    SELECT id, token, user_id, expires_at, used, created_at 
                    FROM password_reset_tokens 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """))
                tokens = result.fetchall()
                for token in tokens:
                    token_id, token_val, user_id, expires_at, used, created_at = token
                    status = "✅ Usado" if used else "⏳ Pendiente"
                    print(f"   - Token {token_id}: {token_val[:10]}... - {status} - {expires_at}")
            
            # 2. Verificar usuarios disponibles
            print("\n2️⃣ USUARIOS DISPONIBLES:")
            result = conn.execute(text("SELECT id, username, email, first_name, last_name FROM users"))
            users = result.fetchall()
            for user in users:
                user_id, username, email, first_name, last_name = user
                print(f"   - {username} ({email}) - {first_name} {last_name} - ID: {user_id}")
            
            # 3. Verificar configuración de email
            print("\n3️⃣ CONFIGURACIÓN DE EMAIL:")
            print("   📧 Verificar variables de entorno:")
            print("   - EMAIL_HOST")
            print("   - EMAIL_PORT") 
            print("   - EMAIL_USERNAME")
            print("   - EMAIL_PASSWORD")
            print("   - EMAIL_USE_TLS")
            
            # 4. Verificar endpoints de la API
            print("\n4️⃣ ENDPOINTS DE RESTABLECIMIENTO:")
            print("   🔗 POST /api/auth/forgot-password")
            print("   🔗 POST /api/auth/reset-password")
            print("   🔗 GET /reset-password/{token}")
            
            # 5. Verificar logs de la aplicación
            print("\n5️⃣ LOGS DE LA APLICACIÓN:")
            print("   📝 Verificar logs en /app/logs/app.log")
            
            # 6. Verificar tokens válidos
            print("\n6️⃣ TOKENS VÁLIDOS (NO EXPIRADOS):")
            result = conn.execute(text("""
                SELECT id, token, user_id, expires_at, used 
                FROM password_reset_tokens 
                WHERE expires_at > NOW() AND used = false
                ORDER BY created_at DESC
            """))
            valid_tokens = result.fetchall()
            print(f"   🔑 Tokens válidos: {len(valid_tokens)}")
            
            for token in valid_tokens:
                token_id, token_val, user_id, expires_at, used = token
                print(f"   - Token {token_id}: {token_val[:10]}... - Expira: {expires_at}")
        
        print(f"\n🔧 DIAGNÓSTICO:")
        print("=" * 30)
        print(f"📊 Tokens totales: {token_count}")
        print(f"🔑 Tokens válidos: {len(valid_tokens)}")
        print(f"👥 Usuarios: {len(users)}")
        
        if token_count == 0:
            print("⚠️  No hay tokens de restablecimiento")
        elif len(valid_tokens) == 0:
            print("⚠️  No hay tokens válidos (todos expirados o usados)")
        else:
            print("✅ Hay tokens válidos disponibles")
        
        print(f"\n🌐 ACCESO A LA APLICACIÓN:")
        print("=" * 30)
        print(f"🔗 URL: https://guia.papyrus.com.co")
        print(f"🔗 Forgot Password: https://guia.papyrus.com.co/forgot-password")
        
        print(f"\n✅ VERIFICACIÓN COMPLETADA!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Verificación exitosa!")
    else:
        print("\n❌ Error en la verificación")
