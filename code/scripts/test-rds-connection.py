#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test de Conexión RDS
# ========================================
# Script para verificar la conexión a la base de datos RDS de AWS

import sys
import os
import psycopg2
from datetime import datetime

# Configuración de la base de datos RDS
DB_CONFIG = {
    'host': 'ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'paqueteria',
    'user': 'jveyes',
    'password': 'a?HC!2.*1#?[==:|289qAI=)#V4kDzl$'
}

def test_rds_connection():
    """Probar la conexión a la base de datos RDS"""
    print("🗄️ Test de Conexión RDS AWS")
    print("=" * 50)
    
    print(f"\n📋 Configuración:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Puerto: {DB_CONFIG['port']}")
    print(f"   Base de datos: {DB_CONFIG['database']}")
    print(f"   Usuario: {DB_CONFIG['user']}")
    
    try:
        print(f"\n🔌 Conectando a RDS...")
        connection = psycopg2.connect(**DB_CONFIG)
        
        if connection:
            print("✅ Conexión exitosa a RDS")
            
            # Crear cursor
            cursor = connection.cursor()
            
            # Test 1: Verificar versión de PostgreSQL
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"\n📊 Versión de PostgreSQL:")
            print(f"   {version[0]}")
            
            # Test 2: Verificar tablas existentes
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            print(f"\n📋 Tablas existentes:")
            if tables:
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("   No hay tablas en la base de datos")
            
            # Test 3: Verificar zona horaria del servidor
            cursor.execute("SHOW timezone;")
            timezone = cursor.fetchone()
            print(f"\n🕐 Zona horaria del servidor:")
            print(f"   {timezone[0]}")
            
            # Test 4: Verificar hora actual del servidor
            cursor.execute("SELECT NOW();")
            server_time = cursor.fetchone()
            print(f"\n⏰ Hora actual del servidor:")
            print(f"   {server_time[0]}")
            
            # Test 5: Verificar conexiones activas
            cursor.execute("SELECT count(*) FROM pg_stat_activity;")
            active_connections = cursor.fetchone()
            print(f"\n🔗 Conexiones activas:")
            print(f"   {active_connections[0]}")
            
            # Cerrar conexión
            cursor.close()
            connection.close()
            print(f"\n✅ Conexión cerrada correctamente")
            
        else:
            print("❌ No se pudo establecer la conexión")
            
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        print(f"\n🔍 Posibles causas:")
        print(f"   - El servidor RDS no está disponible")
        print(f"   - Credenciales incorrectas")
        print(f"   - Firewall bloqueando la conexión")
        print(f"   - Grupo de seguridad no permite conexiones desde esta IP")
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_database_operations():
    """Probar operaciones básicas en la base de datos"""
    print(f"\n🧪 Test de Operaciones de Base de Datos")
    print("=" * 50)
    
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Test 1: Crear tabla de prueba
        print(f"\n📝 Creando tabla de prueba...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_connection (
                id SERIAL PRIMARY KEY,
                test_message VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        connection.commit()
        print("✅ Tabla de prueba creada")
        
        # Test 2: Insertar datos
        print(f"\n📤 Insertando datos de prueba...")
        cursor.execute("""
            INSERT INTO test_connection (test_message) 
            VALUES (%s) 
            RETURNING id, test_message, created_at;
        """, (f"Test desde localhost - {datetime.now()}",))
        
        result = cursor.fetchone()
        print(f"✅ Datos insertados:")
        print(f"   ID: {result[0]}")
        print(f"   Mensaje: {result[1]}")
        print(f"   Creado: {result[2]}")
        
        # Test 3: Consultar datos
        print(f"\n📥 Consultando datos...")
        cursor.execute("SELECT COUNT(*) FROM test_connection;")
        count = cursor.fetchone()
        print(f"✅ Total de registros en tabla de prueba: {count[0]}")
        
        # Test 4: Limpiar datos de prueba
        print(f"\n🧹 Limpiando datos de prueba...")
        cursor.execute("DELETE FROM test_connection;")
        connection.commit()
        print("✅ Datos de prueba eliminados")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error en operaciones: {e}")

if __name__ == "__main__":
    test_rds_connection()
    test_database_operations()
    print(f"\n�� Test completado")
