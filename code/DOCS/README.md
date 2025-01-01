# PAQUETES EL CLUB v3.1 - Sistema de Gestión de Paquetería

## 📋 Descripción
Sistema completo de gestión de paquetería desarrollado con FastAPI, PostgreSQL y Docker. Optimizado para manejar anuncios de paquetes, seguimiento y gestión de clientes.

## 🏗️ Estructura del Proyecto

```
code/
├── src/                    # Código fuente principal
│   ├── routers/           # Endpoints de la API
│   ├── models/            # Modelos de base de datos
│   ├── schemas/           # Esquemas de validación
│   ├── services/          # Lógica de negocio
│   ├── utils/             # Utilidades y helpers
│   └── dependencies.py    # Dependencias de la aplicación
├── templates/             # Plantillas HTML
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── database/              # Scripts de base de datos
├── alembic/               # Migraciones de base de datos
├── scripts/               # Scripts útiles para desarrollo
├── tests/                 # Tests y configuraciones de testing
├── docs/                  # Documentación del proyecto
├── uploads/               # Archivos subidos por usuarios
├── logs/                  # Logs de la aplicación
├── config/                # Configuraciones
├── nginx/                 # Configuración de Nginx
├── ssl/                   # Certificados SSL
├── monitoring/            # Configuración de monitoreo
├── docker-compose.yml     # Configuración de Docker Compose
├── Dockerfile             # Dockerfile para la aplicación
├── requirements.txt       # Dependencias de Python
└── alembic.ini           # Configuración de Alembic
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Docker y Docker Compose
- Python 3.8+
- PostgreSQL

### Configuración Rápida
```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd Paqueteria-v3.1

# 2. Configurar variables de entorno
cp code/env.example code/.env
# Editar code/.env con tus configuraciones

# 3. Iniciar servicios
cd code
docker-compose up -d

# 4. Ejecutar migraciones
docker-compose exec app alembic upgrade head
```

## 🌐 Acceso a la Aplicación

- **Aplicación Principal**: http://localhost
- **API Documentation**: http://localhost/docs
- **Health Check**: http://localhost/health

## 📊 Funcionalidades Principales

### 🔐 Autenticación
- Registro de usuarios
- Login con email/username
- Restablecimiento de contraseña
- Gestión de sesiones

### 📦 Gestión de Paquetes
- Anuncio de paquetes
- Seguimiento de paquetes
- Estados de paquetes (anunciado, recibido, entregado, cancelado)
- Cálculo automático de tarifas

### 👥 Gestión de Clientes
- Registro de clientes
- Historial de paquetes por cliente
- Información de contacto

### 📧 Notificaciones
- Sistema de notificaciones por email
- Notificaciones automáticas de cambios de estado

## 🛠️ Desarrollo

### Scripts Útiles
```bash
# Ejecutar tests
python code/tests/run_all_tests.py

# Crear backup de base de datos
bash code/scripts/create-backup.sh

# Test rápido del sistema
bash code/scripts/quick-test.sh
```

### Estructura de Testing
```
tests/
├── run_all_tests.py      # Ejecutor principal de tests
├── data/                 # Datos de prueba
├── results/              # Resultados de tests
├── reports/              # Reportes de testing
├── screenshots/          # Capturas de pantalla de tests
└── config/               # Configuraciones de testing
```

## 📚 Documentación

- **Guía de Deployment**: `docs/DEPLOYMENT-GUIDE.md`
- **README de Scripts**: `docs/README.md`
- **API Documentation**: http://localhost/docs

## 🔧 Configuración de Entorno

### Variables de Entorno Principales
```env
DATABASE_URL=postgresql://user:password@localhost:5432/paqueteria
SECRET_KEY=your-secret-key
DEBUG=True
ENVIRONMENT=development
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

## 📈 Monitoreo

- **Health Checks**: Endpoints automáticos de verificación
- **Logs**: Sistema de logging estructurado
- **Métricas**: Endpoints de métricas del sistema

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o preguntas sobre el proyecto, contacta al equipo de desarrollo.

---

**PAQUETES EL CLUB v3.1** - Sistema de gestión de paquetería optimizado y escalable.
