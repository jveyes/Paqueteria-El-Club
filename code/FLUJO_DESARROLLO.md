# 🔄 FLUJO DE DESARROLLO Y DESPLIEGUE - PAQUETES EL CLUB v3.1

## 📋 **RESUMEN DEL FLUJO**

Este documento describe el flujo de trabajo para desarrollar en localhost y desplegar automáticamente en AWS.

### 🎯 **OBJETIVO**
- **Desarrollo**: Localhost (localhost)
- **Producción**: AWS (pull automático desde GitHub)
- **Despliegue**: Script automatizado en AWS

---

## 🏠 **DESARROLLO LOCAL (localhost)**

### **Configuración Local**
- **Archivo**: `docker-compose.yml`
- **Entorno**: `env.development`
- **Nginx**: `nginx/conf.d/localhost.conf`
- **Base de datos**: PostgreSQL local
- **Puertos**: 80 (nginx), 8001 (app), 5432 (postgres), 6380 (redis)

### **Comandos de Desarrollo**
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Detener servicios
docker-compose down

# Reconstruir después de cambios
docker-compose up -d --build
```

### **URLs de Acceso Local**
- 🌐 **Aplicación**: http://localhost
- 📊 **Health Check**: http://localhost/health
- 📚 **API Docs**: http://localhost/docs
- 🗄️ **Base de datos**: localhost:5432

---

## ☁️ **PRODUCCIÓN AWS**

### **Configuración AWS**
- **Archivo**: `docker-compose.aws.yml`
- **Entorno**: `env.aws`
- **Nginx**: `nginx/conf.d/nginx-papyrus.conf`
- **Base de datos**: PostgreSQL local (temporal) / RDS (futuro)
- **Dominio**: https://guia.papyrus.com.co

### **Script de Despliegue**
```bash
# En el servidor AWS
cd /home/ubuntu/Paquetes/code
./deploy-aws.sh
```

### **URLs de Acceso AWS**
- 🌐 **Aplicación**: https://guia.papyrus.com.co
- 📊 **Health Check**: https://guia.papyrus.com.co/health
- 📚 **API Docs**: https://guia.papyrus.com.co/docs

---

## 🔄 **FLUJO DE TRABAJO**

### **1. Desarrollo en Localhost**
```bash
# 1. Hacer cambios en el código
# 2. Probar localmente
docker-compose up -d

# 3. Verificar que todo funcione
curl http://localhost/health

# 4. Commit y push a GitHub
git add .
git commit -m "Descripción de cambios"
git push origin main
```

### **2. Despliegue en AWS**
```bash
# 1. Conectarse al servidor AWS
ssh papyrus

# 2. Ejecutar script de despliegue
cd /home/ubuntu/Paquetes/code
./deploy-aws.sh
```

---

## 📁 **ARCHIVOS DE CONFIGURACIÓN**

### **Localhost (Desarrollo)**
```
├── docker-compose.yml          # Configuración local
├── env.development             # Variables de entorno local
├── nginx/conf.d/localhost.conf # Nginx local
└── database/init.sql          # Inicialización BD local
```

### **AWS (Producción)**
```
├── docker-compose.aws.yml      # Configuración AWS
├── env.aws                     # Variables de entorno AWS
├── nginx/conf.d/nginx-papyrus.conf # Nginx AWS
├── deploy-aws.sh              # Script de despliegue
└── ssl/                       # Certificados SSL
```

---

## 🛠️ **SCRIPT DE DESPLIEGUE AWS**

### **Funcionalidades del Script**
1. **Backup automático** de la versión actual
2. **Pull del código** desde GitHub
3. **Verificación** de archivos de configuración
4. **Reinicio** de contenedores y servicios
5. **Health checks** automáticos
6. **Verificación de logs** y errores
7. **Reporte final** del estado

### **Uso del Script**
```bash
# Ejecutar despliegue completo
./deploy-aws.sh

# Ver logs del despliegue
tail -f /var/log/deploy.log
```

---

## 🔧 **OPTIMIZACIÓN DE ARCHIVOS ESTÁTICOS**

### **Script de Optimización**
```bash
# Optimizar archivos estáticos
python scripts/optimize_static.py
```

### **Características**
- **Compresión gzip** automática
- **Hashing de archivos** para cache
- **Manifest JSON** con metadatos
- **Configuración Nginx** optimizada

---

## 📊 **MONITOREO Y LOGS**

### **Comandos de Monitoreo**
```bash
# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs específicos
docker-compose logs app
docker-compose logs nginx

# Health check
curl http://localhost/health
```

### **Logs Importantes**
- **Aplicación**: `/app/logs/app.log`
- **Nginx**: `/var/log/nginx/`
- **Docker**: `docker-compose logs`

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Problemas Comunes**

#### **1. Servicios no inician**
```bash
# Verificar logs
docker-compose logs

# Reconstruir imágenes
docker-compose build --no-cache

# Limpiar recursos
docker system prune -f
```

#### **2. Base de datos no conecta**
```bash
# Verificar PostgreSQL
docker-compose logs postgres

# Verificar variables de entorno
cat env.development | grep DATABASE_URL
```

#### **3. Nginx no sirve archivos estáticos**
```bash
# Verificar configuración
docker-compose logs nginx

# Verificar permisos
ls -la static/
```

---

## 🔐 **SEGURIDAD**

### **Variables de Entorno**
- **Local**: `env.development` (DEBUG=true)
- **AWS**: `env.aws` (DEBUG=false)

### **SSL/HTTPS**
- **Local**: No requerido
- **AWS**: Certificados en `ssl/`

### **Base de Datos**
- **Local**: PostgreSQL local
- **AWS**: PostgreSQL local (temporal) / RDS (futuro)

---

## 📈 **ESCALABILIDAD**

### **Recursos Docker**
- **Local**: Recursos limitados para desarrollo
- **AWS**: Recursos optimizados para producción

### **Cache y Performance**
- **Local**: Cache corto (1 hora)
- **AWS**: Cache largo (1 año)

---

## 📞 **CONTACTO Y SOPORTE**

### **Comandos de Emergencia**
```bash
# Rollback rápido
docker-compose -f docker-compose.aws.yml down
git reset --hard HEAD~1
docker-compose -f docker-compose.aws.yml up -d

# Backup manual
tar czf backup_$(date +%Y%m%d_%H%M%S).tar.gz .
```

### **Logs de Despliegue**
- **Ubicación**: `/home/ubuntu/Paquetes/backups/`
- **Formato**: `paqueteria_backup_YYYYMMDD_HHMMSS.tar.gz`

---

## ✅ **CHECKLIST DE DESPLIEGUE**

### **Antes del Despliegue**
- [ ] Código probado en localhost
- [ ] Tests pasando
- [ ] Commit y push a GitHub
- [ ] Backup de producción (automático)

### **Después del Despliegue**
- [ ] Health check exitoso
- [ ] Logs sin errores críticos
- [ ] Archivos estáticos cargando
- [ ] Base de datos conectada
- [ ] SSL funcionando
- [ ] Dominio respondiendo

---

**🎉 ¡El flujo está configurado y listo para usar!**
