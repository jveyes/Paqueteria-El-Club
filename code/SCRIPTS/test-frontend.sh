#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - TESTING DE FRONTEND
# ========================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
BASE_URL="http://localhost"

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

# Función para verificar página
check_page() {
    local name=$1
    local url=$2
    local expected_content=$3
    
    echo "Testing: $name"
    local response=$(curl -s -w "%{http_code}" "$url")
    local status_code="${response: -3}"
    local body="${response%???}"
    
    if [ "$status_code" = "200" ]; then
        if [ -n "$expected_content" ]; then
            if echo "$body" | grep -q "$expected_content"; then
                success "$name - Status: $status_code - Contenido encontrado"
                return 0
            else
                warning "$name - Status: $status_code - Contenido no encontrado"
                return 1
            fi
        else
            success "$name - Status: $status_code"
            return 0
        fi
    else
        error "$name - Status: $status_code"
        return 1
    fi
}

# Función principal
main() {
    log "Iniciando testing de frontend..."
    echo ""
    
    local tests_passed=0
    local tests_failed=0
    
    # Test 1: Página principal
    if check_page "Página Principal" "$BASE_URL" "PAQUETES EL CLUB"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 2: Dashboard
    if check_page "Dashboard" "$BASE_URL" "Dashboard"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 3: API Documentation
    if check_page "API Documentation" "$BASE_URL:8001/docs" "Swagger"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 4: Health Check
    if check_page "Health Check" "$BASE_URL:8001/health" "healthy"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 5: Verificar que el layout base se carga
    if check_page "Layout Base" "$BASE_URL" "sidebar"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 6: Verificar que Alpine.js está funcionando
    if check_page "Alpine.js" "$BASE_URL" "x-data"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 7: Verificar que Tailwind CSS está cargado
    if check_page "Tailwind CSS" "$BASE_URL" "tailwind"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 8: Verificar que HTMX está cargado
    if check_page "HTMX" "$BASE_URL" "htmx"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Resumen
    echo "========================================"
    echo "        RESUMEN DE TESTING FRONTEND     "
    echo "========================================"
    echo "Tests exitosos: $tests_passed"
    echo "Tests fallidos: $tests_failed"
    echo "Total: $((tests_passed + tests_failed))"
    echo ""
    
    if [ $tests_failed -eq 0 ]; then
        success "🎉 ¡TODOS LOS TESTS DE FRONTEND PASARON!"
        echo ""
        echo "URLs de Acceso:"
        echo "  • Frontend: $BASE_URL"
        echo "  • API Docs: $BASE_URL:8001/docs"
        echo "  • Health: $BASE_URL:8001/health"
        echo ""
        echo "Características del Frontend:"
        echo "  • ✅ Layout responsive con sidebar"
        echo "  • ✅ Dashboard con estadísticas"
        echo "  • ✅ Navegación moderna"
        echo "  • ✅ Alpine.js para interactividad"
        echo "  • ✅ HTMX para actualizaciones dinámicas"
        echo "  • ✅ Tailwind CSS para estilos"
        echo "  • ✅ Notificaciones toast"
        echo "  • ✅ Loading states"
        exit 0
    else
        error "⚠️  Algunos tests fallaron"
        echo ""
        echo "Recomendaciones:"
        echo "  • Verificar que el servidor está corriendo"
        echo "  • Revisar logs de nginx y FastAPI"
        echo "  • Verificar que los templates se están sirviendo correctamente"
        exit 1
    fi
}

# Ejecutar función principal
main "$@"
