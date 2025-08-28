#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Install Auto Organize
# ========================================
#
# 🎯 OBJETIVO: Instalar sistema de organización automática de archivos
# 📅 FECHA: 2025-08-27
# 👤 AUTOR: Sistema Automático
# 🔄 VERSIÓN: 1.0.0
#
# 📋 USO:
#   ./install_auto_organize.sh                    # Instalar sistema completo
#   ./install_auto_organize.sh --deps-only        # Solo instalar dependencias
#   ./install_auto_organize.sh --test             # Probar instalación
#
# 📊 RESULTADOS:
#   - Dependencias instaladas
#   - Scripts configurados
#   - Sistema listo para usar
#
# ⚠️ DEPENDENCIAS:
#   - Python 3.8+
#   - pip
#   - git
#
# ========================================

set -e

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

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar que estamos en el directorio correcto
check_directory() {
    if [ ! -f "auto_organize_files.py" ]; then
        error "No se encontró auto_organize_files.py. Ejecuta este script desde el directorio SCRIPTS/"
    fi
}

# Instalar dependencias de Python
install_python_deps() {
    log "Instalando dependencias de Python..."
    
    # Verificar si pip está disponible
    if ! command -v pip3 &> /dev/null; then
        error "pip3 no está instalado. Instala Python y pip primero."
    fi
    
    # Instalar watchdog para el observador de archivos
    pip3 install watchdog
    
    success "Dependencias de Python instaladas"
}

# Crear directorios necesarios
create_directories() {
    log "Creando directorios necesarios..."
    
    # Directorios para logs y reportes
    mkdir -p ../logs
    mkdir -p ../TEST/reports
    mkdir -p ../config
    
    success "Directorios creados"
}

# Configurar permisos de ejecución
setup_permissions() {
    log "Configurando permisos de ejecución..."
    
    chmod +x auto_organize_files.py
    chmod +x auto_organize_watcher.py
    
    success "Permisos configurados"
}

# Crear archivo de configuración
create_config() {
    log "Creando archivo de configuración..."
    
    cat > ../config/auto_organize.conf << 'EOF'
# ========================================
# PAQUETES EL CLUB v3.1 - Auto Organize Config
# ========================================

[PATTERNS]
# Patrones para tests
test_patterns = test_*.py, *_test.py, test_*.html, *_test.html, test_*.sh, *_test.sh

# Patrones para scripts
script_patterns = *.sh, *_script.py, setup_*.py, deploy_*.py, *_runner.py, *_automation.py

# Patrones para documentación de deployment
deployment_doc_patterns = *_GUIDE.md, *_COMPLETADO.md, *_LIGHTSAIL.md, *_DEPLOYMENT.md

# Patrones para documentación general
general_doc_patterns = *_FIXES.md, *_SUMMARY.md, *_ANALISIS.md, *_SOLUTION.md

# Patrones para configuración
config_patterns = *.config, *.conf, env_*, config_*, settings_*

[SETTINGS]
# Directorio base para organización
base_dir = code

# Cooldown entre organizaciones (segundos)
cooldown_period = 5

# Habilitar observador automático
auto_watcher = true

# Generar reportes automáticamente
auto_reports = true

# Logging level (DEBUG, INFO, WARNING, ERROR)
log_level = INFO

[PATHS]
# Directorios de destino
tests_dir = code/TEST
scripts_dir = code/SCRIPTS
deployment_docs_dir = docs/deployment-docs
general_docs_dir = docs
config_dir = code/config

# Directorios de logs y reportes
logs_dir = code/logs
reports_dir = code/TEST/reports
EOF

    success "Archivo de configuración creado"
}

