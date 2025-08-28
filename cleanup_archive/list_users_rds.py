#!/usr/bin/env python3
"""
Script para listar todos los usuarios en la base de datos AWS RDS
"""

import sys
from sqlalchemy import create_engine, text

def main():
    try:
        print("👥 ========================================")
        print("👥 USUARIOS EN LA BASE DE DATOS AWS RDS")
        print("👥 PAQUETES EL CLUB v3.1")
        print("👥 ========================================")
        print("")
        
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos AWS RDS...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a AWS RDS establecida")
        
        print("\n📋 LISTANDO TODOS LOS USUARIOS:")
        print("=" * 50)
        
        with engine.connect() as conn:
            # Contar total de usuarios
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            total_users = result.fetchone()[0]
            print(f"📊 Total de usuarios en RDS: {total_users}")
            print("")
            
            if total_users > 0:
                # Obtener todos los usuarios con detalles completos
                result = conn.execute(text("""
                    SELECT 
                        id,
                        username,
                        email,
                        first_name,
                        last_name,
                        phone,
                        is_active,
                        role,
                        created_at,
                        updated_at,
                        last_login
                    FROM users 
                    ORDER BY created_at DESC
                """))
                
                users = result.fetchall()
                
                for i, user in enumerate(users, 1):
                    user_id, username, email, first_name, last_name, phone, is_active, role, created_at, updated_at, last_login = user
                    
                    print(f"👤 USUARIO #{i}:")
                    print(f"   🆔 ID: {user_id}")
                    print(f"   👤 Username: {username}")
                    print(f"   📧 Email: {email}")
                    print(f"   👨‍💼 Nombre: {first_name} {last_name}")
                    print(f"   📱 Teléfono: {phone if phone else 'No especificado'}")
                    print(f"   🔐 Rol: {role}")
                    print(f"   ✅ Estado: {'🟢 Activo' if is_active else '🔴 Inactivo'}")
                    print(f"   📅 Creado: {created_at}")
                    print(f"   🔄 Actualizado: {updated_at}")
                    print(f"   🕐 Último login: {last_login if last_login else 'Nunca'}")
                    print("-" * 40)
            else:
                print("❌ No se encontraron usuarios en la base de datos")
        
        print(f"\n🌐 ACCESO A LA APLICACIÓN:")
        print("=" * 30)
        print(f"🔗 URL: https://guia.papyrus.com.co")
        print(f"🔗 Health Check: https://guia.papyrus.com.co/health")
        
        if total_users > 0:
            print(f"\n🔐 CREDENCIALES DE ACCESO:")
            print("=" * 30)
            print(f"👤 Usuario: jveyes")
            print(f"📧 Email: jveyes@gmail.com")
            print(f"🔑 Contraseña: (la misma del sistema local)")
        
        print(f"\n✅ LISTADO COMPLETADO!")
        print(f"📊 Total de usuarios encontrados: {total_users}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Listado exitoso!")
    else:
        print("\n❌ Error en el listado")
