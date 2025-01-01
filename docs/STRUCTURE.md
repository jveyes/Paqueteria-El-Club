# Estructura del Proyecto PAQUETERIA EL CLUB v3.1

## 📁 Estructura de Directorios

```
paqueteria-v3.1/
├── 📄 .env                    # Variables de entorno (NO incluir en git)
├── 📄 env.example            # Template de variables de entorno
├── 📄 docker-compose.yml     # Configuración de contenedores
├── 📄 docker-compose.override.yml  # Configuración local
├── 📄 setup-structure.sh     # Script de configuración inicial
├── 📄 README.md              # Documentación principal
│
├── 📁 code/                  # Código fuente de la aplicación
│   ├── 📁 src/              # Código Python (FastAPI)
│   ├── 📁 templates/        # Templates HTML
│   ├── 📁 static/           # CSS, JS, imágenes
│   ├── 📁 nginx/            # Configuración de Nginx
│   ├── 📄 requirements.txt  # Dependencias Python
│   └── 📄 Dockerfile        # Configuración de imagen
│
├── 📁 uploads/              # Archivos subidos por usuarios
│   ├── 📁 documents/        # Documentos
│   └── 📁 images/           # Imágenes
│
├── 📁 logs/                 # Logs del sistema
│   ├── 📁 app/              # Logs de la aplicación
│   ├── 📁 nginx/            # Logs del servidor web
│   └── 📁 postgres/         # Logs de base de datos
│
├── 📁 database/             # Base de datos y migraciones
│   ├── 📁 init/             # Scripts de inicialización
│   ├── 📁 backups/          # Backups automáticos
│   └── 📁 migrations/       # Migraciones Alembic
│
├── 📁 scripts/              # Scripts de automatización
│   ├── 📄 backup.sh         # Script de backup
│   ├── 📄 restore.sh        # Script de restauración
│   ├── 📄 deploy.sh         # Script de deployment
│   └── 📄 health-check.sh   # Script de verificación
│
├── 📁 tests/                # Tests automatizados
│   ├── 📄 test_api.py       # Tests de API
│   └── 📄 test_database.py  # Tests de base de datos
│
├── 📁 docs/                 # Documentación
│   ├── 📄 README.md         # Documentación principal
│   ├── 📄 DEPLOYMENT.md     # Guía de deployment
│   ├── 📄 API.md           # Documentación de API
│   └── 📄 STRUCTURE.md     # Este archivo
│
├── 📁 monitoring/           # Configuración de monitoreo
│   ├── 📄 prometheus.yml    # Configuración de Prometheus
│   └── 📁 grafana/          # Dashboards de Grafana
│
└── 📁 ssl/                  # Certificados SSL
```

## 🚀 Configuración Inicial

### 1. Crear estructura de directorios
```bash
chmod +x setup-structure.sh
./setup-structure.sh
```

### 2. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus valores
```

### 3. Iniciar servicios
```bash
docker-compose up -d
```

### 4. Verificar estado
```bash
./scripts/health-check.sh
```

## 📋 Volúmenes Configurados

### Volúmenes de Desarrollo
- `./code:/app/code` - Código fuente completo
- `./uploads:/app/uploads` - Archivos de usuario
- `./logs:/app/logs` - Logs del sistema
- `./database:/app/database` - Base de datos y backups

### Volúmenes de Configuración
- `./scripts:/app/scripts` - Scripts de automatización
- `./tests:/app/tests` - Tests automatizados
- `./docs:/app/docs` - Documentación
- `./monitoring:/app/monitoring` - Configuración de monitoreo

## 🔧 Scripts Disponibles

### Backup y Restauración
```bash
# Crear backup
./scripts/backup.sh

# Restaurar backup
./scripts/restore.sh <archivo_backup>
```

### Monitoreo
```bash
# Verificar estado de servicios
./scripts/health-check.sh

# Ver logs en tiempo real
docker-compose logs -f app
```

### Deployment
```bash
# Desplegar aplicación
./scripts/deploy.sh

# Reiniciar servicios
docker-compose restart
```

## 🌐 URLs de Acceso

- **Aplicación Principal**: http://localhost
- **API**: http://localhost:8001
- **Documentación API**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

## 📝 Logs

### Ubicación de Logs
- **Aplicación**: `logs/app/app.log`
- **Nginx**: `logs/nginx/access.log` y `logs/nginx/error.log`
- **PostgreSQL**: `logs/postgres/postgres.log`

### Ver Logs en Tiempo Real
```bash
# Logs de la aplicación
tail -f logs/app/app.log

# Logs de todos los servicios
docker-compose logs -f
```

## 🔒 Seguridad

### Archivos Sensibles
- `.env` - NO incluir en control de versiones
- `ssl/` - Certificados SSL
- `database/backups/` - Backups de base de datos

### Permisos Recomendados
```bash
chmod 600 .env
chmod 700 database/backups
chmod 755 uploads
```

## 🚨 Troubleshooting

### Problemas Comunes

1. **Puerto 8001 ocupado**
   ```bash
   sudo lsof -i :8001
   sudo kill -9 <PID>
   ```

2. **Base de datos no conecta**
   ```bash
   docker-compose restart postgres
   ./scripts/health-check.sh
   ```

3. **Logs de error**
   ```bash
   docker-compose logs app | grep ERROR
   ```

### Comandos Útiles
```bash
# Reiniciar todos los servicios
docker-compose down && docker-compose up -d

# Ver estado de contenedores
docker-compose ps

# Limpiar contenedores no utilizados
docker system prune -f
```

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs: `./scripts/health-check.sh`
2. Verificar configuración: `docker-compose config`
3. Revisar documentación en `docs/`
