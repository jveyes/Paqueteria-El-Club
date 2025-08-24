# ========================================
# PAQUETES EL CLUB v3.0 - Scripts de Pruebas
# ========================================

## 🎯 **OBJETIVO**
Scripts automatizados para probar el backend de PAQUETES EL CLUB v3.0

## 📁 **ESTRUCTURA**

```
SCRIPTS/
├── 📄 README.md                     # Esta documentación
├── 📄 setup-test-env.sh             # Configurar entorno de pruebas
├── 📄 start-services.sh             # Iniciar servicios Docker
├── 📄 stop-services.sh              # Detener servicios Docker
├── 📄 run-migrations.sh             # Ejecutar migraciones de BD
├── 📄 test-database.sh              # Probar conexión a BD
├── 📄 test-api-endpoints.sh         # Probar endpoints de API
├── 📄 test-authentication.sh        # Probar sistema de autenticación
├── 📄 test-packages.sh              # Probar funcionalidad de paquetes
├── 📄 test-customers.sh             # Probar funcionalidad de clientes
├── 📄 test-rates.sh                 # Probar cálculo de tarifas
├── 📄 test-notifications.sh         # Probar sistema de notificaciones
├── 📄 load-test-data.sh             # Cargar datos de prueba
├── 📄 cleanup-test-data.sh          # Limpiar datos de prueba
├── 📄 generate-test-report.sh       # Generar reporte de pruebas
└── 📄 run-all-tests.sh              # Ejecutar todas las pruebas
```

## 🚀 **USO RÁPIDO**

### **1. Configurar entorno**
```bash
./SCRIPTS/setup-test-env.sh
```

### **2. Iniciar servicios**
```bash
./SCRIPTS/start-services.sh
```

### **3. Ejecutar todas las pruebas**
```bash
./SCRIPTS/run-all-tests.sh
```

### **4. Generar reporte**
```bash
./SCRIPTS/generate-test-report.sh
```

## 📊 **TIPOS DE PRUEBAS**

### **🔧 Pruebas de Infraestructura**
- Docker services
- Base de datos
- Redis cache
- Nginx proxy

### **🔐 Pruebas de Autenticación**
- Registro de usuarios
- Login/logout
- JWT tokens
- Roles y permisos

### **📦 Pruebas de Paquetes**
- Crear paquetes
- Tracking
- Estados
- Cálculo de tarifas

### **👥 Pruebas de Clientes**
- CRUD de clientes
- Búsqueda
- Validaciones

### **💰 Pruebas de Tarifas**
- Cálculo automático
- Diferentes tipos
- Historial

### **📧 Pruebas de Notificaciones**
- Email
- SMS
- Estados

## 📋 **CHECKLIST DE PRUEBAS**

### **✅ Infraestructura**
- [ ] Docker containers iniciando
- [ ] Base de datos conectando
- [ ] Redis funcionando
- [ ] Nginx sirviendo

### **✅ APIs**
- [ ] Health check respondiendo
- [ ] Endpoints accesibles
- [ ] CORS configurado
- [ ] Rate limiting funcionando

### **✅ Autenticación**
- [ ] Registro de usuarios
- [ ] Login exitoso
- [ ] JWT tokens válidos
- [ ] Logout funcionando

### **✅ Funcionalidad Core**
- [ ] Crear paquetes
- [ ] Tracking de paquetes
- [ ] Gestión de clientes
- [ ] Cálculo de tarifas

### **✅ Notificaciones**
- [ ] Email enviándose
- [ ] SMS configurado
- [ ] Estados actualizándose

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

### **❌ Servicios no inician**
```bash
./SCRIPTS/stop-services.sh
./SCRIPTS/start-services.sh
```

### **❌ Base de datos no conecta**
```bash
./SCRIPTS/test-database.sh
```

### **❌ APIs no responden**
```bash
./SCRIPTS/test-api-endpoints.sh
```

### **❌ Autenticación falla**
```bash
./SCRIPTS/test-authentication.sh
```

---

**Última actualización**: Enero 2025  
**Versión**: 3.0.0  
**Mantenido por**: Equipo de Desarrollo PAQUETES EL CLUB
