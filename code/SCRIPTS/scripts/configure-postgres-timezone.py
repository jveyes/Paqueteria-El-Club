#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Configuración de Zona Horaria en PostgreSQL RDS
# ========================================
# Script para configurar la zona horaria de Colombia en PostgreSQL RDS

import psycopg2
from datetime import datetime
import pytz

# Configuración de la base de datos RDS
DB_CONFIG = {
    'host': 'ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'paqueteria',
    'user': 'jveyes',
    'password': 'a?HC!2.*1#?[==:|289qAI=)#V4kDzl$'
}

def configure_postgres_timezone():
    """Configurar zona horaria de Colombia en PostgreSQL"""
    print("🕐 Configurando zona horaria de Colombia en PostgreSQL RDS")
    print("=" * 60)
    
    try:
        # Conectar a la base de datos
        print("\n🔌 Conectando a PostgreSQL RDS...")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conexión exitosa")
        
        # Verificar configuración actual
        print("\n📋 Configuración actual de PostgreSQL:")
        
        # Verificar timezone actual
        cursor.execute("SHOW timezone;")
        current_timezone = cursor.fetchone()[0]
        print(f"   Timezone actual: {current_timezone}")
        
        # Verificar hora actual del servidor
        cursor.execute("SELECT NOW();")
        server_time = cursor.fetchone()[0]
        print(f"   Hora actual del servidor: {server_time}")
        
        # Verificar si timezone está en la lista de timezones disponibles
        cursor.execute("SELECT name FROM pg_timezone_names WHERE name = 'America/Bogota';")
        timezone_exists = cursor.fetchone()
        
        if timezone_exists:
            print("✅ Timezone 'America/Bogota' está disponible")
        else:
            print("❌ Timezone 'America/Bogota' no está disponible")
            print("   Verificando timezones disponibles...")
            cursor.execute("SELECT name FROM pg_timezone_names WHERE name LIKE '%Bogota%' OR name LIKE '%Colombia%';")
            available_tz = cursor.fetchall()
            if available_tz:
                print(f"   Timezones relacionados disponibles: {[tz[0] for tz in available_tz]}")
            else:
                print("   No se encontraron timezones relacionados")
        
        # Intentar configurar timezone
        print(f"\n🔧 Configurando timezone a 'America/Bogota'...")
        
        # Configurar timezone para la sesión actual
        cursor.execute("SET timezone = 'America/Bogota';")
        
        # Verificar que se aplicó
        cursor.execute("SHOW timezone;")
        new_timezone = cursor.fetchone()[0]
        print(f"   Nuevo timezone: {new_timezone}")
        
        # Verificar hora actual
        cursor.execute("SELECT NOW();")
        new_server_time = cursor.fetchone()[0]
        print(f"   Nueva hora del servidor: {new_server_time}")
        
        # Verificar diferencia horaria
        colombia_tz = pytz.timezone('America/Bogota')
        utc_now = datetime.now(pytz.UTC)
        colombia_now = utc_now.astimezone(colombia_tz)
        
        print(f"\n⏰ Comparación de horarios:")
        print(f"   UTC: {utc_now}")
        print(f"   Colombia: {colombia_now}")
        print(f"   PostgreSQL: {new_server_time}")
        
        # Crear una tabla de prueba para verificar el comportamiento
        print(f"\n🧪 Creando tabla de prueba...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timezone_test (
                id SERIAL PRIMARY KEY,
                utc_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                local_time TIMESTAMP DEFAULT NOW(),
                colombia_time TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'America/Bogota'),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        connection.commit()
        
        # Insertar datos de prueba
        print(f"📝 Insertando datos de prueba...")
        cursor.execute("""
            INSERT INTO timezone_test (utc_time, local_time, colombia_time, created_at)
            VALUES (NOW(), NOW(), NOW() AT TIME ZONE 'America/Bogota', NOW())
            RETURNING id, utc_time, local_time, colombia_time, created_at;
        """)
        
        result = cursor.fetchone()
        print(f"✅ Datos insertados:")
        print(f"   ID: {result[0]}")
        print(f"   UTC Time: {result[1]}")
        print(f"   Local Time: {result[2]}")
        print(f"   Colombia Time: {result[3]}")
        print(f"   Created At: {result[4]}")
        
        # Limpiar datos de prueba
        cursor.execute("DELETE FROM timezone_test;")
        connection.commit()
        print(f"🧹 Datos de prueba eliminados")
        
        cursor.close()
        connection.close()
        
        print(f"\n✅ Configuración completada")
        print(f"   PostgreSQL ahora usa timezone: {new_timezone}")
        
    except Exception as e:
        print(f"❌ Error configurando timezone: {e}")

def test_timezone_behavior():
    """Probar el comportamiento de timezone en diferentes operaciones"""
    print(f"\n🧪 Test de Comportamiento de Timezone")
    print("=" * 50)
    
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Configurar timezone para la sesión
        cursor.execute("SET timezone = 'America/Bogota';")
        
        # Probar diferentes tipos de timestamp
        print(f"\n📊 Probando diferentes tipos de timestamp:")
        
        # 1. TIMESTAMP WITH TIME ZONE (UTC)
        cursor.execute("SELECT NOW() AS utc_timestamp;")
        utc_result = cursor.fetchone()[0]
        print(f"   TIMESTAMP WITH TIME ZONE: {utc_result}")
        
        # 2. TIMESTAMP sin timezone (local)
        cursor.execute("SELECT NOW()::timestamp AS local_timestamp;")
        local_result = cursor.fetchone()[0]
        print(f"   TIMESTAMP local: {local_result}")
        
        # 3. TIMESTAMP convertido a Colombia
        cursor.execute("SELECT NOW() AT TIME ZONE 'America/Bogota' AS colombia_timestamp;")
        colombia_result = cursor.fetchone()[0]
        print(f"   TIMESTAMP Colombia: {colombia_result}")
        
        # 4. Función personalizada
        cursor.execute("""
            SELECT 
                NOW() AS current_utc,
                NOW() AT TIME ZONE 'America/Bogota' AS current_colombia,
                EXTRACT(EPOCH FROM NOW()) AS unix_timestamp
        """)
        test_result = cursor.fetchone()
        print(f"\n📅 Resultados detallados:")
        print(f"   UTC actual: {test_result[0]}")
        print(f"   Colombia actual: {test_result[1]}")
        print(f"   Unix timestamp: {test_result[2]}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error en test de timezone: {e}")

if __name__ == "__main__":
    configure_postgres_timezone()
    test_timezone_behavior()
    print(f"\n🎉 Configuración de timezone completada")