# Crear script de inicio automático
create_startup_script() {
    log "Creando script de inicio automático..."
    
    cat > start_auto_organize.sh << 'EOF'
#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Start Auto Organize
# ========================================

# Iniciar observador automático
echo "🚀 Iniciando sistema de organización automática..."
python3 auto_organize_watcher.py --daemon

# Verificar que se inició correctamente
sleep 2
if python3 auto_organize_watcher.py --status; then
    echo "✅ Sistema iniciado correctamente"
    echo "📁 Observando cambios en archivos..."
    echo "🛑 Para detener: python3 auto_organize_watcher.py --stop"
else
    echo "❌ Error iniciando el sistema"
    exit 1
fi
EOF

    chmod +x start_auto_organize.sh
    success "Script de inicio creado"
}

# Crear script de detención
create_stop_script() {
    log "Creando script de detención..."
    
    cat > stop_auto_organize.sh << 'EOF'
#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Stop Auto Organize
# ========================================

echo "🛑 Deteniendo sistema de organización automática..."
python3 auto_organize_watcher.py --stop

if [ $? -eq 0 ]; then
    echo "✅ Sistema detenido correctamente"
else
    echo "❌ Error deteniendo el sistema"
    exit 1
fi
EOF

    chmod +x stop_auto_organize.sh
    success "Script de detención creado"
}

# Probar instalación
test_installation() {
    log "Probando instalación..."
    
    # Verificar que los scripts existen
    if [ ! -f "auto_organize_files.py" ]; then
        error "Script auto_organize_files.py no encontrado"
    fi
    
    if [ ! -f "auto_organize_watcher.py" ]; then
        error "Script auto_organize_watcher.py no encontrado"
    fi
    
    # Verificar dependencias
    if ! python3 -c "import watchdog" 2>/dev/null; then
        error "Dependencia watchdog no instalada"
    fi
    
    # Probar organización manual
    log "Probando organización manual..."
    python3 auto_organize_files.py --check
    
    if [ $? -eq 0 ]; then
        success "Prueba de organización exitosa"
    else
        warning "Prueba de organización falló (puede ser normal si no hay archivos para organizar)"
    fi
    
    success "Instalación verificada correctamente"
}

# Mostrar información de uso
show_usage_info() {
    echo ""
    echo "🎉 ¡Sistema de organización automática instalado!"
    echo ""
    echo "📋 Comandos disponibles:"
    echo "   ./start_auto_organize.sh              # Iniciar sistema automático"
    echo "   ./stop_auto_organize.sh               # Detener sistema automático"
    echo "   python3 auto_organize_files.py        # Organización manual"
    echo "   python3 auto_organize_watcher.py      # Observador manual"
    echo ""
    echo "🔧 Opciones de organización manual:"
    echo "   python3 auto_organize_files.py --check    # Verificar estructura"
    echo "   python3 auto_organize_files.py --report   # Generar reporte"
    echo "   python3 auto_organize_files.py --dry-run  # Simular organización"
    echo ""
    echo "📊 Archivos generados:"
    echo "   - Logs: ../logs/auto_organize.log"
    echo "   - Reportes: ../TEST/reports/file_organization_report.md"
    echo "   - Configuración: ../config/auto_organize.conf"
    echo ""
    echo "🚀 Para iniciar automáticamente:"
    echo "   ./start_auto_organize.sh"
    echo ""
}

# Función principal
main() {
    echo "🚀 PAQUETES EL CLUB v3.1 - Instalación del Sistema de Organización Automática"
    echo "=" * 70
    
    # Verificar argumentos
    if [ "$1" = "--deps-only" ]; then
        install_python_deps
        exit 0
    elif [ "$1" = "--test" ]; then
        test_installation
        exit 0
    fi
    
    # Verificaciones iniciales
    check_directory
    
    # Instalación completa
    install_python_deps
    create_directories
    setup_permissions
    create_config
    create_startup_script
    create_stop_script
    
    # Probar instalación
    test_installation
    
    # Mostrar información de uso
    show_usage_info
    
    success "🎉 Instalación completada exitosamente!"
}

# Ejecutar función principal
main "$@"
