# 🚀 Guía de Deployment en AWS Lightsail - PAQUETES EL CLUB v3.1

## 📋 **Descripción**

Esta guía te ayudará a desplegar PAQUETES EL CLUB v3.1 en AWS Lightsail usando un solo contenedor Docker.

## 🎯 **Configuración Específica**

### **Información del Proyecto**
- **Usuario Docker Hub**: `jveyes25`
- **Dominio**: `guia.papyrus.com.co`
- **IP del Servidor**: `18.214.124.14`
- **Puertos**: 80 (HTTP) y 443 (HTTPS)
- **SSL**: Habilitado con Let's Encrypt

---

## 🏗️ **Arquitectura AWS Lightsail**

```
🌐 Internet (guia.papyrus.com.co)
├── 🔒 AWS Lightsail Instance (18.214.124.14)
├── 🐳 Contenedor Único (paqueteria-club-lightsail)
│   ├── 🚀 FastAPI (Aplicación)
│   ├── 🗄️ PostgreSQL (Base de datos)
│   ├── 🔴 Redis (Cache)
│   ├── 🌐 Nginx (Web server)
│   └── 📊 Supervisor (Gestión de procesos)
└── 📁 Volumes Persistentes
    ├── 📊 Base de datos
    ├── 📁 Uploads
    ├── 📝 Logs
    └── 🔐 SSL Certificates
```

---

## 🚀 **Pasos de Deployment**

### **1. Preparar la Instancia AWS Lightsail**

```bash
# Conectar a la instancia
ssh ubuntu@18.214.124.14

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y curl wget git net-tools dnsutils

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### **2. Configurar Firewall**

```bash
# Instalar UFW
sudo apt install -y ufw

# Configurar reglas
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### **3. Clonar el Repositorio**

```bash
# Clonar repositorio
git clone https://github.com/jveyes/Paqueteria-El-Club.git
cd Paqueteria-El-Club/production-deployment

# Verificar archivos
ls -la
```

### **4. Configurar Variables de Entorno**

```bash
# Copiar archivo de configuración
cp env.production .env

# Verificar configuración
cat .env | grep -E "(DOMAIN|DOCKER_USERNAME|SECRET_KEY)"
```

**Variables ya configuradas:**
- `DOCKER_USERNAME=jveyes25`
- `DOMAIN=guia.papyrus.com.co`
- `INSTANCE_IP=18.214.124.14`
- `SECRET_KEY=paqueteria_club_v3_1_0_super_secret_key_2025_aws_lightsail_production`

### **5. Construir y Subir Imagen Docker**

```bash
# Login a Docker Hub
docker login

# Construir y subir imagen
./scripts/build-and-push.sh
```

### **6. Desplegar en AWS Lightsail**

```bash
# Ejecutar deployment
./scripts/deploy-lightsail.sh
```

---

## 🔒 **Configuración de SSL**

### **1. Verificar DNS**

```bash
# Verificar que el dominio apunta al servidor
dig guia.papyrus.com.co

# Debe mostrar: 18.214.124.14
```

### **2. Configurar SSL Automático**

```bash
# El script ya incluye configuración SSL automática
# Si necesitas configurar manualmente:

docker-compose -f docker-compose.lightsail.yml exec paqueteria-club certbot --nginx -d guia.papyrus.com.co --non-interactive --agree-tos --email admin@papyrus.com.co
```

---

## 📊 **Monitoreo y Logs**

### **Ver Logs**

```bash
# Logs de la aplicación
docker-compose -f docker-compose.lightsail.yml logs -f paqueteria-club

# Logs específicos
docker-compose -f docker-compose.lightsail.yml logs -f paqueteria-club | grep ERROR
```

### **Health Checks**

```bash
# Verificar aplicación
curl http://guia.papyrus.com.co/health

# Verificar API
curl http://guia.papyrus.com.co/docs

# Verificar SSL
curl -I https://guia.papyrus.com.co
```

---

## 🔄 **Backup y Recovery**

### **Backup Automático**

