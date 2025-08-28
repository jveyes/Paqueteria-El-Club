# ========================================
# PAQUETES EL CLUB v3.1 - Imagen Docker
# ========================================

## 📦 **INFORMACIÓN DE LA IMAGEN**

- **Nombre**: `paqueteria-club`
- **Versión**: `v3.1.0`
- **Tag**: `latest`
- **Tamaño**: 806MB
- **Fecha de Construcción**: 25 de Agosto, 2025
- **Estado**: ✅ CONSTRUIDA Y VERIFICADA

## 🏗️ **ESPECIFICACIONES TÉCNICAS**

### **Imagen Base:**
- **Sistema Operativo**: Debian (Python 3.11-slim)
- **Python**: 3.11
- **Arquitectura**: Multi-arch (amd64, arm64)

### **Optimizaciones:**
- ✅ Usuario no-root (appuser)
- ✅ Health check configurado
- ✅ Labels de metadatos
- ✅ .dockerignore optimizado
- ✅ Multi-stage build ready
- ✅ Security best practices

### **Contenido Incluido:**
- ✅ Código completo de la aplicación
- ✅ Dependencias Python instaladas
- ✅ Scripts de gestión
- ✅ Documentación completa
- ✅ Configuración Nginx
- ✅ Esquema de base de datos

## 🚀 **USO DE LA IMAGEN**

### **Ejecución Básica:**
```bash
# Ejecutar imagen
docker run -d \
  --name paqueteria-club \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e REDIS_URL="redis://host:6379/0" \
  -e SECRET_KEY="your-secret-key" \
  paqueteria-club:v3.1.0
```

### **Ejecución con Volúmenes:**
```bash
# Ejecutar con volúmenes persistentes
docker run -d \
  --name paqueteria-club \
  -p 8000:8000 \
  -v paqueteria_uploads:/app/uploads \
  -v paqueteria_logs:/app/logs \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e REDIS_URL="redis://host:6379/0" \
  -e SECRET_KEY="your-secret-key" \
  paqueteria-club:v3.1.0
```

### **Ejecución con Docker Compose:**
```yaml
version: '3.8'
services:
  app:
    image: paqueteria-club:v3.1.0
    container_name: paqueteria-club
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key
    volumes:
      - paqueteria_uploads:/app/uploads
      - paqueteria_logs:/app/logs
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: paqueteria
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7.0-alpine
    volumes:
      - redis_data:/data

volumes:
  paqueteria_uploads:
  paqueteria_logs:
  postgres_data:
  redis_data:
```

## 🔧 **VARIABLES DE ENTORNO**

### **Obligatorias:**
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `REDIS_URL`: URL de conexión a Redis
- `SECRET_KEY`: Clave secreta para JWT

### **Opcionales:**
- `DEBUG`: Modo debug (default: False)
- `ENVIRONMENT`: Ambiente (development/production)
- `LOG_LEVEL`: Nivel de logging
- `SMTP_HOST`: Servidor SMTP
- `SMTP_PORT`: Puerto SMTP
- `SMTP_USER`: Usuario SMTP
- `SMTP_PASSWORD`: Contraseña SMTP

### **Ejemplo Completo:**
```bash
docker run -d \
  --name paqueteria-club \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://paqueteria_user:Paqueteria2025!Secure@postgres:5432/paqueteria" \
  -e REDIS_URL="redis://:Redis2025!Secure@redis:6379/0" \
  -e SECRET_KEY="paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication" \
  -e DEBUG="False" \
  -e ENVIRONMENT="production" \
  -e LOG_LEVEL="INFO" \
  -e SMTP_HOST="taylor.mxrouting.net" \
  -e SMTP_PORT="587" \
  -e SMTP_USER="guia@papyrus.com.co" \
  -e SMTP_PASSWORD="90@5fmCU%gabP4%*" \
  paqueteria-club:v3.1.0
```

## 🌐 **PUERTOS Y ACCESO**

### **Puertos Expuestos:**
- **8000**: Aplicación FastAPI

### **URLs de Acceso:**
- **Aplicación Principal**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **API Directa**: http://localhost:8000

## 📊 **MONITOREO Y LOGS**

### **Health Check:**
```bash
# Verificar estado del contenedor
docker inspect paqueteria-club | grep Health -A 10

# Verificar health check manualmente
curl http://localhost:8000/health
```

