#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test Runner
# ========================================

import os
import sys
import subprocess
import time
from pathlib import Path

def run_test(test_file):
    """Ejecutar un test específico"""
    print(f"🔧 Ejecutando: {test_file}")
    print("-" * 50)
    
    try:
        if test_file.endswith('.py'):
            result = subprocess.run([sys.executable, test_file], 
                                  capture_output=True, text=True, cwd=os.getcwd())
        elif test_file.endswith('.html'):
            print(f"📄 Archivo HTML: {test_file}")
            print("   Abre este archivo en tu navegador para probar la funcionalidad")
            return True
        
        if result.returncode == 0:
            print("✅ Test completado exitosamente")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Test falló")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {test_file}: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("🚀 PAQUETES EL CLUB v3.1 - Test Runner")
    print("=" * 60)
    
    # Obtener directorio actual
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    # Lista de tests en orden de ejecución
    tests = [
        "test_login.py",
        "test_auth_system.py", 
        "test_email_system_simple.py",
        "test_email_system.py",
        "test_email_format.py",
        "test_email_real.py",
        "test_focus.html"
    ]
    
    results = {}
    
    for test in tests:
        if os.path.exists(test):
            print(f"\n📋 Test: {test}")
            success = run_test(test)
            results[test] = success
            time.sleep(1)  # Pausa entre tests
        else:
            print(f"⚠️  Test no encontrado: {test}")
            results[test] = False
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test, success in results.items():
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{status} - {test}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Resultados:")
    print(f"   ✅ Pasaron: {passed}")
    print(f"   ❌ Fallaron: {failed}")
    print(f"   📊 Total: {len(results)}")
    
    if failed == 0:
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
    else:
        print(f"\n⚠️  {failed} test(s) fallaron. Revisa los errores arriba.")
    
    print("\n💡 Uso:")
    print("   python3 run_all_tests.py                    # Ejecutar todos los tests")
    print("   python3 test_auth_system.py                 # Ejecutar test específico")
    print("   python3 test_email_real.py tuemail@ejemplo.com  # Con parámetros")

if __name__ == "__main__":
    main()
