#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test Dashboard Directo
# ========================================

import sys
import os
import requests
import json
from datetime import datetime

def test_dashboard_direct():
    """Probar el dashboard directamente"""
    print("🎯 PROBANDO DASHBOARD DIRECTO")
    print("=" * 50)
    
    # URL del dashboard
    dashboard_url = "http://localhost:8001/dashboard"
    
    try:
        # Hacer request al dashboard
        print(f"📡 Haciendo request a: {dashboard_url}")
        response = requests.get(dashboard_url, allow_redirects=False)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Headers: {dict(response.headers)}")
        
        if response.status_code == 302:
            print("🔄 Redirigiendo a login...")
            redirect_url = response.headers.get('location', '')
            print(f"📍 URL de redirección: {redirect_url}")
            
            # Probar el login
            login_url = "http://localhost:8001/api/auth/login"
            login_data = {
                "username": "admin_test",
                "password": "admin123"
            }
            
            print(f"\n🔐 Probando login en: {login_url}")
            login_response = requests.post(
                login_url,
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            print(f"📊 Login Status: {login_response.status_code}")
            print(f"📊 Login Response: {login_response.text}")
            
            if login_response.status_code == 200:
                # Obtener el token
                token_data = login_response.json()
                access_token = token_data.get('access_token')
                
                if access_token:
                    print(f"✅ Token obtenido: {access_token[:20]}...")
                    
                    # Probar dashboard con token
                    headers = {"Authorization": f"Bearer {access_token}"}
                    dashboard_response = requests.get(dashboard_url, headers=headers)
                    
                    print(f"\n📊 Dashboard con token - Status: {dashboard_response.status_code}")
                    
                    if dashboard_response.status_code == 200:
                        print("✅ Dashboard accesible con token")
                        # Buscar datos en el HTML
                        content = dashboard_response.text
                        
                        # Guardar el HTML en un archivo para inspección
                        with open("dashboard_content.html", "w", encoding="utf-8") as f:
                            f.write(content)
                        print("💾 HTML guardado en dashboard_content.html")
                        
                        # Buscar estadísticas
                        stats_indicators = [
                            "Total Paquetes",
                            "Pendientes", 
                            "Entregados",
                            "Total Clientes",
                            "Total Anuncios",
                            "Anuncios Pendientes",
                            "Anuncios Procesados"
                        ]
                        
                        print("\n📈 Buscando estadísticas en el HTML:")
                        for indicator in stats_indicators:
                            if indicator in content:
                                print(f"   ✅ {indicator}: Encontrado")
                            else:
                                print(f"   ❌ {indicator}: No encontrado")
                        
                        # Buscar números específicos
                        if "6" in content:
                            print("   ✅ Número 6 (paquetes) encontrado")
                        if "5" in content:
                            print("   ✅ Número 5 (clientes) encontrado")
                        if "9" in content:
                            print("   ✅ Número 9 (anuncios) encontrado")
                        
                        # Mostrar fragmento del contenido
                        print(f"\n📄 Fragmento del contenido HTML:")
                        print(content[:1000])
                        
                    else:
                        print(f"❌ Error accediendo al dashboard: {dashboard_response.text}")
                else:
                    print("❌ No se pudo obtener el token")
            else:
                print(f"❌ Error en login: {login_response.text}")
                
        elif response.status_code == 200:
            print("✅ Dashboard accesible directamente")
            print(f"📄 Contenido: {response.text[:500]}...")
        else:
            print(f"❌ Error inesperado: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

def test_api_endpoints():
    """Probar endpoints de API directamente"""
    print("\n🔌 PROBANDO ENDPOINTS DE API")
    print("=" * 50)
    
    # Probar endpoint de estadísticas
    stats_url = "http://localhost:8001/api/packages/stats/summary"
    
    try:
        print(f"📡 Probando: {stats_url}")
        response = requests.get(stats_url)
        
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"📈 Estadísticas: {json.dumps(stats, indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DEL DASHBOARD")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_dashboard_direct()
    test_api_endpoints()
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    main()
