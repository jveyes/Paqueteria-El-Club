#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.0 - Pruebas de API Endpoints
# ========================================

set -e

echo "🔍 Probando endpoints de API de PAQUETES EL CLUB v3.0..."

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
BASE_URL="http://localhost"
API_BASE_URL="$BASE_URL/api"
TIMEOUT=30
RESULTS_DIR="TEST/results/api-responses"
LOGS_DIR="TEST/results/logs"

# Crear directorios si no existen
mkdir -p "$RESULTS_DIR"
mkdir -p "$LOGS_DIR"

# Función para hacer request HTTP
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local headers=$4
    
    local url="$BASE_URL$endpoint"
    local response_file="$RESULTS_DIR/$(echo $endpoint | sed 's/\//_/g').json"
    
    log_info "Probando $method $endpoint"
    
    # Construir comando curl
    local curl_cmd="curl -s -w '\nHTTP_CODE:%{http_code}\nTIME:%{time_total}\n'"
    curl_cmd="$curl_cmd -X $method"
    curl_cmd="$curl_cmd --connect-timeout $TIMEOUT"
    curl_cmd="$curl_cmd --max-time $TIMEOUT"
    
    if [ ! -z "$headers" ]; then
        curl_cmd="$curl_cmd -H '$headers'"
    fi
    
    if [ ! -z "$data" ]; then
        curl_cmd="$curl_cmd -d '$data'"
        curl_cmd="$curl_cmd -H 'Content-Type: application/json'"
    fi
    
    curl_cmd="$curl_cmd '$url'"
    
    # Ejecutar request
    local response=$(eval $curl_cmd 2>/dev/null)
    
    # Extraer información
    local http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)
    local time_total=$(echo "$response" | grep "TIME:" | cut -d: -f2)
    local body=$(echo "$response" | sed '/HTTP_CODE:/d' | sed '/TIME:/d')
    
    # Guardar respuesta
    echo "$body" > "$response_file"
    
    # Evaluar resultado
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        log_success "$method $endpoint - $http_code (${time_total}s)"
        return 0
    elif [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        log_warning "$method $endpoint - $http_code (${time_total}s) - Error del cliente"
        return 1
    else
        log_error "$method $endpoint - $http_code (${time_total}s) - Error del servidor"
        return 1
    fi
}

# Función para validar JSON
validate_json() {
    local json_file=$1
    if command -v jq > /dev/null 2>&1; then
        if jq empty "$json_file" 2>/dev/null; then
            return 0
        else
            return 1
        fi
    else
        # Validación básica sin jq
        if grep -q "^{" "$json_file" && grep -q "}$" "$json_file"; then
            return 0
        else
            return 1
        fi
    fi
}

# Inicializar contadores
total_tests=0
passed_tests=0
failed_tests=0

# Función para ejecutar test
run_test() {
    local test_name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local headers=$5
    
    total_tests=$((total_tests + 1))
    
    if make_request "$method" "$endpoint" "$data" "$headers"; then
        passed_tests=$((passed_tests + 1))
    else
        failed_tests=$((failed_tests + 1))
    fi
}

# Iniciar pruebas
echo ""
log_info "Iniciando pruebas de endpoints..."

# 1. Health Check
echo ""
log_info "=== 1. Health Check ==="
run_test "Health Check" "GET" "/health"

# 2. Metrics
echo ""
log_info "=== 2. Metrics ==="
run_test "Metrics" "GET" "/metrics"

# 3. API Documentation
echo ""
log_info "=== 3. API Documentation ==="
run_test "API Docs" "GET" "/api/docs"

# 4. Authentication Endpoints
echo ""
log_info "=== 4. Authentication Endpoints ==="

# Registrar usuario
register_data='{
  "username": "testuser",
  "email": "test@papyrus.com.co",
  "password": "Test2025!Secure",
  "first_name": "Usuario",
  "last_name": "Prueba"
}'
run_test "Register User" "POST" "/api/auth/register" "$register_data"

# Login
login_data='{
  "username": "testuser",
  "password": "Test2025!Secure"
}'
run_test "Login" "POST" "/api/auth/login" "$login_data"

# Extraer token para pruebas posteriores
TOKEN=""
if [ -f "$RESULTS_DIR/_api_auth_login.json" ]; then
    if command -v jq > /dev/null 2>&1; then
        TOKEN=$(jq -r '.access_token' "$RESULTS_DIR/_api_auth_login.json" 2>/dev/null || echo "")
    fi
fi

# 5. Packages Endpoints
echo ""
log_info "=== 5. Packages Endpoints ==="

