# 🚀 RESUMEN COMPLETO: PROYECTO PAQUETES EL CLUB v3.1 EN AWS

## 📍 **INFORMACIÓN DEL SERVIDOR**

- **🌐 IP Pública**: 18.214.124.14
- **🏠 IP Privada**: 172.26.15.87
- **👤 Usuario**: ubuntu
- **🖥️ Sistema**: Ubuntu 24.04.3 LTS
- **💾 CPU**: 2 Cores
- **🧠 RAM**: 1GB
- **💿 Disco**: 37.70GB
- **🔌 Puertos**: 80, 443
- **🗄️ Base de Datos**: AWS RDS (PostgreSQL)
- **🔑 Alias SSH**: papyrus

## 🏗️ **ESTRUCTURA DEL PROYECTO EN AWS**

```
/home/ubuntu/Paquetes/
├── 📄 ARCHIVOS PRINCIPALES
│   ├── .env                          # Variables de entorno
│   ├── docker-compose.yml            # Configuración Docker
│   ├── Dockerfile                    # Imagen de la aplicación
│   └── requirements.txt              # Dependencias Python
│
├── 🐳 CONTENEDORES DOCKER
│   ├── paqueteria_v31_app            # Aplicación FastAPI (Puerto 8001)
│   ├── paqueteria_v31_nginx          # Servidor web Nginx (Puertos 80, 443)
│   ├── paqueteria_v31_redis          # Cache Redis (Puerto 6380)
│   └── paqueteria_v31_celery_worker  # Procesador de tareas
│
├── 📁 CÓDIGO DE LA APLICACIÓN
│   ├── src/                          # Código fuente Python
│   ├── templates/                    # Plantillas HTML
│   ├── static/                       # Archivos estáticos
│   └── assets/                       # Recursos (CSS, JS, imágenes)
│
├── 🌐 CONFIGURACIÓN WEB
│   ├── nginx/conf.d/paqueteria.conf  # Configuración Nginx
│   └── ssl/                          # Certificados SSL
│
└── 📊 DATOS Y LOGS
    ├── uploads/                      # Archivos subidos
    ├── logs/                         # Logs de la aplicación
    └── Volumenes/                    # Volúmenes adicionales
```

## 🔧 **ARCHIVOS CLAVE PARA MODIFICACIONES**

### **Configuración Principal**
- **`.env`** - Variables de entorno (SMTP, base de datos, etc.)
- **`docker-compose.yml`** - Configuración de contenedores
- **`Dockerfile`** - Construcción de la imagen

### **Aplicación Web**
- **`src/main.py`** - Punto de entrada de la aplicación
- **`src/routers/`** - Rutas y endpoints de la API
- **`src/models/`** - Modelos de base de datos
- **`templates/`** - Plantillas HTML
- **`static/`** - CSS, JavaScript, imágenes

### **Servidor Web**
- **`nginx/conf.d/paqueteria.conf`** - Configuración de Nginx
- **`ssl/`** - Certificados SSL

## 🔄 **SINCRONIZACIÓN LOCAL → AWS**

### **Script Automático (Recomendado)**
```bash
# Usar el script de sincronización
./sync-to-aws.sh
```

### **Método Manual**
```bash
# 1. Crear tarball del código local
cd /ruta/local/del/proyecto
tar -czf app-code.tar.gz code/

# 2. Transferir a AWS
scp -i ~/.ssh/PAPYRUS.pem app-code.tar.gz ubuntu@18.214.124.14:/home/ubuntu/Paquetes/

# 3. Extraer en AWS
papyrus
cd /home/ubuntu/Paquetes
tar -xzf app-code.tar.gz --strip-components=1

# 4. Reiniciar contenedores
docker-compose down
docker-compose up -d --build
```

### **Sincronización Selectiva**
```bash
# Sincronizar archivos específicos
scp -i ~/.ssh/PAPYRUS.pem \
    src/main.py \
    templates/login.html \
    ubuntu@18.214.124.14:/home/ubuntu/Paquetes/

# Reiniciar solo la aplicación
papyrus
docker restart paqueteria_v31_app
```

## 🛠️ **MODIFICACIONES COMUNES**

### **1. Cambiar Configuración de Email**
```bash
papyrus
cd /home/ubuntu/Paquetes
nano .env
# Modificar EMAIL_PASSWORD, EMAIL_HOST, etc.
docker-compose restart app
```

### **2. Modificar Plantillas HTML**
```bash
# Local → AWS
scp -i ~/.ssh/PAPYRUS.pem templates/login.html ubuntu@18.214.124.14:/home/ubuntu/Paquetes/templates/
papyrus
docker restart paqueteria_v31_app
```

### **3. Cambiar Configuración de Nginx**
```bash
# Local → AWS
scp -i ~/.ssh/PAPYRUS.pem nginx/conf.d/paqueteria.conf ubuntu@18.214.124.14:/home/ubuntu/Paquetes/nginx/conf.d/
papyrus
docker restart paqueteria_v31_nginx
```

### **4. Agregar Nuevas Rutas API**
```bash
# Local → AWS
scp -i ~/.ssh/PAPYRUS.pem src/routers/new_router.py ubuntu@18.214.124.14:/home/ubuntu/Paquetes/src/routers/
papyrus
docker restart paqueteria_v31_app
```

## 📊 **ESTADO DE LOS CONTENEDORES**

### **Verificar Estado**
```bash
papyrus
cd /home/ubuntu/Paquetes
docker ps
docker-compose ps
```

