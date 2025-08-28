#!/usr/bin/env python3
"""
Script para crear la base de datos en AWS RDS (versión corregida)
"""

import sys
from sqlalchemy import create_engine, text

def main():
    try:
        # URL de la base de datos postgres (por defecto)
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/postgres"
        
        print("🔍 Conectando a la base de datos postgres...")
        engine = create_engine(database_url)
        
        # Verificar bases de datos existentes
        print("📋 Verificando bases de datos existentes...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
            databases = result.fetchall()
            
            print("Bases de datos existentes:")
            for db in databases:
                print(f"   - {db[0]}")
            
            # Verificar si paqueteria ya existe
            db_names = [db[0] for db in databases]
            if 'paqueteria' in db_names:
                print("\n✅ La base de datos 'paqueteria' ya existe")
                return
        
        # Crear la base de datos usando autocommit
        print("\n🔧 Creando base de datos 'paqueteria'...")
        engine_autocommit = create_engine(database_url, isolation_level='AUTOCOMMIT')
        with engine_autocommit.connect() as conn:
            conn.execute(text("CREATE DATABASE paqueteria;"))
            print("✅ Base de datos 'paqueteria' creada exitosamente")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
