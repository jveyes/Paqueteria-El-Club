#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Submissión del Formulario
=================================

Este script simula exactamente lo que hace el formulario de announce.html
cuando se envía, para verificar que el SMS se envíe correctamente.
"""

import requests
import json
import time

def test_form_submission():
    """Probar la submissión del formulario"""
    
    print("🧪 TEST DE SUBMISIÓN DEL FORMULARIO")
    print("=" * 50)
    
    # URL del endpoint
    url = "http://localhost:8000/api/announcements/"
    
    # Datos del formulario (exactamente como los envía announce.html)
    form_data = {
        "customer_name": "JUAN PÉREZ",
        "guide_number": f"TEST{int(time.time())}",  # Guía única
        "phone_number": "3002596319"  # Tu número real
    }
    
    print(f"📝 Datos del formulario:")
    print(f"   Nombre: {form_data['customer_name']}")
    print(f"   Guía: {form_data['guide_number']}")
    print(f"   Teléfono: {form_data['phone_number']}")
    print()
    
    print(f"🌐 Enviando POST a: {url}")
    print(f"📤 Datos: {json.dumps(form_data, indent=2)}")
    print()
    
    try:
        # Enviar POST request (exactamente como lo hace el frontend)
        response = requests.post(
            url,
            json=form_data,
            headers={
                'Content-Type': 'application/json',
            },
            timeout=30
        )
        
        print(f"📊 Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            # Éxito
            result = response.json()
            print("✅ FORMULARIO ENVIADO EXITOSAMENTE")
            print("=" * 50)
            print(f"🎯 Código de tracking: {result.get('tracking_code')}")
            print(f"📦 Número de guía: {result.get('guide_number')}")
            print(f"👤 Cliente: {result.get('customer_name')}")
            print(f"📱 Teléfono: {result.get('phone_number')}")
            print(f"📅 Fecha: {result.get('announced_at')}")
            print()
            
            print("📱 VERIFICACIÓN DEL SMS:")
            print("   • El sistema debería haber enviado un SMS automáticamente")
            print("   • El SMS debería contener el código de tracking")
            print("   • El número debería estar formateado con 57")
            print()
            
            print("🔍 PRÓXIMOS PASOS:")
            print("   1. Verifica que recibiste el SMS")
            print("   2. Si no lo recibiste, revisa los logs del servidor")
            print("   3. El SMS debería contener el código de consulta")
            
            return True
            
        elif response.status_code == 400:
            # Error de validación
            error_data = response.json()
            print("❌ ERROR DE VALIDACIÓN")
            print(f"   Detalle: {error_data.get('detail')}")
            
            if "Ya existe un anuncio" in str(error_data.get('detail', '')):
                print("   💡 La guía ya existe, esto es normal en pruebas repetidas")
                print("   💡 Intenta con una guía diferente")
            
            return False
            
        else:
            # Otro error
            print(f"❌ ERROR DEL SERVIDOR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalle: {error_data}")
            except:
                print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR DE CONEXIÓN")
        print("   El servidor no está respondiendo")
        print("   Verifica que esté ejecutándose en http://localhost:8000")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT")
        print("   La petición tardó demasiado")
        print("   El servidor puede estar sobrecargado")
        return False
        
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO TEST DEL FORMULARIO DE ANUNCIOS")
    print("=" * 60)
    print("Este test simula exactamente lo que hace announce.html")
    print("cuando un usuario envía el formulario de anuncio de paquetes.")
    print()
    
    try:
        success = test_form_submission()
        if success:
            print("\n🎉 TEST COMPLETADO EXITOSAMENTE")
            print("✅ El formulario está funcionando correctamente")
            print("📱 El SMS debería haberse enviado automáticamente")
        else:
            print("\n❌ HAY PROBLEMAS EN EL FORMULARIO")
            print("🔧 Revisa los logs del servidor para más detalles")
            
    except Exception as e:
        print(f"\n💥 ERROR INESPERADO: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
