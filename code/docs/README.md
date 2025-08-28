# ========================================
# PAQUETES EL CLUB v3.1 - Scripts de Gestión y Testing
# ========================================

## 🎯 **OBJETIVO**
Scripts automatizados para el despliegue, gestión y testing del backend de PAQUETES EL CLUB v3.1

## 📁 **ESTRUCTURA**

```
SCRIPTS/
├── 📄 README.md                     # Esta documentación
├── 📄 DEPLOYMENT-GUIDE.md           # Guía completa de despliegue
├── 📄 deploy-full.sh                # DESPLIEGUE COMPLETO AUTOMATIZADO
├── 📄 verify-deployment.sh          # Verificación del despliegue
├── 📄 setup-environment.sh          # Configurar entorno
├── 📄 cleanup-containers.sh         # Limpiar contenedores
├── 📄 start-services.sh             # Iniciar servicios Docker
├── 📄 stop-services.sh              # Detener servicios Docker
├── 📄 view-logs.sh                  # Visualizar logs
├── 📄 monitor-resources.sh          # Monitorear recursos
├── 📄 backup-database.sh            # Backup de BD
├── 📄 restore-database.sh           # Restaurar BD
├── 📄 test-database.sh              # Probar conexión a BD
├── 📄 test-api-endpoints.sh         # Probar endpoints de API
├── 📄 quick-test.sh                 # Test rápido
├── 📄 run-all-tests.sh              # Ejecutar todas las pruebas
├── 📄 restart-for-development.sh    # Reiniciar servicios para desarrollo
└── 📄 check-volumes.sh              # Verificar volúmenes de desarrollo
```

## 🚀 **USO RÁPIDO**

### **Opción 1: Despliegue Automatizado (Recomendado)**
```bash
# Desde el directorio raíz del proyecto
./code/SCRIPTS/deploy-full.sh
```

### **Opción 2: Despliegue Manual**
```bash
# 1. Configurar entorno
./code/SCRIPTS/setup-environment.sh

# 2. Iniciar servicios
./code/SCRIPTS/start-services.sh

# 3. Verificar despliegue
./code/SCRIPTS/verify-deployment.sh
```

### **Opción 3: Solo Testing**
```bash
# Ejecutar todas las pruebas
./code/SCRIPTS/run-all-tests.sh

# Test rápido
./code/SCRIPTS/quick-test.sh
```

## 📊 **TIPOS DE SCRIPTS**

### **🚀 Scripts de Despliegue**
- **deploy-full.sh**: Despliegue completo automatizado con todas las correcciones
- **verify-deployment.sh**: Verificación completa del despliegue (25+ tests)
- **test-api-simple.sh**: Testing básico de APIs (5 tests principales)
- **monitor-resources.sh**: Monitoreo de recursos del sistema y contenedores
- **backup-automatic.sh**: Backup automático de base de datos, archivos y configuración
- **optimize-performance.sh**: Optimización de rendimiento de PostgreSQL, Redis y sistema
- **test-frontend.sh**: Testing del frontend y verificación de páginas web
- **setup-environment.sh**: Configuración del entorno y variables de entorno

### **🔧 Scripts de Gestión**
- **cleanup-containers.sh**: Limpieza de contenedores y recursos Docker
- **start-services.sh**: Inicio de servicios con verificaciones
- **stop-services.sh**: Detención segura de servicios
- **view-logs.sh**: Visualización de logs en tiempo real

### **📊 Scripts de Monitoreo**
- **monitor-resources.sh**: Monitoreo de recursos del sistema
- **backup-database.sh**: Backup automático de base de datos
- **restore-database.sh**: Restauración de base de datos

### **🧪 Scripts de Testing**
- **test-database.sh**: Pruebas de conexión a base de datos
- **test-api-endpoints.sh**: Pruebas de endpoints de API
- **test-frontend.sh**: Pruebas del frontend y páginas web
- **test-customers-page.sh**: Pruebas de la página de consulta de paquetes y anuncios
- **test-main-page.sh**: Pruebas completas de la página principal (formulario de anuncio)
- **quick-test.sh**: Test rápido del sistema
- **run-all-tests.sh**: Ejecución completa de todas las pruebas

### **🔧 Scripts de Desarrollo**
- **restart-for-development.sh**: Reinicia servicios para aplicar cambios de volúmenes
- **check-volumes.sh**: Verifica que los volúmenes estén montados correctamente

