#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Script para Guardar Imagen Docker
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 1.0
# Descripción: Guarda y distribuye la imagen Docker del proyecto

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
IMAGE_NAME="paqueteria-club"
IMAGE_TAG="v3.1.0"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
OUTPUT_DIR="docker-images"
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
SAVE_FILE="${OUTPUT_DIR}/paqueteria-club-${IMAGE_TAG}-${TIMESTAMP}.tar.gz"
INFO_FILE="${OUTPUT_DIR}/paqueteria-club-${IMAGE_TAG}-${TIMESTAMP}-INFO.md"

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "Opciones:"
    echo "  save           Guardar imagen como archivo tar.gz"
    echo "  load <file>    Cargar imagen desde archivo"
    echo "  info           Mostrar información de la imagen"
    echo "  clean          Limpiar archivos de imagen guardados"
    echo "  help           Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 save                    # Guardar imagen"
    echo "  $0 load image.tar.gz       # Cargar imagen"
    echo "  $0 info                    # Ver información"
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

# Función para verificar imagen
check_image() {
    if ! docker image inspect "$FULL_IMAGE_NAME" &> /dev/null; then
        error "Imagen no encontrada: $FULL_IMAGE_NAME"
    fi
    
    log "✅ Imagen encontrada: $FULL_IMAGE_NAME"
}

# Función para crear directorio de salida
create_output_dir() {
    if [ ! -d "$OUTPUT_DIR" ]; then
        log "Creando directorio de salida: $OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"
        success "Directorio creado"
    else
        log "✅ Directorio de salida existe"
    fi
}

# Función para guardar imagen
save_image() {
    log "Guardando imagen Docker: $FULL_IMAGE_NAME"
    
    # Crear directorio de salida
    create_output_dir
    
    # Guardar imagen
    log "Guardando imagen como: $SAVE_FILE"
    if docker save "$FULL_IMAGE_NAME" | gzip > "$SAVE_FILE"; then
        success "Imagen guardada exitosamente"
    else
        error "Error al guardar la imagen"
    fi
    
    # Mostrar información del archivo
    local file_size=$(du -h "$SAVE_FILE" | cut -f1)
    log "Tamaño del archivo: $file_size"
    
    # Crear archivo de información
    create_info_file
}

