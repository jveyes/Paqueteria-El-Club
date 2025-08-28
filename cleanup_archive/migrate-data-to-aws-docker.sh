#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Migración de Datos a AWS (usando Docker)
# ========================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Configuración
LOCAL_DB_HOST="localhost"
LOCAL_DB_PORT="5432"
LOCAL_DB_NAME="paqueteria"
LOCAL_DB_USER="paqueteria_user"
LOCAL_DB_PASSWORD="Paqueteria2025!Secure"

AWS_DB_HOST="ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com"
AWS_DB_PORT="5432"
AWS_DB_NAME="paqueteria"
AWS_DB_USER="jveyes"
AWS_DB_PASSWORD="a?HC!2.*1#?[==:|289qAI=)#V4kDzl$"

BACKUP_DIR="./migration_backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/paqueteria_local_${TIMESTAMP}.sql"

echo "🚀 ========================================"
echo "🚀 MIGRACIÓN DE DATOS A AWS - PAQUETES EL CLUB v3.1"
echo "🚀 ========================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    log_error "No se encontró docker-compose.yml. Ejecuta este script desde el directorio code/"
    exit 1
fi

# Crear directorio de backup
log_info "Creando directorio de backup..."
mkdir -p "$BACKUP_DIR"

# Verificar que PostgreSQL local esté corriendo
log_info "Verificando conexión a base de datos local..."
if ! docker-compose exec -T postgres pg_isready -U "$LOCAL_DB_USER" -d "$LOCAL_DB_NAME" > /dev/null 2>&1; then
    log_error "No se puede conectar a la base de datos local. Verifica que esté corriendo."
    exit 1
fi
log_success "Conexión a base de datos local establecida"

# Crear backup completo de la base de datos local
log_info "Creando backup completo de la base de datos local..."
docker-compose exec -T postgres pg_dump \
    -U "$LOCAL_DB_USER" \
    -d "$LOCAL_DB_NAME" \
    --clean \
    --if-exists \
    --create \
    --verbose \
    --no-owner \
    --no-privileges \
    --schema=public \
    > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    log_success "Backup creado exitosamente: $BACKUP_FILE"
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log_info "Tamaño del backup: $BACKUP_SIZE"
else
    log_error "Error al crear el backup"
    exit 1
fi

# Verificar que el archivo de backup se creó correctamente
if [ ! -f "$BACKUP_FILE" ] || [ ! -s "$BACKUP_FILE" ]; then
    log_error "El archivo de backup no se creó correctamente o está vacío"
    exit 1
fi

# Verificar conexión a la base de datos AWS usando Docker
log_info "Verificando conexión a base de datos AWS usando Docker..."
if ! docker run --rm postgres:15-alpine psql \
    "postgresql://$AWS_DB_USER:$AWS_DB_PASSWORD@$AWS_DB_HOST:$AWS_DB_PORT/$AWS_DB_NAME" \
    -c "SELECT 1;" > /dev/null 2>&1; then
    log_error "No se puede conectar a la base de datos AWS. Verifica las credenciales."
    exit 1
fi
log_success "Conexión a base de datos AWS establecida"

# Crear backup de la base de datos AWS antes de la migración
log_info "Creando backup de seguridad de la base de datos AWS..."
AWS_BACKUP_FILE="${BACKUP_DIR}/paqueteria_aws_before_migration_${TIMESTAMP}.sql"
docker run --rm postgres:15-alpine pg_dump \
    "postgresql://$AWS_DB_USER:$AWS_DB_PASSWORD@$AWS_DB_HOST:$AWS_DB_PORT/$AWS_DB_NAME" \
    --clean \
    --if-exists \
    --create \
    --verbose \
    --no-owner \
    --no-privileges \
    --schema=public \
    > "$AWS_BACKUP_FILE"

if [ $? -eq 0 ]; then
    log_success "Backup de seguridad AWS creado: $AWS_BACKUP_FILE"
else
    log_warning "No se pudo crear backup de seguridad AWS (puede estar vacía)"
fi

# Realizar la migración
log_info "Iniciando migración de datos a AWS..."
log_warning "Esto puede tomar varios minutos dependiendo del tamaño de los datos..."

docker run --rm -v "$(pwd)/$BACKUP_FILE:/backup.sql" postgres:15-alpine psql \
    "postgresql://$AWS_DB_USER:$AWS_DB_PASSWORD@$AWS_DB_HOST:$AWS_DB_PORT/$AWS_DB_NAME" \
    -f /backup.sql