### **Logs:**
```bash
# Ver logs en tiempo real
docker logs -f paqueteria-club

# Ver logs de los últimos 100 líneas
docker logs --tail 100 paqueteria-club
```

### **Métricas:**
```bash
# Ver uso de recursos
docker stats paqueteria-club

# Ver información del contenedor
docker inspect paqueteria-club
```

## 🔍 **INSPECCIÓN Y DEBUGGING**

### **Información de la Imagen:**
```bash
# Ver detalles de la imagen
docker image inspect paqueteria-club:v3.1.0

# Ver historial de la imagen
docker history paqueteria-club:v3.1.0

# Ver labels de la imagen
docker image inspect paqueteria-club:v3.1.0 --format='{{.Config.Labels}}'
```

### **Ejecutar Comandos en el Contenedor:**
```bash
# Acceder al shell del contenedor
docker exec -it paqueteria-club /bin/bash

# Ejecutar comando específico
docker exec paqueteria-club python -c "import sys; print(sys.version)"

# Ver archivos en el contenedor
docker exec paqueteria-club ls -la /app
```

## 📦 **DISTRIBUCIÓN**

### **Guardar Imagen:**
```bash
# Guardar imagen como archivo tar
docker save paqueteria-club:v3.1.0 | gzip > paqueteria-club-v3.1.0.tar.gz

# Tamaño aproximado: ~400MB comprimido
```

### **Cargar Imagen:**
```bash
# Cargar imagen desde archivo tar
docker load < paqueteria-club-v3.1.0.tar.gz
```

### **Subir a Registro:**
```bash
# Tag para registro
docker tag paqueteria-club:v3.1.0 your-registry.com/paqueteria-club:v3.1.0

# Subir imagen
docker push your-registry.com/paqueteria-club:v3.1.0
```

## 🛠️ **CONSTRUCCIÓN PERSONALIZADA**

### **Construir desde Fuente:**
```bash
# Clonar repositorio
git clone <repository-url>
cd Paqueteria\ v3.1

# Construir imagen
docker build -t paqueteria-club:custom .

# Ejecutar imagen personalizada
docker run -d -p 8000:8000 paqueteria-club:custom
```

### **Script de Construcción:**
```bash
# Usar script automatizado
./code/SCRIPTS/build-docker-image.sh build

# Ver ayuda del script
./code/SCRIPTS/build-docker-image.sh help
```

## 🔒 **SEGURIDAD**

### **Buenas Prácticas Implementadas:**
- ✅ Usuario no-root (appuser)
- ✅ Imagen base oficial de Python
- ✅ Actualización de paquetes del sistema
- ✅ Eliminación de archivos temporales
- ✅ Variables de entorno para configuración
- ✅ Health check para monitoreo

### **Recomendaciones de Seguridad:**
1. **Nunca ejecutar como root**
2. **Usar secrets para credenciales**
3. **Limitar recursos del contenedor**
4. **Escanear vulnerabilidades regularmente**
5. **Mantener imagen actualizada**

## 📝 **TROUBLESHOOTING**

### **Problemas Comunes:**

#### **Contenedor no inicia:**
```bash
# Verificar logs
docker logs paqueteria-club

# Verificar variables de entorno
docker inspect paqueteria-club | grep -A 20 "Env"
```

#### **Error de conexión a base de datos:**
```bash
# Verificar DATABASE_URL
docker exec paqueteria-club env | grep DATABASE_URL

# Probar conexión manualmente
docker exec paqueteria-club python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
print('Conexión exitosa')
"
```

#### **Error de permisos:**
```bash
# Verificar propietario de archivos
docker exec paqueteria-club ls -la /app

# Corregir permisos si es necesario
docker exec paqueteria-club chown -R appuser:appuser /app
```

## 📞 **SOPORTE**

### **Información de Contacto:**
- **Mantenedor**: PAQUETES EL CLUB
- **Email**: guia@papyrus.com.co
- **Versión**: 3.1.0
- **Fecha**: 25 de Agosto, 2025

### **Recursos Adicionales:**
- **Documentación**: `/app/SCRIPTS/DEPLOYMENT-GUIDE.md`
- **README**: `/app/README.md`
- **Scripts**: `/app/SCRIPTS/`

---

**🎉 ¡Imagen Docker lista para producción!**

**Estado**: ✅ VERIFICADA Y FUNCIONAL  
**Optimizada para**: 50 usuarios simultáneos  
**Especificaciones**: 1GB RAM, 2 vCPUs, 40GB SSD
