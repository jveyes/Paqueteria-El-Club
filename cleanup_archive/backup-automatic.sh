#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - BACKUP AUTOMÁTICO
# ========================================

set -e

# Configuración
BACKUP_DIR="./backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="paqueteria_v31_backup_${DATE}"
LOG_FILE="./backups/backup_${DATE}.log"

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

# Función principal
main() {
    log "Iniciando backup automático..."
    
    # Crear directorio de backup si no existe
    mkdir -p "$BACKUP_DIR"
    
    # Backup de la base de datos
    log "Creando backup de la base de datos..."
    if docker exec paqueteria_v31_postgres pg_dump -U postgres paqueteria > "$BACKUP_DIR/${BACKUP_NAME}_database.sql"; then
        success "Backup de base de datos creado: ${BACKUP_NAME}_database.sql"
    else
        error "Error al crear backup de base de datos"
        return 1
    fi
    
    # Backup de archivos del proyecto
    log "Creando backup de archivos del proyecto..."
    if tar -czf "$BACKUP_DIR/${BACKUP_NAME}_files.tar.gz" \
        --exclude='./backups' \
        --exclude='./node_modules' \
        --exclude='./.git' \
        --exclude='./*.log' \
        .; then
        success "Backup de archivos creado: ${BACKUP_NAME}_files.tar.gz"
    else
        error "Error al crear backup de archivos"
        return 1
    fi
    
    # Backup de configuración
    log "Creando backup de configuración..."
    if tar -czf "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz" \
        .env \
        code/.env \
        docker-compose.yml \
        code/nginx/; then
        success "Backup de configuración creado: ${BACKUP_NAME}_config.tar.gz"
    else
        error "Error al crear backup de configuración"
        return 1
    fi
    
    # Crear archivo de información
    cat > "$BACKUP_DIR/${BACKUP_NAME}_info.md" << EOF
# Backup PAQUETES EL CLUB v3.1

**Fecha:** $(date)
**Versión:** 3.1.0
**Tipo:** Backup automático

## Archivos incluidos:
- \`${BACKUP_NAME}_database.sql\`: Dump completo de PostgreSQL
- \`${BACKUP_NAME}_files.tar.gz\`: Archivos del proyecto
- \`${BACKUP_NAME}_config.tar.gz\`: Configuración y nginx

## Tamaños:
- Database: $(du -h "$BACKUP_DIR/${BACKUP_NAME}_database.sql" | cut -f1)
- Files: $(du -h "$BACKUP_DIR/${BACKUP_NAME}_files.tar.gz" | cut -f1)
- Config: $(du -h "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz" | cut -f1)

## Estado del sistema:
- Contenedores: $(docker ps --format "table {{.Names}}\t{{.Status}}" | grep paqueteria_v31 | wc -l) corriendo
- Memoria: $(free -h | grep Mem | awk '{print $3"/"$2}')
- Disco: $(df -h / | tail -1 | awk '{print $5}')

## Comandos útiles:
\`\`\`bash
# Restaurar base de datos
docker exec -i paqueteria_v31_postgres psql -U postgres paqueteria < ${BACKUP_NAME}_database.sql

# Extraer archivos
tar -xzf ${BACKUP_NAME}_files.tar.gz

# Extraer configuración
tar -xzf ${BACKUP_NAME}_config.tar.gz
\`\`\`
EOF
    
    success "Archivo de información creado: ${BACKUP_NAME}_info.md"
    
    # Limpiar backups antiguos (mantener solo los últimos 7 días)
    log "Limpiando backups antiguos..."
    find "$BACKUP_DIR" -name "paqueteria_v31_backup_*.tar.gz" -mtime +7 -delete
    find "$BACKUP_DIR" -name "paqueteria_v31_backup_*.sql" -mtime +7 -delete
    find "$BACKUP_DIR" -name "paqueteria_v31_backup_*.md" -mtime +7 -delete
    find "$BACKUP_DIR" -name "backup_*.log" -mtime +7 -delete
    
    # Resumen final
    echo ""
    echo "========================================"
    echo "        RESUMEN DEL BACKUP              "
    echo "========================================"
    echo "Backup completado: $BACKUP_NAME"
    echo "Ubicación: $BACKUP_DIR"
    echo "Log: $LOG_FILE"
    echo ""
    echo "Archivos creados:"
    ls -lh "$BACKUP_DIR/${BACKUP_NAME}"*
    echo ""
    
    success "🎉 Backup automático completado exitosamente"
}

# Ejecutar función principal
main "$@"
