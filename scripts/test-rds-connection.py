#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAQUETERIA v3.1 - Prueba de Conexión a AWS RDS
===============================================

Script para probar la conectividad a la base de datos AWS RDS.
"""

import sys
import os
import psycopg2
from datetime import datetime

# Configuración de la base de datos AWS RDS
DB_CONFIG = {
    'host': 'ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'paqueteria',
    'user': 'jveyes',
    'password': 'a?HC!2.*1#?[==:|289qAI=)#V4kDzl$'
}

def test_connection():
    """Probar conexión básica a la base de datos"""
    try:
        print("🔌 Probando conexión a AWS RDS...")
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a AWS RDS")
        
        # Probar consulta básica
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"📊 Versión de PostgreSQL: {version}")
        
        # Probar consulta de tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tablas encontradas: {len(tables)}")
        
        if tables:
            print("   Tablas principales:")
            for table in tables[:5]:  # Mostrar solo las primeras 5
                print(f"   - {table}")
            if len(tables) > 5:
                print(f"   ... y {len(tables) - 5} más")
        
        # Probar consulta de usuarios
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"👥 Usuarios en la base de datos: {user_count}")
        
        # Probar consulta de paquetes
        cursor.execute("SELECT COUNT(*) FROM packages;")
        package_count = cursor.fetchone()[0]
        print(f"📦 Paquetes en la base de datos: {package_count}")
        
        # Verificar columnas críticas
        print("\n🔍 Verificando columnas críticas...")
        
        critical_checks = [
            ("users", "profile_photo"),
            ("packages", "tracking_code"),
            ("customers", "phone")
        ]
        
        for table, column in critical_checks:
            try:
                cursor.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' AND column_name = '{column}'
                """)
                result = cursor.fetchone()
                
                if result:
                    print(f"   ✅ {table}.{column}: {result[1]}")
                else:
                    print(f"   ❌ {table}.{column}: NO EXISTE")
            except Exception as e:
                print(f"   ⚠️  {table}.{column}: Error verificando - {e}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Prueba de conexión completada exitosamente")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🛡️  PRUEBA DE CONEXIÓN A AWS RDS")
    print("=" * 50)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if test_connection():
        print("\n✅ La base de datos está funcionando correctamente")
        sys.exit(0)
    else:
        print("\n❌ Problemas de conectividad detectados")
        sys.exit(1)

if __name__ == "__main__":
    main()
