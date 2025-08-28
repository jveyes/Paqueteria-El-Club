#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Configuración del Entorno
# ========================================

echo "🚀 Configurando entorno de PAQUETES EL CLUB v3.1..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

echo "✅ Docker y Docker Compose están instalados"

# Limpiar contenedores existentes
echo "🧹 Limpiando contenedores existentes..."
./cleanup-containers.sh

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p uploads logs static ssl
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p database/init

# Configurar archivo de entorno
echo "⚙️ Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "✅ Archivo .env creado desde env.example"
    echo "📝 Por favor edita .env con tus configuraciones específicas"
else
    echo "ℹ️ Archivo .env ya existe"
fi

echo "✅ Configuración del entorno completada!"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Edita .env con tus configuraciones"
echo "   2. Ejecuta: ./start-services.sh"
echo "   3. Accede a: http://localhost"
