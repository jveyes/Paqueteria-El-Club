#!/usr/bin/env python3
"""
Script para consultar usuarios directamente en la base de datos AWS
"""

import sys
from sqlalchemy import create_engine, text

def main():
    try:
        # URL de la base de datos AWS directamente
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos AWS...")
        engine = create_engine(database_url)
        
        # Consultar tablas existentes primero
        print("📋 Consultando tablas existentes...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            
            tables = result.fetchall()
            
            if not tables:
                print("⚠️  No se encontraron tablas en la base de datos")
                return
            
            print(f"\n✅ Se encontraron {len(tables)} tablas:")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Verificar si existe la tabla users
            table_names = [table[0] for table in tables]
            if 'users' not in table_names:
                print("\n❌ La tabla 'users' no existe")
                return
            
            # Consultar usuarios
            print("\n📋 Consultando usuarios...")
            result = conn.execute(text("""
                SELECT 
                    id, 
                    username, 
                    email, 
                    first_name, 
                    last_name, 
                    role, 
                    is_active, 
                    created_at 
                FROM users 
                ORDER BY id
            """))
            
            users = result.fetchall()
            
            if not users:
                print("⚠️  No se encontraron usuarios en la tabla")
                return
            
            print(f"\n✅ Se encontraron {len(users)} usuarios:")
            print("=" * 80)
            print(f"{'ID':<4} {'Usuario':<15} {'Email':<25} {'Nombre':<20} {'Rol':<12} {'Activo':<8} {'Creado'}")
            print("=" * 80)
            
            for user in users:
                id_user, username, email, first_name, last_name, role, is_active, created_at = user
                full_name = f"{first_name or ''} {last_name or ''}".strip()
                active_status = "✅ Sí" if is_active else "❌ No"
                created_str = str(created_at)[:19] if created_at else "N/A"
                
                print(f"{id_user:<4} {username:<15} {email:<25} {full_name:<20} {role:<12} {active_status:<8} {created_str}")
            
            print("=" * 80)
            
            # Resumen por roles
            print("\n📊 Resumen por roles:")
            role_counts = {}
            for user in users:
                role = user[5]  # role column
                role_counts[role] = role_counts.get(role, 0) + 1
            
            for role, count in role_counts.items():
                print(f"   - {role}: {count} usuarios")
            
            # Usuarios activos vs inactivos
            active_count = sum(1 for user in users if user[6])  # is_active column
            inactive_count = len(users) - active_count
            print(f"\n👥 Estado de usuarios:")
            print(f"   - Activos: {active_count}")
            print(f"   - Inactivos: {inactive_count}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
