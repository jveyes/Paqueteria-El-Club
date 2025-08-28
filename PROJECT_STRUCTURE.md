# Estructura del Proyecto PAQUETES EL CLUB v3.1

## 📁 Estructura Principal

```
Paqueteria v3.1/
├── code/                          # 🎯 CÓDIGO PRINCIPAL DE LA APLICACIÓN
│   ├── src/                       # Código fuente Python
│   ├── templates/                 # Plantillas HTML
│   ├── static/                    # Archivos estáticos (CSS, JS, imágenes)
│   │   ├── images/                # Imágenes del proyecto
│   │   └── documents/             # Documentos (PDFs, etc.)
│   ├── database/                  # Configuración y migraciones de BD
│   │   ├── init/                  # Scripts de inicialización
│   │   └── database.sql           # Esquema de base de datos
│   ├── logs/                      # Logs de la aplicación
│   ├── uploads/                   # Archivos subidos por usuarios
│   ├── monitoring/                # Configuración de monitoreo
│   ├── SCRIPTS/                   # Scripts de desarrollo y testing
│   ├── TEST/                      # Tests automatizados
│   ├── ssl/                       # Certificados SSL
│   ├── nginx/                     # Configuración de Nginx
│   ├── alembic/                   # Migraciones de base de datos
│   ├── assets/                    # Assets adicionales
│   ├── admin/                     # Panel de administración
│   ├── public/                    # Archivos públicos
│   ├── requirements.txt           # Dependencias Python
│   ├── requirements-dev.txt       # Dependencias de desarrollo
│   ├── Dockerfile                 # Configuración Docker
│   ├── docker-compose.yml         # Configuración Docker Compose
│   ├── setup.sh                   # Script de configuración
│   ├── env.example                # Variables de entorno de ejemplo
│   ├── alembic.ini               # Configuración Alembic
│   ├── README.md                  # Documentación del código
│   ├── .cursorrules              # Reglas de Cursor
│   └── .gitignore                # Archivos ignorados por Git
│
├── docs/                          # 📚 DOCUMENTACIÓN DEL PROYECTO
│   ├── summaries/                 # Resúmenes de cambios
│   ├── solutions/                 # Soluciones a problemas
│   ├── API.md                     # Documentación de API
│   ├── DEPLOYMENT.md              # Guía de despliegue
│   ├── STRUCTURE.md               # Estructura del proyecto
│   ├── MIGRATION-SUMMARY.md       # Resumen de migraciones
│   ├── Sistema de Paquetería v3.0.md
│   ├── Diseno y Estilos v3.0.md
│   ├── CODIGOS_CON_ESTADOS.md
│   ├── ESTADOS_PAQUETES_CORREGIDOS.md
│   ├── USERS.md
│   ├── README-BASE-TEMPLATE.md    # Plantilla base para README
│   ├── DOCKER-IMAGE-README.md     # Documentación de imágenes Docker
│   └── [otros archivos de documentación]
│
├── backups/                       # 💾 BACKUPS DEL SISTEMA
│   ├── BACKUP_INFO.md
│   └── paqueteria_v31_backup_*.tar.gz
│
├── Proyecto/                      # 📁 CARPETA DEL PROYECTO
│
├── docker-images/                 # 🐳 IMÁGENES DOCKER
│   ├── paqueteria-club-v3.1.0-*.tar.gz
│   └── paqueteria-club-v3.1.0-*-INFO.md
│
├── .dockerignore                  # 🐳 Archivos ignorados por Docker
├── README.md                      # 📖 Documentación principal
├── CHANGELOG.md                   # 📝 Registro de cambios
├── CONTRIBUTING.md                # 🤝 Guía de contribución
├── LICENSE                        # ⚖️ Licencia del proyecto
├── GIT-WORKFLOW.md                # 🔄 Flujo de trabajo Git
├── PROJECT_STRUCTURE.md           # 📁 Este archivo
├── .gitignore                     # 🚫 Archivos ignorados por Git
└── [archivos de configuración adicionales]
```

## 🎯 Organización por Funcionalidad

