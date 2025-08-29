#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Verificar Estructura de Tablas
# ========================================
# Script para verificar la estructura de las tablas en la base de datos

import psycopg2

# Configuración de la base de datos RDS
DB_CONFIG = {
    'host': 'ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'paqueteria',
    'user': 'jveyes',
    'password': 'a?HC!2.*1#?[==:|289qAI=)#V4kDzl$'
}

def check_table_structure():
    """Verificar la estructura de las tablas"""
    print("📋 Verificando Estructura de Tablas")
    print("=" * 50)
    
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Configurar timezone
        cursor.execute("SET timezone = 'America/Bogota';")
        
        # Verificar estructura de la tabla customers
        print(f"\n👥 Estructura de la tabla 'customers':")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'customers'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        
        # Verificar estructura de la tabla packages
        print(f"\n📦 Estructura de la tabla 'packages':")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'packages'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        
        # Verificar estructura de la tabla users
        print(f"\n👤 Estructura de la tabla 'users':")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        
        # Verificar timezone actual
        print(f"\n🕐 Configuración de Timezone:")
        cursor.execute("SHOW timezone;")
        timezone = cursor.fetchone()[0]
        print(f"   Timezone actual: {timezone}")
        
        cursor.execute("SELECT NOW();")
        current_time = cursor.fetchone()[0]
        print(f"   Hora actual: {current_time}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")

if __name__ == "__main__":
    check_table_structure()
