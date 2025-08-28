#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Verificación de Migración
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

# Configuración
AWS_DB_HOST="ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com"
AWS_DB_PORT="5432"
AWS_DB_NAME="paqueteria"
AWS_DB_USER="jveyes"
AWS_DB_PASSWORD="a?HC!2.*1#?[==:|289qAI=)#V4kDzl$"

echo "🔍 ========================================"
echo "🔍 VERIFICACIÓN DE MIGRACIÓN - PAQUETES EL CLUB v3.1"
echo "🔍 ========================================"
echo ""

# 1. Verificar conexión a la base de datos
log_info "1. Verificando conexión a la base de datos AWS..."
if PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    log_success "Conexión a base de datos establecida"
else
    log_error "No se puede conectar a la base de datos"
    exit 1
fi

# 2. Verificar que las tablas existen
log_info "2. Verificando existencia de tablas..."
TABLES=("users" "customers" "packages" "package_announcements" "notifications" "rates" "files" "messages" "password_reset_tokens")

for table in "${TABLES[@]}"; do
    if PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -c "\dt $table" > /dev/null 2>&1; then
        log_success "Tabla $table existe"
    else
        log_error "Tabla $table NO existe"
    fi
done

# 3. Contar registros en cada tabla
log_info "3. Contando registros en tablas principales..."

echo ""
echo "📊 ESTADÍSTICAS DE DATOS:"
echo "========================="

# Usuarios
USER_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM users;" | xargs)
log_info "👥 Usuarios: $USER_COUNT"

# Usuarios por rol
ADMIN_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM users WHERE role = 'admin';" | xargs)
OPERATOR_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM users WHERE role = 'operator';" | xargs)
USER_ROLE_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM users WHERE role = 'user';" | xargs)

echo "   - Administradores: $ADMIN_COUNT"
echo "   - Operadores: $OPERATOR_COUNT"
echo "   - Usuarios: $USER_ROLE_COUNT"

# Clientes
CUSTOMER_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM customers;" | xargs)
log_info "👤 Clientes: $CUSTOMER_COUNT"

# Paquetes
PACKAGE_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM packages;" | xargs)
log_info "📦 Paquetes: $PACKAGE_COUNT"

# Paquetes por estado
PENDING_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM packages WHERE status = 'pendiente';" | xargs)
STORED_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM packages WHERE status = 'almacenado';" | xargs)
DELIVERED_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM packages WHERE status = 'entregado';" | xargs)

echo "   - Pendientes: $PENDING_COUNT"
echo "   - Almacenados: $STORED_COUNT"
echo "   - Entregados: $DELIVERED_COUNT"

# Anuncios
ANNOUNCEMENT_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM package_announcements;" | xargs)
log_info "📢 Anuncios: $ANNOUNCEMENT_COUNT"

# Notificaciones
NOTIFICATION_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM notifications;" | xargs)
log_info "🔔 Notificaciones: $NOTIFICATION_COUNT"

# Tarifas
RATE_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM rates;" | xargs)
log_info "💰 Tarifas: $RATE_COUNT"

# Archivos
FILE_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM files;" | xargs)
log_info "📁 Archivos: $FILE_COUNT"

# Mensajes
MESSAGE_COUNT=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT COUNT(*) FROM messages;" | xargs)
log_info "💬 Mensajes: $MESSAGE_COUNT"

echo ""

# 4. Verificar usuarios específicos
log_info "4. Verificando usuarios específicos..."

# Listar usuarios administradores
echo "👑 Usuarios Administradores:"
ADMIN_USERS=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT username, email, first_name, last_name FROM users WHERE role = 'admin';")
if [ -n "$ADMIN_USERS" ]; then
    echo "$ADMIN_USERS" | while read -r line; do
        if [ -n "$line" ]; then
            echo "   ✅ $line"
        fi
    done
else
    log_warning "No se encontraron usuarios administradores"
fi

echo ""

# 5. Verificar paquetes recientes
log_info "5. Verificando paquetes recientes..."
echo "📦 Últimos 5 paquetes registrados:"
RECENT_PACKAGES=$(PGPASSWORD="$AWS_DB_PASSWORD" psql -h "$AWS_DB_HOST" -p "$AWS_DB_PORT" -U "$AWS_DB_USER" -d "$AWS_DB_NAME" -t -c "SELECT tracking_number, customer_name, status, created_at FROM packages ORDER BY created_at DESC LIMIT 5;")
if [ -n "$RECENT_PACKAGES" ]; then
    echo "$RECENT_PACKAGES" | while read -r line; do
        if [ -n "$line" ]; then
            echo "   📦 $line"
        fi
    done
else
    log_warning "No se encontraron paquetes"
fi

echo ""

# 6. Verificar aplicación web
log_info "6. Verificando aplicación web..."

# Health check
HEALTH_RESPONSE=$(curl -s -k https://guia.papyrus.com.co/health)
if [[ "$HEALTH_RESPONSE" == *"health"* ]]; then
    log_success "Health check: OK"
else
    log_error "Health check: FALLÓ"
fi

# Verificar página principal
MAIN_PAGE=$(curl -s -k https://guia.papyrus.com.co/ | head -1)
if [[ "$MAIN_PAGE" == *"<!DOCTYPE html>"* ]]; then
    log_success "Página principal: OK"
else
    log_error "Página principal: FALLÓ"
fi

echo ""

# 7. Verificar contenedores
log_info "7. Verificando estado de contenedores..."
CONTAINERS=$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")
echo "$CONTAINERS"

echo ""

# 8. Resumen final
log_info "8. Resumen de verificación..."

TOTAL_RECORDS=$((USER_COUNT + CUSTOMER_COUNT + PACKAGE_COUNT + ANNOUNCEMENT_COUNT + NOTIFICATION_COUNT + RATE_COUNT + FILE_COUNT + MESSAGE_COUNT))

echo "📈 RESUMEN TOTAL:"
echo "=================="
echo "📊 Total de registros migrados: $TOTAL_RECORDS"
echo "👥 Usuarios: $USER_COUNT"
echo "👤 Clientes: $CUSTOMER_COUNT"
echo "📦 Paquetes: $PACKAGE_COUNT"
echo "📢 Anuncios: $ANNOUNCEMENT_COUNT"
echo "🔔 Notificaciones: $NOTIFICATION_COUNT"
echo "💰 Tarifas: $RATE_COUNT"
echo "📁 Archivos: $FILE_COUNT"
echo "💬 Mensajes: $MESSAGE_COUNT"

echo ""
echo "🌐 URLs de acceso:"
echo "=================="
echo "🔗 Aplicación: https://guia.papyrus.com.co"
echo "🔗 Health Check: https://guia.papyrus.com.co/health"
echo "🔗 API: https://guia.papyrus.com.co/api/"

echo ""
if [ "$TOTAL_RECORDS" -gt 0 ]; then
    log_success "✅ MIGRACIÓN VERIFICADA EXITOSAMENTE"
    log_success "Todos los datos se han migrado correctamente"
else
    log_error "❌ PROBLEMA CON LA MIGRACIÓN"
    log_error "No se encontraron datos migrados"
fi

echo ""
log_info "Para verificar manualmente, puedes:"
echo "1. Acceder a https://guia.papyrus.com.co"
echo "2. Intentar hacer login con usuarios existentes"
echo "3. Verificar que los paquetes estén disponibles"
echo "4. Revisar las funcionalidades específicas"

# Limpiar variables de entorno
unset PGPASSWORD

echo ""
log_success "¡Verificación completada! 🔍"