### **Código de la Aplicación** (`code/`)
- **`src/`**: Lógica de negocio, modelos, rutas, configuraciones
- **`templates/`**: Plantillas HTML con Jinja2
- **`static/`**: Archivos estáticos (CSS, JS, imágenes, documentos)
- **`database/`**: Configuración de base de datos y migraciones
- **`logs/`**: Logs de la aplicación
- **`uploads/`**: Archivos subidos por usuarios
- **`monitoring/`**: Configuración de monitoreo (Prometheus, Grafana)
- **`SCRIPTS/`**: Scripts de desarrollo, testing y despliegue
- **`TEST/`**: Tests automatizados y configuraciones de testing

### **Documentación** (`docs/`)
- **`summaries/`**: Resúmenes de cambios y mejoras
- **`solutions/`**: Soluciones documentadas a problemas
- **`README-BASE-TEMPLATE.md`**: Plantilla base para README
- **`DOCKER-IMAGE-README.md`**: Documentación específica de Docker
- **Archivos MD**: Documentación técnica y de usuario

### **Infraestructura** (raíz)
- **`backups/`**: Backups automáticos del sistema
- **`docker-images/`**: Imágenes Docker del proyecto
- **`Proyecto/`**: Carpeta del proyecto

### **Docker** (`code/`)
- **`Dockerfile`**: Configuración de contenedores
- **`docker-compose.yml`**: Orquestación de servicios

## 🧹 Limpieza y Reubicación Realizada

### **Carpetas Eliminadas de la Raíz** (duplicadas en `code/`):
- ❌ `static/` → Usa `code/static/`
- ❌ `database/` → Usa `code/database/`
- ❌ `monitoring/` → Usa `code/monitoring/`
- ❌ `scripts/` → Usa `code/SCRIPTS/`
- ❌ `logs/` → Usa `code/logs/`
- ❌ `uploads/` → Usa `code/uploads/`
- ❌ `ssl/` → Usa `code/ssl/`
- ❌ `tests/` → Usa `code/TEST/`

### **Archivos Movidos**:
- ✅ `favicon-papyrus.png` → `code/static/images/`
- ✅ `TERMINOS Y CONDICIONES PAQUETES.pdf` → `code/static/documents/`
- ✅ `README-BASE-TEMPLATE.md` → `docs/`
- ✅ `DOCKER-IMAGE-README.md` → `docs/`
- ✅ `env.example` → `code/`
- ✅ `database.sql` → `code/database/`

### **Archivos Mantenidos en la Raíz**:
- ✅ `README.md` → Documentación principal del proyecto
- ✅ `LICENSE` → Licencia del proyecto
- ✅ `CHANGELOG.md` → Registro de cambios
- ✅ `CONTRIBUTING.md` → Guía de contribución
- ✅ `PROJECT_STRUCTURE.md` → Este archivo
- ✅ `GIT-WORKFLOW.md` → Flujo de trabajo Git
- ✅ `.gitignore` → Configuración Git
- ✅ `.dockerignore` → Configuración Docker

### **Archivos Movidos a `code/`**:
- ✅ `Dockerfile` → Configuración Docker
- ✅ `docker-compose.yml` → Orquestación Docker

## 📋 Beneficios de la Nueva Estructura

1. **🎯 Claridad**: Todo el código está en `code/`
2. **🚫 Sin Duplicación**: Eliminadas carpetas duplicadas
3. **📚 Documentación Separada**: `docs/` para documentación
4. **💾 Backups Organizados**: `backups/` para respaldos
5. **🐳 Docker Separado**: Imágenes en `docker-images/`
6. **🔧 Configuración Clara**: Archivos de configuración en la raíz
7. **📄 Documentos Accesibles**: PDFs en `code/static/documents/`

## 🚀 Próximos Pasos

1. **Verificar Referencias**: Asegurar que todas las rutas apunten a `code/`
2. **Actualizar Docker**: Verificar que `docker-compose.yml` use las rutas correctas
3. **Documentar Cambios**: Actualizar documentación de despliegue
4. **Testing**: Verificar que todo funcione correctamente
