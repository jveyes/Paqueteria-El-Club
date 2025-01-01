#!/bin/bash

# ========================================
# Script para Pull desde GitHub y Deploy en AWS
# PAQUETES EL CLUB v3.1
# ========================================

set -e

echo "🚀 PULL DESDE GITHUB Y DEPLOY EN AWS"
echo "====================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Git está instalado
if ! command -v git &> /dev/null; then
    print_error "Git no está instalado. Instala Git primero."
    exit 1
fi

# Verificar si estamos en un repositorio Git
if [ ! -d ".git" ]; then
    print_error "No estás en un repositorio Git. Clona el repositorio primero."
    exit 1
fi

# Verificar el estado actual
print_status "Verificando estado actual del repositorio..."
git status --porcelain

# Verificar la rama actual
CURRENT_BRANCH=$(git branch --show-current)
print_status "Rama actual: $CURRENT_BRANCH"

# Preguntar qué rama usar
echo ""
echo "¿Qué rama quieres usar para el deployment?"
echo "1) main (recomendado para producción)"
echo "2) develop (para desarrollo/testing)"
echo "3) Otra rama específica"
read -p "Selecciona una opción (1-3): " choice

case $choice in
    1)
        TARGET_BRANCH="main"
        ;;
    2)
        TARGET_BRANCH="develop"
        ;;
    3)
        read -p "Ingresa el nombre de la rama: " TARGET_BRANCH
        ;;
    *)
        print_error "Opción inválida. Usando main por defecto."
        TARGET_BRANCH="main"
        ;;
esac

print_status "Usando rama: $TARGET_BRANCH"

# Cambiar a la rama objetivo si es necesario
if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
    print_status "Cambiando a la rama $TARGET_BRANCH..."
    git checkout $TARGET_BRANCH
fi

# Hacer pull de los cambios más recientes
print_status "Haciendo pull de los cambios más recientes..."
git pull origin $TARGET_BRANCH

# Verificar si hay cambios
if [ -n "$(git status --porcelain)" ]; then
    print_warning "Hay cambios locales no committeados:"
    git status --porcelain
    read -p "¿Quieres continuar de todas formas? (y/N): " continue_anyway
    if [[ ! $continue_anyway =~ ^[Yy]$ ]]; then
        print_error "Deployment cancelado."
        exit 1
    fi
fi

# Verificar que los archivos necesarios existan
print_status "Verificando archivos necesarios..."

REQUIRED_FILES=("docker-compose.aws.yml" "env.aws" "Dockerfile")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo requerido no encontrado: $file"
        exit 1
    fi
done

print_success "Todos los archivos requeridos están presentes"

# Hacer el archivo de deployment ejecutable
chmod +x deploy-aws.sh

# Ejecutar el deployment
print_status "Iniciando deployment..."
./deploy-aws.sh

print_success "¡Pull y deployment completados exitosamente!"
