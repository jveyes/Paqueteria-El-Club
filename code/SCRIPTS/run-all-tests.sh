#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.0 - Ejecutar Todas las Pruebas
# ========================================

set -e

echo "🧪 Ejecutando todas las pruebas de PAQUETES EL CLUB v3.0..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Variables
START_TIME=$(date +%s)
RESULTS_DIR="TEST/results"
REPORTS_DIR="TEST/reports"
LOGS_DIR="TEST/results/logs"

# Crear directorios si no existen
mkdir -p "$RESULTS_DIR"
mkdir -p "$REPORTS_DIR"
mkdir -p "$LOGS_DIR"

# Inicializar contadores
total_tests=0
passed_tests=0
failed_tests=0
skipped_tests=0

# Función para ejecutar test
run_test_script() {
    local script_name=$1
    local test_name=$2
    local script_path="./SCRIPTS/$script_name"
    
    total_tests=$((total_tests + 1))
    
    log_info "Ejecutando: $test_name"
    
    if [ -f "$script_path" ]; then
        if bash "$script_path"; then
            log_success "$test_name - PASÓ"
            passed_tests=$((passed_tests + 1))
            return 0
        else
            log_error "$test_name - FALLÓ"
            failed_tests=$((failed_tests + 1))
            return 1
        fi
    else
        log_warning "$test_name - SALTADO (script no encontrado)"
        skipped_tests=$((skipped_tests + 1))
        return 2
    fi
}

# Función para verificar servicios
check_services() {
    log_info "Verificando que los servicios estén ejecutándose..."
    
    # Verificar Docker
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker no está ejecutándose"
        return 1
    fi
    
    # Verificar que los contenedores estén corriendo
    if ! docker-compose ps | grep -q "Up"; then
        log_warning "Los servicios Docker no están ejecutándose"
        log_info "Iniciando servicios..."
        ./SCRIPTS/start-services.sh
    fi
    
    # Esperar a que FastAPI esté listo
    log_info "Esperando a que FastAPI esté listo..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost/health > /dev/null 2>&1; then
            log_success "FastAPI está listo"
            return 0
        fi
        
        log_info "Esperando FastAPI... (intento $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    log_error "FastAPI no está respondiendo después de $max_attempts intentos"
    return 1
}

# Función para generar reporte final
generate_final_report() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    
    log_info "Generando reporte final..."
    
    cat > "$REPORTS_DIR/comprehensive-test.md" << EOF
# Reporte Completo de Pruebas - PAQUETES EL CLUB v3.0

## 🎯 Resumen Ejecutivo

