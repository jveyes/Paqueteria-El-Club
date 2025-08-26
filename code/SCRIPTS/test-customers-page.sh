#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - TESTING DE PÁGINA DE CLIENTES
# ========================================
# set -e

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

# Función para verificar funcionalidades específicas
check_functionality() {
    local name=$1
    local url=$2
    local content_check=$3
    
    echo "Testing: $name"
    local response=$(curl -s "$url")
    
    if echo "$response" | grep -q "$content_check"; then
        success "$name - Funcionalidad encontrada"
        return 0
    else
        error "$name - Funcionalidad no encontrada"
        return 1
    fi
}

# Función principal
main() {
    log "Iniciando testing de página de clientes..."
    echo ""
    
    local tests_passed=0
    local tests_failed=0
    
    # Test 1: Página principal de clientes
    if check_page "Página de Clientes" "$BASE_URL/customers" "Consulta de Paquetes"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 2: Verificar formulario de búsqueda de paquetes
    if check_functionality "Formulario de Búsqueda" "$BASE_URL/customers" "tracking_number"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 3: Verificar formulario de anuncios
    if check_functionality "Formulario de Anuncios" "$BASE_URL/customers" "guide_number"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 4: Verificar sección de paquetes anunciados
    if check_functionality "Paquetes Anunciados" "$BASE_URL/customers" "Juan Pérez"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 5: Verificar botones de contacto
    if check_functionality "Botones de Contacto" "$BASE_URL/customers" "Llamar"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 6: Verificar diseño responsivo
    if check_functionality "Diseño Responsivo" "$BASE_URL/customers" "sm:flex"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 7: Verificar colores PAPYRUS
    if check_functionality "Colores PAPYRUS" "$BASE_URL/customers" "papyrus-blue"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 8: Verificar JavaScript interactivo
    if check_functionality "JavaScript Interactivo" "$BASE_URL/customers" "showToast"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 9: Verificar Alpine.js
    if check_functionality "Alpine.js" "$BASE_URL/customers" "x-data"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 10: Verificar HTMX
    if check_functionality "HTMX" "$BASE_URL/customers" "htmx"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Resumen
    echo "========================================"
    echo "    RESUMEN DE TESTING PÁGINA CLIENTES  "
    echo "========================================"
    echo "Tests exitosos: $tests_passed"
    echo "Tests fallidos: $tests_failed"
    echo "Total: $((tests_passed + tests_failed))"
    echo ""
    
    if [ $tests_failed -eq 0 ]; then
        success "🎉 ¡TODOS LOS TESTS DE LA PÁGINA DE CLIENTES PASARON!"
        echo ""
        echo "Funcionalidades Verificadas:"
        echo "  • ✅ Página de consulta de paquetes"
        echo "  • ✅ Formulario de búsqueda por tracking"
        echo "  • ✅ Formulario de anuncios de paquetes"
        echo "  • ✅ Lista de paquetes anunciados"
        echo "  • ✅ Botones de contacto (Llamar/WhatsApp)"
        echo "  • ✅ Diseño responsivo"
        echo "  • ✅ Colores del sistema PAPYRUS"
        echo "  • ✅ JavaScript interactivo"
        echo "  • ✅ Alpine.js para interactividad"
        echo "  • ✅ HTMX para actualizaciones dinámicas"
        echo ""
        echo "URL de Acceso: $BASE_URL/customers"
        echo ""
        echo "Características de la Página:"
        echo "  • 🔍 Búsqueda de paquetes por número de seguimiento"
        echo "  • 📢 Anuncios de paquetes con formulario"
        echo "  • 📞 Contacto directo con clientes"
        echo "  • 📱 Diseño móvil responsive"
        echo "  • 🎨 Diseño PAPYRUS v3.0"
        echo "  • ⚡ Interactividad con Alpine.js y HTMX"
        exit 0
    else
        error "⚠️  Algunos tests fallaron"
        echo ""
        echo "Recomendaciones:"
        echo "  • Verificar que el servidor está corriendo"
        echo "  • Revisar logs de nginx y FastAPI"
        echo "  • Verificar que los templates se están sirviendo correctamente"
        echo "  • Comprobar que los archivos JavaScript están cargando"
        exit 1
    fi
}

# Ejecutar función principal
main "$@"
