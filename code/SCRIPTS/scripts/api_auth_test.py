#!/usr/bin/env python3
"""
Script de prueba de autenticación de la API
Solución para endpoints protegidos
"""

import sys
import os
import requests
import json
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.config import settings
    
    class APIAuthTester:
        """Clase para probar autenticación de la API"""
        
        def __init__(self):
            self.base_url = "http://localhost"
            self.session = requests.Session()
            self.auth_token = None
            
        def test_public_endpoints(self):
            """Probar endpoints públicos"""
            print("🌐 PROBANDO ENDPOINTS PÚBLICOS")
            print("=" * 40)
            
            public_endpoints = [
                "/",
                "/announce",
                "/search",
                "/help",
                "/policies",
                "/cookies",
                "/health",
                "/docs"
            ]
            
            for endpoint in public_endpoints:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 200:
                        print(f"✅ {endpoint}: OK")
                    else:
                        print(f"⚠️ {endpoint}: {response.status_code}")
                except Exception as e:
                    print(f"❌ {endpoint}: Error - {e}")
            
            print()
        
        def test_protected_endpoints_without_auth(self):
            """Probar endpoints protegidos sin autenticación"""
            print("🔒 PROBANDO ENDPOINTS PROTEGIDOS SIN AUTH")
            print("=" * 50)
            
            protected_endpoints = [
                "/api/announcements/",
                "/api/packages/",
                "/api/admin/users",
                "/api/messages/",
                "/api/notifications/",
                "/api/profile/api/profile"
            ]
            
            for endpoint in protected_endpoints:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 401:
                        print(f"✅ {endpoint}: Correctamente protegido (401)")
                    elif response.status_code == 403:
                        print(f"✅ {endpoint}: Correctamente protegido (403)")
                    else:
                        print(f"⚠️ {endpoint}: {response.status_code} (esperaba 401/403)")
                except Exception as e:
                    print(f"❌ {endpoint}: Error - {e}")
            
            print()
        
        def test_auth_flow(self):
            """Probar flujo de autenticación"""
            print("🔐 PROBANDO FLUJO DE AUTENTICACIÓN")
            print("=" * 40)
            
            # Datos de prueba (usuario de prueba)
            test_user = {
                "username": "admin@papyrus.com.co",
                "password": "admin123"
            }
            
            try:
                # Intentar login
                print("📝 Intentando login...")
                login_response = self.session.post(
                    f"{self.base_url}/api/auth/login",
                    data=test_user
                )
                
                if login_response.status_code == 200:
                    data = login_response.json()
                    if "access_token" in data:
                        self.auth_token = data["access_token"]
                        print("✅ Login exitoso, token obtenido")
                        
                        # Probar endpoint protegido con token
                        self.test_protected_endpoints_with_auth()
                    else:
                        print("❌ Login exitoso pero no hay token")
                else:
                    print(f"❌ Login falló: {login_response.status_code}")
                    print(f"Respuesta: {login_response.text}")
                    
            except Exception as e:
                print(f"❌ Error en login: {e}")
            
            print()
        
        def test_protected_endpoints_with_auth(self):
            """Probar endpoints protegidos con autenticación"""
            if not self.auth_token:
                print("❌ No hay token de autenticación")
                return
                
            print("🔓 PROBANDO ENDPOINTS PROTEGIDOS CON AUTH")
            print("=" * 50)
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            protected_endpoints = [
                "/api/announcements/",
                "/api/packages/",
                "/api/admin/users",
                "/api/messages/",
                "/api/notifications/"
            ]
            
            for endpoint in protected_endpoints:
                try:
                    response = self.session.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers
                    )
                    if response.status_code == 200:
                        print(f"✅ {endpoint}: Acceso permitido con auth")
                    elif response.status_code == 404:
                        print(f"⚠️ {endpoint}: Endpoint no encontrado (404)")
                    else:
                        print(f"⚠️ {endpoint}: {response.status_code}")
                except Exception as e:
                    print(f"❌ {endpoint}: Error - {e}")
            
            print()
        
        def run_all_tests(self):
            """Ejecutar todas las pruebas"""
            print("🧪 TEST COMPLETO DE AUTENTICACIÓN DE LA API")
            print("=" * 60)
            print()
            
            self.test_public_endpoints()
            self.test_protected_endpoints_without_auth()
            self.test_auth_flow()
            
            print("🏁 TEST DE AUTENTICACIÓN COMPLETADO")
            print("=" * 60)
    
    if __name__ == "__main__":
        tester = APIAuthTester()
        tester.run_all_tests()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de ejecutar desde el directorio raíz del proyecto")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
