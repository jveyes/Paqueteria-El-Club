#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Verificador de Servidor
# ========================================

import requests
import time
import sys

def check_server():
    """Verificar si el servidor está funcionando"""
    print("🔍 Verificando estado del servidor...")
    
    try:
        # Verificar página principal
        response = requests.get("http://localhost/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            print(f"📄 Página principal: http://localhost/")
            return True
        else:
            print(f"⚠️  Servidor respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_urls():
    """Mostrar URLs de acceso al módulo de perfiles"""
    print("\n" + "="*60)
    print("🎯 MÓDULO DE PERFILES - URLs DE ACCESO")
    print("="*60)
    
    print("\n📱 PÁGINAS WEB:")
    print("   • Página Principal: http://localhost/")
    print("   • Perfil de Usuario: http://localhost/profile/")
    print("   • Editar Perfil: http://localhost/profile/edit")
    print("   • Cambiar Contraseña: http://localhost/profile/change-password")
    print("   • Dashboard Admin: http://localhost/dashboard")
    print("   • Login: http://localhost/login")
    
    print("\n🔌 API ENDPOINTS:")
    print("   • Perfil API: http://localhost/profile/api/profile")
    print("   • Logs de Actividad: http://localhost/profile/api/profile/activity-logs")
    print("   • Estadísticas: http://localhost/profile/api/profile/activity-stats")
    print("   • Verificar Auth: http://localhost/api/auth/check")
    
    print("\n👤 CREDENCIALES DE PRUEBA:")
    print("   • Usuario: jveyes")
    print("   • Email: jveyes@gmail.com")
    print("   • Contraseña: Seaboard12")
    
    print("\n🎨 FUNCIONALIDADES IMPLEMENTADAS:")
    print("   ✅ Header mejorado con área de perfil clickable")
    print("   ✅ Página de perfil completa")
    print("   ✅ Edición de información personal")
    print("   ✅ Cambio de contraseña")
    print("   ✅ Foto de perfil")
    print("   ✅ Logs de actividad")
    print("   ✅ Estadísticas de uso")
    print("   ✅ Gestión de roles (solo admin)")
    print("   ✅ Gestión de estados (solo admin)")

def main():
    """Función principal"""
    print("🚀 PAQUETES EL CLUB v3.1 - Verificador de Servidor")
    print("="*60)
    
    # Verificar servidor
    if check_server():
        show_urls()
        print("\n🎉 ¡El módulo de perfiles está listo para usar!")
        print("💡 Para acceder, abre tu navegador y ve a: http://localhost/")
    else:
        print("\n❌ El servidor no está funcionando")
        print("💡 Ejecuta: docker-compose up -d")
        sys.exit(1)

if __name__ == "__main__":
    main()