```bash
# Crear script de backup
cat > backup-lightsail.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.lightsail.yml exec -T paqueteria-club pg_dump -U paqueteria_user paqueteria_club > backup_$DATE.sql
gzip backup_$DATE.sql
echo "Backup creado: backup_$DATE.sql.gz"
EOF

chmod +x backup-lightsail.sh

# Ejecutar backup
./backup-lightsail.sh
```

### **Restore**

```bash
# Restaurar backup
gunzip backup_20250828_120000.sql.gz
docker-compose -f docker-compose.lightsail.yml exec -T paqueteria-club psql -U paqueteria_user paqueteria_club < backup_20250828_120000.sql
```

---

## 🆘 **Troubleshooting AWS Lightsail**

### **Problemas Comunes**

#### **1. Error de memoria**
```bash
# Verificar uso de memoria
free -h

# Si es necesario, aumentar swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### **2. Error de puertos**
```bash
# Verificar puertos en uso
sudo netstat -tulpn | grep -E ":80|:443"

# Si hay conflictos, parar servicios
sudo systemctl stop apache2 nginx
```

#### **3. Error de DNS**
```bash
# Verificar resolución DNS
nslookup guia.papyrus.com.co

# Verificar desde internet
curl -I http://guia.papyrus.com.co
```

#### **4. Error de SSL**
```bash
# Verificar certificados
docker-compose -f docker-compose.lightsail.yml exec paqueteria-club certbot certificates

# Renovar certificados
docker-compose -f docker-compose.lightsail.yml exec paqueteria-club certbot renew
```

---

## 📈 **Escalabilidad**

### **Actualizar Aplicación**

```bash
# Parar servicios
docker-compose -f docker-compose.lightsail.yml down

# Actualizar imagen
docker pull jveyes25/paqueteria-club:v3.1.0

# Reiniciar servicios
docker-compose -f docker-compose.lightsail.yml up -d
```

### **Monitoreo de Recursos**

```bash
# Ver uso de recursos
docker stats paqueteria-club-lightsail

# Ver logs en tiempo real
docker-compose -f docker-compose.lightsail.yml logs -f --tail=100
```

---

## 🔧 **Mantenimiento**

### **Actualizaciones Automáticas**

```bash
# Crear script de actualización
cat > update-lightsail.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/Paqueteria-El-Club/production-deployment
git pull
docker-compose -f docker-compose.lightsail.yml pull
docker-compose -f docker-compose.lightsail.yml up -d
echo "Actualización completada: $(date)"
EOF

chmod +x update-lightsail.sh

# Agregar a crontab (actualizar cada domingo a las 2 AM)
echo "0 2 * * 0 /home/ubuntu/Paqueteria-El-Club/production-deployment/update-lightsail.sh" | crontab -
```

### **Limpieza de Recursos**

```bash
# Limpiar imágenes no utilizadas
docker image prune -f

# Limpiar contenedores detenidos
docker container prune -f

# Limpiar volúmenes no utilizados
docker volume prune -f
```

---

## 📞 **Información de Contacto**

- **Email**: guia@papyrus.com.co
- **Teléfono**: +57 333 400 4007
- **WhatsApp**: +57 333 400 4007
- **Dirección**: Cra. 91 #54-120, Local 12

---

## 🎊 **Estado Final**

### ✅ **Configuración Completada**
- **Docker Image**: `jveyes25/paqueteria-club:v3.1.0`
- **Dominio**: `guia.papyrus.com.co`
- **SSL**: Let's Encrypt configurado
- **Base de datos**: PostgreSQL local
- **Cache**: Redis local
- **Email**: SMTP configurado

### 🚀 **URLs de Acceso**
- **Aplicación**: https://guia.papyrus.com.co
- **API Docs**: https://guia.papyrus.com.co/docs
- **Health Check**: https://guia.papyrus.com.co/health

---

**🎉 ¡Tu aplicación está lista en AWS Lightsail! 🎉**

**La aplicación estará disponible en: https://guia.papyrus.com.co**
