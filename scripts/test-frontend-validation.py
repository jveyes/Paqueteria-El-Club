#!/usr/bin/env python3
"""
Script de Pruebas de Validación del Frontend - PAQUETES EL CLUB v3.1
===================================================================

Pruebas exhaustivas para verificar validaciones, errores y comportamiento del frontend
"""

import requests
import json
from datetime import datetime

def test_frontend_access():
    """Prueba acceso al frontend"""
    print("🔍 Probando acceso al frontend...")
    
    try:
        response = requests.get("http://localhost/")
        if response.status_code == 200:
            print("✅ Frontend accesible")
            
            # Verificar elementos del formulario
            html = response.text
            required_elements = [
                "announcementForm",
                "customer_name",
                "guide_number", 
                "phone_number",
                "terms_conditions"
            ]
            
            for element in required_elements:
                if element in html:
                    print(f"✅ Elemento {element} presente")
                else:
                    print(f"❌ Elemento {element} no encontrado")
                    
        else:
            print(f"❌ Error accediendo al frontend: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_endpoint():
    """Prueba el endpoint de la API"""
    print("\n🔍 Probando endpoint de la API...")
    
    api_url = "http://localhost/api/announcements/"
    
    # Prueba método GET (no permitido)
    try:
        response = requests.get(api_url)
        if response.status_code == 405:
            print("✅ Método GET correctamente rechazado")
        else:
            print(f"❌ Método GET debería ser rechazado, status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error probando GET: {e}")

def test_validation_cases():
    """Prueba casos de validación"""
    print("\n🔍 Probando casos de validación...")
    
    api_url = "http://localhost/api/announcements/"
    
    test_cases = [
        {
            "name": "Datos válidos",
            "data": {
                "customer_name": "Juan Pérez",
                "guide_number": "TEST123456",
                "phone_number": "3001234567"
            },
            "expected_status": 201
        },
        {
            "name": "Nombre vacío",
            "data": {
                "customer_name": "",
                "guide_number": "TEST123456",
                "phone_number": "3001234567"
            },
            "expected_status": 422
        },
        {
            "name": "Guía muy corta",
            "data": {
                "customer_name": "Juan Pérez",
                "guide_number": "1234",
                "phone_number": "3001234567"
            },
            "expected_status": 422
        },
        {
            "name": "Teléfono muy corto",
            "data": {
                "customer_name": "Juan Pérez",
                "guide_number": "TEST123456",
                "phone_number": "123"
            },
            "expected_status": 422
        },
        {
            "name": "Datos completamente vacíos",
            "data": {},
            "expected_status": 422
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(api_url, json=test_case["data"])
            
            if response.status_code == test_case["expected_status"]:
                print(f"✅ {test_case['name']}: Status {response.status_code}")
            else:
                print(f"❌ {test_case['name']}: Expected {test_case['expected_status']}, Got {response.status_code}")
                
                # Mostrar detalles del error si es 422
                if response.status_code == 422:
                    try:
                        error_data = response.json()
                        if "detail" in error_data:
                            print(f"   Error: {error_data['detail']}")
                    except:
                        pass
                        
        except Exception as e:
            print(f"❌ {test_case['name']}: Error - {e}")

def test_error_handling():
    """Prueba manejo de errores"""
    print("\n🔍 Probando manejo de errores...")
    
    # Prueba URL inexistente
    try:
        response = requests.post("http://localhost/api/nonexistent/")
        if response.status_code == 404:
            print("✅ URL inexistente correctamente manejada")
        else:
            print(f"❌ URL inexistente debería dar 404, status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error probando URL inexistente: {e}")
    
    # Prueba JSON malformado
    try:
        response = requests.post(
            "http://localhost/api/announcements/",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 422:
            print("✅ JSON malformado correctamente rechazado")
        else:
            print(f"❌ JSON malformado debería ser rechazado, status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error probando JSON malformado: {e}")

def test_success_response():
    """Prueba respuesta exitosa"""
    print("\n🔍 Probando respuesta exitosa...")
    
    api_url = "http://localhost/api/announcements/"
    
    valid_data = {
        "customer_name": "Test User",
        "guide_number": "SUCCESS123",
        "phone_number": "3001234567"
    }
    
    try:
        response = requests.post(api_url, json=valid_data)
        
        if response.status_code == 201:
            print("✅ Respuesta exitosa recibida")
            
            # Verificar estructura de respuesta
            try:
                response_data = response.json()
                
                if "tracking_number" in response_data:
                    print(f"✅ Tracking number generado: {response_data['tracking_number']}")
                else:
                    print("❌ No se encontró tracking_number en la respuesta")
                    
                if "announced_at" in response_data:
                    print(f"✅ Fecha de anuncio: {response_data['announced_at']}")
                else:
                    print("❌ No se encontró announced_at en la respuesta")
                    
                if "customer_name" in response_data:
                    print(f"✅ Nombre del cliente: {response_data['customer_name']}")
                else:
                    print("❌ No se encontró customer_name en la respuesta")
                    
            except json.JSONDecodeError:
                print("❌ Respuesta no es JSON válido")
                
        else:
            print(f"❌ Respuesta exitosa esperada, status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error probando respuesta exitosa: {e}")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DEL FRONTEND")
    print("=" * 50)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    test_frontend_access()
    test_api_endpoint()
    test_validation_cases()
    test_error_handling()
    test_success_response()
    
    print("\n" + "=" * 50)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 50)

if __name__ == "__main__":
    main()
