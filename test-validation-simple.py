#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAQUETERIA v3.1 - Validación Simplificada
==========================================

Script de validación que funciona sin problemas de imports complejos.
"""

import sys
import os
import subprocess
from datetime import datetime

def test_database_connection():
    """Probar conexión a la base de datos usando el script existente"""
    print("🔍 Probando conexión a la base de datos...")
    
    try:
        # Usar el script existente que ya funciona
        result = subprocess.run(
            ['python3', 'scripts/test-rds-connection.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Conexión a base de datos exitosa")
            return True
        else:
            print(f"❌ Error en conexión: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando script: {e}")
        return False

def test_docker_services():
    """Verificar estado de servicios Docker"""
    print("🔍 Verificando servicios Docker...")
    
    try:
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}\t{{.Status}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            services = result.stdout.strip().split('\n')
            running_services = [s for s in services if 'Up' in s]
            
            expected_services = [
                'paqueteria_v31_app',
                'paqueteria_v31_nginx', 
                'paqueteria_v31_redis'
            ]
            
            missing_services = []
            for service in expected_services:
                if not any(service in s for s in running_services):
                    missing_services.append(service)
            
            if missing_services:
                print(f"❌ Servicios faltantes: {', '.join(missing_services)}")
                return False
            else:
                print(f"✅ Todos los servicios ejecutándose ({len(running_services)} servicios)")
                return True
        else:
            print(f"❌ Error ejecutando Docker: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando Docker: {e}")
        return False

def test_web_endpoints():
    """Probar endpoints web básicos"""
    print("🔍 Probando endpoints web...")
    
    try:
        import requests
        
        endpoints = [
            ('http://localhost/', 'Home Page'),
            ('http://localhost/search', 'Search Page'),
            ('http://localhost/login', 'Login Page')
        ]
        
        failed_endpoints = []
        successful_endpoints = []
        
        for url, name in endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    successful_endpoints.append(f"{name} ({url})")
                else:
                    failed_endpoints.append(f"{name} ({url}) - Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{name} ({url}) - Error: {e}")
        
        if failed_endpoints:
            print(f"❌ Endpoints fallando: {len(failed_endpoints)}")
            for endpoint in failed_endpoints[:3]:  # Mostrar solo los primeros 3
                print(f"   - {endpoint}")
            return False
        else:
            print(f"✅ Todos los endpoints funcionando ({len(successful_endpoints)} endpoints)")
            return True
            
    except ImportError:
        print("⚠️  Requests no disponible, saltando prueba de endpoints")
        return True
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def test_critical_files():
    """Verificar archivos críticos"""
    print("🔍 Verificando archivos críticos...")
    
    critical_files = [
        'code/src/config.py',
        'code/src/main.py',
        'code/alembic.ini',
        'docker-compose-aws-fixed.yml'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos críticos faltantes: {len(missing_files)}")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print(f"✅ Todos los archivos críticos presentes ({len(existing_files)} archivos)")
        return True

def run_complete_validation():
    """Ejecutar validación completa"""
    print("🛡️  VALIDACIÓN SIMPLIFICADA DEL SISTEMA")
    print("=" * 50)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Conexión a Base de Datos", test_database_connection),
        ("Servicios Docker", test_docker_services),
        ("Endpoints Web", test_web_endpoints),
        ("Archivos Críticos", test_critical_files)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Generar reporte
    print("\n" + "=" * 50)
    print("📊 REPORTE DE VALIDACIÓN")
    print("=" * 50)
    
    total_tests = len(results)
    successful_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - successful_tests
    
    print(f"📈 Resumen General:")
    print(f"   - Total de pruebas: {total_tests}")
    print(f"   - Pruebas exitosas: {successful_tests}")
    print(f"   - Pruebas fallidas: {failed_tests}")
    
    if failed_tests > 0:
        print(f"\n⚠️  PRUEBAS FALLIDAS:")
        for test_name, success in results:
            if not success:
                print(f"   🔴 {test_name}")
        
        print(f"\n💡 RECOMENDACIONES:")
        print("   1. Revisar logs de Docker: docker logs paqueteria_v31_app")
        print("   2. Verificar conectividad a AWS RDS")
        print("   3. Revisar configuración del entorno")
        print("   4. Ejecutar: docker-compose restart")
        
        return False
    else:
        print(f"\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ El sistema está funcionando correctamente")
        return True

def main():
    """Función principal"""
    try:
        success = run_complete_validation()
        if success:
            print("\n🎉 ¡Validación completada exitosamente!")
            sys.exit(0)
        else:
            print("\n⚠️  Se encontraron problemas que requieren atención")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error durante la validación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
