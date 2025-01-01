#!/usr/bin/env python3
"""
Script de Pruebas para las Nuevas Validaciones - PAQUETES EL CLUB v3.1
====================================================================

Pruebas para verificar que las nuevas reglas de validación funcionen correctamente:
- No se aceptan emojis
- No se aceptan caracteres especiales peligrosos
- Teléfono debe tener al menos 10 dígitos
- No se aceptan guiones o paréntesis en teléfonos
- Backend valida mínimo 5 caracteres para guía
- No se aceptan caracteres potencialmente peligrosos
- Protección contra SQL Injection/XSS
"""

import requests
import json
from datetime import datetime

def test_validation_cases():
    """Prueba casos de validación con las nuevas reglas"""
    print("🚀 INICIANDO PRUEBAS DE NUEVAS VALIDACIONES")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    api_url = "http://localhost/api/announcements/"
    
    test_cases = [
        # ===== PRUEBAS DE NOMBRE =====
        {
            "name": "Nombre con emoji",
            "data": {"customer_name": "Juan Pérez 🚀", "guide_number": "TEST123456", "phone_number": "3001234567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Nombre con caracteres especiales",
            "data": {"customer_name": "Juan@Pérez#123", "guide_number": "TEST123456", "phone_number": "3001234567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Nombre con SQL Injection",
            "data": {"customer_name": "'; DROP TABLE packages; --", "guide_number": "TEST123456", "phone_number": "3001234567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Nombre con XSS",
            "data": {"customer_name": "<script>alert('XSS')</script>", "guide_number": "TEST123456", "phone_number": "3001234567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Nombre válido con acentos",
            "data": {"customer_name": "José María Ñoño", "guide_number": "TEST123456", "phone_number": "3001234567"},
            "expected_status": 201,
            "expected_error": None
        },
        
        # ===== PRUEBAS DE TELÉFONO =====
        {
            "name": "Teléfono con guiones",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST123456", "phone_number": "300-123-4567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Teléfono con paréntesis",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST123456", "phone_number": "(300) 123-4567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Teléfono muy corto",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST123456", "phone_number": "123456789"},
            "expected_status": 422,
            "expected_error": "al menos 10 dígitos"
        },
        {
            "name": "Teléfono no colombiano",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST123456", "phone_number": "1234567890"},
            "expected_status": 422,
            "expected_error": "número colombiano válido"
        },
        {
            "name": "Teléfono válido celular",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST123456", "phone_number": "3001234567"},
            "expected_status": 201,
            "expected_error": None
        },
        {
            "name": "Teléfono válido fijo",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST123457", "phone_number": "6012345678"},
            "expected_status": 201,
            "expected_error": None
        },
        
        # ===== PRUEBAS DE GUÍA =====
        {
            "name": "Guía muy corta",
            "data": {"customer_name": "Juan Pérez", "guide_number": "1234", "phone_number": "3001234567"},
            "expected_status": 422,
            "expected_error": "al menos 5 caracteres"
        },
        {
            "name": "Guía con caracteres especiales",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST@123#456", "phone_number": "3001234567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Guía con SQL Injection",
            "data": {"customer_name": "Juan Pérez", "guide_number": "'; DROP TABLE packages; --", "phone_number": "3001234567"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Guía válida con guiones",
            "data": {"customer_name": "Juan Pérez", "guide_number": "TEST-123-456", "phone_number": "3001234568"},
            "expected_status": 201,
            "expected_error": None
        },
        
        # ===== PRUEBAS DE SEGURIDAD =====
        {
            "name": "Datos con múltiples ataques",
            "data": {"customer_name": "<script>alert('XSS')</script>", "guide_number": "'; DROP TABLE packages; --", "phone_number": "javascript:alert('XSS')"},
            "expected_status": 422,
            "expected_error": "caracteres no permitidos"
        },
        {
            "name": "Datos completamente válidos",
            "data": {"customer_name": "María José González", "guide_number": "ABC123DEF", "phone_number": "3001234569"},
            "expected_status": 201,
            "expected_error": None
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Prueba {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(api_url, json=test_case["data"])
            
            if response.status_code == test_case["expected_status"]:
                print(f"✅ Status correcto: {response.status_code}")
                
                # Verificar mensaje de error si se esperaba uno
                if test_case["expected_error"]:
                    try:
                        error_data = response.json()
                        error_message = str(error_data)
                        if test_case["expected_error"] in error_message:
                            print(f"✅ Error esperado encontrado: '{test_case['expected_error']}'")
                            passed += 1
                        else:
                            print(f"❌ Error esperado no encontrado. Esperado: '{test_case['expected_error']}', Recibido: '{error_message}'")
                            failed += 1
                    except:
                        print(f"❌ No se pudo parsear el error")
                        failed += 1
                else:
                    print(f"✅ Respuesta exitosa")
                    passed += 1
                    
            else:
                print(f"❌ Status incorrecto. Esperado: {test_case['expected_status']}, Recibido: {response.status_code}")
                failed += 1
                
                # Mostrar detalles del error
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                    
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            failed += 1
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Total de pruebas: {len(test_cases)}")
    print(f"Pruebas exitosas: {passed}")
    print(f"Pruebas fallidas: {failed}")
    print(f"Tasa de éxito: {(passed/len(test_cases))*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ¡Todas las validaciones funcionan correctamente!")
    else:
        print(f"\n⚠️ {failed} pruebas fallaron. Revisar implementación.")
    
    return passed, failed

if __name__ == "__main__":
    test_validation_cases()
