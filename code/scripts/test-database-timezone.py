#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test de Timezone en Base de Datos
# ========================================
# Script para verificar que las fechas se guarden en hora de Colombia

import requests
import json
from datetime import datetime
import pytz

# Configuración
APP_URL = "http://localhost:8001"

def test_package_creation():
    """Probar la creación de un paquete y verificar las fechas"""
    print("📦 Test de Creación de Paquete con Timezone")
    print("=" * 50)
    
    # Datos del paquete de prueba
    package_data = {
        "customer_name": "TEST TIMEZONE",
        "customer_phone": "3001234567",
        "package_type": "normal",
        "package_condition": "bueno",
        "observations": "Test de timezone - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"\n📤 Creando paquete de prueba...")
    print(f"   Datos: {package_data}")
    
    try:
        # Crear paquete usando la API
        response = requests.post(
            f"{APP_URL}/api/packages/announce",
            json=package_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            package = response.json()
            print(f"✅ Paquete creado exitosamente")
            print(f"   Tracking Number: {package.get('tracking_number')}")
            print(f"   Status: {package.get('status')}")
            
            # Verificar fechas
            print(f"\n📅 Verificando fechas:")
            
            # Fecha de anuncio
            announced_at = package.get('announced_at')
            if announced_at:
                print(f"   Announced At: {announced_at}")
                
                # Convertir a datetime para verificar
                try:
                    dt = datetime.fromisoformat(announced_at.replace('Z', '+00:00'))
                    colombia_tz = pytz.timezone('America/Bogota')
                    colombia_time = dt.astimezone(colombia_tz)
                    print(f"   Colombia Time: {colombia_time}")
                    
                    # Verificar si está en hora de Colombia
                    current_colombia = datetime.now(colombia_tz)
                    time_diff = abs((colombia_time - current_colombia).total_seconds())
                    
                    if time_diff < 60:  # Diferencia menor a 1 minuto
                        print(f"   ✅ Fecha en hora de Colombia (diferencia: {time_diff:.1f}s)")
                    else:
                        print(f"   ❌ Fecha no está en hora de Colombia (diferencia: {time_diff:.1f}s)")
                        
                except Exception as e:
                    print(f"   ❌ Error procesando fecha: {e}")
            
            # Fechas de creación y actualización
            created_at = package.get('created_at')
            updated_at = package.get('updated_at')
            
            if created_at:
                print(f"   Created At: {created_at}")
            if updated_at:
                print(f"   Updated At: {updated_at}")
            
            return package.get('tracking_number')
            
        else:
            print(f"❌ Error creando paquete: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return None

def test_database_direct_query():
    """Consultar directamente la base de datos para verificar fechas"""
    print(f"\n🗄️ Consulta Directa a Base de Datos")
    print("=" * 50)
    
    try:
        import psycopg2
        
        # Configuración de la base de datos RDS
        DB_CONFIG = {
            'host': 'ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com',
            'port': 5432,
            'database': 'paqueteria',
            'user': 'jveyes',
            'password': 'a?HC!2.*1#?[==:|289qAI=)#V4kDzl$'
        }
        
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Configurar timezone para la consulta
        cursor.execute("SET timezone = 'America/Bogota';")
        
        # Consultar el último paquete creado
        cursor.execute("""
            SELECT 
                tracking_number,
                customer_name,
                announced_at,
                created_at,
                updated_at,
                NOW() as current_time,
                NOW() AT TIME ZONE 'America/Bogota' as colombia_time
            FROM packages 
            WHERE customer_name LIKE '%TEST TIMEZONE%'
            ORDER BY created_at DESC 
            LIMIT 1;
        """)
        
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Paquete encontrado en base de datos:")
            print(f"   Tracking: {result[0]}")
            print(f"   Customer: {result[1]}")
            print(f"   Announced At: {result[2]}")
            print(f"   Created At: {result[3]}")
            print(f"   Updated At: {result[4]}")
            print(f"   Current Time (DB): {result[5]}")
            print(f"   Colombia Time (DB): {result[6]}")
            
            # Verificar si las fechas están en hora de Colombia
            colombia_tz = pytz.timezone('America/Bogota')
            current_colombia = datetime.now(colombia_tz)
            
            if result[2]:  # announced_at
                announced_dt = result[2]
                if hasattr(announced_dt, 'tzinfo') and announced_dt.tzinfo:
                    announced_colombia = announced_dt.astimezone(colombia_tz)
                else:
                    announced_colombia = announced_dt
                
                time_diff = abs((announced_colombia - current_colombia).total_seconds())
                print(f"\n⏰ Verificación de timezone:")
                print(f"   Hora actual Colombia: {current_colombia}")
                print(f"   Hora anunciado: {announced_colombia}")
                print(f"   Diferencia: {time_diff:.1f} segundos")
                
                if time_diff < 300:  # Diferencia menor a 5 minutos
                    print(f"   ✅ Fechas están en hora de Colombia")
                else:
                    print(f"   ❌ Fechas NO están en hora de Colombia")
        else:
            print(f"❌ No se encontraron paquetes de prueba")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error consultando base de datos: {e}")

def main():
    """Función principal"""
    print("🧪 Test de Timezone en Base de Datos")
    print("=" * 60)
    
    # Test 1: Crear paquete
    tracking_number = test_package_creation()
    
    if tracking_number:
        # Test 2: Consultar base de datos directamente
        test_database_direct_query()
    
    print(f"\n🎉 Test completado")

if __name__ == "__main__":
    main()
