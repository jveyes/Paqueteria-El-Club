#!/bin/bash

# Script para verificar configuración SMS
echo "🔍 Verificando configuración SMS LIWA.co..."

# Verificar variables de entorno
echo "📋 Variables de entorno:"
echo "LIWA_API_KEY: ${LIWA_API_KEY:-'NO CONFIGURADA'}"
echo "LIWA_ACCOUNT: ${LIWA_ACCOUNT:-'NO CONFIGURADA'}"
echo "LIWA_PASSWORD: ${LIWA_PASSWORD:-'NO CONFIGURADA'}"

# Verificar archivo de configuración
echo -e "\n📁 Archivo de configuración:"
if [ -f "src/config.py" ]; then
    echo "✅ src/config.py existe"
    echo " Buscando configuración LIWA:"
    grep -n "liwa" src/config.py | head -5
else
    echo "❌ src/config.py no encontrado"
fi

# Verificar servicio SMS
echo -e "\n🔧 Servicio SMS:"
if [ -f "src/services/sms_service.py" ]; then
    echo "✅ sms_service.py existe"
else
    echo "❌ sms_service.py no encontrado"
fi

# Verificar dependencias
echo -e "\n📦 Dependencias:"
if command -v python3 &> /dev/null; then
    echo "✅ Python3 disponible"
    python3 --version
else
    echo "❌ Python3 no encontrado"
fi

echo -e "\n🏁 Verificación completada"
