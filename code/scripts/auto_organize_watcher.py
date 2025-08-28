#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Auto Organize Watcher
# ========================================
#
# 🎯 OBJETIVO: Observar cambios en archivos y organizar automáticamente
# 📅 FECHA: 2025-08-27
# 👤 AUTOR: Sistema Automático
# 🔄 VERSIÓN: 1.0.0
#
# 📋 USO:
#   python3 auto_organize_watcher.py                    # Iniciar observador
#   python3 auto_organize_watcher.py --daemon          # Ejecutar en segundo plano
#   python3 auto_organize_watcher.py --stop            # Detener observador
#
# 📊 RESULTADOS:
#   - Log: code/logs/auto_organize_watcher.log
#   - PID: code/logs/watcher.pid
#   - Reportes automáticos en code/TEST/reports/
#
# ⚠️ DEPENDENCIAS:
#   - Python 3.8+
#   - watchdog (pip install watchdog)
#   - auto_organize_files.py
#
# ========================================

import os
import sys
import time
import signal
import argparse
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AutoOrganizeHandler(FileSystemEventHandler):
    """Manejador de eventos para organización automática"""
    
    def __init__(self, organizer_script: str):
        self.organizer_script = organizer_script
        self.last_organization = 0
        self.cooldown_period = 5  # Segundos entre organizaciones
        self.logger = logging.getLogger(__name__)
        
    def on_created(self, event):
        """Cuando se crea un archivo"""
        if not event.is_directory:
            self.logger.info(f"📄 Archivo creado: {event.src_path}")
            self.trigger_organization("archivo creado")
    
    def on_moved(self, event):
        """Cuando se mueve un archivo"""
        if not event.is_directory:
            self.logger.info(f"📁 Archivo movido: {event.src_path} → {event.dest_path}")
            self.trigger_organization("archivo movido")
    
    def on_modified(self, event):
        """Cuando se modifica un archivo"""
        if not event.is_directory:
            # Solo organizar si es un archivo de configuración o script
            file_path = Path(event.src_path)
            if any(pattern in file_path.name for pattern in ['*.sh', '*.py', '*.md', '*.conf', '*.config']):
                self.logger.info(f"✏️ Archivo modificado: {event.src_path}")
                self.trigger_organization("archivo modificado")
    
    def trigger_organization(self, reason: str):
        """Disparar organización automática"""
        current_time = time.time()
        
        # Evitar organizaciones muy frecuentes
        if current_time - self.last_organization < self.cooldown_period:
            self.logger.info(f"⏳ Organización en cooldown ({self.cooldown_period}s restantes)")
            return
        
        self.logger.info(f"🚀 Disparando organización automática: {reason}")
        
        try:
            # Ejecutar organización
            result = subprocess.run([
                sys.executable, self.organizer_script, '--dry-run'
            ], capture_output=True, text=True, cwd=Path(self.organizer_script).parent)
            
            if result.returncode == 0:
                # Si hay archivos para mover, ejecutar organización real
                if "archivos para organizar" in result.stdout or "misplaced_files" in result.stdout:
                    self.logger.info("📋 Archivos detectados, ejecutando organización...")
                    
                    result = subprocess.run([
                        sys.executable, self.organizer_script
                    ], capture_output=True, text=True, cwd=Path(self.organizer_script).parent)
                    
                    if result.returncode == 0:
                        self.logger.info("✅ Organización automática completada")
                        
                        # Generar reporte
                        subprocess.run([
                            sys.executable, self.organizer_script, '--report'
                        ], cwd=Path(self.organizer_script).parent)
                        
                    else:
                        self.logger.error(f"❌ Error en organización: {result.stderr}")
                else:
                    self.logger.info("✅ No se encontraron archivos para organizar")
            
            self.last_organization = current_time
            
        except Exception as e:
            self.logger.error(f"❌ Error ejecutando organización: {e}")

