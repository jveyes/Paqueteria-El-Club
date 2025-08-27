#!/usr/bin/env python3
"""
Script de prueba para el sistema de códigos de seguimiento de paquetes
"""

import requests
import json
import random
import string

BASE_URL = "http://localhost"

def generate_test_data():
    """Generar datos de prueba únicos"""
    # Generar nombre único
    name = f"Test User {random.randint(1000, 9999)}"
    
    # Generar teléfono único
    phone = f"300{random.randint(1000000, 9999999)}"
    
    # Generar número de guía único
    guide = f"TEST{random.randint(100, 999)}"
    
    return {
        "customer_name": name,
        "phone_number": phone,
        "guide_number": guide
    }

def test_create_announcement():
    """Probar creación de anuncio con código de seguimiento"""
    print("🔍 Probando creación de anuncio...")
    
    test_data = generate_test_data()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/announcements/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Anuncio creado exitosamente")
            print(f"   Cliente: {data['customer_name']}")
            print(f"   Guía: {data['guide_number']}")
            print(f"   Código de seguimiento: {data['tracking_code']}")
            print(f"   Estado: {data['status']}")
            return data
        else:
            print(f"❌ Error al crear anuncio: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_track_by_code(tracking_code):
    """Probar consulta por código de seguimiento"""
    print(f"\n🔍 Probando consulta por código: {tracking_code}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/announcements/tracking/{tracking_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Paquete encontrado")
            print(f"   Cliente: {data['customer_name']}")
            print(f"   Teléfono: {data['phone_number']}")
            print(f"   Guía: {data['guide_number']}")
            print(f"   Código: {data['tracking_code']}")
            print(f"   Estado: {data['status']}")
            print(f"   Fecha: {data['announced_at']}")
            return True
        else:
            print(f"❌ Error al consultar: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_track_by_guide(guide_number):
    """Probar consulta por número de guía"""
    print(f"\n🔍 Probando consulta por guía: {guide_number}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/announcements/guide/{guide_number}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Paquete encontrado por guía")
            print(f"   Código de seguimiento: {data['tracking_code']}")
            return True
        else:
            print(f"❌ Error al consultar por guía: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_invalid_tracking_code():
    """Probar código de seguimiento inválido"""
    print(f"\n🔍 Probando código inválido: INVALID")
    
    try:
        response = requests.get(f"{BASE_URL}/api/announcements/tracking/INVALID")
        
        if response.status_code == 404:
            print(f"✅ Correcto: Código inválido no encontrado")
            return True
        else:
            print(f"❌ Error: Debería retornar 404, pero retornó {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_frontend_pages():
    """Probar que las páginas frontend estén disponibles"""
    print(f"\n🔍 Probando páginas frontend...")
    
    pages = [
        ("/", "Página principal (anuncio)"),
        ("/track", "Página de consulta por código"),
        ("/search", "Página de búsqueda")
    ]
    
    all_ok = True
    
    for page, description in pages:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: Error {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"❌ {description}: Error de conexión - {e}")
            all_ok = False
    
    return all_ok

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema de códigos de seguimiento")
    print("=" * 60)
    
    # Probar creación de anuncio
    announcement = test_create_announcement()
    
    if announcement:
        tracking_code = announcement['tracking_code']
        guide_number = announcement['guide_number']
        
        # Probar consulta por código de seguimiento
        test_track_by_code(tracking_code)
        
        # Probar consulta por número de guía
        test_track_by_guide(guide_number)
        
        # Probar código inválido
        test_invalid_tracking_code()
        
        # Probar páginas frontend
        test_frontend_pages()
        
        print("\n" + "=" * 60)
        print("📋 Resumen de pruebas:")
        print(f"   • Código de seguimiento generado: {tracking_code}")
        print(f"   • Número de guía: {guide_number}")
        print(f"   • URL de consulta: {BASE_URL}/track")
        print(f"   • URL de anuncio: {BASE_URL}/")
        
    else:
        print("❌ No se pudo crear el anuncio de prueba")
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    main()
