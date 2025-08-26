# 🚀 PAQUETERIA EL CLUB v3.1

Sistema de gestión de paquetería optimizado para el Club, desarrollado con FastAPI, PostgreSQL y Docker.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API](#-api)
- [Desarrollo](#-desarrollo)
- [Deployment](#-deployment)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🔐 Sistema de Autenticación
- **Login/Logout** con JWT tokens
- **Registro de usuarios** (solo para autenticados)
- **Recuperación de contraseñas**
- **Roles de usuario** (admin, operator, user)

### 📦 Gestión de Paquetes
- **Anuncio de paquetes** para clientes
- **Consulta de estado** de paquetes
- **Seguimiento** con números de guía
- **Notificaciones** automáticas

### 🎨 Interfaz de Usuario
- **Diseño responsive** (mobile-first)
- **Templates optimizados** con Tailwind CSS
- **Componentes reutilizables**
- **UX/UI moderna** y accesible

### 🛠️ Funcionalidades Técnicas
- **API RESTful** completa
- **Base de datos PostgreSQL** optimizada
- **Cache Redis** para mejor rendimiento
- **Docker** para deployment fácil
- **Scripts de automatización**

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno
- **PostgreSQL** - Base de datos principal
- **Redis** - Cache y sesiones
- **SQLAlchemy** - ORM
- **Alembic** - Migraciones de BD
- **JWT** - Autenticación

### Frontend
- **Tailwind CSS** - Framework CSS
- **Alpine.js** - JavaScript reactivo
- **HTMX** - Interacciones dinámicas
- **Jinja2** - Templates

### DevOps
- **Docker** - Contenedores
- **Docker Compose** - Orquestación
- **Nginx** - Proxy reverso
- **Prometheus/Grafana** - Monitoreo

## 🚀 Instalación

### Prerrequisitos
- Docker y Docker Compose
- Git
- 4GB RAM mínimo

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/paqueteria-club.git
cd paqueteria-club
```

2. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus valores
```

3. **Crear estructura de directorios**
```bash
chmod +x setup-structure.sh
./setup-structure.sh
```

4. **Iniciar servicios**
```bash
docker-compose up -d
```

5. **Verificar instalación**
```bash
./scripts/health-check.sh
```

## ⚙️ Configuración

### Variables de Entorno

Copia `env.example` a `.env` y configura:

```bash
# Configuración de la aplicación
APP_NAME=PAQUETERIA EL CLUB
APP_VERSION=3.1.0
ENVIRONMENT=development

# Base de datos
POSTGRES_PASSWORD=tu_password_seguro
DATABASE_URL=postgresql://paqueteria_user:password@postgres:5432/paqueteria

# Redis
REDIS_PASSWORD=tu_redis_password
REDIS_URL=redis://:password@redis:6379/0

# Seguridad
SECRET_KEY=tu_super_secret_key_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (SMTP)
SMTP_HOST=tu_servidor_smtp
SMTP_PORT=587
SMTP_USER=tu_email
SMTP_PASSWORD=tu_password_smtp

# WhatsApp (Liwa API)
LIWA_API_KEY=tu_api_key
LIWA_PHONE_NUMBER=tu_numero
```

### Configuración de Docker

El proyecto incluye:
- **PostgreSQL** optimizado para 1GB RAM
- **Redis** con límites de memoria
- **FastAPI** con workers optimizados
- **Nginx** como proxy reverso

## 🎯 Uso

### URLs de Acceso

- **Aplicación Principal**: http://localhost
- **API**: http://localhost:8001
- **Documentación API**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

### Páginas Principales

- **Página Principal** (`/`) - Anunciar paquetes
- **Consulta** (`/search`) - Buscar paquetes
- **Login** (`/auth/login`) - Iniciar sesión
- **Registro** (`/auth/register`) - Crear cuenta (solo autenticados)
- **Ayuda** (`/help`) - Centro de ayuda

### Comandos Útiles

```bash
# Ver estado de servicios
./scripts/health-check.sh

# Crear backup de BD
./scripts/backup.sh

# Ver logs
docker-compose logs -f app

# Reiniciar servicios
docker-compose restart

# Parar todos los servicios
docker-compose down
```

## 📁 Estructura del Proyecto

```
paqueteria-v3.1/
├── 📁 code/                    # Código fuente
│   ├── 📁 src/                # Backend FastAPI
│   │   ├── 📁 models/         # Modelos de BD
│   │   ├── 📁 routers/        # Rutas API
│   │   ├── 📁 schemas/        # Esquemas Pydantic
│   │   └── 📁 services/       # Lógica de negocio
│   ├── 📁 templates/          # Templates HTML
│   │   ├── 📁 components/     # Componentes base
│   │   ├── 📁 auth/           # Páginas de autenticación
│   │   └── 📁 customers/      # Páginas de clientes
│   ├── 📁 static/             # CSS, JS, imágenes
│   └── 📁 nginx/              # Configuración Nginx
├── 📁 uploads/                # Archivos subidos
├── 📁 logs/                   # Logs del sistema
├── 📁 database/               # BD y migraciones
├── 📁 scripts/                # Scripts de automatización
├── 📁 docs/                   # Documentación
├── 📁 monitoring/             # Configuración de monitoreo
└── 📁 ssl/                    # Certificados SSL
```

## 🔌 API

### Endpoints Principales

#### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/forgot-password` - Recuperar contraseña
- `GET /api/auth/check` - Verificar autenticación

#### Paquetes
- `GET /api/packages` - Listar paquetes
- `POST /api/packages` - Crear paquete
- `GET /api/packages/{id}` - Obtener paquete
- `PUT /api/packages/{id}` - Actualizar paquete

#### Clientes
- `GET /api/customers` - Listar clientes
- `POST /api/customers` - Crear cliente
- `GET /api/customers/{id}` - Obtener cliente

### Documentación Completa
Accede a la documentación interactiva en: http://localhost:8001/docs

## 👨‍💻 Desarrollo

### Configuración del Entorno de Desarrollo

1. **Instalar dependencias de desarrollo**
```bash
cd code
pip install -r requirements-dev.txt
```

2. **Configurar pre-commit hooks**
```bash
pre-commit install
```

3. **Ejecutar tests**
```bash
./scripts/test-api.sh
```

### Convenciones de Código

- **Python**: PEP 8, docstrings obligatorios
- **HTML**: Indentación 2 espacios, atributos en orden alfabético
- **CSS**: Clases de Tailwind, comentarios para secciones
- **JavaScript**: ES6+, funciones con nombres descriptivos

### Estructura de Commits

```
feat: agregar funcionalidad de notificaciones
fix: corregir error en validación de email
docs: actualizar documentación de API
style: mejorar diseño del formulario de login
refactor: optimizar consultas de base de datos
test: agregar tests para autenticación
```

## 🚀 Deployment

### Producción

1. **Configurar variables de producción**
```bash
cp env.example .env.production
# Editar con valores de producción
```

2. **Construir imagen Docker**
```bash
./scripts/build-docker-image.sh
```

3. **Desplegar**
```bash
./scripts/deploy.sh
```

### Monitoreo

- **Health Checks**: `/health`
- **Métricas**: Prometheus en puerto 9090
- **Logs**: Centralizados en `/logs/`
- **Backups**: Automáticos diarios

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- **Issues**: Usar templates predefinidos
- **PRs**: Incluir descripción detallada y tests
- **Code Review**: Mínimo 1 aprobación requerida
- **Tests**: Todos los tests deben pasar

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

- **Documentación**: `/docs/`
- **Issues**: GitHub Issues
- **Email**: soporte@paqueteselclub.com
- **WhatsApp**: +57 333 400 4007

## 🏆 Agradecimientos

- **JEMAVI** - Desarrollo y mantenimiento
- **PAQUETES EL CLUB** - Requerimientos y testing
- **FastAPI Community** - Framework y documentación

---

**Desarrollado con ❤️ por JEMAVI para PAQUETES EL CLUB**