### **Logs de los Contenedores**
```bash
# Logs de la aplicación
docker logs paqueteria_v31_app

# Logs de Nginx
docker logs paqueteria_v31_nginx

# Logs de Redis
docker logs paqueteria_v31_redis

# Logs de Celery
docker logs paqueteria_v31_celery_worker
```

## 🔍 **MONITOREO Y DEBUGGING**

### **Verificar Configuración**
```bash
# Verificar variables de entorno
papyrus
cd /home/ubuntu/Paquetes
cat .env

# Verificar configuración de Nginx
docker exec paqueteria_v31_nginx nginx -t

# Verificar conexión a base de datos
docker exec paqueteria_v31_app python -c "from src.database.database import engine; print('DB OK')"
```

### **Acceso Directo a Contenedores**
```bash
# Acceder a la aplicación
docker exec -it paqueteria_v31_app bash

# Acceder a Nginx
docker exec -it paqueteria_v31_nginx sh

# Ejecutar comandos Python
docker exec paqueteria_v31_app python -c "print('Hello from container')"
```

## 🚀 **COMANDOS ÚTILES**

### **Gestión de Contenedores**
```bash
# Iniciar todo
docker-compose up -d

# Detener todo
docker-compose down

# Reconstruir y reiniciar
docker-compose down
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f app
```

### **Backup y Restore**
```bash
# Crear backup completo
tar -czf backup-$(date +%Y%m%d_%H%M%S).tar.gz /home/ubuntu/Paquetes/

# Restaurar desde backup
tar -xzf backup-YYYYMMDD_HHMMSS.tar.gz
```

## 🌐 **URLS IMPORTANTES**

- **🔗 Aplicación Principal**: https://guia.papyrus.com.co
- **🔗 Health Check**: https://guia.papyrus.com.co/health
- **🔗 Login**: https://guia.papyrus.com.co/login
- **🔗 Admin**: https://guia.papyrus.com.co/admin
- **🔗 Forgot Password**: https://guia.papyrus.com.co/forgot-password

## 🔐 **CREDENCIALES DE ACCESO**

- **👤 Usuario**: jveyes
- **📧 Email**: jveyes@gmail.com
- **🔑 Contraseña**: (la misma del sistema local)

## 📧 **CONFIGURACIÓN SMTP**

- **🏢 Servidor**: smtp.gmail.com
- **🔌 Puerto**: 587
- **👤 Usuario**: jveyes@gmail.com
- **🔒 TLS**: Habilitado
- **⚠️ Pendiente**: EMAIL_PASSWORD en .env

## 📋 **CHECKLIST DE SINCRONIZACIÓN**

### **Antes de Sincronizar**
- [ ] Hacer backup del código actual en AWS
- [ ] Verificar que los cambios locales funcionan
- [ ] Actualizar versiones en requirements.txt si es necesario

### **Durante la Sincronización**
- [ ] Transferir archivos modificados
- [ ] Verificar permisos de archivos
- [ ] Reiniciar contenedores necesarios

### **Después de Sincronizar**
- [ ] Verificar que la aplicación funciona
- [ ] Revisar logs por errores
- [ ] Probar funcionalidades críticas
- [ ] Verificar que SSL sigue funcionando

## 🎯 **ESTADO ACTUAL DEL PROYECTO**

### **✅ Funcionando:**
- ✅ **Aplicación web** - https://guia.papyrus.com.co
- ✅ **Base de datos** - AWS RDS PostgreSQL
- ✅ **SSL/HTTPS** - Certificados configurados
- ✅ **Login de usuarios** - Sistema de autenticación
- ✅ **Contenedores Docker** - Todos funcionando
- ✅ **Nginx** - Servidor web y proxy reverso
- ✅ **Redis** - Cache y sesiones
- ✅ **Celery** - Procesamiento de tareas

### **🔄 Pendiente de Configuración:**
- 🔄 **Sistema de emails** - Falta contraseña de aplicación Gmail
- 🔄 **Restablecimiento de contraseña** - Depende de SMTP
- 🔄 **Notificaciones por email** - Depende de SMTP

## 📞 **SOPORTE Y TROUBLESHOOTING**

### **Problemas Comunes**

1. **Aplicación no responde**
   ```bash
   papyrus
   docker logs paqueteria_v31_app
   docker restart paqueteria_v31_app
   ```

2. **Error de SSL**
   ```bash
   papyrus
   docker logs paqueteria_v31_nginx
   docker restart paqueteria_v31_nginx
   ```

3. **Error de base de datos**
   ```bash
   papyrus
   docker exec paqueteria_v31_app python -c "from src.database.database import engine; print('DB OK')"
   ```

4. **Problemas de permisos**
   ```bash
   papyrus
   sudo chown -R ubuntu:ubuntu /home/ubuntu/Paquetes/
   chmod -R 755 /home/ubuntu/Paquetes/
   ```

### **Logs Importantes**
- **Aplicación**: `docker logs paqueteria_v31_app`
- **Nginx**: `docker logs paqueteria_v31_nginx`
- **Redis**: `docker logs paqueteria_v31_redis`
- **Celery**: `docker logs paqueteria_v31_celery_worker`

---

**💡 CONSEJO**: Siempre haz un backup antes de sincronizar cambios importantes y prueba en un entorno de desarrollo antes de subir a producción.

**🎉 ¡El proyecto está completamente configurado y funcionando en AWS!**
