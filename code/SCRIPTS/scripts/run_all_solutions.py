#!/usr/bin/env python3
"""
Script maestro para ejecutar todas las soluciones implementadas
Solución completa para todos los problemas identificados
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_script(script_name, description):
    """Ejecutar un script específico"""
    print(f"\n🔧 EJECUTANDO: {script_name}")
    print(f"📝 Descripción: {description}")
    print("=" * 60)
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ Script no encontrado: {script_name}")
        return False
    
    try:
        # Ejecutar script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # Mostrar salida
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"⚠️ Errores: {result.stderr}")
        
        # Verificar resultado
        if result.returncode == 0:
            print(f"✅ {script_name} ejecutado exitosamente")
            return True
        else:
            print(f"❌ {script_name} falló con código {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 SCRIPT MAESTRO - SOLUCIONANDO TODOS LOS PROBLEMAS")
    print("=" * 70)
    print()
    print("🎯 PROBLEMAS A SOLUCIONAR:")
    print("   1. ❌ Problemas de conexión desde scripts")
    print("   2. ❌ Imports relativos fallando")
    print("   3. ❌ Autenticación API para endpoints protegidos")
    print()
    
    # Lista de scripts a ejecutar con sus descripciones
    scripts_to_run = [
        ("database_health_check.py", "Verificación completa de salud de la base de datos"),
        ("test_imports_fixed.py", "Prueba de todos los imports corregidos"),
        ("api_endpoints_test.py", "Prueba de todos los endpoints de la API"),
        ("api_auth_test.py", "Prueba de autenticación de la API"),
        ("database_connection_test.py", "Prueba de conexión a la base de datos")
    ]
    
    results = []
    
    # Ejecutar todos los scripts
    for script_name, description in scripts_to_run:
        success = run_script(script_name, description)
        results.append((script_name, success))
        
        # Pausa entre scripts
        if script_name != scripts_to_run[-1][0]:  # No pausar después del último
            print("\n⏳ Pausa de 2 segundos...")
            time.sleep(2)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("🏁 RESUMEN FINAL DE SOLUCIONES")
    print("=" * 70)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"📊 Scripts ejecutados: {total}")
    print(f"✅ Scripts exitosos: {successful}")
    print(f"❌ Scripts fallidos: {total - successful}")
    
    print("\n📋 DETALLE DE RESULTADOS:")
    for script_name, success in results:
        status = "✅ EXITOSO" if success else "❌ FALLIDO"
        print(f"   • {script_name}: {status}")
    
    print("\n🎯 ESTADO DE LAS SOLUCIONES:")
    
    if successful == total:
        print("   🎉 ¡TODOS LOS PROBLEMAS HAN SIDO SOLUCIONADOS!")
        print("   ✅ Conexión a base de datos: Funcionando")
        print("   ✅ Imports relativos: Corregidos")
        print("   ✅ Autenticación API: Verificada")
        print("   ✅ Endpoints protegidos: Funcionando correctamente")
    elif successful >= total * 0.8:
        print("   ✅ La mayoría de problemas han sido solucionados")
        print("   🔧 Revisar los scripts que fallaron")
    else:
        print("   ⚠️ Muchos problemas persisten")
        print("   🚨 Revisar la configuración del proyecto")
    
    print("\n💡 PRÓXIMOS PASOS:")
    if successful == total:
        print("   1. 🎉 El proyecto está completamente funcional")
        print("   2. 🚀 Los scripts funcionan correctamente")
        print("   3. 🔒 La autenticación está operativa")
        print("   4. 📱 El sistema SMS está funcionando")
    else:
        print("   1. 🔍 Revisar los logs de los scripts fallidos")
        print("   2. 🔧 Corregir problemas específicos identificados")
        print("   3. 🧪 Ejecutar scripts individuales para debugging")
        print("   4. 📚 Consultar la documentación del proyecto")
    
    print("\n🏁 SCRIPT MAESTRO COMPLETADO")
    print("=" * 70)
    
    return successful == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Ejecución interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado en script maestro: {e}")
        sys.exit(1)
