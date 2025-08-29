# 🚀 Guía de Deployment AWS - PAQUETES EL CLUB v3.1

## ✅ **Estado: LISTO PARA DEPLOYMENT**

**Versión**: 3.1.1  
**Fecha**: 28 de Agosto, 2025  
**Rama**: main

---

## 📋 **Requisitos Previos**

### **En el servidor AWS:**
- ✅ Docker instalado
- ✅ Docker Compose instalado
- ✅ Git instalado
- ✅ Acceso SSH al servidor
- ✅ Base de datos RDS configurada
- ✅ Dominio configurado (opcional)

### **Configuración necesaria:**
- ✅ Archivo `env.aws` con variables de entorno
- ✅ Archivo `docker-compose.aws.yml` para AWS
- ✅ Scripts de deployment

---

## 🔧 **Configuración para AWS**

### **1. Variables de Entorno (env.aws)**

El archivo `env.aws` contiene la configuración específica para AWS:

```env
# Base de Datos PostgreSQL (AWS RDS)
DATABASE_URL=postgresql://paqueteria_user:Paqueteria2025!Secure@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria

# Configuración SMTP
SMTP_HOST=taylor.mxrouting.net
SMTP_PORT=587
SMTP_USER=guia@papyrus.com.co
SMTP_PASSWORD=^Kxub2aoh@xC2LsK

# Entorno de producción
ENVIRONMENT=production
DEBUG=False
```

### **2. Docker Compose para AWS (docker-compose.aws.yml)**

Diferencias principales con la versión local:
- ❌ **Sin PostgreSQL local** (usa RDS)
- ✅ **Configuración de producción**
- ✅ **Health checks mejorados**
- ✅ **Límites de recursos**
- ✅ **Volúmenes optimizados**

---

## 🚀 **Pasos para Deployment**

### **Opción 1: Deployment Automático (Recomendado)**

```bash
# 1. Conectar al servidor AWS
ssh ubuntu@18.214.124.14

# 2. Navegar al directorio del proyecto
cd /home/ubuntu/Paquetes

# 3. Ejecutar script de pull y deployment
chmod +x code/pull-and-deploy-aws.sh
./code/pull-and-deploy-aws.sh
```

### **Opción 2: Deployment Manual**

```bash
# 1. Hacer pull del código
git pull origin main

# 2. Copiar configuración AWS
cp code/env.aws code/.env

# 3. Ejecutar deployment
cd code
chmod +x deploy-aws.sh
./deploy-aws.sh
```

---

## 🔍 **Verificación del Deployment**

### **1. Verificar servicios**
```bash
docker-compose -f code/docker-compose.aws.yml ps
```

**Estado esperado:**
- ✅ `paqueteria_v31_nginx` - Up
- ✅ `paqueteria_v31_app` - Up (healthy)
- ✅ `paqueteria_v31_redis` - Up
- ✅ `paqueteria_v31_celery_worker` - Up

### **2. Verificar endpoints**
```bash
# Health check
curl http://localhost/health

# API documentation
curl http://localhost/docs

# Aplicación principal
curl http://localhost
```

### **3. Verificar logs**
```bash
# Logs de la aplicación
docker-compose -f code/docker-compose.aws.yml logs app

# Logs de todos los servicios
docker-compose -f code/docker-compose.aws.yml logs -f
```

---

## 🌐 **URLs de Acceso**

### **Local (servidor AWS):**
- **Aplicación**: http://localhost
- **API Docs**: http://localhost/docs
- **Health Check**: http://localhost/health

### **Público (con dominio):**
- **Aplicación**: https://guia.papyrus.com.co
- **API Docs**: https://guia.papyrus.com.co/docs
- **Health Check**: https://guia.papyrus.com.co/health

---

## 🔧 **Comandos Útiles**

### **Gestión de servicios:**
```bash
# Ver estado
docker-compose -f code/docker-compose.aws.yml ps

# Ver logs
docker-compose -f code/docker-compose.aws.yml logs -f

# Reiniciar servicios
docker-compose -f code/docker-compose.aws.yml restart

# Detener servicios
docker-compose -f code/docker-compose.aws.yml down

# Reconstruir y levantar
docker-compose -f code/docker-compose.aws.yml up -d --build
```

### **Gestión de contenedores:**
```bash
# Ver contenedores
docker ps

# Ver logs de un contenedor específico
docker logs paqueteria_v31_app

# Entrar a un contenedor
docker exec -it paqueteria_v31_app bash
```

---

## 🚨 **Solución de Problemas**

### **Problema: Contenedor no inicia**
```bash
# Verificar logs
docker-compose -f code/docker-compose.aws.yml logs app

# Verificar variables de entorno
docker-compose -f code/docker-compose.aws.yml config
```

### **Problema: Error de conexión a base de datos**
```bash
# Verificar DATABASE_URL en .env
cat code/.env | grep DATABASE_URL

# Probar conexión desde contenedor
docker exec -it paqueteria_v31_app python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
print('Conexión exitosa')
"
```

### **Problema: Error de SMTP**
```bash
# Verificar configuración SMTP
docker exec -it paqueteria_v31_app python code/test_smtp.py
```

---

## 📊 **Monitoreo**

### **Recursos del sistema:**
```bash
# Uso de CPU y memoria
docker stats

# Espacio en disco
df -h

# Uso de memoria
free -h
```

### **Logs del sistema:**
```bash
# Logs de Docker
sudo journalctl -u docker

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
```

---

## 🔄 **Actualizaciones**

### **Para actualizar el código:**
```bash
# Opción 1: Automático
./code/pull-and-deploy-aws.sh

# Opción 2: Manual
git pull origin main
docker-compose -f code/docker-compose.aws.yml up -d --build
```

### **Para actualizar configuración:**
```bash
# Editar variables de entorno
nano code/env.aws

# Aplicar cambios
docker-compose -f code/docker-compose.aws.yml restart
```

---

## ✅ **Checklist de Deployment**

- [ ] ✅ Código en rama main
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Base de datos RDS accesible
- [ ] ✅ SMTP configurado
- [ ] ✅ Docker y Docker Compose instalados
- [ ] ✅ Scripts de deployment ejecutables
- [ ] ✅ Servicios iniciados correctamente
- [ ] ✅ Health checks pasando
- [ ] ✅ Aplicación accesible
- [ ] ✅ Logs sin errores críticos

---

## 🎉 **¡Deployment Listo!**

**El código en la rama main está completamente configurado para funcionar en AWS.**

**Para hacer el deployment:**
1. Conecta al servidor AWS
2. Ejecuta: `./code/pull-and-deploy-aws.sh`
3. Selecciona la rama `main`
4. ¡Listo!

**¡El sistema estará funcionando en minutos!** 🚀
