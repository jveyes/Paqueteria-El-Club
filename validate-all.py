#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAQUETES EL CLUB v3.1 - Validador Completo del Sistema
=======================================================

Este script ejecuta todos los validadores en secuencia:
1. Validación de sincronización de modelos
2. Validación de migraciones
3. Health check avanzado
4. Genera un reporte consolidado
"""

import sys
import os
import subprocess
import time
from datetime import datetime
from typing import List, Dict, Any

class CompleteValidator:
    """Validador completo del sistema"""
    
    def __init__(self):
        self.validators = [
            {
                'name': 'Sincronización de Modelos',
                'script': 'validate-model-sync.py',
                'description': 'Valida que los modelos SQLAlchemy estén sincronizados con la BD'
            },
            {
                'name': 'Migraciones Alembic',
                'script': 'validate-migrations.py',
                'description': 'Verifica el estado de las migraciones de la base de datos'
            },
            {
                'name': 'Health Check Avanzado',
                'script': 'advanced-health-check.py',
                'description': 'Realiza un health check completo de la aplicación'
            }
        ]
        self.results: List[Dict[str, Any]] = []
        
    def run_validator(self, validator_info: Dict[str, str]) -> Dict[str, Any]:
        """Ejecutar un validador específico"""
        print(f"\n🔍 Ejecutando: {validator_info['name']}")
        print(f"📝 Descripción: {validator_info['description']}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            # Ejecutar el script de validación
            result = subprocess.run(
                [sys.executable, validator_info['script']],
                capture_output=True,
                text=True,
                timeout=120  # 2 minutos de timeout
            )
            
            execution_time = time.time() - start_time
            
            # Determinar si fue exitoso basado en el código de salida
            success = result.returncode == 0
            
            # Parsear la salida para obtener información útil
            output_lines = result.stdout.strip().split('\n')
            error_lines = result.stderr.strip().split('\n') if result.stderr else []
            
            # Buscar información clave en la salida
            summary_info = self._extract_summary_info(output_lines)
            
            result_info = {
                'name': validator_info['name'],
                'script': validator_info['script'],
                'success': success,
                'return_code': result.returncode,
                'execution_time': execution_time,
                'output': output_lines,
                'errors': error_lines,
                'summary': summary_info
            }
            
            # Mostrar resultado
            if success:
                print(f"✅ {validator_info['name']}: Completado exitosamente")
                if summary_info:
                    for key, value in summary_info.items():
                        print(f"   📊 {key}: {value}")
            else:
                print(f"❌ {validator_info['name']}: Falló (código: {result.returncode})")
                if error_lines:
                    print(f"   💥 Errores: {error_lines[0] if error_lines else 'N/A'}")
            
            return result_info
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"⏰ {validator_info['name']}: Timeout después de {execution_time:.1f}s")
            return {
                'name': validator_info['name'],
                'script': validator_info['script'],
                'success': False,
                'return_code': -1,
                'execution_time': execution_time,
                'output': [],
                'errors': ['Timeout expired'],
                'summary': {'status': 'Timeout'}
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"💥 {validator_info['name']}: Error inesperado - {e}")
            return {
                'name': validator_info['name'],
                'script': validator_info['script'],
                'success': False,
                'return_code': -1,
                'execution_time': execution_time,
                'output': [],
                'errors': [str(e)],
                'summary': {'status': 'Error inesperado'}
            }
    
    def _extract_summary_info(self, output_lines: List[str]) -> Dict[str, str]:
        """Extraer información de resumen de la salida del validador"""
        summary = {}
        
        for line in output_lines:
            line = line.strip()
            
            # Buscar patrones específicos en la salida
            if "Tablas validadas:" in line:
                summary['tablas_validadas'] = line.split(':')[1].strip()
            elif "Migraciones aplicadas:" in line:
                summary['migraciones_aplicadas'] = line.split(':')[1].strip()
            elif "Verificaciones exitosas:" in line:
                summary['verificaciones_exitosas'] = line.split(':')[1].strip()
            elif "Total de migraciones:" in line:
                summary['total_migraciones'] = line.split(':')[1].strip()
            elif "Total de verificaciones:" in line:
                summary['total_verificaciones'] = line.split(':')[1].strip()
            elif "Versión actual en BD:" in line:
                summary['version_bd'] = line.split(':')[1].strip()
        
        return summary
    
    def run_all_validators(self):
        """Ejecutar todos los validadores"""
        print("🛡️  VALIDADOR COMPLETO DEL SISTEMA")
        print("=" * 60)
        print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Validadores a ejecutar: {len(self.validators)}")
        
        total_start_time = time.time()
        
        for validator in self.validators:
            result = self.run_validator(validator)
            self.results.append(result)
            
            # Pausa entre validadores
            if validator != self.validators[-1]:  # No pausar después del último
                print("\n⏳ Esperando 2 segundos antes del siguiente validador...")
                time.sleep(2)
        
        total_execution_time = time.time() - total_start_time
        
        print(f"\n⏱️  Tiempo total de ejecución: {total_execution_time:.1f} segundos")
        
        return True
    
    def generate_consolidated_report(self):
        """Generar reporte consolidado de todos los validadores"""
        print("\n" + "=" * 60)
        print("📊 REPORTE CONSOLIDADO DE VALIDACIÓN")
        print("=" * 60)
        
        total_validators = len(self.results)
        successful_validators = sum(1 for r in self.results if r['success'])
        failed_validators = total_validators - successful_validators
        
        print(f"📈 Resumen General:")
        print(f"   - Total de validadores: {total_validators}")
        print(f"   - Validadores exitosos: {successful_validators}")
        print(f"   - Validadores fallidos: {failed_validators}")
        print(f"   - Tasa de éxito: {(successful_validators/total_validators)*100:.1f}%")
        
        if failed_validators > 0:
            print(f"\n⚠️  VALIDADORES FALLIDOS:")
            for result in self.results:
                if not result['success']:
                    print(f"\n   🔴 {result['name']}:")
                    print(f"      - Script: {result['script']}")
                    print(f"      - Código de salida: {result['return_code']}")
                    print(f"      - Tiempo de ejecución: {result['execution_time']:.1f}s")
                    if result['errors']:
                        print(f"      - Errores: {', '.join(result['errors'][:2])}")
                    if result['summary']:
                        for key, value in result['summary'].items():
                            print(f"      - {key}: {value}")
        else:
            print(f"\n🎉 ¡TODOS LOS VALIDADORES EXITOSOS!")
        
        print(f"\n📋 Estado por validador:")
        for result in self.results:
            status = "✅" if result['success'] else "❌"
            time_str = f"{result['execution_time']:.1f}s"
            print(f"   {status} {result['name']} ({time_str})")
        
        return failed_validators == 0
    
    def generate_recommendations(self):
        """Generar recomendaciones basadas en los resultados"""
        print(f"\n💡 RECOMENDACIONES:")
        
        if not any(r['success'] for r in self.results):
            print("   🔴 Todos los validadores fallaron:")
            print("      - Verificar conectividad a la base de datos")
            print("      - Verificar que los servicios Docker estén ejecutándose")
            print("      - Verificar configuración del entorno")
            return
        
        # Recomendaciones específicas basadas en resultados
        for result in self.results:
            if not result['success']:
                print(f"\n   🔴 {result['name']}:")
                
                if "Sincronización de Modelos" in result['name']:
                    print("      - Ejecutar migraciones pendientes")
                    print("      - Verificar estructura de la base de datos")
                    print("      - Revisar modelos SQLAlchemy")
                
                elif "Migraciones Alembic" in result['name']:
                    print("      - Ejecutar: alembic upgrade head")
                    print("      - Verificar archivos de migración")
                    print("      - Revisar estado de la tabla alembic_version")
                
                elif "Health Check Avanzado" in result['name']:
                    print("      - Verificar servicios Docker")
                    print("      - Revisar logs de la aplicación")
                    print("      - Verificar conectividad de red")
        
        print(f"\n   🟢 Validadores exitosos:")
        successful_names = [r['name'] for r in self.results if r['success']]
        for name in successful_names:
            print(f"      - ✅ {name}")
        
        print(f"\n   📚 Próximos pasos recomendados:")
        print("      1. Resolver problemas de validadores fallidos")
        print("      2. Ejecutar validadores individuales para más detalles")
        print("      3. Implementar correcciones sugeridas")
        print("      4. Re-ejecutar validación completa")
    
    def save_report_to_file(self):
        """Guardar reporte en archivo"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"validation_report_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE VALIDACIÓN COMPLETA\n")
                f.write("=" * 50 + "\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for result in self.results:
                    f.write(f"VALIDADOR: {result['name']}\n")
                    f.write(f"Estado: {'✅ EXITOSO' if result['success'] else '❌ FALLIDO'}\n")
                    f.write(f"Script: {result['script']}\n")
                    f.write(f"Tiempo: {result['execution_time']:.1f}s\n")
                    f.write(f"Código: {result['return_code']}\n")
                    
                    if result['summary']:
                        f.write("Resumen:\n")
                        for key, value in result['summary'].items():
                            f.write(f"  - {key}: {value}\n")
                    
                    if result['errors']:
                        f.write("Errores:\n")
                        for error in result['errors']:
                            f.write(f"  - {error}\n")
                    
                    f.write("\n" + "-" * 30 + "\n\n")
            
            print(f"\n📄 Reporte guardado en: {filename}")
            
        except Exception as e:
            print(f"\n⚠️  Error guardando reporte: {e}")

def main():
    """Función principal"""
    validator = CompleteValidator()
    
    if validator.run_all_validators():
        success = validator.generate_consolidated_report()
        validator.generate_recommendations()
        validator.save_report_to_file()
        
        if success:
            print("\n🎉 ¡Validación completa exitosa!")
            print("✅ El sistema está funcionando correctamente")
            sys.exit(0)
        else:
            print("\n⚠️  Se encontraron problemas que requieren atención")
            print("🔧 Revisa las recomendaciones y ejecuta los validadores individuales")
            sys.exit(1)
    else:
        print("\n❌ Error durante la validación completa")
        sys.exit(1)

if __name__ == "__main__":
    main()
