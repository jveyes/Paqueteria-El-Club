#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Script Runner
# ========================================

import os
import sys
import subprocess
import argparse
from pathlib import Path

def list_scripts():
    """Listar todos los scripts disponibles"""
    script_dir = Path(__file__).parent
    scripts = []
    
    for file in script_dir.glob("*.sh"):
        if file.is_file() and file.stat().st_mode & 0o111:  # Executable
            scripts.append(file.name)
    
    for file in script_dir.glob("*.py"):
        if file.is_file() and file.name != "run_script.py":
            scripts.append(file.name)
    
    return sorted(scripts)

def run_script(script_name, args=None):
    """Ejecutar un script específico"""
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"❌ Script no encontrado: {script_name}")
        return False
    
    print(f"🔧 Ejecutando: {script_name}")
    print("=" * 60)
    
    try:
        if script_name.endswith('.sh'):
            cmd = ['bash', str(script_path)]
        elif script_name.endswith('.py'):
            cmd = [sys.executable, str(script_path)]
        else:
            print(f"❌ Tipo de archivo no soportado: {script_name}")
            return False
        
        # Agregar argumentos adicionales si los hay
        if args:
            cmd.extend(args)
        
        # Ejecutar el script
        result = subprocess.run(cmd, cwd=script_dir)
        
        if result.returncode == 0:
            print(f"\n✅ Script {script_name} completado exitosamente")
            return True
        else:
            print(f"\n❌ Script {script_name} falló con código {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False

def show_script_info(script_name):
    """Mostrar información sobre un script específico"""
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"❌ Script no encontrado: {script_name}")
        return
    
    print(f"📋 Información del script: {script_name}")
    print("=" * 50)
    
    try:
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Buscar descripción en comentarios
        lines = content.split('\n')
        description = ""
        
        for line in lines[:10]:  # Buscar en las primeras 10 líneas
            if line.strip().startswith('#') and 'PAQUETES EL CLUB' in line:
                description = line.strip('#').strip()
                break
        
        if description:
            print(f"📝 Descripción: {description}")
        
        print(f"📁 Ubicación: {script_path}")
        print(f"📊 Tamaño: {script_path.stat().st_size} bytes")
        
        # Mostrar primeras líneas del script
        print(f"\n📄 Primeras líneas:")
        for i, line in enumerate(lines[:5]):
            if line.strip():
                print(f"   {i+1}: {line}")
        
        if len(lines) > 5:
            print(f"   ... ({len(lines)-5} líneas más)")
            
    except Exception as e:
        print(f"❌ Error leyendo script: {e}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Script Runner para PAQUETES EL CLUB v3.1')
    parser.add_argument('script', nargs='?', help='Nombre del script a ejecutar')
    parser.add_argument('args', nargs='*', help='Argumentos adicionales para el script')
    parser.add_argument('-l', '--list', action='store_true', help='Listar todos los scripts disponibles')
    parser.add_argument('-i', '--info', help='Mostrar información sobre un script específico')
    
    args = parser.parse_args()
    
    print("🚀 PAQUETES EL CLUB v3.1 - Script Runner")
    print("=" * 60)
    
    if args.list:
        print("📋 Scripts disponibles:")
        print("-" * 40)
        scripts = list_scripts()
        for script in scripts:
            print(f"   📄 {script}")
        print(f"\n📊 Total: {len(scripts)} scripts")
        return
    
    if args.info:
        show_script_info(args.info)
        return
    
    if not args.script:
        print("❌ Debes especificar un script para ejecutar")
        print("\n💡 Uso:")
        print("   python3 run_script.py -l                    # Listar scripts")
        print("   python3 run_script.py -i script.sh          # Info del script")
        print("   python3 run_script.py script.sh             # Ejecutar script")
        print("   python3 run_script.py script.sh arg1 arg2   # Con argumentos")
        return
    
    # Ejecutar el script
    success = run_script(args.script, args.args)
    
    if success:
        print("\n🎉 Script ejecutado correctamente")
    else:
        print("\n⚠️  El script falló. Revisa los errores arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()