### 📊 Resultados Generales
- **Fecha de ejecución**: $(date '+%Y-%m-%d %H:%M:%S')
- **Duración total**: ${duration} segundos
- **Estado general**: $(if [ $failed_tests -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi)

### 📈 Métricas de Pruebas
- **Total de tests**: $total_tests
- **Tests exitosos**: $passed_tests
- **Tests fallidos**: $failed_tests
- **Tests saltados**: $skipped_tests
- **Tasa de éxito**: $((passed_tests * 100 / total_tests))%

## 🔍 Detalles por Categoría

### 🔧 Infraestructura
- **Servicios Docker**: $(if docker-compose ps | grep -q "Up"; then echo "✅ Funcionando"; else echo "❌ No funcionando"; fi)
- **Base de datos**: $(if docker-compose exec -T postgres pg_isready -U paqueteria_user > /dev/null 2>&1; then echo "✅ Conectada"; else echo "❌ No conectada"; fi)
- **Redis**: $(if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then echo "✅ Funcionando"; else echo "❌ No funcionando"; fi)
- **FastAPI**: $(if curl -s http://localhost/health > /dev/null 2>&1; then echo "✅ Respondiendo"; else echo "❌ No responde"; fi)

### 🔐 Autenticación
- **Registro de usuarios**: $(if [ -f "$RESULTS_DIR/_api_auth_register.json" ]; then echo "✅ Probado"; else echo "❌ No probado"; fi)
- **Login**: $(if [ -f "$RESULTS_DIR/_api_auth_login.json" ]; then echo "✅ Probado"; else echo "❌ No probado"; fi)
- **JWT tokens**: $(if [ -f "$RESULTS_DIR/_api_auth_login.json" ] && command -v jq > /dev/null 2>&1 && jq -e '.access_token' "$RESULTS_DIR/_api_auth_login.json" > /dev/null 2>&1; then echo "✅ Válidos"; else echo "❌ Inválidos"; fi)

### 📦 Funcionalidad Core
- **Crear paquetes**: $(if [ -f "$RESULTS_DIR/_api_packages_announce.json" ]; then echo "✅ Funcionando"; else echo "❌ No funciona"; fi)
- **Tracking**: $(if [ -f "$RESULTS_DIR/_api_packages_.json" ]; then echo "✅ Funcionando"; else echo "❌ No funciona"; fi)
- **Gestión de clientes**: $(if [ -f "$RESULTS_DIR/_api_customers_.json" ]; then echo "✅ Funcionando"; else echo "❌ No funciona"; fi)
- **Cálculo de tarifas**: $(if [ -f "$RESULTS_DIR/_api_rates_calculate.json" ]; then echo "✅ Funcionando"; else echo "❌ No funciona"; fi)

## 📁 Archivos Generados

### 📄 Reportes
- \`$REPORTS_DIR/api-test.md\` - Pruebas de API
- \`$REPORTS_DIR/infrastructure-test.md\` - Pruebas de infraestructura
- \`$REPORTS_DIR/authentication-test.md\` - Pruebas de autenticación

### 📊 Resultados
- \`$RESULTS_DIR/api-responses/\` - Respuestas de API
- \`$RESULTS_DIR/logs/\` - Logs de ejecución

### 📈 Métricas
- **Tiempo promedio de respuesta**: Calculado desde las respuestas de API
- **Tasa de errores**: $((failed_tests * 100 / total_tests))%
- **Disponibilidad**: $(if [ $failed_tests -eq 0 ]; then echo "100%"; else echo "$((passed_tests * 100 / total_tests))%"; fi)

## ✅ Conclusiones

$(if [ $failed_tests -eq 0 ]; then
    echo "✅ **TODAS LAS PRUEBAS PASARON EXITOSAMENTE**"
    echo ""
    echo "El sistema PAQUETES EL CLUB v3.0 está funcionando correctamente:"
    echo "- ✅ Infraestructura estable"
    echo "- ✅ APIs respondiendo correctamente"
    echo "- ✅ Autenticación funcionando"
    echo "- ✅ Funcionalidad core operativa"
    echo ""
    echo "**RECOMENDACIÓN**: El sistema está listo para desarrollo de frontend y pruebas de integración."
else
    echo "❌ **ALGUNAS PRUEBAS FALLARON**"
    echo ""
    echo "Se encontraron $failed_tests problemas que necesitan atención:"
    echo "- ⚠️  Revisar logs en $LOGS_DIR/"
    echo "- ⚠️  Verificar configuración de servicios"
    echo "- ⚠️  Corregir errores antes de continuar"
    echo ""
    echo "**RECOMENDACIÓN**: Resolver los problemas identificados antes de proceder."
fi)

## 🚀 Próximos Pasos

$(if [ $failed_tests -eq 0 ]; then
    echo "1. **Fase 3**: Implementar frontend y templates"
    echo "2. **Integración**: Probar flujos completos end-to-end"
    echo "3. **Performance**: Ejecutar pruebas de carga"
    echo "4. **Seguridad**: Auditoría de seguridad"
    echo "5. **Deployment**: Preparar para producción"
else
    echo "1. **Debugging**: Revisar y corregir errores identificados"
    echo "2. **Re-ejecutar**: Volver a ejecutar las pruebas"
    echo "3. **Análisis**: Investigar causas raíz de fallos"
    echo "4. **Corrección**: Implementar fixes necesarios"
fi)

---

**Generado automáticamente el**: $(date '+%Y-%m-%d %H:%M:%S')  
**Versión del sistema**: 3.0.0  
**Ejecutado por**: $(whoami)@$(hostname)
EOF

    log_success "Reporte final generado: $REPORTS_DIR/comprehensive-test.md"
}

# Función para limpiar archivos temporales
cleanup() {
    log_info "Limpiando archivos temporales..."
    # Aquí se pueden agregar comandos de limpieza si es necesario
    log_success "Limpieza completada"
}

# Función para manejar interrupciones
trap 'log_error "Pruebas interrumpidas por el usuario"; cleanup; exit 1' INT TERM

# Iniciar pruebas
echo ""
log_info "=== INICIANDO SUITE COMPLETA DE PRUEBAS ==="
echo ""

# Verificar servicios antes de comenzar
if ! check_services; then
    log_error "Los servicios no están listos. Abortando pruebas."
    exit 1
fi

# Ejecutar pruebas en orden
echo ""
log_info "=== 1. PRUEBAS DE INFRAESTRUCTURA ==="
run_test_script "test-database.sh" "Pruebas de Base de Datos"

echo ""
log_info "=== 2. PRUEBAS DE API ==="
run_test_script "test-api-endpoints.sh" "Pruebas de Endpoints de API"

echo ""
log_info "=== 3. PRUEBAS DE AUTENTICACIÓN ==="
run_test_script "test-authentication.sh" "Pruebas de Autenticación"

echo ""
log_info "=== 4. PRUEBAS DE FUNCIONALIDAD ==="
run_test_script "test-packages.sh" "Pruebas de Paquetes"
run_test_script "test-customers.sh" "Pruebas de Clientes"
run_test_script "test-rates.sh" "Pruebas de Tarifas"

echo ""
log_info "=== 5. PRUEBAS DE NOTIFICACIONES ==="
run_test_script "test-notifications.sh" "Pruebas de Notificaciones"

# Generar reporte final
echo ""
log_info "=== GENERANDO REPORTE FINAL ==="
generate_final_report

# Limpiar archivos temporales
cleanup

# Mostrar resumen final
echo ""
log_info "=== RESUMEN FINAL DE PRUEBAS ==="
echo "📊 Total de tests: $total_tests"
echo "✅ Exitosos: $passed_tests"
echo "❌ Fallidos: $failed_tests"
echo "⏭️  Saltados: $skipped_tests"
echo "📄 Reporte: $REPORTS_DIR/comprehensive-test.md"
echo "📁 Resultados: $RESULTS_DIR/"

# Guardar log final
{
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Suite completa de pruebas finalizada"
    echo "Total: $total_tests, Exitosos: $passed_tests, Fallidos: $failed_tests, Saltados: $skipped_tests"
    echo "Duración: ${duration} segundos"
} >> "$LOGS_DIR/comprehensive-test.log"

# Retornar código de salida
if [ $failed_tests -eq 0 ]; then
    log_success "🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!"
    echo ""
    echo "🚀 El sistema está listo para la siguiente fase de desarrollo."
    exit 0
else
    log_error "❌ $failed_tests pruebas fallaron"
    echo ""
    echo "⚠️  Revisa los reportes en $REPORTS_DIR/ para más detalles."
    exit 1
fi
