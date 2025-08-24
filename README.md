# 🚚 Sistema de Paquetería v3.0

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

**Sistema de Paquetería v3.0** es una plataforma moderna y completa para la gestión de servicios de paquetería, desarrollada con tecnologías de vanguardia. Combina la eficiencia del sistema automático de tarifas de la v1.1 con la modularidad y escalabilidad de la v2.0.

### 🎯 Características Principales

- **🔐 Autenticación JWT** con roles de usuario (Admin, User)
- **📦 Gestión completa de paquetes** con estados y tracking
- **💰 Sistema automático de tarifas** basado en peso y dimensiones
- **👥 Gestión de clientes** con historial completo
- **📊 Dashboard administrativo** con métricas en tiempo real
- **🔔 Sistema de notificaciones** automáticas
- **📈 Monitoreo avanzado** con Prometheus y Grafana
- **🔄 Procesamiento asíncrono** con Celery y Redis
- **🛡️ Seguridad robusta** con rate limiting y validaciones
- **📱 API RESTful** documentada con Swagger/OpenAPI

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (HTMX +       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Tailwind)     │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Cache & Queue │
                       │   (Redis)       │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Monitoring    │
                       │   (Prometheus + │
                       │    Grafana)     │
                       └─────────────────┘
```

## 🚀 Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **PostgreSQL** - Base de datos relacional robusta
- **SQLAlchemy** - ORM para Python
- **Alembic** - Migraciones de base de datos
- **Redis** - Cache y cola de tareas
- **Celery** - Procesamiento asíncrono
- **JWT** - Autenticación segura

### Frontend
- **HTMX** - Interactividad sin JavaScript
- **Tailwind CSS** - Framework CSS utilitario
- **Alpine.js** - JavaScript reactivo ligero

### Infraestructura
- **Docker & Docker Compose** - Containerización
- **Nginx** - Proxy reverso y servidor web
- **Prometheus** - Monitoreo y métricas
- **Grafana** - Visualización de datos

## 📦 Instalación

### Prerrequisitos

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/paqueteria-v3.0.git
cd paqueteria-v3.0

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 3. Iniciar servicios
docker-compose up -d

# 4. Ejecutar migraciones
docker-compose exec app alembic upgrade head

# 5. Crear usuario administrador
curl -X POST "http://localhost/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@papyrus.com.co",
    "password": "Admin2025!",
    "first_name": "Administrador",
    "last_name": "Sistema",
    "role": "admin"
  }'
```

### Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar base de datos
# Crear base de datos PostgreSQL y configurar .env

# 4. Ejecutar migraciones
alembic upgrade head

# 5. Iniciar aplicación
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Database
DATABASE_URL=postgresql://paqueteria_user:password@localhost:5432/paqueteria

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379

# Email (opcional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Configuración de Docker

El proyecto incluye `docker-compose.yml` con todos los servicios necesarios:

- **app** - Aplicación FastAPI
- **postgres** - Base de datos PostgreSQL
- **redis** - Cache y cola de tareas
- **nginx** - Proxy reverso
- **prometheus** - Monitoreo
- **grafana** - Visualización

## 📚 Uso

### Acceso a la Aplicación

- **Aplicación principal:** http://localhost
- **API Documentation:** http://localhost/api/docs
- **Admin Dashboard:** http://localhost/admin
- **Grafana:** http://localhost:3000 (admin/admin)
- **Prometheus:** http://localhost:9090

### Comandos Útiles

```bash
# Ver logs de la aplicación
docker-compose logs app

# Ejecutar tests
./SCRIPTS/run-all-tests.sh

# Backup del sistema
./SCRIPTS/quick-backup.sh

# Restaurar backup
./SCRIPTS/restore-backup.sh backup_file.tar.gz

# Configurar backups automáticos
./SCRIPTS/setup-backup-cron.sh -d
```

## 🔌 API Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/me` - Obtener perfil

### Paquetes
- `GET /api/packages/` - Listar paquetes
- `POST /api/packages/announce` - Anunciar paquete
- `GET /api/packages/{package_id}` - Obtener paquete
- `PUT /api/packages/{package_id}` - Actualizar paquete

### Tarifas
- `GET /api/rates/` - Listar tarifas
- `POST /api/rates/calculate` - Calcular tarifa
- `POST /api/rates/` - Crear tarifa

### Clientes
- `GET /api/customers/` - Listar clientes
- `POST /api/customers/` - Crear cliente
- `GET /api/customers/{customer_id}` - Obtener cliente

## 🧪 Testing

```bash
# Ejecutar todos los tests
./SCRIPTS/run-all-tests.sh

# Tests específicos
./SCRIPTS/test-database.sh
./SCRIPTS/test-api-endpoints.sh

# Ver reportes
ls TEST/reports/
```

## 📊 Monitoreo

### Métricas Disponibles

- **Performance:** Tiempo de respuesta, throughput
- **Business:** Paquetes procesados, ingresos
- **System:** CPU, memoria, disco
- **Application:** Errores, logs, usuarios activos

### Dashboards Grafana

- **Overview:** Vista general del sistema
- **Performance:** Métricas de rendimiento
- **Business:** KPIs del negocio
- **System:** Estado de la infraestructura

## 🔄 Backup y Restauración

### Backup Automático

```bash
# Configurar backup diario
./SCRIPTS/setup-backup-cron.sh -d

# Backup manual
./SCRIPTS/quick-backup.sh
```

### Restauración

```bash
# Restaurar backup completo
./SCRIPTS/restore-backup.sh backup_file.tar.gz

# Restaurar solo base de datos
./SCRIPTS/restore-backup.sh -d backup_file.tar.gz
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```
src/
├── main.py              # Punto de entrada de la aplicación
├── config.py            # Configuraciones
├── dependencies.py      # Dependencias de FastAPI
├── database/            # Configuración de base de datos
├── models/              # Modelos SQLAlchemy
├── schemas/             # Esquemas Pydantic
├── routers/             # Rutas de la API
├── services/            # Lógica de negocio
├── utils/               # Utilidades
└── tasks/               # Tareas asíncronas
```

### Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Soporte

- **Documentación:** [Wiki del proyecto](https://github.com/tu-usuario/paqueteria-v3.0/wiki)
- **Issues:** [GitHub Issues](https://github.com/tu-usuario/paqueteria-v3.0/issues)
- **Email:** soporte@papyrus.com.co

## 🏆 Estado del Proyecto

- ✅ **Backend:** Completamente funcional
- ✅ **API:** Documentada y probada
- ✅ **Base de datos:** Migraciones y seed data
- ✅ **Monitoreo:** Prometheus y Grafana configurados
- ✅ **Backup:** Sistema automatizado
- 🔄 **Frontend:** En desarrollo
- 🔄 **Deployment:** Configuración en progreso

---

**Desarrollado con ❤️ por el Equipo de Paquetería v3.0**
