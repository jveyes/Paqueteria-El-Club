# 🚀 PAQUETES EL CLUB v3.0

Sistema de gestión de paquetería con tarifas automáticas, notificaciones multicanal y dashboard administrativo.

## 📋 Características

- ✅ **Gestión de Paquetes**: Anunciar, recibir, entregar y cancelar paquetes
- ✅ **Clientes Simplificados**: Solo nombre, teléfono y número de tracking
- ✅ **Tarifas Automáticas**: Cálculo automático de costos
- ✅ **Notificaciones**: Email y SMS (LIWA.co)
- ✅ **Dashboard**: Estadísticas y métricas en tiempo real
- ✅ **API RESTful**: Documentación automática con Swagger
- ✅ **Autenticación JWT**: Roles y permisos
- ✅ **Monitoreo**: Prometheus y Grafana
- ✅ **Responsive**: Diseño mobile-first

## 🛠️ Tecnologías

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Base de Datos**: PostgreSQL 15
- **Cache**: Redis 7.0
- **Frontend**: HTMX, Tailwind CSS, Alpine.js
- **Contenedores**: Docker, Docker Compose
- **Monitoreo**: Prometheus, Grafana
- **Web Server**: Nginx

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd paqueteria-v3.0/CODE
```

### 2. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 3. Ejecutar script de configuración
```bash
chmod +x setup.sh
./setup.sh
```

### 4. Iniciar servicios
```bash
docker-compose up -d
```

### 5. Ejecutar migraciones
```bash
docker-compose exec app alembic upgrade head
```

## 🌐 Acceso

- **Aplicación**: http://localhost
- **API Docs**: http://localhost/api/docs
- **Grafana**: http://localhost:3000 (admin/Grafana2025!Secure)
- **Prometheus**: http://localhost:9090

## 📊 Estructura del Proyecto

```
CODE/
├── src/                    # Código fuente Python
│   ├── database/          # Configuración de BD
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Esquemas Pydantic
│   ├── routers/           # Endpoints API
│   ├── services/          # Lógica de negocio
│   └── utils/             # Utilidades
├── alembic/               # Migraciones de BD
├── nginx/                 # Configuración Nginx
├── monitoring/            # Configuración monitoreo
├── templates/             # Templates HTML
├── static/                # Archivos estáticos
├── uploads/               # Archivos subidos
└── logs/                  # Logs de aplicación
```

## 🔧 Configuración

### Variables de Entorno Principales

```env
# Base de Datos
POSTGRES_PASSWORD=Paqueteria2025!Secure
DATABASE_URL=postgresql://paqueteria_user:Paqueteria2025!Secure@postgres:5432/paqueteria

# Cache
REDIS_PASSWORD=Redis2025!Secure

# Seguridad
SECRET_KEY=paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication

# Email
SMTP_HOST=taylor.mxrouting.net
SMTP_USER=guia@papyrus.com.co
SMTP_PASSWORD=90@5fmCU%gabP4%*

# SMS (LIWA.co)
LIWA_API_KEY=your_liwa_api_key_here
LIWA_PHONE_NUMBER=your_liwa_phone_number_here
```

## 📱 API Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Información del usuario

### Paquetes
- `POST /api/packages/announce` - Anunciar paquete
- `GET /api/packages/{tracking_number}` - Consultar paquete
- `PUT /api/packages/{id}/receive` - Recibir paquete
- `PUT /api/packages/{id}/deliver` - Entregar paquete
- `GET /api/packages/stats/summary` - Estadísticas

### Clientes
- `GET /api/customers/` - Listar clientes
- `GET /api/customers/{tracking_number}` - Obtener cliente

### Tarifas
- `GET /api/rates/` - Listar tarifas
- `POST /api/rates/calculate` - Calcular tarifa

## 🔍 Monitoreo

### Métricas Disponibles
- Número de paquetes por estado
- Ingresos totales
- Tiempo de respuesta de la API
- Uso de recursos del sistema

### Alertas Configuradas
- Paquetes sin entregar por más de 7 días
- Errores de API > 5%
- Uso de CPU > 80%

## 🚀 Despliegue

### Desarrollo Local
```bash
docker-compose up -d
```

### Producción
```bash
# Configurar SSL
# Configurar dominio
# Configurar backup automático
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Logs

Los logs se encuentran en:
- **Aplicación**: `logs/app.log`
- **Nginx**: `logs/nginx/`
- **Docker**: `docker-compose logs -f`

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

- **Email**: guia@papyrus.com.co
- **Teléfono**: 3334004007
- **Dirección**: Cra. 91 #54-120, Local 12

---

**PAQUETES EL CLUB v3.0** - Sistema de gestión de paquetería profesional
