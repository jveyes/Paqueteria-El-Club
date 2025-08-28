#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - TESTING SIMPLE
# ========================================

echo "🧪 Iniciando testing de APIs..."
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Función para test
test_endpoint() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo "Testing: $name"
    local status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$status" = "$expected" ]; then
        echo -e "${GREEN}✅ $name - Status: $status${NC}"
        return 0
    else
        echo -e "${RED}❌ $name - Status: $status (esperado: $expected)${NC}"
        return 1
    fi
}

# Tests
passed=0
failed=0

# Test 1: Health
if test_endpoint "Health Check" "http://localhost:8001/health" "200"; then
    ((passed++))
else
    ((failed++))
fi

# Test 2: Docs
if test_endpoint "API Docs" "http://localhost:8001/docs" "200"; then
    ((passed++))
else
    ((failed++))
fi

# Test 3: Main page
if test_endpoint "Main Page" "http://localhost:8001/" "200"; then
    ((passed++))
else
    ((failed++))
fi

# Test 4: Auth endpoint (should be 401 or 403)
if test_endpoint "Auth (unauthorized)" "http://localhost:8001/api/auth/me" "403"; then
    ((passed++))
else
    ((failed++))
fi

# Test 5: Rates endpoint (should be 200 or 307)
if test_endpoint "Rates" "http://localhost:8001/api/rates" "307"; then
    ((passed++))
else
    ((failed++))
fi

echo ""
echo "========================================"
echo "        RESUMEN DE TESTING              "
echo "========================================"
echo "Tests exitosos: $passed"
echo "Tests fallidos: $failed"
echo "Total: $((passed + failed))"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡TODOS LOS TESTS PASARON!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Algunos tests fallaron${NC}"
    exit 1
fi