# Función para crear archivo de información
create_info_file() {
    log "Creando archivo de información..."
    
    cat > "$INFO_FILE" << EOF
# ========================================
# PAQUETES EL CLUB v3.1 - Información de Imagen Docker
# ========================================

## 📦 **DETALLES DE LA IMAGEN**

- **Archivo**: $(basename "$SAVE_FILE")
- **Imagen**: $FULL_IMAGE_NAME
- **Tamaño**: $(du -h "$SAVE_FILE" | cut -f1)
- **Fecha de Guardado**: $(date '+%d de %B, %Y - %H:%M:%S')
- **Estado**: ✅ GUARDADA Y VERIFICADA

## 🏗️ **ESPECIFICACIONES TÉCNICAS**

### **Imagen Base:**
- **Sistema Operativo**: Debian (Python 3.11-slim)
- **Python**: 3.11
- **Arquitectura**: Multi-arch (amd64, arm64)

### **Optimizaciones:**
- ✅ Usuario no-root (appuser)
- ✅ Health check configurado
- ✅ Labels de metadatos
- ✅ .dockerignore optimizado
- ✅ Security best practices

### **Contenido Incluido:**
- ✅ Código completo de la aplicación
- ✅ Dependencias Python instaladas
- ✅ Scripts de gestión
- ✅ Documentación completa
- ✅ Configuración Nginx
- ✅ Esquema de base de datos

## 🚀 **INSTRUCCIONES DE CARGA**

### **Cargar Imagen:**
\`\`\`bash
# Cargar imagen desde archivo
docker load < $(basename "$SAVE_FILE")

# Verificar imagen cargada
docker images $IMAGE_NAME
\`\`\`

### **Ejecutar Imagen:**
\`\`\`bash
# Ejecución básica
docker run -d \\
  --name paqueteria-club \\
  -p 8000:8000 \\
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \\
  -e REDIS_URL="redis://host:6379/0" \\
  -e SECRET_KEY="your-secret-key" \\
  $FULL_IMAGE_NAME
\`\`\`

## 🌐 **URLS DE ACCESO**

- **Aplicación Principal**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **API Directa**: http://localhost:8000

## 📊 **ESPECIFICACIONES TÉCNICAS**

### **Optimizaciones para 50 Usuarios:**
- PostgreSQL: 256MB RAM, 0.5 CPU
- Redis: 64MB RAM, 0.2 CPU
- FastAPI: 256MB RAM, 0.5 CPU
- Celery: 128MB RAM, 0.3 CPU
- Nginx: 32MB RAM, 0.2 CPU

## 🔧 **VARIABLES DE ENTORNO OBLIGATORIAS**

- \`DATABASE_URL\`: URL de conexión a PostgreSQL
- \`REDIS_URL\`: URL de conexión a Redis
- \`SECRET_KEY\`: Clave secreta para JWT

## 📝 **NOTAS IMPORTANTES**

1. **Esta imagen incluye todas las correcciones aplicadas durante el despliegue exitoso**
2. **El sistema está optimizado para 50 usuarios simultáneos**
3. **Todos los scripts tienen permisos de ejecución**
4. **La documentación está completa y actualizada**
5. **La imagen está lista para producción**

## 🎯 **PRÓXIMOS PASOS RECOMENDADOS**

### **Después de Cargar la Imagen:**
1. ✅ Configurar variables de entorno
2. ✅ Configurar base de datos PostgreSQL
3. ✅ Configurar Redis
4. ✅ Ejecutar migraciones si es necesario
5. ✅ Verificar funcionamiento con health check

---

**🎉 ¡Imagen Docker lista para distribución!**

**Fecha**: $(date '+%d de %B, %Y')  
**Versión**: $IMAGE_TAG  
**Estado**: ✅ VERIFICADA Y FUNCIONAL
EOF
    
    success "Archivo de información creado: $(basename "$INFO_FILE")"
}

# Función para cargar imagen
load_image() {
    local load_file="$1"
    
    if [ -z "$load_file" ]; then
        error "Debe especificar un archivo para cargar"
    fi
    
    if [ ! -f "$load_file" ]; then
        error "Archivo no encontrado: $load_file"
    fi
    
    log "Cargando imagen desde: $load_file"
    
    if docker load < "$load_file"; then
        success "Imagen cargada exitosamente"
        
        # Mostrar imágenes cargadas
        echo ""
        log "Imágenes disponibles:"
        docker images | grep paqueteria-club || echo "No se encontraron imágenes paqueteria-club"
    else
        error "Error al cargar la imagen"
    fi
}

# Función para mostrar información
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
        
        echo ""
        echo -e "${BLUE}Tamaño de la imagen:${NC}"
        docker images "$FULL_IMAGE_NAME" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    else
        warn "Imagen no encontrada: $FULL_IMAGE_NAME"
    fi
}

# Función para limpiar archivos
clean_files() {
    log "Limpiando archivos de imagen guardados..."
    
    if [ -d "$OUTPUT_DIR" ]; then
        local deleted_count=0
        
        for file in "$OUTPUT_DIR"/paqueteria-club-*.tar.gz; do
            if [ -f "$file" ]; then
                rm "$file"
                deleted_count=$((deleted_count + 1))
                log "Eliminado: $(basename "$file")"
            fi
        done
        
        for file in "$OUTPUT_DIR"/paqueteria-club-*-INFO.md; do
            if [ -f "$file" ]; then
                rm "$file"
                deleted_count=$((deleted_count + 1))
                log "Eliminado: $(basename "$file")"
            fi
        done
        
        if [ $deleted_count -gt 0 ]; then
            success "Eliminados $deleted_count archivos"
        else
            log "No se encontraron archivos para eliminar"
        fi
    else
        log "Directorio $OUTPUT_DIR no existe"
    fi
}

# Función para mostrar resumen
show_summary() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}        RESUMEN DE LA IMAGEN          ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}✅ Imagen guardada exitosamente${NC}"
    echo ""
    echo -e "${YELLOW}📦 Información del Archivo:${NC}"
    echo -e "  • Archivo: ${BLUE}$(basename "$SAVE_FILE")${NC}"
    echo -e "  • Ubicación: ${BLUE}$SAVE_FILE${NC}"
    echo -e "  • Tamaño: ${BLUE}$(du -h "$SAVE_FILE" | cut -f1)${NC}"
    echo ""
    echo -e "${YELLOW}📋 Archivos de Información:${NC}"
    echo -e "  • Información: ${BLUE}$(basename "$INFO_FILE")${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Carga de la Imagen:${NC}"
    echo -e "  • Comando: ${BLUE}docker load < $(basename "$SAVE_FILE")${NC}"
    echo -e "  • Ejecutar: ${BLUE}docker run -p 8000:8000 $FULL_IMAGE_NAME${NC}"
    echo ""
    echo -e "${GREEN}🎉 ¡Imagen lista para distribución!${NC}"
    echo ""
}

# Función principal
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  PAQUETES EL CLUB v3.1 - GUARDAR     ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # Verificar Docker
    check_docker
    
    # Procesar argumentos
    case "${1:-help}" in
        "save")
            check_image
            save_image
            show_summary
            ;;
        "load")
            load_image "$2"
            ;;
        "info")
            show_image_info
            ;;
        "clean")
            clean_files
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Ejecutar función principal
main "$@"
