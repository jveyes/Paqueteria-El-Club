#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAQUETES EL CLUB v3.1 - Health Check Avanzado
==============================================

Este script realiza un health check completo de la aplicación, validando:
- Conectividad a base de datos
- Estado de servicios Docker
- Funcionalidad de la API
- Estructura de archivos críticos
- Configuración de la aplicación
"""

import sys
import os
import requests
import subprocess
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

# Agregar el directorio src al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'code', 'src')
sys.path.insert(0, src_path)

try:
    from sqlalchemy import create_engine, text
    from config import settings
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
    sys.exit(1)

@dataclass
class HealthCheckResult:
    """Resultado de un health check específico"""
    name: str
    status: bool
    message: str
    details: Dict[str, Any] = None

class AdvancedHealthChecker:
    """Health checker avanzado para la aplicación"""
    
    def __init__(self):
        self.results: List[HealthCheckResult] = []
        self.base_url = "http://localhost"
        
    def check_docker_services(self) -> HealthCheckResult:
        """Verificar estado de servicios Docker"""
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}\t{{.Status}}'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                services = result.stdout.strip().split('\n')
                running_services = [s for s in services if 'Up' in s]
                
                expected_services = [
                    'paqueteria_v31_app',
                    'paqueteria_v31_nginx',
                    'paqueteria_v31_redis',
                    'paqueteria_v31_celery_worker'
                ]
                
                missing_services = []
                for service in expected_services:
                    if not any(service in s for s in running_services):
                        missing_services.append(service)
                
                if missing_services:
                    return HealthCheckResult(
                        name="Docker Services",
                        status=False,
                        message=f"Servicios faltantes: {', '.join(missing_services)}",
                        details={'running': running_services, 'missing': missing_services}
                    )
                else:
                    return HealthCheckResult(
                        name="Docker Services",
                        status=True,
                        message=f"Todos los servicios ejecutándose ({len(running_services)} servicios)",
                        details={'running': running_services}
                    )
            else:
                return HealthCheckResult(
                    name="Docker Services",
                    status=False,
                    message="Error ejecutando comando Docker",
                    details={'error': result.stderr}
                )
                
        except Exception as e:
            return HealthCheckResult(
                name="Docker Services",
                status=False,
                message=f"Error verificando servicios Docker: {e}"
            )
    
    def check_database_connection(self) -> HealthCheckResult:
        """Verificar conectividad a la base de datos"""
        try:
            engine = create_engine(settings.database_url)
            with engine.connect() as conn:
                # Verificar conexión básica
                result = conn.execute(text("SELECT 1"))
                if result.fetchone():
                    # Verificar tablas críticas
                    tables_result = conn.execute(text("""
                        SELECT table_name FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        ORDER BY table_name
                    """))
                    tables = [row[0] for row in tables_result]
                    
                    critical_tables = ['users', 'packages', 'customers', 'files']
                    missing_tables = [t for t in critical_tables if t not in tables]
                    
                    if missing_tables:
                        return HealthCheckResult(
                            name="Database Connection",
                            status=False,
                            message=f"Tablas críticas faltantes: {', '.join(missing_tables)}",
                            details={'tables': tables, 'missing': missing_tables}
                        )
                    else:
                        return HealthCheckResult(
                            name="Database Connection",
                            status=True,
                            message=f"Conectado correctamente ({len(tables)} tablas)",
                            details={'tables': tables}
                        )
                        
        except Exception as e:
            return HealthCheckResult(
                name="Database Connection",
                status=False,
                message=f"Error de conexión: {e}"
            )
    
    def check_api_endpoints(self) -> HealthCheckResult:
        """Verificar endpoints de la API"""
        endpoints = [
            ('/health', 'Health Check'),
            ('/api/auth/check', 'Auth Check'),
            ('/', 'Home Page'),
            ('/search', 'Search Page'),
            ('/login', 'Login Page')
        ]
        
        failed_endpoints = []
        successful_endpoints = []
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    successful_endpoints.append(f"{name} ({endpoint})")
                else:
                    failed_endpoints.append(f"{name} ({endpoint}) - Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{name} ({endpoint}) - Error: {e}")
        
        if failed_endpoints:
            return HealthCheckResult(
                name="API Endpoints",
                status=False,
                message=f"Endpoints fallando: {len(failed_endpoints)}",
                details={'failed': failed_endpoints, 'successful': successful_endpoints}
            )
        else:
            return HealthCheckResult(
                name="API Endpoints",
                status=True,
                message=f"Todos los endpoints funcionando ({len(successful_endpoints)} endpoints)",
                details={'successful': successful_endpoints}
            )
    
    def check_critical_files(self) -> HealthCheckResult:
        """Verificar archivos críticos de la aplicación"""
        critical_files = [
            'code/src/config.py',
            'code/src/main.py',
            'code/alembic.ini',
            'code/requirements.txt',
            'docker-compose-aws-fixed.yml'
        ]
        
        missing_files = []
        existing_files = []
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        if missing_files:
            return HealthCheckResult(
                name="Critical Files",
                status=False,
                message=f"Archivos críticos faltantes: {len(missing_files)}",
                details={'missing': missing_files, 'existing': existing_files}
            )
        else:
            return HealthCheckResult(
                name="Critical Files",
                status=True,
                message=f"Todos los archivos críticos presentes ({len(existing_files)} archivos)",
                details={'existing': existing_files}
            )
    
    def check_environment_config(self) -> HealthCheckResult:
        """Verificar configuración del entorno"""
        try:
            # Verificar variables críticas
            critical_vars = [
                'DATABASE_URL',
                'SECRET_KEY',
                'ENVIRONMENT'
            ]
            
            missing_vars = []
            for var in critical_vars:
                if not hasattr(settings, var.lower()) or not getattr(settings, var.lower()):
                    missing_vars.append(var)
            
            if missing_vars:
                return HealthCheckResult(
                    name="Environment Config",
                    status=False,
                    message=f"Variables críticas faltantes: {', '.join(missing_vars)}",
                    details={'missing': missing_vars}
                )
            else:
                return HealthCheckResult(
                    name="Environment Config",
                    status=True,
                    message="Configuración del entorno correcta",
                    details={'environment': settings.environment}
                )
                
        except Exception as e:
            return HealthCheckResult(
                name="Environment Config",
                status=False,
                message=f"Error verificando configuración: {e}"
            )
    
    def check_database_schema(self) -> HealthCheckResult:
        """Verificar esquema de la base de datos"""
        try:
            engine = create_engine(settings.database_url)
            with engine.connect() as conn:
                # Verificar columnas críticas en tablas importantes
                critical_checks = [
                    ("users", "profile_photo", "VARCHAR"),
                    ("packages", "tracking_code", "VARCHAR"),
                    ("customers", "phone", "VARCHAR")
                ]
                
                failed_checks = []
                successful_checks = []
                
                for table, column, expected_type in critical_checks:
                    try:
                        result = conn.execute(text(f"""
                            SELECT column_name, data_type 
                            FROM information_schema.columns 
                            WHERE table_name = '{table}' AND column_name = '{column}'
                        """))
                        row = result.fetchone()
                        
                        if row:
                            if expected_type.lower() in row[1].lower():
                                successful_checks.append(f"{table}.{column}")
                            else:
                                failed_checks.append(f"{table}.{column} (tipo: {row[1]})")
                        else:
                            failed_checks.append(f"{table}.{column} (no existe)")
                            
                    except Exception as e:
                        failed_checks.append(f"{table}.{column} (error: {e})")
                
                if failed_checks:
                    return HealthCheckResult(
                        name="Database Schema",
                        status=False,
                        message=f"Problemas de esquema: {len(failed_checks)}",
                        details={'failed': failed_checks, 'successful': successful_checks}
                    )
                else:
                    return HealthCheckResult(
                        name="Database Schema",
                        status=True,
                        message="Esquema de base de datos correcto",
                        details={'successful': successful_checks}
                    )
                    
        except Exception as e:
            return HealthCheckResult(
                name="Database Schema",
                status=False,
                message=f"Error verificando esquema: {e}"
            )
    
    def run_all_checks(self):
        """Ejecutar todos los health checks"""
        print("🔍 Iniciando Health Check Avanzado...")
        print("=" * 60)
        
        checks = [
            self.check_docker_services,
            self.check_database_connection,
            self.check_api_endpoints,
            self.check_critical_files,
            self.check_environment_config,
            self.check_database_schema
        ]
        
        for check_func in checks:
            result = check_func()
            self.results.append(result)
            
            status_icon = "✅" if result.status else "❌"
            print(f"{status_icon} {result.name}: {result.message}")
            
            if result.details:
                for key, value in result.details.items():
                    if isinstance(value, list) and len(value) > 0:
                        print(f"   {key}: {', '.join(value[:3])}{'...' if len(value) > 3 else ''}")
                    else:
                        print(f"   {key}: {value}")
        
        return True
    
    def generate_report(self):
        """Generar reporte de health check"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE HEALTH CHECK AVANZADO")
        print("=" * 60)
        
        total_checks = len(self.results)
        successful_checks = sum(1 for r in self.results if r.status)
        failed_checks = total_checks - successful_checks
        
        print(f"📈 Resumen General:")
        print(f"   - Total de verificaciones: {total_checks}")
        print(f"   - Verificaciones exitosas: {successful_checks}")
        print(f"   - Verificaciones fallidas: {failed_checks}")
        
        if failed_checks > 0:
            print(f"\n⚠️  VERIFICACIONES FALLIDAS:")
            for result in self.results:
                if not result.status:
                    print(f"\n   🔴 {result.name}:")
                    print(f"      - {result.message}")
                    if result.details:
                        for key, value in result.details.items():
                            print(f"      - {key}: {value}")
        else:
            print(f"\n🎉 ¡TODAS LAS VERIFICACIONES EXITOSAS!")
        
        print(f"\n📋 Estado por verificación:")
        for result in self.results:
            status = "✅" if result.status else "❌"
            print(f"   {status} {result.name}")
        
        return failed_checks == 0
    
    def suggest_fixes(self):
        """Sugerir correcciones para problemas encontrados"""
        print(f"\n🔧 SUGERENCIAS DE CORRECCIÓN:")
        
        for result in self.results:
            if not result.status:
                print(f"\n   🔴 {result.name}:")
                
                if "Docker Services" in result.name:
                    print(f"      - Verificar estado: docker ps")
                    print(f"      - Reiniciar servicios: docker-compose restart")
                
                elif "Database Connection" in result.name:
                    print(f"      - Verificar conectividad a AWS RDS")
                    print(f"      - Ejecutar: python validate-model-sync.py")
                
                elif "API Endpoints" in result.name:
                    print(f"      - Verificar logs: docker logs paqueteria_v31_app")
                    print(f"      - Reiniciar aplicación: docker restart paqueteria_v31_app")
                
                elif "Critical Files" in result.name:
                    print(f"      - Verificar estructura del proyecto")
                    print(f"      - Restaurar archivos faltantes desde Git")
                
                elif "Environment Config" in result.name:
                    print(f"      - Verificar archivos .env")
                    print(f"      - Configurar variables faltantes")
                
                elif "Database Schema" in result.name:
                    print(f"      - Ejecutar migraciones: alembic upgrade head")
                    print(f"      - Verificar modelos: python validate-model-sync.py")

def main():
    """Función principal"""
    print("🛡️  HEALTH CHECK AVANZADO")
    print("=" * 60)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checker = AdvancedHealthChecker()
    
    if checker.run_all_checks():
        success = checker.generate_report()
        checker.suggest_fixes()
        
        if success:
            print("\n🎉 ¡Health Check completado exitosamente!")
            sys.exit(0)
        else:
            print("\n⚠️  Se encontraron problemas que requieren atención")
            sys.exit(1)
    else:
        print("\n❌ Error durante el Health Check")
        sys.exit(1)

if __name__ == "__main__":
    main()
