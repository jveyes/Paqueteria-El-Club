#!/usr/bin/env python3
"""
Script de Pruebas Exhaustivas para el Frontend - PAQUETES EL CLUB v3.1
=====================================================================

Este script realiza pruebas exhaustivas a la vista http://localhost/ para verificar:
- Validaciones de campos del formulario
- Manejo de errores del lado del cliente
- Respuestas del servidor
- Casos edge y límites
- Experiencia del usuario

Autor: JEMAVI
Fecha: 2024
"""

import requests
import json
import time
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TestCase:
    """Estructura para casos de prueba"""
    name: str
    description: str
    data: Dict[str, Any]
    expected_status: int
    expected_errors: List[str]
    category: str

class FrontendComprehensiveTest:
    """Clase principal para pruebas del frontend"""
    
    def __init__(self):
        self.base_url = "http://localhost"
        self.api_url = f"{self.base_url}/api/announcements/"
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Registra resultado de prueba"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            "timestamp": timestamp,
            "test": test_name,
            "status": status,
            "details": details
        }
        self.test_results.append(result)
        print(f"[{timestamp}] {status.upper()}: {test_name}")
        if details:
            print(f"    → {details}")
    
    def test_frontend_accessibility(self):
        """Prueba 1: Accesibilidad del frontend"""
        print("\n" + "="*60)
        print("PRUEBA 1: ACCESIBILIDAD DEL FRONTEND")
        print("="*60)
        
        try:
            # Verificar que la página principal carga
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                self.log_test("Página principal carga", "PASS", f"Status: {response.status_code}")
                
                # Verificar contenido HTML
                if "announcementForm" in response.text:
                    self.log_test("Formulario presente", "PASS", "Formulario de anuncio encontrado")
                else:
                    self.log_test("Formulario presente", "FAIL", "Formulario no encontrado")
                
                # Verificar campos requeridos
                required_fields = ["customer_name", "guide_number", "phone_number", "terms_conditions"]
                for field in required_fields:
                    if f'id="{field}"' in response.text:
                        self.log_test(f"Campo {field} presente", "PASS", f"Campo {field} encontrado")
                    else:
                        self.log_test(f"Campo {field} presente", "FAIL", f"Campo {field} no encontrado")
                        
            else:
                self.log_test("Página principal carga", "FAIL", f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Accesibilidad del frontend", "ERROR", str(e))
    
    def test_customer_name_validations(self):
        """Prueba 2: Validaciones del campo Nombre del Cliente"""
        print("\n" + "="*60)
        print("PRUEBA 2: VALIDACIONES - NOMBRE DEL CLIENTE")
        print("="*60)
        
        test_cases = [
            TestCase(
                name="Nombre vacío",
                description="Enviar nombre vacío",
                data={"customer_name": "", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=422,
                expected_errors=["El nombre del cliente es requerido"],
                category="validation"
            ),
            TestCase(
                name="Nombre con espacios",
                description="Enviar solo espacios en blanco",
                data={"customer_name": "   ", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=422,
                expected_errors=["El nombre del cliente es requerido"],
                category="validation"
            ),
            TestCase(
                name="Nombre válido corto",
                description="Nombre de 2 caracteres",
                data={"customer_name": "Jo", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Nombre válido largo",
                description="Nombre de 50 caracteres",
                data={"customer_name": "Juan Carlos Rodríguez Martínez de la Cruz y Fernández", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Nombre con caracteres especiales",
                description="Nombre con acentos y ñ",
                data={"customer_name": "María José Ñoño", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Nombre con números",
                description="Nombre que incluye números",
                data={"customer_name": "Juan123", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Nombre con símbolos",
                description="Nombre con símbolos especiales",
                data={"customer_name": "Juan-Carlos", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            )
        ]
        
        for test_case in test_cases:
            try:
                response = self.session.post(self.api_url, json=test_case.data)
                
                if response.status_code == test_case.expected_status:
                    self.log_test(test_case.name, "PASS", f"Status: {response.status_code}")
                else:
                    self.log_test(test_case.name, "FAIL", f"Expected: {test_case.expected_status}, Got: {response.status_code}")
                    
            except Exception as e:
                self.log_test(test_case.name, "ERROR", str(e))
    
    def test_guide_number_validations(self):
        """Prueba 3: Validaciones del campo Número de Guía"""
        print("\n" + "="*60)
        print("PRUEBA 3: VALIDACIONES - NÚMERO DE GUÍA")
        print("="*60)
        
        test_cases = [
            TestCase(
                name="Guía vacía",
                description="Enviar número de guía vacío",
                data={"customer_name": "Juan Pérez", "guide_number": "", "phone_number": "3001234567"},
                expected_status=422,
                expected_errors=["El número de guía es requerido"],
                category="validation"
            ),
            TestCase(
                name="Guía muy corta",
                description="Guía de menos de 5 caracteres",
                data={"customer_name": "Juan Pérez", "guide_number": "1234", "phone_number": "3001234567"},
                expected_status=422,
                expected_errors=["El número de guía debe tener al menos 5 caracteres"],
                category="validation"
            ),
            TestCase(
                name="Guía mínima válida",
                description="Guía de exactamente 5 caracteres",
                data={"customer_name": "Juan Pérez", "guide_number": "12345", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Guía larga válida",
                description="Guía de 20 caracteres",
                data={"customer_name": "Juan Pérez", "guide_number": "12345678901234567890", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Guía con letras",
                description="Guía que incluye letras",
                data={"customer_name": "Juan Pérez", "guide_number": "ABC123DEF", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Guía con caracteres especiales",
                description="Guía con guiones y puntos",
                data={"customer_name": "Juan Pérez", "guide_number": "123-456.789", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Guía duplicada",
                description="Intentar usar una guía ya existente",
                data={"customer_name": "María López", "guide_number": "123456789", "phone_number": "3001234567"},
                expected_status=422,
                expected_errors=["Ya existe un anuncio con este número de guía"],
                category="validation"
            )
        ]
        
        for test_case in test_cases:
            try:
                response = self.session.post(self.api_url, json=test_case.data)
                
                if response.status_code == test_case.expected_status:
                    self.log_test(test_case.name, "PASS", f"Status: {response.status_code}")
                else:
                    self.log_test(test_case.name, "FAIL", f"Expected: {test_case.expected_status}, Got: {response.status_code}")
                    
            except Exception as e:
                self.log_test(test_case.name, "ERROR", str(e))
    
    def test_phone_number_validations(self):
        """Prueba 4: Validaciones del campo Teléfono"""
        print("\n" + "="*60)
        print("PRUEBA 4: VALIDACIONES - TELÉFONO")
        print("="*60)
        
        test_cases = [
            TestCase(
                name="Teléfono vacío",
                description="Enviar teléfono vacío",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": ""},
                expected_status=422,
                expected_errors=["El teléfono del cliente es requerido"],
                category="validation"
            ),
            TestCase(
                name="Teléfono muy corto",
                description="Teléfono de menos de 7 dígitos",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": "123456"},
                expected_status=422,
                expected_errors=["El teléfono debe tener al menos 7 dígitos"],
                category="validation"
            ),
            TestCase(
                name="Teléfono mínimo válido",
                description="Teléfono de exactamente 7 dígitos",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": "1234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Teléfono celular colombiano",
                description="Teléfono celular típico colombiano",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Teléfono con formato",
                description="Teléfono con guiones y espacios",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": "300-123-4567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Teléfono con paréntesis",
                description="Teléfono con paréntesis",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": "(300) 123-4567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Teléfono internacional",
                description="Teléfono con código de país",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": "+57 300 123 4567"},
                expected_status=201,
                expected_errors=[],
                category="validation"
            ),
            TestCase(
                name="Teléfono muy largo",
                description="Teléfono de más de 20 caracteres",
                data={"customer_name": "Juan Pérez", "guide_number": "987654321", "phone_number": "300123456789012345678"},
                expected_status=422,
                expected_errors=["El teléfono no puede exceder 20 caracteres"],
                category="validation"
            )
        ]
        
        for test_case in test_cases:
            try:
                response = self.session.post(self.api_url, json=test_case.data)
                
                if response.status_code == test_case.expected_status:
                    self.log_test(test_case.name, "PASS", f"Status: {response.status_code}")
                else:
                    self.log_test(test_case.name, "FAIL", f"Expected: {test_case.expected_status}, Got: {response.status_code}")
                    
            except Exception as e:
                self.log_test(test_case.name, "ERROR", str(e))
    
    def test_terms_conditions_validations(self):
        """Prueba 5: Validaciones de Términos y Condiciones"""
        print("\n" + "="*60)
        print("PRUEBA 5: VALIDACIONES - TÉRMINOS Y CONDICIONES")
        print("="*60)
        
        test_cases = [
            TestCase(
                name="Términos no aceptados",
                description="Enviar sin aceptar términos",
                data={"customer_name": "Juan Pérez", "guide_number": "111111111", "phone_number": "3001234567", "terms_conditions": False},
                expected_status=422,
                expected_errors=["Debe aceptar los términos y condiciones"],
                category="validation"
            ),
            TestCase(
                name="Términos aceptados",
                description="Enviar con términos aceptados",
                data={"customer_name": "Juan Pérez", "guide_number": "111111111", "phone_number": "3001234567", "terms_conditions": True},
                expected_status=201,
                expected_errors=[],
                category="validation"
            )
        ]
        
        for test_case in test_cases:
            try:
                response = self.session.post(self.api_url, json=test_case.data)
                
                if response.status_code == test_case.expected_status:
                    self.log_test(test_case.name, "PASS", f"Status: {response.status_code}")
                else:
                    self.log_test(test_case.name, "FAIL", f"Expected: {test_case.expected_status}, Got: {response.status_code}")
                    
            except Exception as e:
                self.log_test(test_case.name, "ERROR", str(e))
    
    def test_edge_cases(self):
        """Prueba 6: Casos Edge y Límites"""
        print("\n" + "="*60)
        print("PRUEBA 6: CASOS EDGE Y LÍMITES")
        print("="*60)
        
        test_cases = [
            TestCase(
                name="Datos completamente vacíos",
                description="Enviar formulario completamente vacío",
                data={},
                expected_status=422,
                expected_errors=["El nombre del cliente es requerido"],
                category="edge"
            ),
            TestCase(
                name="Solo un campo lleno",
                description="Llenar solo el nombre",
                data={"customer_name": "Juan Pérez"},
                expected_status=422,
                expected_errors=["El número de guía es requerido"],
                category="edge"
            ),
            TestCase(
                name="Caracteres especiales extremos",
                description="Usar caracteres Unicode especiales",
                data={"customer_name": "José María 🚀", "guide_number": "12345", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="edge"
            ),
            TestCase(
                name="SQL Injection básico",
                description="Intentar inyección SQL en nombre",
                data={"customer_name": "'; DROP TABLE packages; --", "guide_number": "12345", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="security"
            ),
            TestCase(
                name="XSS básico",
                description="Intentar XSS en nombre",
                data={"customer_name": "<script>alert('XSS')</script>", "guide_number": "12345", "phone_number": "3001234567"},
                expected_status=201,
                expected_errors=[],
                category="security"
            ),
            TestCase(
                name="Datos muy largos",
                description="Enviar datos extremadamente largos",
                data={"customer_name": "A" * 1000, "guide_number": "B" * 1000, "phone_number": "C" * 1000},
                expected_status=422,
                expected_errors=["Datos demasiado largos"],
                category="edge"
            )
        ]
        
        for test_case in test_cases:
            try:
                response = self.session.post(self.api_url, json=test_case.data)
                
                if response.status_code == test_case.expected_status:
                    self.log_test(test_case.name, "PASS", f"Status: {response.status_code}")
                else:
                    self.log_test(test_case.name, "FAIL", f"Expected: {test_case.expected_status}, Got: {response.status_code}")
                    
            except Exception as e:
                self.log_test(test_case.name, "ERROR", str(e))
    
    def test_server_responses(self):
        """Prueba 7: Respuestas del Servidor"""
        print("\n" + "="*60)
        print("PRUEBA 7: RESPUESTAS DEL SERVIDOR")
        print("="*60)
        
        # Prueba de respuesta exitosa
        try:
            valid_data = {
                "customer_name": "Test User",
                "guide_number": "TEST123456",
                "phone_number": "3001234567"
            }
            
            response = self.session.post(self.api_url, json=valid_data)
            
            if response.status_code == 201:
                self.log_test("Respuesta exitosa", "PASS", f"Status: {response.status_code}")
                
                # Verificar estructura de respuesta
                try:
                    response_data = response.json()
                    if "tracking_number" in response_data:
                        self.log_test("Tracking number generado", "PASS", f"Tracking: {response_data['tracking_number']}")
                    else:
                        self.log_test("Tracking number generado", "FAIL", "No se encontró tracking_number")
                        
                    if "announced_at" in response_data:
                        self.log_test("Fecha de anuncio", "PASS", f"Fecha: {response_data['announced_at']}")
                    else:
                        self.log_test("Fecha de anuncio", "FAIL", "No se encontró announced_at")
                        
                except json.JSONDecodeError:
                    self.log_test("Respuesta JSON válida", "FAIL", "Respuesta no es JSON válido")
                    
            else:
                self.log_test("Respuesta exitosa", "FAIL", f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Respuesta del servidor", "ERROR", str(e))
    
    def test_error_handling(self):
        """Prueba 8: Manejo de Errores"""
        print("\n" + "="*60)
        print("PRUEBA 8: MANEJO DE ERRORES")
        print("="*60)
        
        # Prueba de método no permitido
        try:
            response = self.session.get(self.api_url)
            if response.status_code == 405:
                self.log_test("Método GET no permitido", "PASS", f"Status: {response.status_code}")
            else:
                self.log_test("Método GET no permitido", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Método GET no permitido", "ERROR", str(e))
        
        # Prueba de URL inexistente
        try:
            response = self.session.post(f"{self.base_url}/api/nonexistent/")
            if response.status_code == 404:
                self.log_test("URL inexistente", "PASS", f"Status: {response.status_code}")
            else:
                self.log_test("URL inexistente", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("URL inexistente", "ERROR", str(e))
        
        # Prueba de datos malformados
        try:
            response = self.session.post(self.api_url, data="invalid json", headers={"Content-Type": "application/json"})
            if response.status_code == 422:
                self.log_test("JSON malformado", "PASS", f"Status: {response.status_code}")
            else:
                self.log_test("JSON malformado", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("JSON malformado", "ERROR", str(e))
    
    def generate_report(self):
        """Genera reporte final de pruebas"""
        print("\n" + "="*60)
        print("REPORTE FINAL DE PRUEBAS")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        error_tests = len([r for r in self.test_results if r["status"] == "ERROR"])
        
        print(f"Total de pruebas: {total_tests}")
        print(f"Pruebas exitosas: {passed_tests}")
        print(f"Pruebas fallidas: {failed_tests}")
        print(f"Pruebas con error: {error_tests}")
        print(f"Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        # Mostrar pruebas fallidas
        if failed_tests > 0:
            print("\nPRUEBAS FALLIDAS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        # Mostrar errores
        if error_tests > 0:
            print("\nPRUEBAS CON ERROR:")
            for result in self.test_results:
                if result["status"] == "ERROR":
                    print(f"  - {result['test']}: {result['details']}")
        
        # Guardar reporte
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "success_rate": (passed_tests/total_tests)*100
            },
            "results": self.test_results
        }
        
        with open("docs/reports/frontend-comprehensive-test-report.md", "w", encoding="utf-8") as f:
            f.write("# Reporte de Pruebas Exhaustivas del Frontend\n\n")
            f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total de pruebas:** {total_tests}\n")
            f.write(f"**Pruebas exitosas:** {passed_tests}\n")
            f.write(f"**Pruebas fallidas:** {failed_tests}\n")
            f.write(f"**Pruebas con error:** {error_tests}\n")
            f.write(f"**Tasa de éxito:** {(passed_tests/total_tests)*100:.1f}%\n\n")
            
            f.write("## Detalles de Pruebas\n\n")
            for result in self.test_results:
                status_emoji = {"PASS": "✅", "FAIL": "❌", "ERROR": "⚠️"}
                f.write(f"- {status_emoji.get(result['status'], '❓')} **{result['test']}** ({result['status']})\n")
                if result['details']:
                    f.write(f"  - {result['details']}\n")
                f.write("\n")
        
        print(f"\nReporte guardado en: docs/reports/frontend-comprehensive-test-report.md")
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("🚀 INICIANDO PRUEBAS EXHAUSTIVAS DEL FRONTEND")
        print("="*60)
        print(f"URL Base: {self.base_url}")
        print(f"API URL: {self.api_url}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Ejecutar todas las pruebas
        self.test_frontend_accessibility()
        self.test_customer_name_validations()
        self.test_guide_number_validations()
        self.test_phone_number_validations()
        self.test_terms_conditions_validations()
        self.test_edge_cases()
        self.test_server_responses()
        self.test_error_handling()
        
        # Generar reporte
        self.generate_report()

if __name__ == "__main__":
    tester = FrontendComprehensiveTest()
    tester.run_all_tests()
