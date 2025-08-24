#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.0 - Documentar Resultados de Pruebas
# ========================================
#
# 🎯 OBJETIVO: Documentar automáticamente los resultados de las pruebas
# 📅 FECHA: 2025-01-24
# 👤 AUTOR: Sistema Automatizado
# 🔄 VERSIÓN: 1.0.0
#
# 📋 USO:
#   ./SCRIPTS/document-test-results.sh [nombre-prueba] [resultado]
#
# 📊 RESULTADOS:
#   - Archivo de log: logs/document-test.log
#   - Reporte: TEST/reports/[nombre-prueba]-report.md
#   - Datos: TEST/results/[nombre-prueba]/
#
# ⚠️ DEPENDENCIAS:
#   - jq (para procesar JSON)
#   - curl (para pruebas de API)
#   - docker-compose (para servicios)
#
# ========================================

set -e

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEST_DIR="$PROJECT_ROOT/TEST"
LOGS_DIR="$PROJECT_ROOT/logs"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOGS_DIR/document-test.log"
}

# Función para crear directorios si no existen
create_directories() {
    mkdir -p "$TEST_DIR/reports"
    mkdir -p "$TEST_DIR/results"
    mkdir -p "$LOGS_DIR"
}

# Función para generar reporte de prueba
generate_test_report() {
    local test_name="$1"
    local test_result="$2"
    local test_details="$3"
    local execution_time="$4"
    
    local report_file="$TEST_DIR/reports/${test_name}-report.md"
    
    cat > "$report_file" << EOF
# ========================================
# PAQUETES EL CLUB v3.0 - ${test_name^}
# ========================================
#
# 🎯 OBJETIVO: Resultados de la prueba ${test_name}
# 📅 FECHA: ${TIMESTAMP}
# 👤 EJECUTOR: Sistema Automatizado
# 🔄 VERSIÓN: 3.0.0
#
# 📊 RESULTADOS:
#   - Estado: ${test_result}
#   - Tiempo de ejecución: ${execution_time}
#   - Errores encontrados: $(echo "$test_details" | grep -c "❌" || echo "0")
#   - Advertencias: $(echo "$test_details" | grep -c "⚠️" || echo "0")
#
# 🔍 DETALLES:
\`\`\`
${test_details}
\`\`\`
#
# 📈 MÉTRICAS:
#   - Fecha de ejecución: ${TIMESTAMP}
#   - Entorno: development
#   - Versión del sistema: 3.0.0
#
# ✅ CONCLUSIONES:
#   ${test_result} - ${test_name} completada
#
# ========================================
EOF

    log "✅ Reporte generado: $report_file"
}

# Función para documentar prueba de API
document_api_test() {
    local test_name="api-endpoints"
    local start_time=$(date +%s)
    
    log "🔍 Iniciando documentación de prueba de API..."
    
    # Ejecutar prueba de API
    local test_output
    test_output=$(./SCRIPTS/test-api-endpoints.sh 2>&1)
    local exit_code=$?
    
    local end_time=$(date +%s)
    local execution_time=$((end_time - start_time))
    
    # Determinar resultado
    local test_result
    if [ $exit_code -eq 0 ]; then
        test_result="✅ PASS"
    else
        test_result="❌ FAIL"
    fi
    
    # Generar reporte
    generate_test_report "$test_name" "$test_result" "$test_output" "${execution_time}s"
    
    log "📊 Resultado: $test_result"
    log "⏱️ Tiempo de ejecución: ${execution_time}s"
}

# Función para documentar prueba de base de datos
document_database_test() {
    local test_name="database"
    local start_time=$(date +%s)
    
    log "🗄️ Iniciando documentación de prueba de base de datos..."
    
    # Ejecutar prueba de base de datos
    local test_output
    test_output=$(./SCRIPTS/test-database.sh 2>&1)
    local exit_code=$?
    
    local end_time=$(date +%s)
    local execution_time=$((end_time - start_time))
    
    # Determinar resultado
    local test_result
    if [ $exit_code -eq 0 ]; then
        test_result="✅ PASS"
    else
        test_result="❌ FAIL"
    fi
    
    # Generar reporte
    generate_test_report "$test_name" "$test_result" "$test_output" "${execution_time}s"
    
    log "📊 Resultado: $test_result"
    log "⏱️ Tiempo de ejecución: ${execution_time}s"
}

# Función para documentar prueba rápida
document_quick_test() {
    local test_name="quick-test"
    local start_time=$(date +%s)
    
    log "⚡ Iniciando documentación de prueba rápida..."
    
    # Ejecutar prueba rápida
    local test_output
    test_output=$(./SCRIPTS/quick-test.sh 2>&1)
    local exit_code=$?
    
    local end_time=$(date +%s)
    local execution_time=$((end_time - start_time))
    
    # Determinar resultado
    local test_result
    if [ $exit_code -eq 0 ]; then
        test_result="✅ PASS"
    else
        test_result="❌ FAIL"
    fi
    
    # Generar reporte
    generate_test_report "$test_name" "$test_result" "$test_output" "${execution_time}s"
    
    log "📊 Resultado: $test_result"
    log "⏱️ Tiempo de ejecución: ${execution_time}s"
}

# Función para documentar todas las pruebas
document_all_tests() {
    log "🚀 Iniciando documentación de todas las pruebas..."
    
    document_quick_test
    document_database_test
    document_api_test
    
    log "✅ Documentación de todas las pruebas completada"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  quick-test     Documentar prueba rápida"
    echo "  database       Documentar prueba de base de datos"
    echo "  api            Documentar prueba de API"
    echo "  all            Documentar todas las pruebas"
    echo "  help           Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 quick-test"
    echo "  $0 all"
}

# Función principal
main() {
    # Crear directorios necesarios
    create_directories
    
    # Verificar argumentos
    if [ $# -eq 0 ]; then
        log "❌ Error: Se requiere un argumento"
        show_help
        exit 1
    fi
    
    case "$1" in
        "quick-test")
            document_quick_test
            ;;
        "database")
            document_database_test
            ;;
        "api")
            document_api_test
            ;;
        "all")
            document_all_tests
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log "❌ Error: Opción desconocida '$1'"
            show_help
            exit 1
            ;;
    esac
    
    log "🎉 Documentación completada exitosamente"
}

# Ejecutar función principal
main "$@"
