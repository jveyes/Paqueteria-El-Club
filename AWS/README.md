# Despliegue de Nginx en AWS
## PAQUETES EL CLUB v3.1

### ¿Qué hace este primer contenedor?

Este contenedor de **Nginx** actúa como el **servidor web principal** y **proxy reverso** para el sistema de paquetería. Sus funciones principales son:

#### 🚀 **Funciones Principales**

1. **Servidor Web Principal**
   - Sirve archivos estáticos (CSS, JS, imágenes)
   - Maneja las rutas principales del sitio web
   - Proporciona una interfaz web para los usuarios

2. **Proxy Reverso**
   - Redirige las peticiones HTTP/HTTPS a la aplicación backend
   - Balancea la carga entre diferentes servicios
   - Maneja la terminación SSL/HTTPS

3. **Seguridad y Optimización**
   - Implementa rate limiting para prevenir ataques
   - Añade headers de seguridad
   - Comprime archivos (gzip) para mejor rendimiento
   - Redirige HTTP a HTTPS automáticamente

#### 🔧 **Configuración Específica**

- **Dominio**: `guia.papyrus.com.co`
- **Puertos**: 80 (HTTP) y 443 (HTTPS)
- **Optimizado para**: 1GB RAM, 2 CPU cores
- **Capacidad**: Hasta 50 usuarios simultáneos

#### 📁 **Estructura de Archivos**

```
/home/ubuntu/Paquetes/
├── nginx/
│   ├── nginx.conf          # Configuración principal
│   └── conf.d/
│       └── paqueteria.conf # Configuración del servidor
├── ssl/
│   ├── cert.pem           # Certificado SSL
│   └── key.pem            # Clave privada SSL
├── static/                # Archivos estáticos
├── uploads/               # Archivos subidos
├── logs/                  # Logs de nginx
└── docker-compose-nginx.yml
```

#### 🌐 **URLs de Acceso**

- **HTTP**: `http://18.214.124.14` (redirige a HTTPS)
- **HTTPS**: `https://18.214.124.14`
- **DNS**: `https://guia.papyrus.com.co`

#### ⚙️ **Características Técnicas**

- **Worker Processes**: 1 (optimizado para poca RAM)
- **Worker Connections**: 100
- **Rate Limiting**: 
  - API: 20 requests/segundo
  - Login: 10 requests/minuto
- **Gzip Compression**: Activado
- **SSL/TLS**: TLS 1.2 y 1.3
- **Security Headers**: HSTS, X-Frame-Options, etc.

#### 🔄 **Flujo de Peticiones**

```
Usuario → Nginx (80/443) → Aplicación Backend (8000)
         ↓
    Archivos Estáticos
    (CSS, JS, imágenes)
```

#### 📊 **Monitoreo**

- **Health Check**: `/health`
- **Logs**: `/var/log/nginx/`
- **Métricas**: Docker stats
- **Estado**: `docker ps`

#### 🛠️ **Comandos Útiles**

```bash
# Ver logs en tiempo real
docker logs -f paqueteria_v31_nginx

# Verificar configuración
docker exec paqueteria_v31_nginx nginx -t

# Reiniciar servicio
docker compose -f docker-compose-nginx.yml restart

# Ver estadísticas
docker stats paqueteria_v31_nginx
```

#### ⚠️ **Notas Importantes**

1. **Certificados SSL**: Actualmente usa certificados temporales
2. **Backend**: Necesita la aplicación backend corriendo en puerto 8000
3. **Firewall**: Asegurar que los puertos 80 y 443 estén abiertos
4. **DNS**: Configurar `guia.papyrus.com.co` para apuntar a la IP

#### 🚀 **Próximos Pasos**

1. Desplegar la aplicación backend
2. Configurar certificados SSL reales
3. Configurar monitoreo y alertas
4. Implementar backup automático
5. Optimizar rendimiento según uso real

---

### Archivos Incluidos

- `NGINX_DEPLOYMENT_GUIDE.md`: Guía paso a paso completa
- `nginx-deploy.sh`: Script de despliegue automatizado
- `README.md`: Este archivo explicativo

### Soporte

Para problemas o preguntas sobre el despliegue, revisar los logs del contenedor y la documentación en la carpeta `docs/`.
