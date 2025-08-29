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

# Función para resolver conflictos de Git automáticamente
resolve_git_conflicts() {
    log "Resolviendo conflictos de Git automáticamente..."
    
    cd "$PROJECT_DIR"
    
    # Verificar si hay cambios locales
    if git status --porcelain | grep -q .; then
        warning "Hay cambios locales no committeados"
        
        # Crear backup de cambios locales
        git stash push -m "Backup cambios locales antes del despliegue - $(date)"
        success "Cambios locales guardados en stash"
    fi
    
    # Verificar archivos no rastreados que puedan causar conflictos
    untracked_files=$(git ls-files --others --exclude-standard)
    if [[ -n "$untracked_files" ]]; then
        warning "Archivos no rastreados encontrados"
        
        # Mover archivos conflictivos a backup
        for file in $untracked_files; do
            if [[ -f "$file" ]]; then
                backup_file="${file}.backup.${TIMESTAMP}"
                mkdir -p "$(dirname "$backup_file")"
                mv "$file" "$backup_file"
                log "Archivo movido a backup: $file -> $backup_file"
            fi
        done
        success "Archivos no rastreados movidos a backup"
    fi
    
    # Verificar si hay conflictos de merge
    if git ls-files --unmerged | grep -q .; then
        warning "Conflictos de merge detectados"
        
        # Abortar merge en progreso
        git merge --abort 2>/dev/null || true
        success "Merge abortado"
    fi
    
    # Verificar si hay rebase en progreso
    if [[ -d ".git/rebase-merge" ]] || [[ -d ".git/rebase-apply" ]]; then
        warning "Rebase en progreso detectado"
        
        # Abortar rebase
        git rebase --abort 2>/dev/null || true
        success "Rebase abortado"
    fi
}

# Función para actualizar código desde GitHub
update_code() {
    log "Actualizando código desde GitHub..."
    
    cd "$PROJECT_DIR"
    
    # Resolver conflictos antes de actualizar
    resolve_git_conflicts
    
    # Verificar conexión a GitHub
    if ! git ls-remote origin > /dev/null 2>&1; then
        error "No se puede conectar a GitHub. Verificar conexión a internet."
        return 1
    fi
    
    # Hacer fetch de los cambios
    log "Obteniendo cambios desde GitHub..."
    git fetch origin main
    
    # Verificar si hay cambios nuevos
    local_commit=$(git rev-parse HEAD)
    remote_commit=$(git rev-parse origin/main)
    
    if [[ "$local_commit" == "$remote_commit" ]]; then
        warning "No hay cambios nuevos en GitHub"
        return 0
    fi
    
    # Hacer reset hard al último commit de main
    log "Aplicando cambios desde GitHub..."
    git reset --hard origin/main
    
    success "Código actualizado desde GitHub"
    log "Commit anterior: $local_commit"
    log "Commit actual: $remote_commit"
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
    
    missing_files=()
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        error "Archivos requeridos no encontrados:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        return 1
    fi
    
    success "Archivos de configuración verificados"
}

# Función para construir y levantar servicios
start_services() {
    log "Construyendo y levantando servicios..."
    
    cd "$PROJECT_DIR"
    
    # Verificar que el archivo .env esté configurado
    if [[ ! -f ".env" ]]; then
        log "Copiando archivo de variables de entorno..."
        cp env.aws .env
    fi
    
    # Construir imágenes
    log "Construyendo imágenes Docker..."
    docker-compose -f docker-compose.aws.yml build --no-cache
    
    # Levantar servicios
    log "Levantando servicios..."
    docker-compose -f docker-compose.aws.yml up -d
    
    success "Servicios levantados"
}

# Función para health checks mejorada
health_checks() {
    log "Realizando health checks..."
    
    local max_attempts=30
    local attempt=1
    local health_endpoints=("http://localhost/health" "https://guia.papyrus.com.co/health")
    
    while [ $attempt -le $max_attempts ]; do
        log "Health check intento $attempt/$max_attempts"
        
        # Verificar que todos los contenedores estén corriendo
        if ! docker-compose -f docker-compose.aws.yml ps | grep -q "Up"; then
            warning "Algunos contenedores no están corriendo"
            sleep 10
            ((attempt++))
            continue
        fi
        
        # Verificar health endpoints
        for endpoint in "${health_endpoints[@]}"; do
            if curl -f -s "$endpoint" > /dev/null 2>&1; then
                success "Health check exitoso en: $endpoint"
                return 0
            fi
        done
        
        sleep 10
        ((attempt++))
    done
    
    error "Health check falló después de $max_attempts intentos"
    return 1
}

