#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Test PDF Link
# ========================================

echo "🔍 Verificando enlace de términos y condiciones..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
BASE_URL="http://localhost"
PDF_URL="/static/documents/TERMINOS%20Y%20CONDICIONES%20PAQUETES.pdf"
MAIN_PAGE_URL="/"

echo -e "\n${YELLOW}1. Verificando que el archivo PDF existe en el servidor...${NC}"
if curl -I "$BASE_URL$PDF_URL" > /dev/null 2>&1; then
    echo -e "   ✅ ${GREEN}PDF accesible en: $BASE_URL$PDF_URL${NC}"
else
    echo -e "   ❌ ${RED}Error: PDF no accesible${NC}"
    exit 1
fi

echo -e "\n${YELLOW}2. Verificando que el enlace está presente en la página principal...${NC}"
if curl -s "$BASE_URL$MAIN_PAGE_URL" | grep -q "términos y condiciones"; then
    echo -e "   ✅ ${GREEN}Enlace encontrado en la página principal${NC}"
else
    echo -e "   ❌ ${RED}Error: Enlace no encontrado en la página principal${NC}"
    exit 1
fi

echo -e "\n${YELLOW}3. Verificando que el enlace apunta al PDF correcto...${NC}"
if curl -s "$BASE_URL$MAIN_PAGE_URL" | grep -q "TERMINOS%20Y%20CONDICIONES%20PAQUETES.pdf"; then
    echo -e "   ✅ ${GREEN}Enlace apunta al archivo PDF correcto${NC}"
else
    echo -e "   ❌ ${RED}Error: Enlace no apunta al archivo PDF correcto${NC}"
    exit 1
fi

echo -e "\n${YELLOW}4. Verificando que el enlace se abre en nueva pestaña...${NC}"
if curl -s "$BASE_URL$MAIN_PAGE_URL" | grep -q "target=\"_blank\""; then
    echo -e "   ✅ ${GREEN}Enlace configurado para abrir en nueva pestaña${NC}"
else
    echo -e "   ❌ ${RED}Error: Enlace no configurado para abrir en nueva pestaña${NC}"
    exit 1
fi

echo -e "\n${YELLOW}5. Verificando contenido del PDF...${NC}"
PDF_SIZE=$(curl -sI "$BASE_URL$PDF_URL" | grep -i "content-length" | awk '{print $2}' | tr -d '\r')
if [ "$PDF_SIZE" -gt 0 ]; then
    echo -e "   ✅ ${GREEN}PDF tiene contenido válido (${PDF_SIZE} bytes)${NC}"
else
    echo -e "   ❌ ${RED}Error: PDF vacío o inválido${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 ¡Todas las verificaciones pasaron exitosamente!${NC}"
echo -e "\n${YELLOW}📋 Resumen:${NC}"
echo -e "   • Archivo PDF: $BASE_URL$PDF_URL"
echo -e "   • Tamaño: ${PDF_SIZE} bytes"
echo -e "   • Enlace: Presente en página principal"
echo -e "   • Comportamiento: Se abre en nueva pestaña"
echo -e "\n${GREEN}✅ El enlace de términos y condiciones está funcionando correctamente${NC}"
