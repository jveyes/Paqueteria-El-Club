#!/bin/bash

# Script de backup para PAQUETERIA EL CLUB v3.1
# Backup automático de la base de datos PostgreSQL

set -e

# Configuración
BACKUP_DIR="/app/database/backups"
RETENTION_DAYS=30
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="paqueteria_backup_${TIMESTAMP}.sql"

echo "🚀 Iniciando backup de la base de datos..."

# Crear directorio de backup si no existe
mkdir -p "$BACKUP_DIR"

# Realizar backup
echo "📦 Creando backup: $BACKUP_FILE"
docker exec paqueteria_v31_postgres pg_dump -U paqueteria_user -d paqueteria > "$BACKUP_DIR/$BACKUP_FILE"

# Comprimir backup
echo "🗜️ Comprimiendo backup..."
gzip "$BACKUP_DIR/$BACKUP_FILE"
BACKUP_FILE_COMPRESSED="$BACKUP_FILE.gz"

# Verificar que el backup se creó correctamente
if [ -f "$BACKUP_DIR/$BACKUP_FILE_COMPRESSED" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE_COMPRESSED" | cut -f1)
    echo "✅ Backup creado exitosamente: $BACKUP_FILE_COMPRESSED ($BACKUP_SIZE)"
else
    echo "❌ Error: No se pudo crear el backup"
    exit 1
fi

# Limpiar backups antiguos
echo "🧹 Limpiando backups antiguos (más de $RETENTION_DAYS días)..."
find "$BACKUP_DIR" -name "paqueteria_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Mostrar backups disponibles
echo ""
echo "📋 Backups disponibles:"
ls -lh "$BACKUP_DIR"/paqueteria_backup_*.sql.gz 2>/dev/null || echo "No hay backups disponibles"

echo ""
echo "🎯 Backup completado exitosamente!"
