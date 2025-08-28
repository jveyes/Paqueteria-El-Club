# Guía de Despliegue de Nginx en AWS
## PAQUETES EL CLUB v3.1

### Información de la Instancia AWS
- **IP Pública**: 18.214.124.14
- **IP Privada**: 172.26.15.87
- **Usuario**: ubuntu
- **Sistema**: Ubuntu 24.04.3 LTS
- **CPU**: 2 Cores
- **RAM**: 1GB
- **Disco**: 37.70GB
- **Puertos**: 80, 443
- **DNS**: guia.papyrus.com.co

### Base de Datos RDS
- **Endpoint**: ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com
- **Usuario**: jveyes
- **Puerto**: 5432

---

## PASO 1: Conectar a la Instancia AWS

```bash
ssh -i tu-clave.pem ubuntu@18.214.124.14
```

---

## PASO 2: Verificar Docker y Docker Compose

```bash
# Verificar versión de Docker
docker --version

# Verificar versión de Docker Compose
docker compose version

# Verificar que los servicios estén corriendo
docker ps
```

---

## PASO 3: Crear Estructura de Directorios

```bash
# Crear directorio principal del proyecto
mkdir -p /home/ubuntu/Paquetes

# Crear directorios necesarios para nginx
mkdir -p /home/ubuntu/Paquetes/nginx/conf.d
mkdir -p /home/ubuntu/Paquetes/ssl
mkdir -p /home/ubuntu/Paquetes/uploads
mkdir -p /home/ubuntu/Paquetes/static
mkdir -p /home/ubuntu/Paquetes/logs

# Crear directorio para volúmenes
mkdir -p /home/ubuntu/Paquetes/Volumenes
```

---

## PASO 4: Crear Archivo de Configuración de Nginx

```bash
# Crear archivo de configuración principal de nginx
cat > /home/ubuntu/Paquetes/nginx/nginx.conf << 'EOF'
# ========================================
# PAQUETES EL CLUB v3.1 - Configuración Nginx Optimizada para AWS
# ========================================

user nginx;
worker_processes 1;  # Un solo worker para ahorrar RAM
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 100;  # Suficiente para 50 usuarios
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # Performance optimizada para poca RAM
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 30;  # Reducido para liberar conexiones
    types_hash_max_size 1024;  # Reducido

    # Gzip optimizado
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 4;  # Reducido para ahorrar CPU
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript;

    # Rate limiting para 50 usuarios
    limit_req_zone $binary_remote_addr zone=api:10m rate=20r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=10r/m;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Include server configurations
    include /etc/nginx/conf.d/*.conf;
}
EOF
```

---

## PASO 5: Crear Configuración del Servidor

```bash
# Crear configuración del servidor para guia.papyrus.com.co
cat > /home/ubuntu/Paquetes/nginx/conf.d/paqueteria.conf << 'EOF'
# ========================================
# Configuración del servidor para PAQUETES EL CLUB
# ========================================

# Redirección HTTP a HTTPS
server {
    listen 80;
    server_name guia.papyrus.com.co;
    
    # Redireccionar todo el tráfico HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

# Configuración HTTPS
server {
    listen 443 ssl http2;
    server_name guia.papyrus.com.co;

    # Configuración SSL (temporal - usar certificados reales en producción)
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Configuración de seguridad
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Configuración de archivos estáticos
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Configuración de uploads
    location /uploads/ {
        alias /var/www/uploads/;
        expires 1y;
        add_header Cache-Control "public";
        access_log off;
    }

    # Configuración de la aplicación principal
    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Rate limiting para API
        limit_req zone=api burst=10 nodelay;
    }

    # Configuración específica para API
    location /api/ {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Rate limiting más estricto para API
        limit_req zone=api burst=5 nodelay;
    }

    # Configuración para login
    location /login {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Rate limiting para login
        limit_req zone=login burst=3 nodelay;
    }

    # Configuración para health check
    location /health {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        access_log off;
    }

    # Configuración para favicon
    location = /favicon.ico {
        alias /var/www/static/favicon.ico;
        access_log off;
        log_not_found off;
    }

    # Configuración para robots.txt
    location = /robots.txt {
        alias /var/www/static/robots.txt;
        access_log off;
        log_not_found off;
    }

    # Configuración de logs
    access_log /var/log/nginx/paqueteria_access.log main;
    error_log /var/log/nginx/paqueteria_error.log warn;
}
EOF
```

---

## PASO 6: Crear Certificados SSL Temporales

```bash
# Crear directorio para certificados SSL
mkdir -p /home/ubuntu/Paquetes/ssl

# Generar certificados SSL temporales (solo para desarrollo)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /home/ubuntu/Paquetes/ssl/key.pem \
    -out /home/ubuntu/Paquetes/ssl/cert.pem \
    -subj "/C=CO/ST=Bogota/L=Bogota/O=PAQUETES EL CLUB/CN=guia.papyrus.com.co"

# Verificar que se crearon los certificados
ls -la /home/ubuntu/Paquetes/ssl/
```

---

## PASO 7: Crear Variables de Entorno

