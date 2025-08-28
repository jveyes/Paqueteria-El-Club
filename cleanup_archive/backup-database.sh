#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Backup de Base de Datos
# ========================================

echo "💾 Creando backup de la base de datos..."

# Crear directorio de backups si no existe
mkdir -p ../backups

# Generar nombre del archivo con timestamp
BACKUP_FILE="../backups/paqueteria_v31_$(date +%Y%m%d_%H%M%S).sql"

# Crear backup
docker-compose exec postgres pg_dump -U paqueteria_user paqueteria > $BACKUP_FILE

echo "✅ Backup creado: $BACKUP_FILE"
