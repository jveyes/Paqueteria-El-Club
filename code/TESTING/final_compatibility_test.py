#!/usr/bin/env python3
"""
Script final para verificar que todas las funcionalidades críticas funcionen con AWS RDS
PAQUETES EL CLUB v3.1
"""

import requests
import json
import psycopg2
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001"
AWS_DB_CONFIG = {
    'host': 'ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'paqueteria',
    'user': 'jveyes',
    'password': 'a?HC!2.*1#?[==:|289qAI=)#V4kDzl$'
}

def print_header(title):
    """Imprimir encabezado de sección"""
    print(f"\n{'='*80}")
    print(f"🔍 {title}")
    print(f"{'='*80}")

def print_subheader(title):
    """Imprimir subencabezado"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")

def test_database_connection():
    """Probar conexión a la base de datos"""
    print_subheader("PRUEBA DE CONEXIÓN A BASE DE DATOS")
    
    try:
        conn = psycopg2.connect(**AWS_DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar que podemos hacer consultas básicas
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Conexión exitosa - Usuarios en BD: {user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM packages")
        package_count = cursor.fetchone()[0]
        print(f"✅ Paquetes en BD: {package_count}")
        
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        print(f"✅ Clientes en BD: {customer_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints críticos de la API"""
    print_subheader("PRUEBA DE ENDPOINTS DE LA API")
    
    endpoints_to_test = [
        ("GET", "/health", "Health Check"),
        ("GET", "/docs", "Documentación API"),
        ("POST", "/api/auth/login", "Login (requiere datos)"),
        ("GET", "/api/auth/me", "Usuario actual (requiere auth)"),
    ]
    
    successful_tests = 0
    
    for method, endpoint, description in endpoints_to_test:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}")
            
            if response.status_code in [200, 401, 422]:  # 401/422 son respuestas válidas para endpoints que requieren auth
                print(f"✅ {description}: Status {response.status_code}")
                successful_tests += 1
            else:
                print(f"❌ {description}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    return successful_tests == len(endpoints_to_test)

def test_authentication_flow():
    """Probar flujo completo de autenticación"""
    print_subheader("PRUEBA DE FLUJO DE AUTENTICACIÓN")
    
    try:
        # 1. Login
        login_data = {
            "username": "jveyes",
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            user = data.get("user", {})
            
            print(f"✅ Login exitoso - Usuario: {user.get('username')}")
            print(f"✅ Token generado: {token[:20]}...")
            
            # 2. Verificar token
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
            
            if me_response.status_code == 200:
                me_data = me_response.json()
                print(f"✅ Token válido - Usuario actual: {me_data.get('username')}")
                return True
            else:
                print(f"❌ Token inválido - Status: {me_response.status_code}")
                return False
        else:
            print(f"❌ Login falló - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en flujo de autenticación: {e}")
        return False

def test_password_reset_flow():
    """Probar flujo de recuperación de contraseña"""
    print_subheader("PRUEBA DE RECUPERACIÓN DE CONTRASEÑA")
    
    try:
        # Solicitar restablecimiento
        reset_data = {
            "email": "jveyes@gmail.com"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/request-reset",
            json=reset_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Solicitud de restablecimiento exitosa")
            print(f"✅ Mensaje: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Solicitud de restablecimiento falló - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en flujo de recuperación: {e}")
        return False

def test_database_operations():
    """Probar operaciones básicas de base de datos"""
    print_subheader("PRUEBA DE OPERACIONES DE BASE DE DATOS")
    
    try:
        conn = psycopg2.connect(**AWS_DB_CONFIG)
        cursor = conn.cursor()
        
        # 1. Verificar usuarios
        cursor.execute("SELECT username, email, role FROM users LIMIT 3")
        users = cursor.fetchall()
        print(f"✅ Consulta de usuarios exitosa - {len(users)} usuarios encontrados")
        
        # 2. Verificar paquetes
        cursor.execute("SELECT tracking_number, status FROM packages LIMIT 3")
        packages = cursor.fetchall()
        print(f"✅ Consulta de paquetes exitosa - {len(packages)} paquetes encontrados")
        
        # 3. Verificar clientes
        cursor.execute("SELECT name, phone FROM customers LIMIT 3")
        customers = cursor.fetchall()
        print(f"✅ Consulta de clientes exitosa - {len(customers)} clientes encontrados")
        
        # 4. Verificar tokens de restablecimiento
        cursor.execute("SELECT COUNT(*) FROM password_reset_tokens WHERE is_used = false")
        active_tokens = cursor.fetchone()[0]
        print(f"✅ Tokens activos: {active_tokens}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones de BD: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print_header("VERIFICACIÓN FINAL DE COMPATIBILIDAD CON AWS RDS")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"🗄️  Base de datos: AWS RDS")
    
    tests = [
        ("Conexión a Base de Datos", test_database_connection),
        ("Endpoints de API", test_api_endpoints),
        ("Flujo de Autenticación", test_authentication_flow),
        ("Recuperación de Contraseña", test_password_reset_flow),
        ("Operaciones de Base de Datos", test_database_operations),
    ]
    
    successful_tests = 0
    total_tests = len(tests)
    
    for test_name, test_function in tests:
        print(f"\n🔍 Ejecutando: {test_name}")
        if test_function():
            successful_tests += 1
            print(f"✅ {test_name}: EXITOSO")
        else:
            print(f"❌ {test_name}: FALLÓ")
    
    print_header("RESULTADOS FINALES")
    print(f"✅ Pruebas exitosas: {successful_tests}/{total_tests}")
    print(f"❌ Pruebas fallidas: {total_tests - successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("\n🎉 ¡TODAS LAS FUNCIONALIDADES CRÍTICAS FUNCIONAN CORRECTAMENTE!")
        print("✅ Base de datos AWS RDS completamente operativa")
        print("✅ API funcionando correctamente")
        print("✅ Autenticación funcionando")
        print("✅ Recuperación de contraseña funcionando")
        print("✅ Operaciones de base de datos funcionando")
    else:
        print("\n⚠️  HAY PROBLEMAS QUE NECESITAN ATENCIÓN")
        print("Revisa los errores anteriores para identificar los problemas")
    
    print("\n📋 Credenciales de prueba:")
    print("   👤 Usuario: jveyes")
    print("   📧 Email: jveyes@gmail.com")
    print("   🔑 Contraseña: admin123")

if __name__ == "__main__":
    main()
