#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - TESTING DE APIs
# ========================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
BASE_URL="http://localhost:8001"
API_BASE="$BASE_URL/api"

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
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    
    local url="$API_BASE$endpoint"
    local status_code
    
    if [ -n "$data" ]; then
        status_code=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" "$url")
    else
        status_code=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url")
    fi
    
    if [ "$status_code" = "$expected_status" ]; then
        success "API $method $endpoint - Status: $status_code"
        return 0
    else
        error "API $method $endpoint - Status: $status_code (esperado: $expected_status)"
        return 1
    fi
}

# Función principal de testing
main() {
    log "Iniciando testing de APIs..."
    echo ""
    
    local tests_passed=0
    local tests_failed=0
    
    # Test 1: Health Check
    log "Test 1: Health Check"
    local health_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health")
    if [ "$health_status" = "200" ]; then
        success "API GET /health - Status: $health_status"
        ((tests_passed++))
    else
        error "API GET /health - Status: $health_status (esperado: 200)"
        ((tests_failed++))
    fi
    echo ""
    
    # Test 2: API Documentation
    log "Test 2: API Documentation"
    local docs_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/docs")
    if [ "$docs_status" = "200" ]; then
        success "API GET /docs - Status: $docs_status"
        ((tests_passed++))
    else
        error "API GET /docs - Status: $docs_status (esperado: 200)"
        ((tests_failed++))
    fi
    echo ""
    
    # Test 3: Auth Endpoints
    log "Test 3: Auth Endpoints"
    if make_request "GET" "/auth/me" "" "401"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 4: Packages Endpoints
    log "Test 4: Packages Endpoints"
    if make_request "GET" "/packages" "" "401"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 5: Customers Endpoints
    log "Test 5: Customers Endpoints"
    if make_request "GET" "/customers" "" "401"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 6: Rates Endpoints
    log "Test 6: Rates Endpoints"
    if make_request "GET" "/rates" "" "200"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 7: Notifications Endpoints
    log "Test 7: Notifications Endpoints"
    if make_request "GET" "/notifications" "" "401"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 8: Messages Endpoints
    log "Test 8: Messages Endpoints"
    if make_request "GET" "/messages" "" "401"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 9: Files Endpoints
    log "Test 9: Files Endpoints"
    if make_request "GET" "/files" "" "401"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 10: Admin Endpoints
    log "Test 10: Admin Endpoints"
    if make_request "GET" "/admin" "" "401"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Resumen
    echo "========================================"
    echo "        RESUMEN DE TESTING API          "
    echo "========================================"
    echo "Tests exitosos: $tests_passed"
    echo "Tests fallidos: $tests_failed"
    echo "Total: $((tests_passed + tests_failed))"
    echo ""
    
    if [ $tests_failed -eq 0 ]; then
        success "🎉 ¡TODOS LOS TESTS DE API PASARON!"
        exit 0
    else
        error "⚠️  Algunos tests fallaron"
        exit 1
    fi
}

# Ejecutar función principal
main "$@"
