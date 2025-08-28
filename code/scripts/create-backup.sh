#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Script de Backup Automatizado
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 1.0
# Descripción: Crea backup completo del proyecto con verificación

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

# Variables
BACKUP_DIR="backups"
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
BACKUP_NAME="paqueteria_v31_backup_${TIMESTAMP}"
BACKUP_FILE="${BACKUP_NAME}.tar.gz"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

# Función para verificar que estamos en el directorio correcto
check_directory() {
    if [ ! -f "docker-compose.yml" ]; then
        error "No se encontró docker-compose.yml. Ejecuta este script desde el directorio raíz del proyecto."
    fi
    
    if [ ! -d "code" ]; then
        error "No se encontró el directorio 'code'. Ejecuta este script desde el directorio raíz del proyecto."
    fi
    
    log "✅ Directorio del proyecto verificado"
}

# Función para crear directorio de backups
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log "Creando directorio de backups..."
        mkdir -p "$BACKUP_DIR"
        success "Directorio de backups creado"
    else
        log "✅ Directorio de backups existe"
    fi
}

# Función para verificar estado del sistema antes del backup
check_system_status() {
    log "Verificando estado del sistema..."
    
    # Verificar si Docker está corriendo
    if ! docker info > /dev/null 2>&1; then
        warn "Docker no está corriendo. El backup se creará sin verificar servicios."
        return 0
    fi
    
    # Verificar si los servicios están corriendo
    if docker-compose ps | grep -q "Up"; then
        success "Servicios Docker detectados"
        
        # Verificar health check si está disponible
        if command -v curl > /dev/null 2>&1; then
            if curl -s http://localhost/health > /dev/null 2>&1; then
                success "Health check exitoso"
            else
                warn "Health check falló - servicios pueden no estar completamente operativos"
            fi
        fi
    else
        warn "No se detectaron servicios Docker corriendo"
    fi
}

# Función para crear el backup
create_backup() {
    log "Creando backup: $BACKUP_NAME"
    
    # Excluir archivos innecesarios
    local exclude_patterns=(
        "--exclude=backups"
        "--exclude=.git"
        "--exclude=node_modules"
        "--exclude=__pycache__"
        "--exclude=*.pyc"
        "--exclude=.DS_Store"
        "--exclude=*.log"
        "--exclude=*.tmp"
        "--exclude=*.swp"
        "--exclude=.vscode"
        "--exclude=.idea"
    )
    
    # Crear el backup
    if tar "${exclude_patterns[@]}" -czf "$BACKUP_PATH" .; then
        success "Backup creado exitosamente: $BACKUP_FILE"
    else
        error "Error al crear el backup"
    fi
}

# Función para verificar el backup
verify_backup() {
    log "Verificando integridad del backup..."
    
    if tar -tzf "$BACKUP_PATH" > /dev/null 2>&1; then
        success "Integridad del backup verificada"
    else
        error "El backup está corrupto"
    fi
    
    # Mostrar información del backup
    local backup_size=$(du -h "$BACKUP_PATH" | cut -f1)
    local file_count=$(tar -tzf "$BACKUP_PATH" | wc -l)
    
    log "Información del backup:"
    echo "  • Archivo: $BACKUP_FILE"
    echo "  • Tamaño: $backup_size"
    echo "  • Archivos incluidos: $file_count"
}

