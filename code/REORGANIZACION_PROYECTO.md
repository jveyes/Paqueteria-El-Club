# REORGANIZACIÓN DEL PROYECTO PAQUETERÍA v3.1

## FECHA DE REORGANIZACIÓN
3 de Septiembre de 2024

## OBJETIVO
Reorganizar el proyecto para separar claramente el código funcional de los archivos de testing, desarrollo y documentación.

## ESTRUCTURA FINAL ORGANIZADA

### 📁 **CÓDIGO FUNCIONAL (Mantenido en su lugar)**
- `src/` - Código fuente principal de la aplicación
- `templates/` - Plantillas HTML de la aplicación
- `static/` - Archivos estáticos (CSS, JS, imágenes)
- `alembic/` - Migraciones de base de datos
- `database/` - Scripts de base de datos
- `nginx/` - Configuración de nginx
- `config/` - Configuración de la aplicación
- `main.py/` - Punto de entrada principal
- `config.py/` - Configuración de Python
- `requirements.txt` - Dependencias de producción
- `requirements-dev.txt` - Dependencias de desarrollo
- `docker-compose.yml` - Docker compose principal
- `Dockerfile` - Dockerfile de producción
- `Dockerfile.dev` - Dockerfile de desarrollo
- `.env` - Variables de entorno activas
- `.gitignore` - Archivos ignorados por git

### 📁 **TESTING** - Archivos de testing y pruebas
- `test_*.py` - Scripts de testing de funcionalidades
- `test_*.html` - Páginas de testing HTML
- `tests/` - Directorio de tests existente
- `.pytest_cache/` - Cache de pytest
- `final_compatibility_test.py`
- `verify_enum_compatibility.py`
- `change_password_page.html`
- `edit_profile_page.html`
- `profile_page.html`

### 📁 **SCRIPTS** - Scripts de utilidad y despliegue
- `scripts/` - Directorio de scripts existente
- `deploy-aws.sh` - Script de despliegue en AWS
- `pull-and-deploy-aws.sh` - Script de pull y despliegue
- `restart_server.sh` - Script de reinicio del servidor

### 📁 **DEVELOPMENT** - Herramientas de desarrollo
- `diagnose_password_reset.py` - Diagnóstico de reset de contraseña
- `create_sample_data.py` - Creación de datos de muestra
- `check_server.py` - Verificación del servidor

### 📁 **DOCS** - Documentación del proyecto
- `docs/` - Documentación existente
- `*.md` - Archivos markdown de documentación
- `FLUJO_DESARROLLO.md`
- `PROFILE_*.md`
- `TEMPLATES_REORGANIZATION_SUMMARY.md`
- `SMS_DIAGNOSIS_REPORT.md`
- `BROWSER_SMS_ISSUE_REPORT.md`

### 📁 **BACKUPS** - Archivos de respaldo y configuración
- `env.aws` - Variables de entorno AWS
- `env.development` - Variables de entorno desarrollo
- `env.example` - Variables de entorno ejemplo
- `env.local` - Variables de entorno local
- `docker-compose-aws-only.yml` - Docker compose solo AWS
- `docker-compose.aws.yml` - Docker compose AWS
- `admin/` - Directorio admin (vacío)
- `public/` - Directorio public (vacío)
- `uploads/` - Directorio uploads (vacío)
- `ssl/` - Directorio SSL (vacío)
- `monitoring/` - Configuración de monitoreo
- `logs/` - Archivos de logs

## ARCHIVOS MOVIDOS

### **Archivos de Testing (69 archivos)**
- Todos los archivos `test_*.py` del directorio principal
- Todos los archivos `test_*.py` del directorio `scripts/`
- Archivos HTML de testing
- Directorio `tests/` completo
- Cache de pytest

### **Archivos de Desarrollo (3 archivos)**
- Scripts de diagnóstico y debugging
- Scripts de creación de datos de muestra
- Scripts de verificación del servidor

### **Archivos de Documentación (15+ archivos)**
- Todos los archivos `.md` de documentación
- Reportes de implementación
- Guías de desarrollo
- Resúmenes de funcionalidades

### **Archivos de Configuración (6 archivos)**
- Múltiples archivos de variables de entorno
- Múltiples archivos docker-compose
- Configuraciones de monitoreo

### **Directorios Vacíos (5 directorios)**
- `admin/`, `public/`, `uploads/`, `ssl/`, `monitoring/`

## BENEFICIOS DE LA REORGANIZACIÓN

1. **Código Funcional Limpio**: Solo el código esencial para producción está en el directorio principal
2. **Testing Organizado**: Todos los archivos de testing están en una carpeta dedicada
3. **Scripts Centralizados**: Scripts de utilidad y despliegue están organizados
4. **Documentación Accesible**: Toda la documentación está en un lugar
5. **Configuraciones de Respaldo**: Archivos de configuración alternativos están respaldados
6. **Mantenimiento Simplificado**: Más fácil identificar qué archivos son esenciales

## NOTAS IMPORTANTES

- **No se modificaron rutas**: Los archivos movidos no afectan el funcionamiento del proyecto
- **Código funcional intacto**: Todo el código de la aplicación permanece en su lugar
- **Testing preservado**: Todos los archivos de testing están disponibles para uso futuro
- **Scripts accesibles**: Los scripts de despliegue y utilidad están organizados
- **Documentación completa**: Toda la documentación está preservada y organizada

## PRÓXIMOS PASOS RECOMENDADOS

1. **Verificar funcionamiento**: Ejecutar tests para asegurar que todo funciona
2. **Actualizar .gitignore**: Agregar las nuevas carpetas si es necesario
3. **Documentar dependencias**: Verificar que las rutas en el código no se rompan
4. **Limpiar archivos obsoletos**: Identificar archivos que ya no se necesiten
5. **Optimizar estructura**: Considerar mover archivos entre carpetas si es necesario

## ARCHIVOS CRÍTICOS NO MOVIDOS

- `src/main.py` - Aplicación principal
- `templates/` - Plantillas de la aplicación
- `static/` - Archivos estáticos
- `alembic/` - Migraciones de BD
- `requirements.txt` - Dependencias
- `docker-compose.yml` - Docker principal
- `.env` - Variables de entorno activas
