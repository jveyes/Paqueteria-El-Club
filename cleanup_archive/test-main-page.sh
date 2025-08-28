#!/bin/bash

# ========================================
# Test Script - Página Principal
# PAQUETES EL CLUB v3.1
# ========================================

echo "🧪 Iniciando pruebas de la página principal..."
echo "=============================================="

# Función para verificar contenido
check_content() {
    local test_name="$1"
    local expected_content="$2"
    local url="$3"
    
    echo "📋 Test: $test_name"
    
    if curl -s "$url" | grep -q "$expected_content"; then
        echo "✅ PASS: $test_name"
        return 0
    else
        echo "❌ FAIL: $test_name"
        return 1
    fi
}

# Función para verificar redirección
check_redirect() {
    local test_name="$1"
    local source_url="$2"
    local expected_redirect="$3"
    
    echo "📋 Test: $test_name"
    
    local status_code=$(curl -s -o /dev/null -w "%{http_code}" "$source_url")
    if [ "$status_code" = "302" ]; then
        echo "✅ PASS: $test_name (302 Found)"
        return 0
    else
        echo "❌ FAIL: $test_name (Status: $status_code)"
        return 1
    fi
}

# Función para verificar ausencia de contenido
check_no_content() {
    local test_name="$1"
    local unwanted_content="$2"
    local url="$3"
    
    echo "📋 Test: $test_name"
    
    if ! curl -s "$url" | grep -q "$unwanted_content"; then
        echo "✅ PASS: $test_name"
        return 0
    else
        echo "❌ FAIL: $test_name"
        return 1
    fi
}

# Contador de pruebas
total_tests=0
passed_tests=0

# Test 1: Página principal muestra formulario de anuncio
if check_content "Página Principal - Formulario de Anuncio" "Anuncia tu Paquete" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 2: Página principal tiene título correcto
if check_content "Título Correcto" "Anunciar Paquete - PAQUETES EL CLUB v3.1" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 3: Formulario tiene campo Nombre del Cliente
if check_content "Campo Nombre del Cliente" "Nombre del Cliente" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 4: Formulario tiene campo Número de Guía
if check_content "Campo Número de Guía" "Número de Guía" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 5: Formulario tiene campo Teléfono del Cliente
if check_content "Campo Teléfono del Cliente" "Teléfono del Cliente" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 6: Formulario tiene términos y condiciones
if check_content "Términos y Condiciones" "Acepto los términos y condiciones" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 7: No hay barra de búsqueda
if check_no_content "Sin Barra de Búsqueda" "Buscar paquetes" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 8: Header tiene ancho completo
if check_content "Header Ancho Completo" "w-full" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 9: Ruta /customers redirige
if check_redirect "Redirección /customers" "http://localhost/customers" "302"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 10: Botón de anunciar paquete
if check_content "Botón Anunciar Paquete" "Anunciar Paquete" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 11: Colores PAPYRUS aplicados
if check_content "Colores PAPYRUS" "papyrus-blue" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

# Test 12: Footer sticky
if check_content "Footer Sticky" "flex-shrink-0" "http://localhost/"; then
    ((passed_tests++))
fi
((total_tests++))

echo ""
echo "=============================================="
echo "📊 Resumen de Pruebas"
echo "=============================================="
echo "Total de pruebas: $total_tests"
echo "Pruebas exitosas: $passed_tests"
echo "Pruebas fallidas: $((total_tests - passed_tests))"

if [ $passed_tests -eq $total_tests ]; then
    echo "🎉 ¡Todas las pruebas pasaron exitosamente!"
    exit 0
else
    echo "⚠️  Algunas pruebas fallaron"
    exit 1
fi