# Anunciar paquete
package_data='{
  "customer_name": "Juan Pérez",
  "customer_phone": "3334004007",
  "package_type": "normal",
  "package_condition": "bueno",
  "observations": "Paquete de prueba"
}'
run_test "Announce Package" "POST" "/api/packages/announce" "$package_data"

# Listar paquetes
headers=""
if [ ! -z "$TOKEN" ]; then
    headers="Authorization: Bearer $TOKEN"
fi
run_test "List Packages" "GET" "/api/packages/" "" "$headers"

# 6. Customers Endpoints
echo ""
log_info "=== 6. Customers Endpoints ==="

# Crear cliente
customer_data='{
  "name": "María García",
  "phone": "3334004008"
}'
run_test "Create Customer" "POST" "/api/customers/" "$customer_data" "$headers"

# Listar clientes
run_test "List Customers" "GET" "/api/customers/" "" "$headers"

# 7. Rates Endpoints
echo ""
log_info "=== 7. Rates Endpoints ==="

# Listar tarifas
run_test "List Rates" "GET" "/api/rates/" "" "$headers"

# Calcular tarifa
rate_calc_data='{
  "package_type": "normal",
  "storage_days": 5,
  "delivery_required": true
}'
run_test "Calculate Rate" "POST" "/api/rates/calculate" "$rate_calc_data" "$headers"

# 8. Admin Endpoints
echo ""
log_info "=== 8. Admin Endpoints ==="

# Dashboard admin
run_test "Admin Dashboard" "GET" "/api/admin/dashboard" "" "$headers"

# 9. Notifications Endpoints
echo ""
log_info "=== 9. Notifications Endpoints ==="

# Listar notificaciones
run_test "List Notifications" "GET" "/api/notifications/" "" "$headers"

# Procesar resultados
echo ""
log_info "=== Resultados de Pruebas ==="

# Validar respuestas JSON
log_info "Validando respuestas JSON..."
json_validation_errors=0
for json_file in "$RESULTS_DIR"/*.json; do
    if [ -f "$json_file" ]; then
        if validate_json "$json_file"; then
            log_success "JSON válido: $(basename $json_file)"
        else
            log_error "JSON inválido: $(basename $json_file)"
            json_validation_errors=$((json_validation_errors + 1))
        fi
    fi
done

# Generar reporte
echo ""
log_info "Generando reporte..."

cat > "TEST/reports/api-test.md" << EOF
# Prueba: API Endpoints Test

## 🎯 Objetivo
Probar todos los endpoints de la API de PAQUETES EL CLUB v3.0

## 🛠️ Configuración
- **Fecha**: $(date '+%Y-%m-%d %H:%M:%S')
- **Entorno**: development
- **Versión**: 3.0.0
- **Base URL**: $BASE_URL
- **Timeout**: ${TIMEOUT}s

## 📊 Resultados
- **Estado**: $(if [ $failed_tests -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi)
- **Tiempo de ejecución**: $(date '+%H:%M:%S')
- **Tests ejecutados**: $total_tests
- **Tests exitosos**: $passed_tests
- **Tests fallidos**: $failed_tests
- **Errores de JSON**: $json_validation_errors

## 🔍 Detalles

### Endpoints probados:
$(ls "$RESULTS_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ') archivos de respuesta generados

### Respuestas guardadas en:
\`\`\`
$RESULTS_DIR/
\`\`\`

## 📈 Métricas
- **Tasa de éxito**: $((passed_tests * 100 / total_tests))%
- **Tasa de fallo**: $((failed_tests * 100 / total_tests))%

## ✅ Conclusiones
$(if [ $failed_tests -eq 0 ]; then
    echo "✅ Todas las pruebas de API pasaron exitosamente"
else
    echo "❌ $failed_tests pruebas fallaron y necesitan atención"
fi)

$(if [ $json_validation_errors -gt 0 ]; then
    echo "⚠️  $json_validation_errors respuestas JSON son inválidas"
fi)
EOF

# Mostrar resumen final
echo ""
log_info "=== Resumen Final ==="
echo "📊 Total de tests: $total_tests"
echo "✅ Exitosos: $passed_tests"
echo "❌ Fallidos: $failed_tests"
echo "📄 Reporte: TEST/reports/api-test.md"
echo "📁 Respuestas: $RESULTS_DIR/"

# Guardar log
{
    echo "$(date '+%Y-%m-%d %H:%M:%S') - API Tests completados"
    echo "Total: $total_tests, Exitosos: $passed_tests, Fallidos: $failed_tests"
} >> "$LOGS_DIR/api-test.log"

# Retornar código de salida
if [ $failed_tests -eq 0 ]; then
    log_success "🎉 Todas las pruebas de API pasaron!"
    exit 0
else
    log_error "❌ $failed_tests pruebas fallaron"
    exit 1
fi
