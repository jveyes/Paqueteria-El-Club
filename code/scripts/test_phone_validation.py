#!/usr/bin/env python3
"""
Script de prueba para validación de números de teléfono
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.validators import validate_international_phone_number

def test_phone_validation():
    """Prueba la validación de números de teléfono"""
    
    test_cases = [
        # Números colombianos válidos
        ("3001234567", "Colombia - 10 dígitos celular"),
        ("6012345", "Colombia - 7 dígitos fijo"),
        ("6023456", "Colombia - 7 dígitos fijo"),
        ("+57 300 123 4567", "Colombia - con código"),
        ("+573001234567", "Colombia - sin espacios"),
        
        # Números internacionales válidos
        ("+1 555 123 4567", "Estados Unidos"),
        ("+44 20 7946 0958", "Reino Unido"),
        ("+81 3 1234 5678", "Japón"),
        ("+52 55 1234 5678", "México"),
        ("+54 11 1234 5678", "Argentina"),
        
        # Números inválidos
        ("123456789", "Colombia - muy corto"),
        ("30012345678", "Colombia - muy largo"),
        ("2001234567", "Colombia - formato inválido"),
        ("1234567890", "Colombia - 10 dígitos pero no celular"),
        ("601234", "Colombia - fijo muy corto"),
        ("60123456", "Colombia - fijo muy largo"),
        ("+123456", "Internacional - muy corto"),
        ("+123456789012345678", "Internacional - muy largo"),
        ("abc123def", "Caracteres no numéricos"),
        ("", "Vacío"),
    ]
    
    print("🧪 PRUEBAS DE VALIDACIÓN DE NÚMEROS DE TELÉFONO")
    print("=" * 60)
    
    for phone, description in test_cases:
        result = validate_international_phone_number(phone)
        
        status = "✅ VÁLIDO" if result['is_valid'] else "❌ INVÁLIDO"
        print(f"\n{status} - {description}")
        print(f"   Entrada: '{phone}'")
        
        if result['is_valid']:
            print(f"   País: {result['country']}")
            print(f"   Formateado: {result['formatted_number']}")
        else:
            print(f"   Error: {result['error_message']}")
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    test_phone_validation()
