#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Verificación Simple de Migración
# ========================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

echo "🔍 ========================================"
echo "🔍 VERIFICACIÓN SIMPLE DE MIGRACIÓN"
echo "🔍 PAQUETES EL CLUB v3.1"
echo "🔍 ========================================"
echo ""

# 1. Verificar que la aplicación esté funcionando
log_info "1. Verificando estado de la aplicación..."

# Health check
HEALTH_RESPONSE=$(curl -s -k https://guia.papyrus.com.co/health)
if [[ "$HEALTH_RESPONSE" == *"health"* ]]; then
    log_success "Health check: OK - $HEALTH_RESPONSE"
else
    log_error "Health check: FALLÓ"
    exit 1
fi

# 2. Verificar página principal
log_info "2. Verificando página principal..."
MAIN_PAGE=$(curl -s -k https://guia.papyrus.com.co/ | head -1)
if [[ "$MAIN_PAGE" == *"<!DOCTYPE html>"* ]]; then
    log_success "Página principal: OK"
else
    log_error "Página principal: FALLÓ"
fi

# 3. Verificar estado de contenedores
log_info "3. Verificando estado de contenedores..."
CONTAINER_STATUS=$(docker ps --format "table {{.Names}}\t{{.Status}}")
echo "$CONTAINER_STATUS"

# 4. Verificar logs de la aplicación
log_info "4. Verificando logs de la aplicación..."
APP_LOGS=$(docker logs paqueteria_v31_app --tail 5)
echo "Últimos 5 logs de la aplicación:"
echo "$APP_LOGS"

# 5. Verificar que la aplicación puede acceder a la base de datos
log_info "5. Verificando acceso a base de datos desde la aplicación..."

# Intentar acceder a un endpoint que requiera base de datos
API_RESPONSE=$(curl -s -k https://guia.papyrus.com.co/api/health)
if [[ "$API_RESPONSE" == *"health"* ]] || [[ "$API_RESPONSE" == *"status"* ]]; then
    log_success "API health check: OK"
else
    log_warning "API health check: No disponible o diferente formato"
fi

# 6. Verificar archivos de migración
log_info "6. Verificando archivos de migración..."
if [ -f "/home/ubuntu/Paquetes/migration_backup/paqueteria_local_20250828_083834.sql" ]; then
    BACKUP_SIZE=$(du -h /home/ubuntu/Paquetes/migration_backup/paqueteria_local_20250828_083834.sql | cut -f1)
    log_success "Backup encontrado: $BACKUP_SIZE"
else
    log_warning "Backup no encontrado"
fi

# 7. Verificar configuración de la aplicación
log_info "7. Verificando configuración de la aplicación..."
if [ -f "/home/ubuntu/Paquetes/.env" ]; then
    log_success "Archivo .env encontrado"
    # Verificar que la configuración de base de datos esté presente
    if grep -q "DATABASE_URL" /home/ubuntu/Paquetes/.env; then
        log_success "Configuración de base de datos presente"
    else
        log_warning "Configuración de base de datos no encontrada"
    fi
else
    log_error "Archivo .env no encontrado"
fi

echo ""
echo "📊 RESUMEN DE VERIFICACIÓN:"
echo "============================"

# Contar contenedores funcionando
RUNNING_CONTAINERS=$(docker ps --format "{{.Names}}" | wc -l)
log_info "Contenedores funcionando: $RUNNING_CONTAINERS"

# Verificar contenedores específicos
if docker ps --format "{{.Names}}" | grep -q "paqueteria_v31_app"; then
    log_success "Contenedor de aplicación: FUNCIONANDO"
else
    log_error "Contenedor de aplicación: NO FUNCIONANDO"
fi

if docker ps --format "{{.Names}}" | grep -q "paqueteria_v31_nginx"; then
    log_success "Contenedor de Nginx: FUNCIONANDO"
else
    log_error "Contenedor de Nginx: NO FUNCIONANDO"
fi

if docker ps --format "{{.Names}}" | grep -q "paqueteria_v31_redis"; then
    log_success "Contenedor de Redis: FUNCIONANDO"
else
    log_error "Contenedor de Redis: NO FUNCIONANDO"
fi

echo ""
echo "🌐 URLs DE ACCESO:"
echo "=================="
echo "🔗 Aplicación: https://guia.papyrus.com.co"
echo "🔗 Health Check: https://guia.papyrus.com.co/health"
echo "🔗 API: https://guia.papyrus.com.co/api/"

echo ""
echo "🔍 VERIFICACIÓN MANUAL RECOMENDADA:"
echo "==================================="
echo "1. 🌐 Acceder a https://guia.papyrus.com.co"
echo "2. 🔐 Intentar hacer login con usuarios existentes"
echo "3. 📦 Verificar que los paquetes estén disponibles"
echo "4. 👥 Verificar listado de clientes"
echo "5. 📢 Verificar anuncios de paquetes"
echo "6. ⚙️  Verificar configuraciones del sistema"

echo ""
if [[ "$HEALTH_RESPONSE" == *"health"* ]] && [[ "$MAIN_PAGE" == *"<!DOCTYPE html>"* ]]; then
    log_success "✅ VERIFICACIÓN BÁSICA EXITOSA"
    log_success "La aplicación está funcionando correctamente"
    log_info "Los datos se han migrado si la aplicación responde correctamente"
else
    log_error "❌ VERIFICACIÓN BÁSICA FALLÓ"
    log_error "Hay problemas con la aplicación"
fi

echo ""
log_info "Para una verificación completa de datos, accede manualmente a la aplicación"
log_success "¡Verificación completada! 🔍"
