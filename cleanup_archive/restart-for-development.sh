#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Script de Reinicio para Desarrollo
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 3.1.0
# Descripción: Reinicia los servicios para aplicar cambios de volúmenes

echo "🔄 Reiniciando servicios para desarrollo..."

# Detener todos los servicios
echo "⏹️  Deteniendo servicios..."
docker-compose down

# Limpiar caché de Docker
echo "🧹 Limpiando caché..."
docker system prune -f

# Reconstruir imágenes si es necesario
echo "🔨 Reconstruyendo imágenes..."
docker-compose build --no-cache

# Iniciar servicios
echo "▶️  Iniciando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado de los servicios
echo "🔍 Verificando estado de los servicios..."
docker-compose ps

echo "✅ Servicios reiniciados exitosamente!"
echo "🌐 La aplicación está disponible en: http://localhost"
echo "📱 API disponible en: http://localhost/api"
echo "📊 Métricas en: http://localhost/metrics"

# Mostrar logs de la aplicación
echo "📋 Mostrando logs de la aplicación..."
docker-compose logs -f app
