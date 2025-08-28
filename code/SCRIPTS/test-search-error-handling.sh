#!/bin/bash

# Script de prueba para verificar el manejo de errores en la búsqueda de paquetes
# Autor: Sistema de Paquetería v3.1
# Fecha: $(date)

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Función para hacer requests HTTP
make_request() {
    local url="$1"
    local expected_status="$2"
    local description="$3"
    
    log "Probando: $description"
    
    # Hacer request y capturar status code y response
    local response=$(curl -s -w "%{http_code}" "$url" 2>/dev/null)
    local status_code="${response: -3}"
    local body="${response%???}"
    
    if [ "$status_code" = "$expected_status" ]; then
        success "Status $status_code recibido correctamente"
        if [ "$expected_status" = "404" ]; then
            if echo "$body" | grep -q "Paquete no encontrado"; then
                success "Mensaje de error correcto: 'Paquete no encontrado'"
            else
                error "Mensaje de error incorrecto o faltante"
                echo "Response body: $body"
            fi
        fi
        return 0
    else
        error "Status $status_code recibido, esperado $expected_status"
        echo "Response body: $body"
        return 1
    fi
}

# Función principal de pruebas
run_tests() {
    log "🧪 Iniciando pruebas de manejo de errores en búsqueda de paquetes..."
    echo
    
    local tests_passed=0
    local tests_failed=0
    
    # Test 1: Verificar que el servicio esté funcionando
    log "1. Verificando estado del servicio..."
    if curl -s -f "http://localhost/search" > /dev/null; then
        success "Servicio funcionando correctamente"
        ((tests_passed++))
    else
        error "Servicio no disponible"
        ((tests_failed++))
        return 1
    fi
    echo
    
    # Test 2: Código válido
    log "2. Probando código válido (YJWX)..."
    if make_request "http://localhost/api/announcements/search/package?query=YJWX" "200" "Código válido YJWX"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo
    
    # Test 3: Código inválido
    log "3. Probando código inválido (INVALID_CODE)..."
    if make_request "http://localhost/api/announcements/search/package?query=INVALID_CODE" "404" "Código inválido INVALID_CODE"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo
    
    # Test 4: Código vacío
    log "4. Probando código vacío..."
    if make_request "http://localhost/api/announcements/search/package?query=" "404" "Código vacío"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo
    
    # Test 5: Código con espacios
    log "5. Probando código con espacios..."
    if make_request "http://localhost/api/announcements/search/package?query=%20%20%20" "404" "Código con espacios"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo
    
    # Test 6: Código muy largo
    log "6. Probando código muy largo..."
    if make_request "http://localhost/api/announcements/search/package?query=CODIGOMUYLARGOQUENOEXISTE" "404" "Código muy largo"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo
    
    # Test 7: Código con caracteres especiales
    log "7. Probando código con caracteres especiales..."
    if make_request "http://localhost/api/announcements/search/package?query=ABC@123" "404" "Código con caracteres especiales"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo
    
    # Resumen de resultados
    log "📊 Resumen de pruebas:"
    success "Pruebas exitosas: $tests_passed"
    if [ $tests_failed -gt 0 ]; then
        error "Pruebas fallidas: $tests_failed"
    fi
    
    local total_tests=$((tests_passed + tests_failed))
    if [ $tests_failed -eq 0 ]; then
        success "🎉 Todas las pruebas pasaron exitosamente ($total_tests/$total_tests)"
        return 0
    else
        error "💥 Algunas pruebas fallaron ($tests_passed/$total_tests pasaron)"
        return 1
    fi
}

# Función para mostrar información del sistema
show_system_info() {
    log "📋 Información del sistema:"
    echo "   - URL de búsqueda: http://localhost/search"
    echo "   - API endpoint: http://localhost/api/announcements/search/package"
    echo "   - Códigos de prueba válidos: YJWX, Z7UH, J1NK, etc."
    echo "   - Códigos de prueba inválidos: INVALID_CODE, CODIGO_INEXISTENTE, etc."
    echo
}

# Función para mostrar instrucciones de uso
show_usage() {
    echo "Uso: $0 [opciones]"
    echo
    echo "Opciones:"
    echo "  -h, --help     Mostrar esta ayuda"
    echo "  -v, --verbose  Modo verbose (mostrar más detalles)"
    echo "  -q, --quiet    Modo silencioso (solo mostrar errores)"
    echo
    echo "Ejemplos:"
    echo "  $0              # Ejecutar todas las pruebas"
    echo "  $0 --verbose    # Ejecutar con más detalles"
    echo
}

# Procesar argumentos de línea de comandos
VERBOSE=false
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        *)
            error "Opción desconocida: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Función principal
main() {
    echo "🚀 Sistema de Paquetería v3.1 - Pruebas de Manejo de Errores"
    echo "=========================================================="
    echo
    
    show_system_info
    
    # Ejecutar pruebas
    if run_tests; then
        echo
        success "🎯 Todas las pruebas de manejo de errores pasaron correctamente"
        success "✅ El sistema está funcionando como se esperaba"
        echo
        log "💡 Para probar manualmente:"
        echo "   1. Ve a http://localhost/search"
        echo "   2. Ingresa un código inválido como 'INVALID_CODE'"
        echo "   3. Verifica que aparezca el mensaje de error apropiado"
        exit 0
    else
        echo
        error "💥 Algunas pruebas fallaron"
        error "❌ El sistema necesita revisión"
        exit 1
    fi
}

# Ejecutar función principal
main "$@"
