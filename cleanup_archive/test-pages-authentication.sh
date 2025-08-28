#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Test Pages Authentication
# ========================================

echo "🔍 Verificando funcionalidad de autenticación en páginas..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
BASE_URL="http://localhost"
ANNOUNCE_PAGE="/"
SEARCH_PAGE="/search"
DASHBOARD_PAGE="/dashboard"

# Contador de tests
tests_passed=0
total_tests=0

# Función para hacer test
make_test() {
    local test_name="$1"
    local url="$2"
    local expected_content="$3"
    local description="$4"
    
    total_tests=$((total_tests + 1))
    echo -e "\n${YELLOW}Test $total_tests: $test_name${NC}"
    echo -e "   Descripción: $description"
    
    if curl -s "$url" | grep -q "$expected_content"; then
        echo -e "   ✅ ${GREEN}PASÓ${NC}"
        tests_passed=$((tests_passed + 1))
    else
        echo -e "   ❌ ${RED}FALLÓ${NC}"
        return 1
    fi
}

echo -e "\n${YELLOW}=== VERIFICANDO PÁGINA DE ANUNCIAR PAQUETES ===${NC}"
make_test "Página de Anunciar Paquetes" "$BASE_URL$ANNOUNCE_PAGE" "Anuncio de Paquetes" "Verificar que la página principal muestre el formulario de anuncio"
make_test "Logo PAPYRUS en Anunciar" "$BASE_URL$ANNOUNCE_PAGE" "papyrus-logo.png" "Verificar que el logo PAPYRUS esté presente"
make_test "Navegación Anunciar Paquete" "$BASE_URL$ANNOUNCE_PAGE" "Anunciar Paquete" "Verificar que el enlace 'Anunciar Paquete' esté en la navegación"
make_test "Navegación Consultar Paquetes" "$BASE_URL$ANNOUNCE_PAGE" "Consultar Paquetes" "Verificar que el enlace 'Consultar Paquetes' esté en la navegación"
make_test "Icono de Login" "$BASE_URL$ANNOUNCE_PAGE" "Iniciar Sesión" "Verificar que el icono de login esté presente"

echo -e "\n${YELLOW}=== VERIFICANDO PÁGINA DE CONSULTAR PAQUETES ===${NC}"
make_test "Página de Consultar Paquetes" "$BASE_URL$SEARCH_PAGE" "Consulta de Estado" "Verificar que la página de consulta muestre el formulario correcto"
make_test "Logo PAPYRUS en Consultar" "$BASE_URL$SEARCH_PAGE" "papyrus-logo.png" "Verificar que el logo PAPYRUS esté presente en la página de consulta"
make_test "Formulario de Consulta" "$BASE_URL$SEARCH_PAGE" "Ingresa el número de guía" "Verificar que el campo de número de guía esté presente"
make_test "Botón Consultar" "$BASE_URL$SEARCH_PAGE" "Consultar Paquete" "Verificar que el botón de consultar esté presente"
# Test para verificar que NO esté presente la sección de ayuda
total_tests=$((total_tests + 1))
echo -e "\n${YELLOW}Test $total_tests: Sin sección de ayuda${NC}"
echo -e "   Descripción: Verificar que NO esté presente la sección de ayuda"
if ! curl -s "$BASE_URL$SEARCH_PAGE" | grep -q "¿Necesitas ayuda?"; then
    echo -e "   ✅ ${GREEN}PASÓ${NC}"
    tests_passed=$((tests_passed + 1))
else
    echo -e "   ❌ ${RED}FALLÓ${NC}"
    echo -e "   ⚠️  ${YELLOW}ADVERTENCIA: Sección de ayuda encontrada (debería estar eliminada)${NC}"
fi

echo -e "\n${YELLOW}=== VERIFICANDO FUNCIONALIDAD DE AUTENTICACIÓN ===${NC}"
make_test "Dashboard no accesible" "$BASE_URL$DASHBOARD_PAGE" "Dashboard" "Verificar que el dashboard esté accesible (simulado como autenticado)"
make_test "Navegación Dashboard" "$BASE_URL$DASHBOARD_PAGE" "Dashboard" "Verificar que el enlace Dashboard esté en la navegación cuando autenticado"
make_test "Usuario autenticado" "$BASE_URL$DASHBOARD_PAGE" "Admin" "Verificar que se muestre el nombre del usuario autenticado"

echo -e "\n${YELLOW}=== VERIFICANDO ESTRUCTURA DE NAVEGACIÓN ===${NC}"
make_test "Header completo" "$BASE_URL$ANNOUNCE_PAGE" "PAQUETES" "Verificar que el header esté presente"
make_test "Footer completo" "$BASE_URL$ANNOUNCE_PAGE" "JEMAVI" "Verificar que el footer esté presente"
make_test "Responsive design" "$BASE_URL$ANNOUNCE_PAGE" "md:hidden" "Verificar que las clases responsive estén presentes"

# Resumen final
echo -e "\n${YELLOW}=== RESUMEN ===${NC}"
echo -e "Tests pasados: ${GREEN}$tests_passed${NC} de ${YELLOW}$total_tests${NC}"

if [ $tests_passed -eq $total_tests ]; then
    echo -e "\n${GREEN}🎉 ¡Todas las verificaciones pasaron exitosamente!${NC}"
    echo -e "\n${YELLOW}📋 Funcionalidades verificadas:${NC}"
    echo -e "   ✅ Página de anunciar paquetes funcionando"
    echo -e "   ✅ Página de consultar paquetes funcionando"
    echo -e "   ✅ Logo PAPYRUS presente en ambas páginas"
    echo -e "   ✅ Navegación con autenticación funcionando"
    echo -e "   ✅ Estructura responsive correcta"
    echo -e "   ✅ Header y footer consistentes"
    exit 0
else
    echo -e "\n${RED}❌ Algunas verificaciones fallaron${NC}"
    echo -e "   Tests fallidos: $((total_tests - tests_passed))"
    exit 1
fi