# Función para verificar logs mejorada
check_logs() {
    log "Verificando logs de servicios..."
    
    cd "$PROJECT_DIR"
    
    # Verificar logs de la aplicación
    log "Verificando logs de la aplicación..."
    app_logs=$(docker-compose -f docker-compose.aws.yml logs app --tail=50)
    
    if echo "$app_logs" | grep -i "error\|exception\|traceback" | grep -v "DEBUG" > /dev/null; then
        warning "Errores encontrados en logs de la aplicación:"
        echo "$app_logs" | grep -i "error\|exception\|traceback" | grep -v "DEBUG" | head -10
    else
        success "Logs de aplicación sin errores críticos"
    fi
    
    # Verificar logs de nginx
    log "Verificando logs de nginx..."
    nginx_logs=$(docker-compose -f docker-compose.aws.yml logs nginx --tail=20)
    
    if echo "$nginx_logs" | grep -i "error" > /dev/null; then
        warning "Errores encontrados en logs de nginx:"
        echo "$nginx_logs" | grep -i "error" | head -5
    else
        success "Logs de nginx sin errores críticos"
    fi
    
    # Verificar logs de PostgreSQL
    log "Verificando logs de PostgreSQL..."
    postgres_logs=$(docker-compose -f docker-compose.aws.yml logs postgres --tail=20)
    
    if echo "$postgres_logs" | grep -i "error\|fatal" > /dev/null; then
        warning "Errores encontrados en logs de PostgreSQL:"
        echo "$postgres_logs" | grep -i "error\|fatal" | head -5
    else
        success "Logs de PostgreSQL sin errores críticos"
    fi
}

# Función para verificar funcionalidad específica
verify_functionality() {
    log "Verificando funcionalidad específica..."
    
    # Verificar que el favicon clickeable esté presente
    local response=$(curl -s https://guia.papyrus.com.co/ 2>/dev/null || curl -s http://localhost/ 2>/dev/null)
    
    if echo "$response" | grep -q 'href="/".*EL CLUB'; then
        success "Favicon clickeable verificado"
    else
        warning "Favicon clickeable no encontrado en la respuesta"
    fi
    
    # Verificar que la base de datos esté funcionando
    if docker-compose -f docker-compose.aws.yml exec -T postgres pg_isready -U paqueteria_user -d paqueteria > /dev/null 2>&1; then
        success "Base de datos PostgreSQL funcionando"
    else
        warning "Base de datos PostgreSQL no responde"
    fi
    
    # Verificar que Redis esté funcionando
    if docker-compose -f docker-compose.aws.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
        success "Redis funcionando"
    else
        warning "Redis no responde"
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
    
    echo ""
    log "Comandos útiles:"
    echo "  📋 Ver logs: docker-compose -f docker-compose.aws.yml logs -f"
    echo "  🔄 Reiniciar: docker-compose -f docker-compose.aws.yml restart"
    echo "  🛑 Detener: docker-compose -f docker-compose.aws.yml down"
    echo "  📊 Estado: docker-compose -f docker-compose.aws.yml ps"
}

# Función para limpiar backups antiguos
cleanup_old_backups() {
    log "Limpiando backups antiguos..."
    
    # Mantener solo los últimos 10 backups
    if [[ -d "$BACKUP_DIR" ]]; then
        cd "$BACKUP_DIR"
        ls -t *.tar.gz | tail -n +11 | xargs -r rm -f
        success "Backups antiguos limpiados"
    fi
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
    
    # Crear directorio de logs si no existe
    mkdir -p "$PROJECT_DIR/logs"
    
    # Ejecutar pasos de despliegue
    check_services || exit 1
    create_backup
    stop_services
    cleanup_docker
    update_code || exit 1
    verify_config || exit 1
    start_services
    health_checks || exit 1
    check_logs
    verify_functionality
    show_status
    cleanup_old_backups
    
    echo ""
    success "🎉 Despliegue completado exitosamente!"
    echo ""
    echo "📋 Resumen:"
    echo "  • Backup creado: $BACKUP_NAME"
    echo "  • Código actualizado desde GitHub"
    echo "  • Conflictos de Git resueltos automáticamente"
    echo "  • Servicios reiniciados"
    echo "  • Health checks pasados"
    echo "  • Funcionalidad verificada"
    echo ""
    echo "🔗 Acceso: https://guia.papyrus.com.co"
    echo ""
    echo "📝 Logs disponibles en: $PROJECT_DIR/logs/"
}

# Función para manejo de errores
error_handler() {
    local exit_code=$?
    local line_number=$1
    
    echo ""
    error "❌ Error en línea $line_number (código: $exit_code)"
    echo ""
    echo "🔧 Pasos para resolver:"
    echo "  1. Verificar logs: docker-compose -f docker-compose.aws.yml logs"
    echo "  2. Verificar estado: docker-compose -f docker-compose.aws.yml ps"
    echo "  3. Revisar configuración: cat .env"
    echo "  4. Restaurar backup si es necesario"
    echo ""
    echo "📞 Para soporte, revisar los logs en: $PROJECT_DIR/logs/"
    
    exit $exit_code
}

# Configurar trap para manejo de errores
trap 'error_handler $LINENO' ERR

# Ejecutar función principal
main "$@"
