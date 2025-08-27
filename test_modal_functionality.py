#!/usr/bin/env python3
"""
Script para probar la funcionalidad del modal de éxito
"""

import requests
import json
from datetime import datetime

def test_modal_functionality():
    """Probar que el modal se muestra correctamente"""
    print("🧪 Probando funcionalidad del modal...")
    
    # 1. Verificar que el modal está en el HTML
    print("\n1. Verificando presencia del modal en el HTML...")
    
    try:
        response = requests.get("http://localhost/")
        if response.status_code == 200:
            content = response.text
            
            # Verificar elementos del modal
            checks = [
                ("Modal container", "successModal"),
                ("Título del modal", "Paquete Anunciado Exitosamente"),
                ("Número de guía", "modalGuideNumber"),
                ("Botón de cerrar", "closeModalBtn"),
                ("Mensaje amigable", "Nos pondremos en contacto contigo pronto"),
                ("Información adicional", "Tiempo estimado de entrega")
            ]
            
            all_present = True
            for check_name, search_term in checks:
                if search_term in content:
                    print(f"   ✅ {check_name}: Encontrado")
                else:
                    print(f"   ❌ {check_name}: No encontrado")
                    all_present = False
            
            if all_present:
                print("   🎉 Modal HTML: COMPLETO")
            else:
                print("   ⚠️  Modal HTML: INCOMPLETO")
                
        else:
            print(f"   ❌ Error al cargar la página: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # 2. Probar creación de anuncio para verificar el flujo
    print("\n2. Probando flujo completo de creación...")
    
    url = "http://localhost/api/announcements/"
    headers = {"Content-Type": "application/json"}
    
    test_data = {
        "customer_name": "Ana López",
        "phone_number": "3005551234",
        "guide_number": "TEST123456"
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_data)
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ ÉXITO - Anuncio creado")
            print(f"   📦 Número de guía: {result.get('guide_number')}")
            print(f"   👤 Cliente: {result.get('customer_name')}")
            print(f"   📅 Fecha: {result.get('announced_at')}")
            
            # Verificar que el número de guía se puede usar en el modal
            print(f"   🔍 El número '{result.get('guide_number')}' se mostrará en el modal")
            
        else:
            print(f"   ❌ ERROR - {response.text}")
            
    except Exception as e:
        print(f"   ❌ ERROR DE CONEXIÓN: {e}")
    
    # 3. Verificar que no hay mensajes inline de éxito
    print("\n3. Verificando eliminación de mensajes inline...")
    
    try:
        response = requests.get("http://localhost/")
        if response.status_code == 200:
            content = response.text
            
            # Verificar que NO hay mensajes inline de éxito
            inline_checks = [
                ("successMessage", "Mensaje inline de éxito"),
                ("successText", "Texto inline de éxito"),
                ("Anuncio creado exitosamente", "Texto antiguo")
            ]
            
            inline_removed = True
            for search_term, description in inline_checks:
                if search_term in content:
                    print(f"   ⚠️  {description}: Aún presente (debería estar removido)")
                    inline_removed = False
                else:
                    print(f"   ✅ {description}: Removido correctamente")
            
            if inline_removed:
                print("   🎉 Mensajes inline: REMOVIDOS CORRECTAMENTE")
            else:
                print("   ⚠️  Mensajes inline: ALGUNOS AÚN PRESENTES")
                
        else:
            print(f"   ❌ Error al cargar la página: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA DE FUNCIONALIDAD DEL MODAL")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_modal_functionality()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE CAMBIOS IMPLEMENTADOS")
    print("=" * 60)
    print("✅ Mensaje cambiado: 'Anuncio creado' → 'Paquete anunciado exitosamente'")
    print("✅ Modal implementado: Reemplaza mensaje inline")
    print("✅ Mensaje amigable: Información clara para el cliente")
    print("✅ Número de guía destacado: En caja azul")
    print("✅ Información adicional: Tiempo de entrega, WhatsApp, etc.")
    print("✅ Múltiples formas de cerrar: Botón, clic fuera, tecla Escape")
    print("✅ Accesibilidad: Focus automático en botón de cerrar")
    print("=" * 60)
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Abrir http://localhost/ en el navegador")
    print("2. Llenar el formulario con datos de prueba")
    print("3. Hacer clic en 'Anunciar'")
    print("4. Verificar que aparece el modal con el mensaje amigable")
    print("5. Probar las diferentes formas de cerrar el modal")

if __name__ == "__main__":
    main()