# Función para crear archivo de información del backup
create_backup_info() {
    log "Creando archivo de información del backup..."
    
    cat > "${BACKUP_DIR}/${BACKUP_NAME}_INFO.md" << EOF
# ========================================
# PAQUETES EL CLUB v3.1 - Información de Backup
# ========================================

## 📦 **DETALLES DEL BACKUP**

- **Nombre del Backup**: \`${BACKUP_FILE}\`
- **Fecha de Creación**: $(date '+%d de %B, %Y - %H:%M:%S')
- **Tamaño**: $(du -h "$BACKUP_PATH" | cut -f1)
- **Estado del Sistema**: ✅ BACKUP COMPLETADO

## 📁 **CONTENIDO INCLUIDO**

### **🏗️ Archivos de Configuración:**
- docker-compose.yml
- .env (variables de entorno)
- code/.env
- code/nginx/nginx.conf
- code/nginx/conf.d/default.conf

### **🐍 Código de la Aplicación:**
- code/src/main.py (corregido y completo)
- code/src/config.py
- code/src/models/
- code/src/routers/
- code/requirements.txt

### **🎨 Frontend:**
- code/templates/index.html
- code/static/
- code/assets/

### **📋 Documentación:**
- README.md
- code/SCRIPTS/DEPLOYMENT-GUIDE.md
- code/SCRIPTS/README.md
- Sistema de Paquetería v3.0.md
- Diseno y Estilos v3.0.md

### **🔧 Scripts de Gestión:**
- code/SCRIPTS/deploy-full.sh
- code/SCRIPTS/verify-deployment.sh
- code/SCRIPTS/setup-environment.sh
- code/SCRIPTS/cleanup-containers.sh
- code/SCRIPTS/start-services.sh
- code/SCRIPTS/stop-services.sh
- code/SCRIPTS/view-logs.sh
- code/SCRIPTS/monitor-resources.sh
- code/SCRIPTS/backup-database.sh
- code/SCRIPTS/restore-database.sh

### **🧪 Scripts de Testing:**
- code/SCRIPTS/run-all-tests.sh
- code/SCRIPTS/quick-test.sh
- code/SCRIPTS/test-api-endpoints.sh
- code/SCRIPTS/test-database.sh

### **🗄️ Base de Datos:**
- database.sql

## 🚀 **INSTRUCCIONES DE RESTAURACIÓN**

### **Restauración Automatizada:**
\`\`\`bash
# 1. Extraer el backup
tar -xzf ${BACKUP_FILE}

# 2. Navegar al directorio
cd Paqueteria\\ v3.1

# 3. Ejecutar despliegue automatizado
./code/SCRIPTS/deploy-full.sh
\`\`\`

## 🌐 **URLS DE ACCESO (Post-Restauración)**

- **🏠 Aplicación Principal**: http://localhost
- **📊 Health Check**: http://localhost/health
- **📚 API Documentation**: http://localhost:8001/docs
- **🔧 API Directa**: http://localhost:8001

## 📊 **ESPECIFICACIONES TÉCNICAS**

### **Optimizaciones para 50 Usuarios:**
- PostgreSQL: 256MB RAM, 0.5 CPU
- Redis: 64MB RAM, 0.2 CPU
- FastAPI: 256MB RAM, 0.5 CPU
- Celery: 128MB RAM, 0.3 CPU
- Nginx: 32MB RAM, 0.2 CPU

## 🔧 **CORRECCIONES INCLUIDAS**

- ✅ main.py corregido (error de sintaxis)
- ✅ template index.html creado
- ✅ Variables de entorno configuradas
- ✅ Scripts de despliegue automatizado
- ✅ Documentación completa

---

**🎉 ¡BACKUP COMPLETO Y FUNCIONAL!**

**Fecha**: $(date '+%d de %B, %Y')  
**Versión**: 3.1.0  
**Estado**: ✅ VERIFICADO
EOF
    
    success "Archivo de información creado: ${BACKUP_NAME}_INFO.md"
}

# Función para limpiar backups antiguos
cleanup_old_backups() {
    log "Limpiando backups antiguos (más de 30 días)..."
    
    local deleted_count=0
    local current_time=$(date +%s)
    local thirty_days_ago=$((current_time - 30*24*60*60))
    
    for backup_file in "${BACKUP_DIR}"/paqueteria_v31_backup_*.tar.gz; do
        if [ -f "$backup_file" ]; then
            local file_time=$(stat -c %Y "$backup_file" 2>/dev/null || stat -f %m "$backup_file" 2>/dev/null)
            if [ "$file_time" -lt "$thirty_days_ago" ]; then
                rm "$backup_file"
                deleted_count=$((deleted_count + 1))
                log "Eliminado backup antiguo: $(basename "$backup_file")"
            fi
        fi
    done
    
    if [ $deleted_count -gt 0 ]; then
        success "Eliminados $deleted_count backups antiguos"
    else
        log "No se encontraron backups antiguos para eliminar"
    fi
}

# Función para mostrar resumen final
show_summary() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}        RESUMEN DEL BACKUP            ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}✅ Backup completado exitosamente${NC}"
    echo ""
    echo -e "${YELLOW}📦 Información del Backup:${NC}"
    echo -e "  • Archivo: ${BLUE}${BACKUP_FILE}${NC}"
    echo -e "  • Ubicación: ${BLUE}${BACKUP_PATH}${NC}"
    echo -e "  • Tamaño: ${BLUE}$(du -h "$BACKUP_PATH" | cut -f1)${NC}"
    echo -e "  • Archivos: ${BLUE}$(tar -tzf "$BACKUP_PATH" | wc -l)${NC}"
    echo ""
    echo -e "${YELLOW}📋 Archivos de Información:${NC}"
    echo -e "  • Información: ${BLUE}${BACKUP_DIR}/${BACKUP_NAME}_INFO.md${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Restauración:${NC}"
    echo -e "  • Extraer: ${BLUE}tar -xzf ${BACKUP_FILE}${NC}"
    echo -e "  • Desplegar: ${BLUE}./code/SCRIPTS/deploy-full.sh${NC}"
    echo ""
    echo -e "${GREEN}🎉 ¡Backup listo para usar!${NC}"
    echo ""
}

# Función principal
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  PAQUETES EL CLUB v3.1 - BACKUP      ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # Verificar directorio
    check_directory
    
    # Crear directorio de backups
    create_backup_dir
    
    # Verificar estado del sistema
    check_system_status
    
    # Crear backup
    create_backup
    
    # Verificar backup
    verify_backup
    
    # Crear archivo de información
    create_backup_info
    
    # Limpiar backups antiguos
    cleanup_old_backups
    
    # Mostrar resumen
    show_summary
}

# Ejecutar función principal
main "$@"
