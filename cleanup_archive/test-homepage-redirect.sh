#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - TESTING DE REDIRECCIÓN DE PÁGINA PRINCIPAL
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

# Función para verificar redirección
check_redirect() {
    local name=$1
    local url=$2
    local expected_content=$3
    
    echo "Testing: $name"
    local response=$(curl -L -s -w "%{http_code}" "$url")
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
    log "Iniciando testing de redirección de página principal..."
    echo ""
    
    local tests_passed=0
    local tests_failed=0
    
    # Test 1: Página principal carga correctamente
    if check_redirect "Página Principal" "$BASE_URL/" "Consulta de Paquetes"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 2: Verificar que no es la página de dashboard (verificar título)
    if check_redirect "Título Correcto" "$BASE_URL/" "Consulta de Paquetes - PAQUETES EL CLUB"; then
        success "Página principal tiene el título correcto"
        ((tests_passed++))
    else
        warning "Página principal no tiene el título correcto"
        ((tests_failed++))
    fi
    echo ""
    
    # Test 3: Verificar que contiene formulario de búsqueda
    if check_redirect "Formulario de Búsqueda" "$BASE_URL/" "tracking_number"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 4: Verificar que contiene formulario de anuncios
    if check_redirect "Formulario de Anuncios" "$BASE_URL/" "guide_number"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 5: Verificar que contiene paquetes anunciados
    if check_redirect "Paquetes Anunciados" "$BASE_URL/" "Juan Pérez"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 6: Verificar que contiene botones de contacto
    if check_redirect "Botones de Contacto" "$BASE_URL/" "Llamar"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 7: Verificar que contiene colores PAPYRUS
    if check_redirect "Colores PAPYRUS" "$BASE_URL/" "papyrus-blue"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 8: Verificar que la ruta /customers también funciona
    if check_redirect "Ruta /customers" "$BASE_URL/customers" "Consulta de Paquetes"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Test 9: Verificar que la ruta /dashboard existe
    if check_redirect "Ruta /dashboard" "$BASE_URL/dashboard" "Dashboard"; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    echo ""
    
    # Resumen
    echo "========================================"
    echo "    RESUMEN DE TESTING REDIRECCIÓN      "
    echo "========================================"
    echo "Tests exitosos: $tests_passed"
    echo "Tests fallidos: $tests_failed"
    echo "Total: $((tests_passed + tests_failed))"
    echo ""
    
    if [ $tests_failed -eq 0 ]; then
        success "🎉 ¡TODOS LOS TESTS DE REDIRECCIÓN PASARON!"
        echo ""
        echo "Funcionalidades Verificadas:"
        echo "  • ✅ Página principal redirige a consulta de paquetes"
        echo "  • ✅ Formulario de búsqueda disponible"
        echo "  • ✅ Formulario de anuncios disponible"
        echo "  • ✅ Paquetes anunciados visibles"
        echo "  • ✅ Botones de contacto funcionando"
        echo "  • ✅ Colores PAPYRUS aplicados"
        echo "  • ✅ Ruta /customers funciona"
        echo "  • ✅ Ruta /dashboard disponible"
        echo ""
        echo "URLs de Acceso:"
        echo "  • Página Principal: $BASE_URL/"
        echo "  • Consulta de Paquetes: $BASE_URL/customers"
        echo "  • Dashboard: $BASE_URL/dashboard"
        echo ""
        echo "Flujo de Usuario:"
        echo "  • 🌐 Usuario visita $BASE_URL/"
        echo "  • 🔄 Automáticamente ve la página de consulta de paquetes"
        echo "  • 🔍 Puede buscar paquetes por tracking"
        echo "  • 📢 Puede anunciar sus propios paquetes"
        echo "  • 📞 Puede contactar a otros clientes"
        echo "  • ⚙️  Administradores pueden acceder al dashboard"
        exit 0
    else
        error "⚠️  Algunos tests fallaron"
        echo ""
        echo "Recomendaciones:"
        echo "  • Verificar que el servidor está corriendo"
        echo "  • Revisar logs de nginx y FastAPI"
        echo "  • Verificar que las rutas están configuradas correctamente"
        echo "  • Comprobar que los templates se están sirviendo"
        exit 1
    fi
}

# Ejecutar función principal
main "$@"