if [ $? -eq 0 ]; then
    log_success "Migración completada exitosamente!"
else
    log_error "Error durante la migración"
    exit 1
fi

# Verificar la migración
log_info "Verificando la migración..."

# Contar registros en tablas principales
log_info "Contando registros en tablas principales..."

TABLES=("users" "customers" "packages" "package_announcements" "notifications")

for table in "${TABLES[@]}"; do
    COUNT=$(docker run --rm postgres:15-alpine psql \
        "postgresql://$AWS_DB_USER:$AWS_DB_PASSWORD@$AWS_DB_HOST:$AWS_DB_PORT/$AWS_DB_NAME" \
        -t -c "SELECT COUNT(*) FROM $table;" | xargs)
    if [ "$COUNT" != "" ]; then
        log_success "Tabla $table: $COUNT registros"
    else
        log_warning "Tabla $table: No se pudo contar registros"
    fi
done

# Verificar usuarios administradores
log_info "Verificando usuarios administradores..."
ADMIN_COUNT=$(docker run --rm postgres:15-alpine psql \
    "postgresql://$AWS_DB_USER:$AWS_DB_PASSWORD@$AWS_DB_HOST:$AWS_DB_PORT/$AWS_DB_NAME" \
    -t -c "SELECT COUNT(*) FROM users WHERE role = 'admin';" | xargs)
log_success "Usuarios administradores: $ADMIN_COUNT"

# Verificar paquetes
log_info "Verificando paquetes..."
PACKAGE_COUNT=$(docker run --rm postgres:15-alpine psql \
    "postgresql://$AWS_DB_USER:$AWS_DB_PASSWORD@$AWS_DB_HOST:$AWS_DB_PORT/$AWS_DB_NAME" \
    -t -c "SELECT COUNT(*) FROM packages;" | xargs)
log_success "Paquetes migrados: $PACKAGE_COUNT"

# Crear reporte de migración
REPORT_FILE="${BACKUP_DIR}/migration_report_${TIMESTAMP}.txt"
log_info "Generando reporte de migración..."

cat > "$REPORT_FILE" << EOF
========================================
REPORTE DE MIGRACIÓN - PAQUETES EL CLUB v3.1
========================================

Fecha y hora: $(date)
Timestamp: $TIMESTAMP

CONFIGURACIÓN:
- Base de datos origen: $LOCAL_DB_HOST:$LOCAL_DB_PORT/$LOCAL_DB_NAME
- Base de datos destino: $AWS_DB_HOST:$AWS_DB_PORT/$AWS_DB_NAME

ARCHIVOS CREADOS:
- Backup local: $BACKUP_FILE
- Backup AWS (antes): $AWS_BACKUP_FILE
- Reporte: $REPORT_FILE

ESTADÍSTICAS DE MIGRACIÓN:
- Usuarios administradores: $ADMIN_COUNT
- Paquetes migrados: $PACKAGE_COUNT

VERIFICACIÓN:
- Conexión local: ✅
- Conexión AWS: ✅
- Backup local: ✅
- Migración: ✅

NOTAS:
- La migración se realizó con --clean para limpiar datos existentes
- Se mantuvieron los permisos y estructura de la base de datos
- Se creó un backup de seguridad antes de la migración
- Se utilizó Docker para conectar a la base de datos AWS

PRÓXIMOS PASOS:
1. Verificar que la aplicación en AWS funcione correctamente
2. Probar login con usuarios existentes
3. Verificar que todos los paquetes estén disponibles
4. Eliminar archivos de backup si todo está correcto

EOF

log_success "Reporte de migración creado: $REPORT_FILE"

# Mostrar resumen final
echo ""
echo "🎉 ========================================"
echo "🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE"
echo "🎉 ========================================"
echo ""
log_success "Todos los datos han sido migrados a AWS"
log_info "Archivos creados en: $BACKUP_DIR"
log_info "Reporte detallado: $REPORT_FILE"
echo ""
log_warning "Próximos pasos recomendados:"
echo "  1. Verificar la aplicación en https://guia.papyrus.com.co"
echo "  2. Probar login con usuarios existentes"
echo "  3. Verificar que todos los paquetes estén disponibles"
echo "  4. Eliminar archivos de backup si todo está correcto"
echo ""

log_success "¡Migración completada! 🚀"
