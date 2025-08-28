#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Auto Organize Files
# ========================================
#
# 🎯 OBJETIVO: Organizar archivos automáticamente según patrones
# 📅 FECHA: 2025-08-27
# 👤 AUTOR: Sistema Automático
# 🔄 VERSIÓN: 1.0.0
#
# 📋 USO:
#   python3 auto_organize_files.py                    # Organizar todos los archivos
#   python3 auto_organize_files.py --check            # Solo verificar estructura
#   python3 auto_organize_files.py --report           # Generar reporte
#   python3 auto_organize_files.py --move-only        # Solo mover archivos
#
# 📊 RESULTADOS:
#   - Log: code/logs/auto_organize.log
#   - Reporte: code/TEST/reports/file_organization_report.md
#   - Historial: code/logs/organization_history.json
#
# ⚠️ DEPENDENCIAS:
#   - Python 3.8+
#   - pathlib
#   - argparse
#   - json
#   - datetime
#
# ========================================

import os
import sys
import json
import shutil
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class FileOrganizer:
    """Organizador automático de archivos basado en patrones"""
    
    def __init__(self, base_dir: str = "code"):
        # Si estamos ejecutando desde SCRIPTS/, ajustar la ruta
        current_dir = Path.cwd()
        if current_dir.name == "SCRIPTS":
            self.base_dir = current_dir.parent
            self.project_root = self.base_dir.parent
        else:
            self.base_dir = Path(base_dir)
            self.project_root = self.base_dir.parent
        
        # Definir patrones de organización
        self.patterns = {
            'tests': {
                'patterns': [
                    'test_*.py', '*_test.py', 'test_*.html', '*_test.html',
                    'test_*.sh', '*_test.sh', 'test_*.js', '*_test.js'
                ],
                'target_dir': self.base_dir / 'TEST',
                'description': 'Archivos de pruebas y tests'
            },
            'scripts': {
                'patterns': [
                    '*.sh', '*_script.py', 'setup_*.py', 'deploy_*.py',
                    '*_runner.py', '*_automation.py', '*_tool.py', '*_helper.py'
                ],
                'target_dir': self.base_dir / 'SCRIPTS',
                'description': 'Scripts de automatización y herramientas'
            },
            'deployment_docs': {
                'patterns': [
                    '*_GUIDE.md', '*_COMPLETADO.md', '*_LIGHTSAIL.md',
                    '*_DEPLOYMENT.md', '*_AWS.md', '*_PRODUCTION.md',
                    '*_STAGING.md', '*_ENVIRONMENT.md'
                ],
                'target_dir': self.project_root / 'docs' / 'deployment-docs',
                'description': 'Documentación de deployment'
            },
            'general_docs': {
                'patterns': [
                    '*_FIXES.md', '*_SUMMARY.md', '*_ANALISIS.md',
                    '*_SOLUTION.md', '*_REPORT.md', '*_DOCUMENTATION.md',
                    '*_README.md', '*_CHANGELOG.md'
                ],
                'target_dir': self.project_root / 'docs',
                'description': 'Documentación general'
            },
            'config': {
                'patterns': [
                    '*.config', '*.conf', 'env_*', 'config_*',
                    'settings_*', '*_config.py', '*_settings.py'
                ],
                'target_dir': self.base_dir / 'config',
                'description': 'Archivos de configuración'
            }
        }
        
        # Configurar logging
        self.setup_logging()
        
        # Historial de movimientos
        self.moved_files = []
        self.errors = []
        
    def setup_logging(self):
        """Configurar sistema de logging"""
        log_dir = self.base_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / 'auto_organize.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def match_pattern(self, filename: str, patterns: List[str]) -> bool:
        """Verificar si un archivo coincide con un patrón"""
        import fnmatch
        
        for pattern in patterns:
            if fnmatch.fnmatch(filename, pattern):
                return True
        return False
    
    def get_target_directory(self, file_path: Path) -> Optional[Path]:
        """Determinar el directorio destino para un archivo"""
        filename = file_path.name
        
        for category, config in self.patterns.items():
            if self.match_pattern(filename, config['patterns']):
                return config['target_dir']
        
        return None
    
    def is_in_correct_location(self, file_path: Path) -> bool:
        """Verificar si un archivo está en la ubicación correcta"""
        target_dir = self.get_target_directory(file_path)
        if not target_dir:
            return True  # Si no hay patrón, asumir que está bien
        
        return file_path.parent == target_dir
    
    def find_misplaced_files(self) -> List[Path]:
        """Encontrar archivos que están en ubicaciones incorrectas"""
        misplaced_files = []
        
        # Buscar en el directorio base y subdirectorios
        for file_path in self.base_dir.rglob('*'):
            if file_path.is_file():
                # Excluir archivos en directorios que ya están organizados
                if any(organized_dir in file_path.parts for organized_dir in ['TEST', 'SCRIPTS', 'config']):
                    continue
                
                if not self.is_in_correct_location(file_path):
                    misplaced_files.append(file_path)
        
        # Buscar en docs también
        docs_dir = self.project_root / 'docs'
        if docs_dir.exists():
            for file_path in docs_dir.rglob('*'):
                if file_path.is_file():
                    if not self.is_in_correct_location(file_path):
                        misplaced_files.append(file_path)
        
        return misplaced_files
    
    def create_directory_if_not_exists(self, directory: Path):
        """Crear directorio si no existe"""
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"📁 Directorio creado: {directory}")
    
    def move_file_safely(self, source: Path, target_dir: Path) -> bool:
        """Mover archivo de forma segura"""
        try:
            # Crear directorio destino si no existe
            self.create_directory_if_not_exists(target_dir)
            
            # Definir ruta destino
            target_path = target_dir / source.name
            
            # Verificar si ya existe un archivo con el mismo nombre
            if target_path.exists():
                # Crear nombre único
                counter = 1
                while target_path.exists():
                    name_parts = source.stem, f"_{counter}", source.suffix
                    target_path = target_dir / "".join(name_parts)
                    counter += 1
                
                self.logger.warning(f"⚠️ Archivo renombrado: {source.name} → {target_path.name}")
            
            # Mover archivo
            shutil.move(str(source), str(target_path))
            
            # Registrar movimiento
            self.moved_files.append({
                'source': str(source),
                'target': str(target_path),
                'timestamp': datetime.now().isoformat(),
                'category': self.get_category_for_file(source)
            })
            
            self.logger.info(f"✅ Archivo movido: {source} → {target_path}")
            return True
            
        except Exception as e:
            error_msg = f"❌ Error moviendo {source}: {e}"
            self.logger.error(error_msg)
            self.errors.append({
                'file': str(source),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def get_category_for_file(self, file_path: Path) -> str:
        """Obtener categoría de un archivo"""
        filename = file_path.name
        
        for category, config in self.patterns.items():
            if self.match_pattern(filename, config['patterns']):
                return category
        
        return 'unknown'
    
    def organize_files(self, dry_run: bool = False) -> Dict:
        """Organizar archivos según patrones"""
        self.logger.info("🚀 Iniciando organización automática de archivos...")
        
        misplaced_files = self.find_misplaced_files()
        
        if not misplaced_files:
            self.logger.info("✅ Todos los archivos están en su lugar correcto")
            return {
                'status': 'success',
                'files_moved': 0,
                'errors': 0,
                'message': 'No se encontraron archivos para mover'
            }
        
        self.logger.info(f"📋 Encontrados {len(misplaced_files)} archivos para organizar")
        
        moved_count = 0
        error_count = 0
        
        for file_path in misplaced_files:
            target_dir = self.get_target_directory(file_path)
            
            if target_dir:
                if dry_run:
                    self.logger.info(f"🔍 [DRY RUN] Movería: {file_path} → {target_dir}")
                else:
                    if self.move_file_safely(file_path, target_dir):
                        moved_count += 1
                    else:
                        error_count += 1
            else:
                self.logger.warning(f"⚠️ No se encontró patrón para: {file_path}")
        
        # Guardar historial
        if not dry_run:
            self.save_history()
        
        return {
            'status': 'success' if error_count == 0 else 'partial',
            'files_moved': moved_count,
            'errors': error_count,
            'total_files': len(misplaced_files)
        }
    
    def save_history(self):
        """Guardar historial de movimientos"""
        history_file = self.base_dir / 'logs' / 'organization_history.json'
        
        try:
            # Cargar historial existente
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Agregar nuevos movimientos
            history.extend(self.moved_files)
            
            # Guardar historial actualizado
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📝 Historial guardado: {history_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Error guardando historial: {e}")
    
    def generate_report(self) -> str:
        """Generar reporte de organización"""
        report_dir = self.base_dir / 'TEST' / 'reports'
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / 'file_organization_report.md'
        
        report_content = f"""# 📁 Reporte de Organización de Archivos - PAQUETES EL CLUB v3.1

## 📊 **Resumen de Organización**

**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Estado**: {'✅ Completado' if not self.errors else '⚠️ Con errores'}  
**Archivos movidos**: {len(self.moved_files)}  
**Errores**: {len(self.errors)}

---

## 📋 **Archivos Movidos**

"""
        
        if self.moved_files:
            for move in self.moved_files:
                report_content += f"""### 📄 {Path(move['source']).name}
- **Desde**: `{move['source']}`
- **Hacia**: `{move['target']}`
- **Categoría**: {move['category']}
- **Fecha**: {move['timestamp']}

"""
        else:
            report_content += "No se movieron archivos.\n\n"
        
        if self.errors:
            report_content += """## ❌ **Errores Encontrados**

"""
            for error in self.errors:
                report_content += f"""### ⚠️ Error en {Path(error['file']).name}
- **Archivo**: `{error['file']}`
- **Error**: {error['error']}
- **Fecha**: {error['timestamp']}

"""
        
        report_content += f"""## 📈 **Estadísticas**

- **Total de archivos procesados**: {len(self.moved_files) + len(self.errors)}
- **Archivos movidos exitosamente**: {len(self.moved_files)}
- **Errores encontrados**: {len(self.errors)}
- **Tasa de éxito**: {(len(self.moved_files) / (len(self.moved_files) + len(self.errors)) * 100):.1f}%

---

## 🎯 **Recomendaciones**

"""
        
        if self.errors:
            report_content += """1. **Revisar errores**: Verificar los archivos que no se pudieron mover
2. **Permisos**: Asegurar permisos de escritura en directorios destino
3. **Archivos en uso**: Verificar que los archivos no estén siendo utilizados
"""
        else:
            report_content += """1. **Mantenimiento**: Ejecutar organización periódicamente
2. **Patrones**: Revisar y actualizar patrones según necesidades
3. **Documentación**: Mantener documentación actualizada
"""
        
        report_content += f"""
---

**Reporte generado automáticamente por el sistema de organización de archivos**  
**PAQUETES EL CLUB v3.1** - {datetime.now().strftime('%Y-%m-%d')}
"""
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info(f"📊 Reporte generado: {report_file}")
            return str(report_file)
            
        except Exception as e:
            self.logger.error(f"❌ Error generando reporte: {e}")
            return ""
    
    def check_structure(self) -> Dict:
        """Verificar estructura actual sin mover archivos"""
        self.logger.info("🔍 Verificando estructura de archivos...")
        
        misplaced_files = self.find_misplaced_files()
        
        structure_report = {
            'total_files_checked': len(list(self.base_dir.rglob('*'))),
            'misplaced_files': len(misplaced_files),
            'files_details': []
        }
        
        for file_path in misplaced_files:
            target_dir = self.get_target_directory(file_path)
            structure_report['files_details'].append({
                'file': str(file_path),
                'current_location': str(file_path.parent),
                'suggested_location': str(target_dir) if target_dir else 'No pattern found',
                'category': self.get_category_for_file(file_path)
            })
        
        return structure_report

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Organizador automático de archivos para PAQUETES EL CLUB v3.1')
    parser.add_argument('--check', action='store_true', help='Solo verificar estructura sin mover archivos')
    parser.add_argument('--report', action='store_true', help='Generar reporte de organización')
    parser.add_argument('--dry-run', action='store_true', help='Simular organización sin mover archivos')
    parser.add_argument('--base-dir', default='code', help='Directorio base para organización')
    
    args = parser.parse_args()
    
    print("🚀 PAQUETES EL CLUB v3.1 - Auto Organize Files")
    print("=" * 60)
    
    organizer = FileOrganizer(args.base_dir)
    
    if args.check:
        # Solo verificar estructura
        structure = organizer.check_structure()
        print(f"\n📊 Estructura actual:")
        print(f"   Archivos verificados: {structure['total_files_checked']}")
        print(f"   Archivos fuera de lugar: {structure['misplaced_files']}")
        
        if structure['files_details']:
            print(f"\n📋 Archivos que necesitan organización:")
            for file_detail in structure['files_details']:
                print(f"   📄 {Path(file_detail['file']).name}")
                print(f"      Actual: {file_detail['current_location']}")
                print(f"      Sugerido: {file_detail['suggested_location']}")
                print()
    
    elif args.report:
        # Generar reporte
        report_file = organizer.generate_report()
        if report_file:
            print(f"📊 Reporte generado: {report_file}")
        else:
            print("❌ Error generando reporte")
    
    else:
        # Organizar archivos
        result = organizer.organize_files(dry_run=args.dry_run)
        
        print(f"\n📈 Resultados:")
        print(f"   Estado: {result['status']}")
        print(f"   Archivos movidos: {result['files_moved']}")
        print(f"   Errores: {result['errors']}")
        
        if result['files_moved'] > 0:
            print(f"\n📊 Generando reporte...")
            report_file = organizer.generate_report()
            if report_file:
                print(f"📄 Reporte: {report_file}")
    
    print("\n✅ Organización completada")

if __name__ == "__main__":
    main()
