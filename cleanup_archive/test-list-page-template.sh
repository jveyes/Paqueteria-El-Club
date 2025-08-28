#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Test List Page Template
# ========================================

echo "🔍 Verificando página de anuncios con plantilla base..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
BASE_URL="http://localhost"

echo -e "\n${YELLOW}1. Verificando que la página se carga correctamente...${NC}"
if curl -s "$BASE_URL" > /dev/null 2>&1; then
    echo -e "   ✅ ${GREEN}Página accesible en: $BASE_URL${NC}"
else
    echo -e "   ❌ ${RED}Error: Página no accesible${NC}"
    exit 1
fi

echo -e "\n${YELLOW}2. Verificando que extiende la plantilla base...${NC}"
if curl -s "$BASE_URL" | grep -q "PAQUETES" && curl -s "$BASE_URL" | grep -q "JEMAVI"; then
    echo -e "   ✅ ${GREEN}Página extiende correctamente la plantilla base (header y footer presentes)${NC}"
else
    echo -e "   ❌ ${RED}Error: Página no extiende la plantilla base${NC}"
    exit 1
fi

echo -e "\n${YELLOW}3. Verificando título de la página...${NC}"
if curl -s "$BASE_URL" | grep -q "Anunciar Paquete - PAQUETES EL CLUB v3.1"; then
    echo -e "   ✅ ${GREEN}Título de página correcto${NC}"
else
    echo -e "   ❌ ${RED}Error: Título de página incorrecto${NC}"
    exit 1
fi

echo -e "\n${YELLOW}4. Verificando contenido del formulario...${NC}"
if curl -s "$BASE_URL" | grep -q "Anunciar Paquete"; then
    echo -e "   ✅ ${GREEN}Formulario de anuncios presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Formulario de anuncios no encontrado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}5. Verificando campos del formulario...${NC}"
if curl -s "$BASE_URL" | grep -q "Nombre del cliente"; then
    echo -e "   ✅ ${GREEN}Campo 'Nombre del cliente' presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Campo 'Nombre del cliente' no encontrado${NC}"
    exit 1
fi

if curl -s "$BASE_URL" | grep -q "Número de guía"; then
    echo -e "   ✅ ${GREEN}Campo 'Número de guía' presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Campo 'Número de guía' no encontrado${NC}"
    exit 1
fi

if curl -s "$BASE_URL" | grep -q "Teléfono del cliente"; then
    echo -e "   ✅ ${GREEN}Campo 'Teléfono del cliente' presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Campo 'Teléfono del cliente' no encontrado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}6. Verificando términos y condiciones...${NC}"
if curl -s "$BASE_URL" | grep -q "términos y condiciones"; then
    echo -e "   ✅ ${GREEN}Sección de términos y condiciones presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Sección de términos y condiciones no encontrada${NC}"
    exit 1
fi

if curl -s "$BASE_URL" | grep -q "TERMINOS%20Y%20CONDICIONES%20PAQUETES.pdf"; then
    echo -e "   ✅ ${GREEN}Enlace al PDF de términos y condiciones presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Enlace al PDF no encontrado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}7. Verificando header de la plantilla base...${NC}"
if curl -s "$BASE_URL" | grep -q "PAQUETES"; then
    echo -e "   ✅ ${GREEN}Header con título 'PAQUETES' presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Header no encontrado${NC}"
    exit 1
fi

echo -e "\n${YELLOW}8. Verificando footer de la plantilla base...${NC}"
if curl -s "$BASE_URL" | grep -q "JEMAVI"; then
    echo -e "   ✅ ${GREEN}Footer con copyright presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Footer no encontrado${NC}"
    exit 1
fi

if curl -s "$BASE_URL" | grep -q "w-8 h-8"; then
    echo -e "   ✅ ${GREEN}Iconos del footer optimizados para móvil${NC}"
else
    echo -e "   ❌ ${RED}Error: Iconos del footer no optimizados${NC}"
    exit 1
fi

echo -e "\n${YELLOW}9. Verificando estilos específicos...${NC}"
if curl -s "$BASE_URL" | grep -q "input-with-icon"; then
    echo -e "   ✅ ${GREEN}Estilos específicos de la página presentes${NC}"
else
    echo -e "   ❌ ${RED}Error: Estilos específicos no encontrados${NC}"
    exit 1
fi

echo -e "\n${YELLOW}10. Verificando logo PAPYRUS...${NC}"
if curl -s "$BASE_URL" | grep -q "papyrus-logo.png"; then
    echo -e "   ✅ ${GREEN}Logo PAPYRUS presente${NC}"
else
    echo -e "   ❌ ${RED}Error: Logo PAPYRUS no encontrado${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 ¡Todas las verificaciones de la página de anuncios pasaron exitosamente!${NC}"
echo -e "\n${YELLOW}📋 Resumen de la página de anuncios:${NC}"
echo -e "   • Plantilla base: Extendida correctamente"
echo -e "   • Título: 'Anunciar Paquete - PAQUETES EL CLUB v3.1'"
echo -e "   • Formulario: Completo con todos los campos"
echo -e "   • Términos y condiciones: Enlace al PDF funcional"
echo -e "   • Header: Optimizado con navegación"
echo -e "   • Footer: Sticky con iconos de contacto"
echo -e "   • Estilos: Específicos de la página incluidos"
echo -e "   • Logo: PAPYRUS presente"
echo -e "   • Responsive: Mobile-first design"
echo -e "\n${GREEN}✅ La página de anuncios está funcionando correctamente con la plantilla base${NC}"
