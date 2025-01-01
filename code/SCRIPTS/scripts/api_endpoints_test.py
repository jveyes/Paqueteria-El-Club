#!/usr/bin/env python3
"""
Script de prueba de endpoints de la API
Solución para verificar funcionalidad completa
"""

import sys
import os
import requests
import json
from pathlib import Path
from urllib.parse import urljoin

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.config import settings
    
    class APIEndpointsTester:
        """Clase para probar todos los endpoints de la API"""
        
        def __init__(self):
            self.base_url = "http://localhost"
            self.session = requests.Session()
            self.auth_token = None
            self.test_results = []
            
        def test_endpoint(self, endpoint, method="GET", expected_status=200, 
                         data=None, headers=None, description=""):
            """Probar un endpoint específico"""
            url = urljoin(self.base_url, endpoint)
            
            try:
                if method.upper() == "GET":
                    response = self.session.get(url, headers=headers)
                elif method.upper() == "POST":
                    response = self.session.post(url, json=data, headers=headers)
                elif method.upper() == "PUT":
                    response = self.session.put(url, json=data, headers=headers)
                elif method.upper() == "DELETE":
                    response = self.session.delete(url, headers=headers)
                else:
                    print(f"❌ Método HTTP no soportado: {method}")
                    return False
                
                # Verificar respuesta
                if response.status_code == expected_status:
                    status_icon = "✅"
                    result = "PASÓ"
                else:
                    status_icon = "⚠️"
                    result = f"FALLÓ (esperaba {expected_status}, obtuvo {response.status_code})"
                
                # Mostrar resultado
                print(f"{status_icon} {endpoint}: {result}")
                if description:
                    print(f"   📝 {description}")
                
                # Guardar resultado
                self.test_results.append({
                    'endpoint': endpoint,
                    'method': method,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'passed': response.status_code == expected_status,
                    'description': description
                })
                
                return response.status_code == expected_status
                
            except Exception as e:
                print(f"❌ {endpoint}: Error - {e}")
                self.test_results.append({
                    'endpoint': endpoint,
                    'method': method,
                    'expected': expected_status,
                    'actual': 'ERROR',
                    'passed': False,
                    'description': description,
                    'error': str(e)
                })
                return False
        
        def test_public_endpoints(self):
            """Probar endpoints públicos"""
            print("🌐 PROBANDO ENDPOINTS PÚBLICOS")
            print("=" * 50)
            
            public_endpoints = [
                ("/", "GET", 200, None, None, "Página principal"),
                ("/announce", "GET", 200, None, None, "Formulario de anuncio"),
                ("/search", "GET", 200, None, None, "Búsqueda de paquetes"),
                ("/help", "GET", 200, None, None, "Página de ayuda"),
                ("/policies", "GET", 200, None, None, "Políticas del servicio"),
                ("/cookies", "GET", 200, None, None, "Política de cookies"),
                ("/health", "GET", 200, None, None, "Health check"),
                ("/docs", "GET", 200, None, None, "Documentación Swagger"),
                ("/openapi.json", "GET", 200, None, None, "Esquema OpenAPI"),
                ("/static/images/logo.png", "GET", 200, None, None, "Logo estático"),
                ("/assets/css/custom.css", "GET", 200, None, None, "CSS personalizado")
            ]
            
            for endpoint, method, expected, data, headers, desc in public_endpoints:
                self.test_endpoint(endpoint, method, expected, data, headers, desc)
            
            print()
        
        def test_protected_endpoints_without_auth(self):
            """Probar endpoints protegidos sin autenticación"""
            print("🔒 PROBANDO ENDPOINTS PROTEGIDOS SIN AUTENTICACIÓN")
            print("=" * 60)
            
            protected_endpoints = [
                ("/api/announcements/", "GET", 401, None, None, "Lista de anuncios"),
                ("/api/packages/", "GET", 401, None, None, "Lista de paquetes"),
                ("/api/admin/users", "GET", 401, None, None, "Usuarios admin"),
                ("/api/messages/", "GET", 401, None, None, "Mensajes"),
                ("/api/notifications/", "GET", 401, None, None, "Notificaciones"),
                ("/api/profile/api/profile", "GET", 401, None, None, "Perfil de usuario"),
                ("/api/auth/me", "GET", 401, None, None, "Usuario actual"),
                ("/api/packages/announce", "POST", 401, None, None, "Anunciar paquete")
            ]
            
            for endpoint, method, expected, data, headers, desc in protected_endpoints:
                self.test_endpoint(endpoint, method, expected, data, headers, desc)
            
            print()
        
        def test_auth_endpoints(self):
            """Probar endpoints de autenticación"""
            print("🔐 PROBANDO ENDPOINTS DE AUTENTICACIÓN")
            print("=" * 50)
            
            # Probar registro (puede fallar si el usuario ya existe)
            register_data = {
                "username": "test_user@example.com",
                "password": "test123456",
                "full_name": "Usuario de Prueba"
            }
            
            auth_endpoints = [
                ("/api/auth/register", "POST", 200, register_data, None, "Registro de usuario"),
                ("/api/auth/check", "GET", 200, None, None, "Verificar estado de auth")
            ]
            
            for endpoint, method, expected, data, headers, desc in auth_endpoints:
                self.test_endpoint(endpoint, method, expected, data, headers, desc)
            
            print()
        
        def test_search_endpoints(self):
            """Probar endpoints de búsqueda"""
            print("🔍 PROBANDO ENDPOINTS DE BÚSQUEDA")
            print("=" * 50)
            
            # Estos endpoints pueden ser públicos o protegidos
            search_endpoints = [
                ("/api/announcements/search/package", "GET", 200, None, None, "Búsqueda de paquetes"),
                ("/api/announcements/tracking/TEST123", "GET", 200, None, None, "Tracking por código"),
                ("/api/announcements/guide/TEST123", "GET", 200, None, None, "Búsqueda por guía")
            ]
            
            for endpoint, method, expected, data, headers, desc in search_endpoints:
                self.test_endpoint(endpoint, method, expected, data, headers, desc)
            
            print()
        
        def test_rate_limit_endpoints(self):
            """Probar endpoints de rate limiting"""
            print("⏱️ PROBANDO ENDPOINTS DE RATE LIMITING")
            print("=" * 50)
            
            rate_limit_endpoints = [
                ("/api/announcements/rate-limit/info", "GET", 200, None, None, "Info de rate limit"),
                ("/api/announcements/rate-limit/reset", "POST", 200, None, None, "Reset de rate limit")
            ]
            
            for endpoint, method, expected, data, headers, desc in rate_limit_endpoints:
                self.test_endpoint(endpoint, method, expected, data, headers, desc)
            
            print()
        
        def generate_report(self):
            """Generar reporte de las pruebas"""
            print("📊 REPORTE DE PRUEBAS DE ENDPOINTS")
            print("=" * 60)
            
            total_tests = len(self.test_results)
            passed_tests = sum(1 for result in self.test_results if result['passed'])
            failed_tests = total_tests - passed_tests
            
            print(f"📈 Total de pruebas: {total_tests}")
            print(f"✅ Pruebas exitosas: {passed_tests}")
            print(f"❌ Pruebas fallidas: {failed_tests}")
            print(f"📊 Porcentaje de éxito: {(passed_tests/total_tests)*100:.1f}%")
            
            if failed_tests > 0:
                print("\n⚠️ ENDPOINTS CON PROBLEMAS:")
                for result in self.test_results:
                    if not result['passed']:
                        print(f"   • {result['endpoint']} ({result['method']}): {result['actual']}")
                        if 'error' in result:
                            print(f"     Error: {result['error']}")
            
            print("\n🎯 RECOMENDACIONES:")
            if passed_tests == total_tests:
                print("   🎉 ¡Todos los endpoints están funcionando correctamente!")
            elif passed_tests >= total_tests * 0.8:
                print("   ✅ La mayoría de endpoints funcionan bien")
                print("   🔧 Revisar los endpoints que fallaron")
            else:
                print("   ⚠️ Muchos endpoints tienen problemas")
                print("   🚨 Revisar la configuración del servidor")
            
            return passed_tests == total_tests
        
        def run_all_tests(self):
            """Ejecutar todas las pruebas"""
            print("🚀 INICIANDO PRUEBAS COMPLETAS DE ENDPOINTS DE LA API")
            print("=" * 70)
            print()
            
            # Ejecutar todas las pruebas
            self.test_public_endpoints()
            self.test_protected_endpoints_without_auth()
            self.test_auth_endpoints()
            self.test_search_endpoints()
            self.test_rate_limit_endpoints()
            
            # Generar reporte
            print("=" * 70)
            success = self.generate_report()
            
            print("\n🏁 PRUEBAS DE ENDPOINTS COMPLETADAS")
            print("=" * 70)
            
            return success
    
    if __name__ == "__main__":
        tester = APIEndpointsTester()
        tester.run_all_tests()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de ejecutar desde el directorio raíz del proyecto")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
