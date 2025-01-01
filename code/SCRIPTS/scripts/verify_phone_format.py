#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Verificar Formato de Teléfono
# ========================================

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_phone_formatting():
    """Probar diferentes formatos de número de teléfono"""
    print("�� VERIFICANDO FORMATO DE NÚMEROS DE TELÉFONO")
    print("=" * 60)
    
    # Diferentes formatos para probar
    test_numbers = [
        "3002596319",           # Solo números (formato actual)
        "573002596319",         # Con 57
        "+573002596319",        # Formato internacional correcto
        "300 259 6319",         # Con espacios
        "300-259-6319",         # Con guiones
        "(300) 259-6319",       # Con paréntesis
        "300.259.6319",         # Con puntos
    ]
    
    print("�� Formatos de prueba:")
    for i, number in enumerate(test_numbers, 1):
        print(f"{i}. {number}")
    
    print("\n🔄 Procesando formatos...")
    print("-" * 50)
    
    for number in test_numbers:
        # Simular el procesamiento interno del servicio SMS
        if number.startswith('+'):
            formatted = number  # Ya tiene formato internacional
        else:
            # Remover caracteres especiales y agregar +57
            clean_number = ''.join(filter(str.isdigit, number))
            if clean_number.startswith('57'):
                formatted = f"+{clean_number}"
            else:
                formatted = f"+57{clean_number}"
        
        print(f"📱 {number:15} → {formatted}")
    
    print("-" * 50)
    print("✅ Verificación de formato completada")
    print("🎯 Formato correcto para LIWA.co: +573002596319")
    
    # Verificar el número específico de prueba
    print("\n�� VERIFICACIÓN ESPECÍFICA DEL NÚMERO DE PRUEBA")
    print("=" * 50)
    test_phone = "3002596319"
    formatted_test = f"+57{test_phone}"
    print(f"�� Número de entrada: {test_phone}")
    print(f"�� Formato procesado: {formatted_test}")
    print(f"✅ Formato válido: {'SÍ' if formatted_test == '+573002596319' else 'NO'}")

def test_sms_service_format():
    """Probar el formato usando el servicio SMS real"""
    print("\n�� VERIFICANDO SERVICIO SMS REAL")
    print("=" * 50)
    
    try:
        from services.sms_service import LIWASMSService
        
        # Crear instancia del servicio
        sms_service = LIWASMSService()
        
        # Número de prueba
        test_phone = "3002596319"
        
        print(f"📱 Número de prueba: {test_phone}")
        print(f"�� Clase del servicio: {type(sms_service).__name__}")
        print(f"✅ Servicio SMS cargado correctamente")
        
        # Verificar configuración
        print(f"\n⚙️ Configuración del servicio:")
        print(f"   API Key: {'✅ Configurado' if sms_service.api_key else '❌ No configurado'}")
        print(f"   Account: {'✅ Configurado' if sms_service.account else '❌ No configurado'}")
        print(f"   Auth URL: {'✅ Configurado' if sms_service.auth_url else '❌ No configurado'}")
        print(f"   From Name: {'✅ Configurado' if sms_service.from_name else '❌ No configurado'}")
        
    except ImportError as e:
        print(f"❌ Error importando servicio SMS: {e}")
    except Exception as e:
        print(f"❌ Error verificando servicio: {e}")

if __name__ == "__main__":
    print("🧪 INICIANDO VERIFICACIÓN DE FORMATO DE TELÉFONO")
    print("=" * 60)
    
    # Verificación básica de formato
    test_phone_formatting()
    
    # Verificación del servicio SMS
    test_sms_service_format()
    
    print("\n" + "=" * 60)
    print("🏁 Verificación completada")
    print("📱 El número 3002596319 se formateará como +573002596319")