## 📋 **CHECKLIST DE DESPLIEGUE**

### **✅ Preparación**
- [ ] Archivo .env creado en raíz
- [ ] Archivo code/.env configurado
- [ ] main.py corregido y completo
- [ ] template index.html creado
- [ ] Estructura de directorios verificada

### **✅ Infraestructura**
- [ ] Docker containers iniciando
- [ ] Base de datos PostgreSQL conectando
- [ ] Redis funcionando
- [ ] Nginx sirviendo como proxy
- [ ] FastAPI aplicación corriendo

### **✅ Servicios**
- [ ] Health check respondiendo (http://localhost/health)
- [ ] Página principal accesible (http://localhost)
- [ ] API documentation disponible (http://localhost:8001/docs)
- [ ] Todos los puertos abiertos (80, 443, 8001, 5432, 6380)

### **✅ Optimizaciones**
- [ ] Límites de memoria configurados
- [ ] Límites de CPU configurados
- [ ] PostgreSQL optimizado para 50 usuarios
- [ ] Redis con política LRU
- [ ] Nginx con worker processes optimizados

## 📝 **LOGS Y REPORTES**

### **📊 Logs de Pruebas**
- `logs/test-api.log` - Logs de pruebas de API
- `logs/test-database.log` - Logs de pruebas de BD
- `logs/test-authentication.log` - Logs de autenticación

### **📈 Reportes**
- `TEST/reports/` - Reportes generados
- `TEST/results/` - Resultados de pruebas
- `TEST/screenshots/` - Capturas de pantalla

## 🛠️ **HERRAMIENTAS UTILIZADAS**

### **🔧 Scripts**
- **Bash**: Scripts de automatización
- **curl**: Pruebas de API
- **jq**: Procesamiento de JSON
- **docker**: Gestión de contenedores

### **📊 Monitoreo**
- **Prometheus**: Métricas
- **Grafana**: Visualización
- **Logs**: Seguimiento de errores

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **❌ Despliegue falla**
```bash
# Verificar despliegue completo
./code/SCRIPTS/verify-deployment.sh

# Reintentar despliegue
./code/SCRIPTS/deploy-full.sh
```

### **❌ Servicios no inician**
```bash
# Limpiar y reiniciar
./code/SCRIPTS/cleanup-containers.sh
./code/SCRIPTS/start-services.sh
```

### **❌ Base de datos no conecta**
```bash
# Verificar PostgreSQL
docker-compose logs postgres
./code/SCRIPTS/test-database.sh
```

### **❌ APIs no responden**
```bash
# Verificar aplicación
docker-compose logs app
./code/SCRIPTS/test-api-endpoints.sh
```

### **❌ Variables de entorno faltan**
```bash
# Recrear archivos .env
./code/SCRIPTS/setup-environment.sh
```

### **❌ Cambios no se reflejan al instante**
```bash
# Verificar volúmenes
./code/SCRIPTS/check-volumes.sh

# Reiniciar servicios para desarrollo
./code/SCRIPTS/restart-for-development.sh
```

## 🚀 **DESARROLLO RÁPIDO**

### **🔄 Para cambios en tiempo real:**
```bash
# 1. Verificar volúmenes
./code/SCRIPTS/check-volumes.sh

# 2. Si hay problemas, reiniciar servicios
./code/SCRIPTS/restart-for-development.sh

# 3. Los cambios en templates y archivos estáticos se reflejan al instante
```

### **📁 Volúmenes configurados para desarrollo:**
- `./src` → `/app/src` (código Python)
- `./templates` → `/app/templates` (plantillas HTML)
- `./static` → `/app/static` (archivos estáticos)
- `./uploads` → `/app/uploads` (archivos subidos)
- `./logs` → `/app/logs` (logs de aplicación)
- `./database` → `/app/database` (scripts de BD)
- `./SCRIPTS` → `/app/SCRIPTS` (scripts de gestión)
- `./TEST` → `/app/TEST` (archivos de testing)
- `../docs` → `/app/docs` (documentación)
- `./monitoring` → `/app/monitoring` (configuración de monitoreo)

---

**Última actualización**: 25 de Agosto, 2025  
**Versión**: 3.1.0  
**Mantenido por**: Asistente IA - PAQUETES EL CLUB
