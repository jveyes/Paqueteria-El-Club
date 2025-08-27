#!/usr/bin/env python3
"""
Script para probar el sistema completo de anuncios de paquetes
"""

import requests
import json
from datetime import datetime

def test_create_announcement():
    """Probar creación de anuncio"""
    print("🧪 Probando creación de anuncio...")
    
    url = "http://localhost/api/announcements/"
    headers = {"Content-Type": "application/json"}
    
    # Datos de prueba
    test_data = {
        "customer_name": "María García",
        "phone_number": "3009876543",
        "guide_number": "XYZ789012"
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_data)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Anuncio creado")
            print(f"👤 Cliente: {result.get('customer_name')}")
            print(f"📞 Teléfono: {result.get('phone_number')}")
            print(f"📦 Guía: {result.get('guide_number')}")
            print(f"🆔 ID: {result.get('id')}")
            print(f"📅 Fecha: {result.get('announced_at')}")
            return result.get('id')
        else:
            print(f"❌ ERROR - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        return None

def test_list_announcements():
    """Probar listado de anuncios"""
    print("\n🧪 Probando listado de anuncios...")
    
    url = "http://localhost/api/announcements/"
    
    try:
        response = requests.get(url)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            announcements = response.json()
            print(f"✅ ÉXITO - {len(announcements)} anuncios encontrados")
            
            for i, announcement in enumerate(announcements[:3], 1):
                print(f"  {i}. {announcement.get('customer_name')} - {announcement.get('guide_number')}")
            
            return len(announcements)
        else:
            print(f"❌ ERROR - {response.text}")
            return 0
            
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        return 0

def test_get_announcement_by_guide():
    """Probar obtención de anuncio por número de guía"""
    print("\n🧪 Probando obtención por número de guía...")
    
    url = "http://localhost/api/announcements/guide/ABC123456"
    
    try:
        response = requests.get(url)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            announcement = response.json()
            print(f"✅ ÉXITO - Anuncio encontrado")
            print(f"👤 Cliente: {announcement.get('customer_name')}")
            print(f"📦 Guía: {announcement.get('guide_number')}")
            return True
        else:
            print(f"❌ ERROR - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        return False

def test_announcement_stats():
    """Probar estadísticas de anuncios"""
    print("\n🧪 Probando estadísticas de anuncios...")
    
    url = "http://localhost/api/announcements/stats/summary"
    
    try:
        response = requests.get(url)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ ÉXITO - Estadísticas obtenidas")
            print(f"📊 Total: {stats.get('total_announcements')}")
            print(f"⏳ Pendientes: {stats.get('pending_announcements')}")
            print(f"✅ Procesados: {stats.get('processed_announcements')}")
            return stats
        else:
            print(f"❌ ERROR - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        return None

def test_frontend_form():
    """Probar que el formulario frontend esté disponible"""
    print("\n🧪 Probando formulario frontend...")
    
    url = "http://localhost/"
    
    try:
        response = requests.get(url)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            if "announcementForm" in content:
                print("✅ ÉXITO - Formulario encontrado en la página principal")
                return True
            else:
                print("❌ ERROR - Formulario no encontrado")
                return False
        else:
            print(f"❌ ERROR - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA COMPLETA DEL SISTEMA DE ANUNCIOS")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Ejecutar todas las pruebas
    tests = [
        ("Creación de anuncio", test_create_announcement),
        ("Listado de anuncios", test_list_announcements),
        ("Obtención por guía", test_get_announcement_by_guide),
        ("Estadísticas", test_announcement_stats),
        ("Formulario frontend", test_frontend_form)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, True, result))
        except Exception as e:
            print(f"❌ ERROR en {test_name}: {e}")
            results.append((test_name, False, None))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success, result in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ El sistema de anuncios está funcionando correctamente")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("🔧 Revisar configuración del sistema")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