class AutoOrganizeWatcher:
    """Observador principal para organización automática"""
    
    def __init__(self, base_dir: str = "code"):
        self.base_dir = Path(base_dir)
        self.organizer_script = self.base_dir / "SCRIPTS" / "auto_organize_files.py"
        self.pid_file = self.base_dir / "logs" / "watcher.pid"
        self.log_dir = self.base_dir / "logs"
        
        # Configurar logging
        self.setup_logging()
        
        # Configurar observador
        self.observer = Observer()
        self.handler = AutoOrganizeHandler(str(self.organizer_script))
        
    def setup_logging(self):
        """Configurar sistema de logging"""
        self.log_dir.mkdir(exist_ok=True)
        
        log_file = self.log_dir / 'auto_organize_watcher.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def start_watching(self):
        """Iniciar observación de archivos"""
        self.logger.info("🚀 Iniciando observador de organización automática...")
        
        # Observar directorio code
        self.observer.schedule(self.handler, str(self.base_dir), recursive=True)
        
        # Observar directorio docs
        docs_dir = self.base_dir.parent / "docs"
        if docs_dir.exists():
            self.observer.schedule(self.handler, str(docs_dir), recursive=True)
        
        # Observar directorio production-deployment
        prod_dir = self.base_dir.parent / "production-deployment"
        if prod_dir.exists():
            self.observer.schedule(self.handler, str(prod_dir), recursive=True)
        
        self.observer.start()
        
        # Guardar PID
        self.save_pid()
        
        self.logger.info("✅ Observador iniciado")
        self.logger.info(f"📁 Observando directorios:")
        self.logger.info(f"   - {self.base_dir}")
        if docs_dir.exists():
            self.logger.info(f"   - {docs_dir}")
        if prod_dir.exists():
            self.logger.info(f"   - {prod_dir}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_watching()
    
    def stop_watching(self):
        """Detener observación"""
        self.logger.info("🛑 Deteniendo observador...")
        self.observer.stop()
        self.observer.join()
        self.remove_pid()
        self.logger.info("✅ Observador detenido")
    
    def save_pid(self):
        """Guardar PID del proceso"""
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
        except Exception as e:
            self.logger.error(f"❌ Error guardando PID: {e}")
    
    def remove_pid(self):
        """Remover archivo PID"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
        except Exception as e:
            self.logger.error(f"❌ Error removiendo PID: {e}")
    
    def is_running(self) -> bool:
        """Verificar si el observador está ejecutándose"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Verificar si el proceso existe
            os.kill(pid, 0)
            return True
        except (ValueError, OSError):
            return False
    
    def stop_daemon(self):
        """Detener proceso daemon"""
        if not self.is_running():
            self.logger.info("ℹ️ Observador no está ejecutándose")
            return
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            os.kill(pid, signal.SIGTERM)
            self.logger.info(f"🛑 Señal de detención enviada al PID {pid}")
            
            # Esperar un poco y verificar
            time.sleep(2)
            if self.is_running():
                os.kill(pid, signal.SIGKILL)
                self.logger.info("🔨 Proceso terminado forzadamente")
            
        except Exception as e:
            self.logger.error(f"❌ Error deteniendo daemon: {e}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Observador automático de organización de archivos')
    parser.add_argument('--daemon', action='store_true', help='Ejecutar en segundo plano')
    parser.add_argument('--stop', action='store_true', help='Detener observador daemon')
    parser.add_argument('--status', action='store_true', help='Verificar estado del observador')
    parser.add_argument('--base-dir', default='code', help='Directorio base para observación')
    
    args = parser.parse_args()
    
    watcher = AutoOrganizeWatcher(args.base_dir)
    
    if args.status:
        if watcher.is_running():
            print("✅ Observador está ejecutándose")
        else:
            print("❌ Observador no está ejecutándose")
        return
    
    if args.stop:
        watcher.stop_daemon()
        return
    
    if args.daemon:
        # Ejecutar en segundo plano
        if watcher.is_running():
            print("⚠️ Observador ya está ejecutándose")
            return
        
        print("🚀 Iniciando observador en segundo plano...")
        watcher.start_watching()
    else:
        # Ejecutar en primer plano
        print("🚀 PAQUETES EL CLUB v3.1 - Auto Organize Watcher")
        print("=" * 60)
        print("📁 Observando cambios en archivos...")
        print("🛑 Presiona Ctrl+C para detener")
        print()
        
        watcher.start_watching()

if __name__ == "__main__":
    main()
