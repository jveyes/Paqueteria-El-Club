#!/usr/bin/env python3
"""
Script para verificar qué tablas existen en la base de datos
"""

import os
import sys
from sqlalchemy import create_engine, text

def main():
    try:
        # Obtener la URL de la base de datos desde las variables de entorno
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ Error: DATABASE_URL no está configurada")
            sys.exit(1)
        
        print("🔍 Conectando a la base de datos...")
        engine = create_engine(database_url)
        
        # Consultar tablas existentes
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
            print("=" * 50)
            for table in tables:
                print(f"   - {table[0]}")
            print("=" * 50)
            
            # Verificar tablas específicas que deberían existir
            expected_tables = ['users', 'customers', 'packages', 'package_announcements', 'notifications', 'rates', 'files', 'messages', 'password_reset_tokens']
            
            print("\n🔍 Verificando tablas esperadas:")
            for expected_table in expected_tables:
                if any(table[0] == expected_table for table in tables):
                    print(f"   ✅ {expected_table}")
                else:
                    print(f"   ❌ {expected_table} - NO EXISTE")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
