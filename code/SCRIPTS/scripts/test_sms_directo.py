#!/usr/bin/env python3
"""
Script para probar SMS directamente con el número exacto
"""

import sys
import os
import requests
import json
import time
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_sms_directo():
    """Probar SMS directamente con el número exacto"""
    print("📱 PRUEBA DIRECTA DE SMS")
    print("=" * 50)
    
    base_url = "http://localhost"
    
    # Datos de prueba con número exacto
    sms_data = {
        "customer_name": "PRUEBA SMS DIRECTO",
        "phone_number": "3002596319",  # Número exacto del usuario
        "guide_number": f"DIRECT{int(time.time())}",
        "tracking_code": "TEST"
    }
    
    print(f"📝 Datos del SMS:")
    print(f"   • Cliente: {sms_data['customer_name']}")
    print(f"   • Teléfono: {sms_data['phone_number']}")
    print(f"   • Guía: {sms_data['guide_number']}")
    print(f"   • Tracking: {sms_data['tracking_code']}")
    print()
    
    print("⚠️ IMPORTANTE: Verifica que tu teléfono esté:")
    print("   • Encendido y con señal")
    print("   • Con el número correcto: 3002596319")
    print("   • Sin bloqueo de SMS")
    print()
    
    input("Presiona ENTER para continuar con el envío del SMS...")
    
    try:
        # Enviar SMS directamente
        print("📤 Enviando SMS directamente...")
        
        response = requests.post(
            f"{base_url}/api/announcements/send-sms-browser",
            json=sms_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "http://localhost/customers/announce.html"
            }
        )
        
        print(f"   📤 Respuesta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SMS enviado exitosamente")
            print(f"   • Resultado: {result}")
            
            # Verificar logs
            print("\n🔍 Verificando logs del contenedor...")
            print("   💡 Buscar: 'SMS enviado exitosamente desde navegador'")
            print("   💡 Buscar: 'SMS enviado exitosamente a 573002596319'")
            
            # Esperar para que se procese
            time.sleep(3)
            
            print("\n📱 INSTRUCCIONES PARA EL USUARIO:")
            print("   1. ✅ El SMS se envió exitosamente desde el backend")
            print("   2. 🔍 Verifica tu teléfono (número: 3002596319)")
            print("   3. 📱 El mensaje debe contener el código: TEST")
            print("   4. ⏰ Puede tardar 1-2 minutos en llegar")
            print("   5. 📞 Si no llega, verifica tu señal y configuración")
            
            return True
            
        else:
            print(f"❌ Error enviando SMS: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verificar_configuracion_telefono():
    """Verificar configuración del teléfono"""
    print("\n📋 VERIFICACIÓN DE CONFIGURACIÓN DEL TELÉFONO")
    print("=" * 60)
    
    print("🔍 PASOS PARA VERIFICAR:")
    print("   1. 📱 Verifica que tu teléfono esté encendido")
    print("   2. 📶 Confirma que tengas señal de celular")
    print("   3. 📞 Verifica que el número sea: 3002596319")
    print("   4. 🔒 Asegúrate de que no tengas SMS bloqueados")
    print("   5. 💰 Verifica que tengas saldo o plan activo")
    print()
    
    print("📱 CONFIGURACIÓN DEL TELÉFONO:")
    print("   • Número: 3002596319")
    print("   • País: Colombia")
    print("   • Operador: Cualquiera (Claro, Movistar, Tigo, etc.)")
    print()
    
    print("⚠️ PROBLEMAS COMUNES:")
    print("   • Teléfono apagado o sin señal")
    print("   • Número bloqueado por el operador")
    print("   • Plan sin SMS incluido")
    print("   • Configuración de privacidad")

def main():
    """Función principal"""
    print("🚀 PRUEBA DIRECTA DE SMS AL TELÉFONO")
    print("=" * 80)
    
    # Probar SMS directo
    success = test_sms_directo()
    
    if success:
        print("\n🎉 PRUEBA COMPLETADA")
        print("✅ El SMS se envió exitosamente desde el backend")
        print("✅ Ahora verifica tu teléfono")
        
        # Instrucciones de configuración
        verificar_configuracion_telefono()
        
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. 📱 Verifica tu teléfono (3002596319)")
        print("   2. ⏰ Espera 1-2 minutos")
        print("   3. 📱 El mensaje debe contener: TEST")
        print("   4. 🔍 Si no llega, revisa la configuración")
        
    else:
        print("\n❌ PRUEBA FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 PRUEBA COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
