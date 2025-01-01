#!/bin/bash

# ========================================
# Script para crear Pull Request en GitHub
# ========================================

echo "🚀 CREANDO PULL REQUEST EN GITHUB"
echo "=================================="

# Información del repositorio
REPO_URL="https://github.com/jveyes/Paqueteria-El-Club"
PR_URL="${REPO_URL}/compare/main...develop"

echo "📋 INFORMACIÓN DEL PULL REQUEST:"
echo "   Repositorio: $REPO_URL"
echo "   Rama origen: develop"
echo "   Rama destino: main"
echo "   URL del PR: $PR_URL"
echo ""

echo "📝 DESCRIPCIÓN DEL PR:"
echo "   - Reorganización completa del proyecto"
echo "   - Corrección del sistema SMTP"
echo "   - Limpieza de archivos temporales"
echo "   - Mejoras en la estructura del código"
echo ""

echo "🔗 ABRIENDO PULL REQUEST EN EL NAVEGADOR..."
echo "   URL: $PR_URL"
echo ""

# Intentar abrir en el navegador
if command -v xdg-open > /dev/null; then
    xdg-open "$PR_URL"
elif command -v open > /dev/null; then
    open "$PR_URL"
elif command -v start > /dev/null; then
    start "$PR_URL"
else
    echo "⚠️  No se pudo abrir automáticamente el navegador"
    echo "   Por favor, copia y pega esta URL en tu navegador:"
    echo "   $PR_URL"
fi

echo ""
echo "📋 PASOS PARA COMPLETAR EL PULL REQUEST:"
echo "1. Copia el contenido de PULL_REQUEST_TEMPLATE.md"
echo "2. Pega la descripción en el campo 'Description' del PR"
echo "3. Asigna el título: 'feat: Reorganización completa y corrección de SMTP'"
echo "4. Asigna reviewers si es necesario"
echo "5. Haz clic en 'Create pull request'"
echo ""

echo "✅ ¡Listo! El Pull Request está listo para ser creado."
