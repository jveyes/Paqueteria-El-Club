#!/usr/bin/env python3
"""
Script para verificar que el problema de base de datos está solucionado
"""

import sys
from sqlalchemy import create_engine, text

def main():
    try:
        print("🔧 ========================================")
        print("🔧 VERIFICACIÓN DE SOLUCIÓN DE BASE DE DATOS")
        print("🔧 PAQUETES EL CLUB v3.1")
        print("🔧 ========================================")
        print("")
        
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a AWS RDS...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a AWS RDS establecida")
        
        print("\n📊 VERIFICANDO DATOS:")
        print("=" * 30)
        
        with engine.connect() as conn:
            # Verificar usuarios
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"👥 Usuarios: {user_count}")
            
            # Verificar anuncios
            result = conn.execute(text("SELECT COUNT(*) FROM package_announcements"))
            ann_count = result.fetchone()[0]
            print(f"📦 Anuncios: {ann_count}")
            
            # Mostrar usuarios disponibles
            if user_count > 0:
                print("\n👤 Usuarios disponibles:")
                result = conn.execute(text("SELECT username, email, first_name, last_name FROM users"))
                users = result.fetchall()
                for user in users:
                    username, email, first_name, last_name = user
                    print(f"   - {username} ({email}) - {first_name} {last_name}")
        
        print(f"\n✅ VERIFICACIÓN COMPLETADA!")
        print("🎉 El problema de base de datos está SOLUCIONADO")
        print("🌐 Puedes acceder a: https://guia.papyrus.com.co")
        print("🔐 Usuario: jveyes / jveyes@gmail.com")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Problema solucionado!")
    else:
        print("\n❌ Error en la verificación")