```bash
# Crear archivo .env con las variables necesarias
cat > /home/ubuntu/Paquetes/.env << 'EOF'
# ========================================
# Variables de Entorno - PAQUETES EL CLUB v3.1
# ========================================

# Base de Datos RDS
DATABASE_URL=postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria

# Configuración de la aplicación
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
ENVIRONMENT=production

# Configuración de email
SMTP_HOST=taylor.mxrouting.net
SMTP_PORT=587
SMTP_USER=guia@papyrus.com.co
SMTP_PASSWORD=90@5fmCU%gabP4%*

# Configuración de Redis (si se usa)
REDIS_URL=redis://localhost:6379/0

# Configuración de Liwa (si se usa)
LIWA_API_KEY=tu-api-key-aqui
LIWA_PHONE_NUMBER=tu-numero-aqui

# Configuración de PostgreSQL local (si se necesita)
POSTGRES_PASSWORD=tu-password-postgres-aqui
EOF

# Verificar que se creó el archivo
cat /home/ubuntu/Paquetes/.env
```

---

## PASO 8: Crear Docker Compose para Nginx

```bash
# Crear docker-compose.yml específico para nginx
cat > /home/ubuntu/Paquetes/docker-compose-nginx.yml << 'EOF'
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    container_name: paqueteria_v31_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./uploads:/var/www/uploads:ro
      - ./static:/var/www/static:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./logs:/var/log/nginx
    networks:
      - paqueteria_network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 32M
          cpus: '0.2'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  paqueteria_network:
    driver: bridge
EOF
```

---

## PASO 9: Crear Archivos Estáticos Básicos

```bash
# Crear favicon básico
echo "Favicon placeholder" > /home/ubuntu/Paquetes/static/favicon.ico

# Crear robots.txt
cat > /home/ubuntu/Paquetes/static/robots.txt << 'EOF'
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
EOF

# Crear archivo de uploads de ejemplo
mkdir -p /home/ubuntu/Paquetes/uploads
echo "Directorio de uploads creado" > /home/ubuntu/Paquetes/uploads/README.txt
```

---

## PASO 10: Desplegar el Contenedor de Nginx

```bash
# Navegar al directorio del proyecto
cd /home/ubuntu/Paquetes

# Verificar que todos los archivos estén en su lugar
ls -la
ls -la nginx/
ls -la nginx/conf.d/
ls -la ssl/
ls -la static/

# Desplegar el contenedor de nginx
docker compose -f docker-compose-nginx.yml up -d

# Verificar que el contenedor esté corriendo
docker ps

# Verificar los logs del contenedor
docker logs paqueteria_v31_nginx

# Verificar que nginx esté respondiendo
curl -I http://localhost
curl -I https://localhost -k
```

---

## PASO 11: Verificar la Configuración

```bash
# Verificar la configuración de nginx dentro del contenedor
docker exec paqueteria_v31_nginx nginx -t

# Verificar que los puertos estén abiertos
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Verificar que el firewall permita el tráfico
sudo ufw status
```

---

## PASO 12: Configurar DNS (Opcional)

```bash
# Verificar que el DNS apunte a la IP correcta
nslookup guia.papyrus.com.co

# Si necesitas configurar el DNS localmente (solo para pruebas)
echo "18.214.124.14 guia.papyrus.com.co" | sudo tee -a /etc/hosts
```

---

## PASO 13: Monitoreo y Logs

```bash
# Ver logs en tiempo real
docker logs -f paqueteria_v31_nginx

# Ver logs de nginx del sistema
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Verificar uso de recursos
docker stats paqueteria_v31_nginx
```

---

## PASO 14: Comandos de Gestión

```bash
# Detener el contenedor
docker compose -f docker-compose-nginx.yml down

# Reiniciar el contenedor
docker compose -f docker-compose-nginx.yml restart

# Ver logs
docker compose -f docker-compose-nginx.yml logs

# Actualizar configuración (después de cambios)
docker compose -f docker-compose-nginx.yml down
docker compose -f docker-compose-nginx.yml up -d
```

---

## NOTAS IMPORTANTES

1. **Certificados SSL**: Los certificados generados son temporales. Para producción, usar certificados reales de Let's Encrypt o un proveedor de confianza.

2. **Seguridad**: 
   - Cambiar las claves secretas en el archivo .env
   - Configurar firewall adecuadamente
   - Usar certificados SSL reales

3. **Rendimiento**: 
   - La configuración está optimizada para 1GB de RAM
   - Monitorear el uso de recursos
   - Ajustar worker_processes según necesidad

4. **Backup**: 
   - Hacer backup de la configuración
   - Backup de certificados SSL
   - Backup de archivos estáticos

5. **Monitoreo**: 
   - Configurar alertas de uso de recursos
   - Monitorear logs de acceso y error
   - Verificar health checks regularmente

---

## PRÓXIMOS PASOS

1. Configurar certificados SSL reales
2. Integrar con la aplicación backend
3. Configurar monitoreo y alertas
4. Implementar backup automático
5. Configurar CDN si es necesario
