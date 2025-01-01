#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Script de Construcción de Imagen Docker
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 1.0
# Descripción: Construye y gestiona imágenes Docker del proyecto

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

# Variables de configuración
IMAGE_NAME="paqueteria-club"
IMAGE_TAG="v3.1.0"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
LATEST_TAG="${IMAGE_NAME}:latest"
REGISTRY=""
BUILD_CONTEXT=".."
DOCKERFILE="Dockerfile"

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "Opciones:"
    echo "  build          Construir imagen Docker"
    echo "  push           Subir imagen a registro"
    echo "  pull           Descargar imagen del registro"
    echo "  run            Ejecutar imagen localmente"
    echo "  clean          Limpiar imágenes locales"
    echo "  info           Mostrar información de la imagen"
    echo "  help           Mostrar esta ayuda"
    echo ""
    echo "Variables de entorno:"
    echo "  REGISTRY       Registro Docker (ej: docker.io/usuario)"
    echo "  IMAGE_TAG      Tag de la imagen (default: v3.1.0)"
    echo ""
    echo "Ejemplos:"
    echo "  $0 build                    # Construir imagen"
    echo "  $0 build push               # Construir y subir"
    echo "  REGISTRY=myregistry.com $0 build push  # Con registro personalizado"
}

# Función para verificar Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado"
    fi
    
    if ! docker info &> /dev/null; then
        error "Docker no está corriendo"
    fi
    
    log "✅ Docker verificado"
}

# Función para verificar archivos necesarios
check_files() {
    local required_files=(
        "../Dockerfile"
        "../code/requirements.txt"
        "../code/src/main.py"
        "../docker-compose.yml"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            error "Archivo requerido no encontrado: $file"
        fi
    done
    
    log "✅ Archivos requeridos verificados"
}

# Función para construir la imagen
build_image() {
    log "Construyendo imagen Docker: $FULL_IMAGE_NAME"
    
    # Cambiar al directorio padre para el contexto de construcción
    cd "$BUILD_CONTEXT"
    
    # Construir la imagen
    if docker build \
        --file "$DOCKERFILE" \
        --tag "$FULL_IMAGE_NAME" \
        --tag "$LATEST_TAG" \
        --label "version=$IMAGE_TAG" \
        --label "maintainer=PAQUETES EL CLUB <guia@papyrus.com.co>" \
        --label "description=Sistema de gestión de paquetería v3.1" \
        --label "build-date=$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --label "vcs-ref=$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')" \
        .; then
        success "Imagen construida exitosamente: $FULL_IMAGE_NAME"
    else
        error "Error al construir la imagen"
    fi
    
    # Volver al directorio original
    cd - > /dev/null
}

# Función para subir imagen al registro
push_image() {
    if [ -z "$REGISTRY" ]; then
        warn "REGISTRY no está configurado. Saltando push."
        return 0
    fi
    
    local registry_image="${REGISTRY}/${FULL_IMAGE_NAME}"
    
    log "Subiendo imagen al registro: $registry_image"
    
    # Tag para el registro
    docker tag "$FULL_IMAGE_NAME" "$registry_image"
    
    # Subir imagen
    if docker push "$registry_image"; then
        success "Imagen subida exitosamente: $registry_image"
    else
        error "Error al subir la imagen"
    fi
}

# Función para descargar imagen del registro
pull_image() {
    if [ -z "$REGISTRY" ]; then
        error "REGISTRY no está configurado"
    fi
    
    local registry_image="${REGISTRY}/${FULL_IMAGE_NAME}"
    
    log "Descargando imagen del registro: $registry_image"
    
    if docker pull "$registry_image"; then
        success "Imagen descargada exitosamente: $registry_image"
        # Tag local
        docker tag "$registry_image" "$FULL_IMAGE_NAME"
    else
        error "Error al descargar la imagen"
    fi
}

# Función para ejecutar imagen localmente
run_image() {
    log "Ejecutando imagen localmente: $FULL_IMAGE_NAME"
    
    # Verificar si la imagen existe
    if ! docker image inspect "$FULL_IMAGE_NAME" &> /dev/null; then
        error "Imagen no encontrada: $FULL_IMAGE_NAME"
    fi
    
    # Ejecutar contenedor
    docker run -d \
        --name "paqueteria-club-test" \
        --publish "8000:8000" \
        --env "DATABASE_URL=postgresql://test:test@host.docker.internal:5432/test" \
        --env "REDIS_URL=redis://host.docker.internal:6379/0" \
        --env "SECRET_KEY=test-secret-key" \
        "$FULL_IMAGE_NAME"
    
    success "Contenedor iniciado: paqueteria-club-test"
    echo "Accede a: http://localhost:8000"
    echo "Para detener: docker stop paqueteria-club-test"
}

# Función para limpiar imágenes
clean_images() {
    log "Limpiando imágenes Docker..."
    
    # Eliminar contenedores detenidos
    docker container prune -f
    
    # Eliminar imágenes sin tag
    docker image prune -f
    
    # Eliminar imágenes específicas
    if docker image inspect "$FULL_IMAGE_NAME" &> /dev/null; then
        docker rmi "$FULL_IMAGE_NAME"
        success "Imagen eliminada: $FULL_IMAGE_NAME"
    fi
    
    if docker image inspect "$LATEST_TAG" &> /dev/null; then
        docker rmi "$LATEST_TAG"
        success "Imagen eliminada: $LATEST_TAG"
    fi
    
    success "Limpieza completada"
}

# Función para mostrar información de la imagen
show_image_info() {
    log "Información de la imagen: $FULL_IMAGE_NAME"
    
    if docker image inspect "$FULL_IMAGE_NAME" &> /dev/null; then
        echo ""
        echo -e "${BLUE}Detalles de la imagen:${NC}"
        docker image inspect "$FULL_IMAGE_NAME" | jq '.[0] | {
            "Id": .Id,
            "Created": .Created,
            "Size": .Size,
            "Labels": .Config.Labels,
            "ExposedPorts": .Config.ExposedPorts,
            "Cmd": .Config.Cmd
        }' 2>/dev/null || docker image inspect "$FULL_IMAGE_NAME"
        
        echo ""
        echo -e "${BLUE}Historial de la imagen:${NC}"
        docker history "$FULL_IMAGE_NAME"
    else
        warn "Imagen no encontrada: $FULL_IMAGE_NAME"
    fi
}

