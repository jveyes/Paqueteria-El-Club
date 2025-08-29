#!/bin/bash

# ========================================
# SCRIPT DE DESPLIEGUE AWS - PAQUETES EL CLUB v3.1
# ========================================

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Configuración
PROJECT_DIR="/home/ubuntu/Paquetes/code"
BACKUP_DIR="/home/ubuntu/Paquetes/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="paqueteria_backup_${TIMESTAMP}.tar.gz"

# Función para crear backup
create_backup() {
    log "Creando backup de la versión actual..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup de volúmenes Docker
    if docker volume ls | grep -q "code_postgres_data"; then
        docker run --rm -v code_postgres_data:/data -v "$BACKUP_DIR":/backup alpine tar czf "/backup/postgres_data_${TIMESTAMP}.tar.gz" -C /data .
        success "Backup de PostgreSQL creado"
    fi
    
    if docker volume ls | grep -q "code_redis_data"; then
        docker run --rm -v code_redis_data:/data -v "$BACKUP_DIR":/backup alpine tar czf "/backup/redis_data_${TIMESTAMP}.tar.gz" -C /data .
        success "Backup de Redis creado"
    fi
    
    # Backup de archivos de configuración
    tar czf "$BACKUP_DIR/$BACKUP_NAME" \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='logs/*' \
        --exclude='uploads/*' \
        -C "$PROJECT_DIR" .
    
    success "Backup completo creado: $BACKUP_NAME"
}

# Función para verificar estado de servicios
check_services() {
    log "Verificando estado de servicios..."
    
    # Verificar que Docker esté corriendo
    if ! docker info > /dev/null 2>&1; then
        error "Docker no está corriendo"
        return 1
    fi
    
    # Verificar que docker-compose esté disponible
    if ! command -v docker-compose > /dev/null 2>&1; then
        error "docker-compose no está instalado"
        return 1
    fi
    
    success "Servicios básicos verificados"
}

# Función para detener servicios
stop_services() {
    log "Deteniendo servicios actuales..."
    
    cd "$PROJECT_DIR"
    
    if docker-compose -f docker-compose.aws.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.aws.yml down
        success "Servicios detenidos"
    else
        warning "No hay servicios corriendo"
    fi
}

# Función para limpiar recursos no utilizados
cleanup_docker() {
    log "Limpiando recursos Docker no utilizados..."
    
    # Limpiar contenedores detenidos
    docker container prune -f
    
    # Limpiar imágenes no utilizadas
    docker image prune -f
    
    # Limpiar redes no utilizadas
    docker network prune -f
    
    success "Limpieza completada"
}

# Función para actualizar código desde GitHub
update_code() {
    log "Actualizando código desde GitHub..."
    
    cd "$PROJECT_DIR"
    
    # Verificar si hay cambios pendientes
    if git status --porcelain | grep -q .; then
        warning "Hay cambios locales no committeados"
        git stash
    fi
    
    # Hacer pull del código
    git fetch origin
    git reset --hard origin/main
    
    success "Código actualizado desde GitHub"
}

# Función para verificar archivos de configuración
verify_config() {
    log "Verificando archivos de configuración..."
    
    cd "$PROJECT_DIR"
    
    # Verificar archivos críticos
    required_files=(
        "docker-compose.aws.yml"
        "env.aws"
        "nginx/conf.d/nginx-papyrus.conf"
        "database/init.sql"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            error "Archivo requerido no encontrado: $file"
            return 1
        fi
    done
    
    success "Archivos de configuración verificados"
}

# Función para construir y levantar servicios
start_services() {
    log "Construyendo y levantando servicios..."
    
    cd "$PROJECT_DIR"
    
    # Construir imágenes
    docker-compose -f docker-compose.aws.yml build --no-cache
    
    # Levantar servicios
    docker-compose -f docker-compose.aws.yml up -d
    
    success "Servicios levantados"
}

# Función para health checks
health_checks() {
    log "Realizando health checks..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log "Health check intento $attempt/$max_attempts"
        
        # Verificar que todos los contenedores estén corriendo
        if docker-compose -f docker-compose.aws.yml ps | grep -q "Up"; then
            # Verificar health endpoint
            if curl -f -s http://localhost/health > /dev/null 2>&1; then
                success "Health check exitoso"
                return 0
            fi
        fi
        
        sleep 10
        ((attempt++))
    done
    
    error "Health check falló después de $max_attempts intentos"
    return 1
}

# Función para verificar logs
check_logs() {
    log "Verificando logs de servicios..."
    
    cd "$PROJECT_DIR"
    
    # Verificar logs de la aplicación
    if docker-compose -f docker-compose.aws.yml logs app | grep -q "ERROR"; then
        warning "Errores encontrados en logs de la aplicación"
        docker-compose -f docker-compose.aws.yml logs app --tail=20
    else
        success "Logs de aplicación sin errores críticos"
    fi
    
    # Verificar logs de nginx
    if docker-compose -f docker-compose.aws.yml logs nginx | grep -q "ERROR"; then
        warning "Errores encontrados en logs de nginx"
        docker-compose -f docker-compose.aws.yml logs nginx --tail=10
    else
        success "Logs de nginx sin errores críticos"
    fi
}

# Función para mostrar estado final
show_status() {
    log "Estado final de servicios:"
    
    cd "$PROJECT_DIR"
    docker-compose -f docker-compose.aws.yml ps
    
    echo ""
    log "URLs de acceso:"
    echo "  🌐 HTTP:  http://guia.papyrus.com.co"
    echo "  🔒 HTTPS: https://guia.papyrus.com.co"
    echo "  📊 Health: https://guia.papyrus.com.co/health"
    echo "  📚 API Docs: https://guia.papyrus.com.co/docs"
}

# Función principal
main() {
    echo "=========================================="
    echo "🚀 DESPLIEGUE AWS - PAQUETES EL CLUB v3.1"
    echo "=========================================="
    echo ""
    
    # Verificar que estamos en el directorio correcto
    if [[ ! -d "$PROJECT_DIR" ]]; then
        error "Directorio del proyecto no encontrado: $PROJECT_DIR"
        exit 1
    fi
    
    # Ejecutar pasos de despliegue
    check_services || exit 1
    create_backup
    stop_services
    cleanup_docker
    update_code
    verify_config || exit 1
    start_services
    health_checks || exit 1
    check_logs
    show_status
    
    echo ""
    success "🎉 Despliegue completado exitosamente!"
    echo ""
    echo "📋 Resumen:"
    echo "  • Backup creado: $BACKUP_NAME"
    echo "  • Código actualizado desde GitHub"
    echo "  • Servicios reiniciados"
    echo "  • Health checks pasados"
    echo ""
    echo "🔗 Acceso: https://guia.papyrus.com.co"
}

# Ejecutar función principal
main "$@"
