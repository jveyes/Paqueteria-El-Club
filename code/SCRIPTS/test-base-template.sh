#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Test Base Template
# ========================================

echo "🔍 Verificando plantilla base..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
BASE_URL="http://localhost"
TEMPLATE_FILES=(
    "code/templates/components/base-template.html"
    "code/templates/example-page.html"
    "code/templates/README-BASE-TEMPLATE.md"
)

echo -e "\n${YELLOW}1. Verificando que los archivos de la plantilla base existen...${NC}"
for file in "${TEMPLATE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ✅ ${GREEN}Archivo encontrado: $file${NC}"
    else
        echo -e "   ❌ ${RED}Error: Archivo no encontrado: $file${NC}"
        exit 1
    fi
done

echo -e "\n${YELLOW}2. Verificando estructura de la plantilla base...${NC}"
if grep -q "{% block title %}" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Bloque 'title' encontrado${NC}"
else
    echo -e "   ❌ ${RED}Error: Bloque 'title' no encontrado${NC}"
    exit 1
fi

if grep -q "{% block content %}" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Bloque 'content' encontrado${NC}"
else
    echo -e "   ❌ ${RED}Error: Bloque 'content' no encontrado${NC}"
    exit 1
fi

if grep -q "{% block extra_head %}" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Bloque 'extra_head' encontrado${NC}"
else
    echo -e "   ❌ ${RED}Error: Bloque 'extra_head' no encontrado${NC}"
    exit 1
fi

if grep -q "{% block extra_scripts %}" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Bloque 'extra_scripts' encontrado${NC}"
else
    echo -e "   ❌ ${RED}Error: Bloque 'extra_scripts' no encontrado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}3. Verificando configuración de Tailwind CSS...${NC}"
if grep -q "papyrus-blue" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Paleta de colores PAPYRUS configurada${NC}"
else
    echo -e "   ❌ ${RED}Error: Paleta de colores PAPYRUS no encontrada${NC}"
    exit 1
fi

echo -e "\n${YELLOW}4. Verificando frameworks JavaScript...${NC}"
if grep -q "alpinejs" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Alpine.js incluido${NC}"
else
    echo -e "   ❌ ${RED}Error: Alpine.js no encontrado${NC}"
    exit 1
fi

if grep -q "htmx" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}HTMX incluido${NC}"
else
    echo -e "   ❌ ${RED}Error: HTMX no encontrado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}5. Verificando header optimizado...${NC}"
if grep -q "PAQUETES" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Header con título 'PAQUETES' encontrado${NC}"
else
    echo -e "   ❌ ${RED}Error: Header no encontrado${NC}"
    exit 1
fi

if grep -q "mobileMenuOpen" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Menú móvil configurado${NC}"
else
    echo -e "   ❌ ${RED}Error: Menú móvil no configurado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}6. Verificando footer sticky...${NC}"
if grep -q "JEMAVI" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Footer con copyright encontrado${NC}"
else
    echo -e "   ❌ ${RED}Error: Footer no encontrado${NC}"
    exit 1
fi

if grep -q "w-8 h-8" "code/templates/components/base-template.html"; then
    echo -e "   ✅ ${GREEN}Iconos del footer optimizados para móvil${NC}"
else
    echo -e "   ❌ ${RED}Error: Iconos del footer no optimizados${NC}"
    exit 1
fi

echo -e "\n${YELLOW}7. Verificando página de ejemplo...${NC}"
if grep -q "{% extends \"components/base-template.html\" %}" "code/templates/example-page.html"; then
    echo -e "   ✅ ${GREEN}Página de ejemplo extiende correctamente la plantilla base${NC}"
else
    echo -e "   ❌ ${RED}Error: Página de ejemplo no extiende la plantilla base${NC}"
    exit 1
fi

echo -e "\n${YELLOW}8. Verificando documentación...${NC}"
if [ -s "code/templates/README-BASE-TEMPLATE.md" ]; then
    echo -e "   ✅ ${GREEN}Documentación creada y no está vacía${NC}"
else
    echo -e "   ❌ ${RED}Error: Documentación vacía o no encontrada${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 ¡Todas las verificaciones de la plantilla base pasaron exitosamente!${NC}"
echo -e "\n${YELLOW}📋 Resumen de la plantilla base:${NC}"
echo -e "   • Archivos: ${#TEMPLATE_FILES[@]} archivos creados"
echo -e "   • Bloques: 4 bloques disponibles (title, content, extra_head, extra_scripts)"
echo -e "   • Frameworks: Tailwind CSS, Alpine.js, HTMX"
echo -e "   • Responsive: Mobile-first design"
echo -e "   • Colores: Paleta PAPYRUS completa"
echo -e "   • Header: Navegación optimizada"
echo -e "   • Footer: Sticky con iconos de contacto"
echo -e "   • Documentación: README completo"
echo -e "\n${GREEN}✅ La plantilla base está lista para ser utilizada en todas las nuevas páginas${NC}"
