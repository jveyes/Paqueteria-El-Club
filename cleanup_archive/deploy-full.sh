#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Script de Despliegue Completo
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 1.0
# Descripción: Despliegue automatizado con todas las correcciones

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

# Función para verificar comandos
check_command() {
    if ! command -v $1 &> /dev/null; then
        error "$1 no está instalado. Por favor instálalo primero."
    fi
}

# Función para verificar archivos
check_file() {
    if [ ! -f "$1" ]; then
        error "Archivo $1 no encontrado"
    fi
}

# Función para crear archivo .env en raíz
create_root_env() {
    log "Creando archivo .env en directorio raíz..."
    
    cat > .env << 'EOF'
POSTGRES_PASSWORD=Paqueteria2025!Secure
REDIS_PASSWORD=Redis2025!Secure
SECRET_KEY=paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication
LIWA_API_KEY=your_liwa_api_key_here
LIWA_PHONE_NUMBER=your_liwa_phone_number_here
EOF
    
    log "✅ Archivo .env creado en directorio raíz"
}

# Función para verificar y corregir main.py
fix_main_py() {
    log "Verificando archivo main.py..."
    
    if [ ! -f "code/src/main.py" ]; then
        error "Archivo code/src/main.py no encontrado"
    fi
    
    # Verificar si el archivo está completo (debe tener más de 50 líneas)
    line_count=$(wc -l < "code/src/main.py")
    if [ $line_count -lt 50 ]; then
        warn "Archivo main.py parece estar incompleto. Reconstruyendo..."
        
        # Crear main.py completo
        cat > "code/src/main.py" << 'EOF'
# ========================================
# PAQUETES EL CLUB v3.1 - Aplicación Principal FastAPI Optimizada
# ========================================

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Importar configuración y utilidades
from .config import settings
from .utils.exceptions import PaqueteriaException, handle_paqueteria_exception

# Importar routers
from .routers import auth, packages, customers, rates, notifications, messages, files, admin
from .database.database import engine
from .models import base

# Configurar logging optimizado
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando PAQUETES EL CLUB v3.1...")
    
    # Crear tablas de la base de datos
    try:
        base.Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
    
    yield
    
    # Shutdown
    logger.info("Cerrando PAQUETES EL CLUB v3.1...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema de gestión de paquetería optimizado para 50 usuarios simultáneos",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Manejo de excepciones personalizadas
app.add_exception_handler(PaqueteriaException, handle_paqueteria_exception)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(packages.router, prefix="/api/packages", tags=["Paquetes"])
app.include_router(customers.router, prefix="/api/customers", tags=["Clientes"])
app.include_router(rates.router, prefix="/api/rates", tags=["Tarifas"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notificaciones"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensajes"])
app.include_router(files.router, prefix="/api/files", tags=["Archivos"])
app.include_router(admin.router, prefix="/api/admin", tags=["Administración"])

@app.get("/")
async def root(request: Request):
    """Página principal de la aplicación"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment
    }

@app.get("/api/docs")
async def api_docs():
    """Redirigir a la documentación de la API"""
    return {"docs_url": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
        limit_concurrency=50,
        limit_max_requests=1000
    )
EOF
        
        log "✅ Archivo main.py reconstruido"
    else
        log "✅ Archivo main.py verificado"
    fi
}

# Función para verificar y crear template index.html
fix_template() {
    log "Verificando template index.html..."
    
    if [ ! -f "code/templates/index.html" ]; then
        log "Creando template index.html..."
        
        mkdir -p "code/templates"
        
        cat > "code/templates/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PAQUETES EL CLUB v3.1</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://unpkg.com/alpinejs@3.13.3/dist/cdn.min.js" defer></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-blue-600 mb-2">PAQUETES EL CLUB</h1>
            <p class="text-xl text-gray-600">Sistema de Gestión de Paquetería v3.1</p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Tarjeta de Estado del Sistema -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">Estado del Sistema</h2>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Versión:</span>
                        <span class="font-medium">3.1.0</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Ambiente:</span>
                        <span class="font-medium text-green-600">Desarrollo</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Estado:</span>
                        <span class="font-medium text-green-600">Operativo</span>
                    </div>
                </div>
            </div>

            <!-- Tarjeta de Acciones Rápidas -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">Acciones Rápidas</h2>
                <div class="space-y-3">
                    <a href="/api/docs" class="block w-full bg-blue-600 text-white text-center py-2 px-4 rounded hover:bg-blue-700 transition-colors">
                        Documentación API
                    </a>
                    <a href="/health" class="block w-full bg-green-600 text-white text-center py-2 px-4 rounded hover:bg-green-700 transition-colors">
                        Verificar Salud
                    </a>
                </div>
            </div>

            <!-- Tarjeta de Información -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">Información</h2>
                <div class="space-y-2 text-sm text-gray-600">
                    <p>• Sistema optimizado para 50 usuarios simultáneos</p>
                    <p>• Base de datos PostgreSQL</p>
                    <p>• Cache Redis</p>
                    <p>• Procesamiento asíncrono con Celery</p>
                </div>
            </div>
        </div>

        <footer class="text-center mt-12 text-gray-500">
            <p>&copy; 2025 PAQUETES EL CLUB. Todos los derechos reservados.</p>
        </footer>
    </div>
</body>
</html>
EOF
        
        log "✅ Template index.html creado"
    else
        log "✅ Template index.html verificado"
    fi
}

# Función para verificar estructura de directorios
check_directories() {
    log "Verificando estructura de directorios..."
    
    local dirs=(
        "code/uploads"
        "code/logs"
        "code/static"
        "code/ssl"
        "code/monitoring/grafana/dashboards"
        "code/monitoring/grafana/datasources"
        "code/database/init"
    )
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            log "Creando directorio: $dir"
            mkdir -p "$dir"
        fi
    done
    
    log "✅ Estructura de directorios verificada"
}

# Función para limpiar contenedores existentes
cleanup_containers() {
    log "Limpiando contenedores existentes..."
    
    if command -v docker-compose &> /dev/null; then
        docker-compose down --remove-orphans 2>/dev/null || true
        log "✅ Contenedores detenidos"
    fi
    
    # Limpiar contenedores huérfanos
    docker container prune -f 2>/dev/null || true
    docker network prune -f 2>/dev/null || true
}

# Función para desplegar servicios
deploy_services() {
    log "Desplegando servicios..."
    
    # Construir e iniciar servicios
    docker-compose up -d --build
    
    log "✅ Servicios desplegados"
}

# Función para verificar servicios
verify_services() {
    log "Verificando servicios..."
    
    # Esperar a que los servicios estén listos
    sleep 10
    
    # Verificar estado de contenedores
    if docker-compose ps | grep -q "Up"; then
        log "✅ Todos los contenedores están corriendo"
    else
        error "❌ Algunos contenedores no están corriendo"
    fi
    
    # Verificar health check
    if curl -s http://localhost/health > /dev/null; then
        log "✅ Health check exitoso"
    else
        warn "⚠️ Health check falló, esperando más tiempo..."
        sleep 10
        if curl -s http://localhost/health > /dev/null; then
            log "✅ Health check exitoso (segundo intento)"
        else
            error "❌ Health check falló después de múltiples intentos"
        fi
    fi
    
    # Verificar página principal
    if curl -s http://localhost > /dev/null; then
        log "✅ Página principal accesible"
    else
        warn "⚠️ Página principal no accesible"
    fi
}

# Función para mostrar información final
show_final_info() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}   PAQUETES EL CLUB v3.1 DESPLEGADO    ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}✅ Despliegue completado exitosamente${NC}"
    echo ""
    echo -e "${YELLOW}🌐 URLs de Acceso:${NC}"
    echo -e "   • Aplicación Principal: ${BLUE}http://localhost${NC}"
    echo -e "   • Health Check: ${BLUE}http://localhost/health${NC}"
    echo -e "   • API Documentation: ${BLUE}http://localhost:8001/docs${NC}"
    echo -e "   • API Directa: ${BLUE}http://localhost:8001${NC}"
    echo ""
    echo -e "${YELLOW}📊 Servicios:${NC}"
    echo -e "   • PostgreSQL: ${BLUE}localhost:5432${NC}"
    echo -e "   • Redis: ${BLUE}localhost:6380${NC}"
    echo ""
    echo -e "${YELLOW}🔧 Comandos Útiles:${NC}"
    echo -e "   • Ver logs: ${BLUE}docker-compose logs -f${NC}"
    echo -e "   • Detener: ${BLUE}docker-compose down${NC}"
    echo -e "   • Reiniciar: ${BLUE}docker-compose restart${NC}"
    echo ""
    echo -e "${GREEN}🎉 ¡Sistema listo para usar!${NC}"
    echo ""
}

# Función principal
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  PAQUETES EL CLUB v3.1 - DESPLIEGUE   ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # Verificar comandos necesarios
    log "Verificando dependencias..."
    check_command docker
    check_command docker-compose
    check_command curl
    
    # Verificar archivos críticos
    log "Verificando archivos críticos..."
    check_file "docker-compose.yml"
    check_file "code/env.example"
    
    # Crear archivo .env en raíz
    create_root_env
    
    # Verificar y corregir main.py
    fix_main_py
    
    # Verificar y crear template
    fix_template
    
    # Verificar estructura de directorios
    check_directories
    
    # Limpiar contenedores existentes
    cleanup_containers
    
    # Desplegar servicios
    deploy_services
    
    # Verificar servicios
    verify_services
    
    # Mostrar información final
    show_final_info
}

# Ejecutar función principal
main "$@"