# Función para mostrar resumen
show_summary() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}        RESUMEN DE LA IMAGEN          ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}📦 Información de la Imagen:${NC}"
    echo -e "  • Nombre: ${BLUE}${FULL_IMAGE_NAME}${NC}"
    echo -e "  • Tag: ${BLUE}${IMAGE_TAG}${NC}"
    echo -e "  • Registro: ${BLUE}${REGISTRY:-'No configurado'}${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Comandos Útiles:${NC}"
    echo -e "  • Ejecutar: ${BLUE}docker run -p 8000:8000 ${FULL_IMAGE_NAME}${NC}"
    echo -e "  • Inspeccionar: ${BLUE}docker image inspect ${FULL_IMAGE_NAME}${NC}"
    echo -e "  • Historial: ${BLUE}docker history ${FULL_IMAGE_NAME}${NC}"
    echo ""
    echo -e "${YELLOW}🌐 Acceso:${NC}"
    echo -e "  • Aplicación: ${BLUE}http://localhost:8000${NC}"
    echo -e "  • Health: ${BLUE}http://localhost:8000/health${NC}"
    echo -e "  • API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${GREEN}🎉 ¡Imagen Docker lista!${NC}"
    echo ""
}

# Función principal
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  PAQUETES EL CLUB v3.1 - DOCKER      ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # Verificar Docker
    check_docker
    
    # Procesar argumentos
    case "${1:-help}" in
        "build")
            check_files
            build_image
            show_summary
            ;;
        "push")
            push_image
            ;;
        "pull")
            pull_image
            ;;
        "run")
            run_image
            ;;
        "clean")
            clean_images
            ;;
        "info")
            show_image_info
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Ejecutar función principal
main "$@"
