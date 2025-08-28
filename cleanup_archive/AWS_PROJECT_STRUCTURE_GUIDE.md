# 🚀 GUÍA COMPLETA: ESTRUCTURA DEL PROYECTO EN AWS Y SINCRONIZACIÓN

## 📍 **UBICACIÓN DEL PROYECTO EN AWS**

```
/home/ubuntu/Paquetes/
```

## 🏗️ **ESTRUCTURA COMPLETA DEL PROYECTO**

```
/home/ubuntu/Paquetes/
├── 📄 ARCHIVOS PRINCIPALES
│   ├── .env                          # Variables de entorno
│   ├── docker-compose.yml            # Configuración de contenedores
│   ├── Dockerfile                    # Imagen de la aplicación
│   ├── requirements.txt              # Dependencias Python
│   └── README.md                     # Documentación
│
├── 🐳 CONFIGURACIÓN DOCKER
│   ├── docker-compose-aws.yml        # Backup configuración AWS
│   ├── docker-compose-nginx.yml      # Solo Nginx
│   └── ssl-renew.sh                  # Renovación SSL
│
├── 🌐 NGINX
│   ├── nginx/
│   │   └── conf.d/
│   │       └── paqueteria.conf       # Configuración del servidor
│   └── ssl/
│       ├── cert.pem                  # Certificado SSL
│       └── key.pem                   # Clave privada SSL
│
├── 📁 CÓDIGO DE LA APLICACIÓN
│   ├── src/                          # Código fuente principal
│   │   ├── main.py                   # Punto de entrada
│   │   ├── config.py                 # Configuración
│   │   ├── models/                   # Modelos de base de datos
│   │   ├── routers/                  # Rutas de la API
│   │   ├── schemas/                  # Esquemas de datos
│   │   ├── services/                 # Lógica de negocio
│   │   └── utils/                    # Utilidades
│   ├── templates/                    # Plantillas HTML
│   ├── static/                       # Archivos estáticos
│   └── assets/                       # Recursos (CSS, JS, imágenes)
│
├── 📊 BASE DE DATOS
│   ├── database/                     # Scripts de base de datos
│   ├── alembic/                      # Migraciones
│   └── migration_backup/             # Backups de migración
│
├── 📁 VOLÚMENES Y DATOS
│   ├── uploads/                      # Archivos subidos por usuarios
│   ├── logs/                         # Logs de la aplicación
│   ├── static/                       # Archivos estáticos servidos
│   └── Volumenes/                    # Volúmenes adicionales
│
├── 🧪 SCRIPTS DE PRUEBA Y MIGRACIÓN
│   ├── test_email_send.py            # Prueba de emails
│   ├── test_password_reset.py        # Prueba de restablecimiento
│   ├── setup_smtp_test.py            # Configuración SMTP
│   ├── verify_rds_data.py            # Verificación de datos
│   └── [otros scripts de migración]
│
└── 📚 DOCUMENTACIÓN
    ├── EMAIL_SETUP_SUMMARY.md        # Configuración de emails
    └── README.md                     # Documentación general
```

## 🔧 **ARCHIVOS CLAVE PARA MODIFICACIONES**

### **1. Configuración Principal**
- **`.env`** - Variables de entorno (SMTP, base de datos, etc.)
- **`docker-compose.yml`** - Configuración de contenedores
- **`Dockerfile`** - Construcción de la imagen

### **2. Aplicación Web**
- **`src/main.py`** - Punto de entrada de la aplicación
- **`src/routers/`** - Rutas y endpoints de la API
- **`src/models/`** - Modelos de base de datos
- **`templates/`** - Plantillas HTML
- **`static/`** - CSS, JavaScript, imágenes

### **3. Servidor Web**
- **`nginx/conf.d/paqueteria.conf`** - Configuración de Nginx
- **`ssl/`** - Certificados SSL

## 🐙 **FLUJO DE TRABAJO CON GITHUB**

### **Configuración Inicial del Repositorio**

```bash
# 1. Inicializar repositorio Git local
cd /home/stk/Insync/dispapyrussas@gmail.com/Google\ Drive/PAPYRUS/EL\ CLUB/SERVICIO\ DE\ PAQUETERIA/Paqueteria\ v3.1/
git init

# 2. Crear .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.production
.env.staging

# Docker
.dockerignore

# Logs
logs/
*.log

# Database
*.db
*.sqlite3

# SSL Certificates
ssl/
*.pem
*.key
*.crt

# Uploads
uploads/
!uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# AWS
*.pem
backup-*.tar.gz

# Temporary files
*.tmp
*.temp
EOF

# 3. Agregar archivos al repositorio
git add .
git commit -m "🎉 Initial commit: Paquetes El Club v3.1"

# 4. Crear repositorio en GitHub (manual)
# Ir a https://github.com/new
# Nombre: paquetes-el-club-v3.1
# Descripción: Sistema de gestión de paquetería para El Club
# Público o Privado según preferencia

# 5. Conectar repositorio local con GitHub
git remote add origin https://github.com/TU_USUARIO/paquetes-el-club-v3.1.git
git branch -M main
git push -u origin main
```

### **Estructura de Ramas (Git Flow)**

```bash
# Rama principal
main                    # Código de producción
develop                 # Código en desarrollo

# Ramas de características
feature/nueva-funcionalidad
feature/mejora-email
feature/optimizacion-db

# Ramas de hotfix
hotfix/correccion-critica
hotfix/seguridad

# Ramas de release
release/v3.1.1
release/v3.2.0
```

### **Flujo de Trabajo Diario**

```bash
# 1. Crear nueva rama para feature
git checkout develop
git pull origin develop
git checkout -b feature/nueva-funcionalidad

# 2. Desarrollar cambios
# ... hacer cambios en el código ...

# 3. Commit de cambios
git add .
git commit -m "✨ feat: agregar nueva funcionalidad de reportes

- Agregar endpoint /api/reports
- Crear plantilla reports.html
- Implementar lógica de generación de reportes
- Agregar tests unitarios"

# 4. Push a GitHub
git push origin feature/nueva-funcionalidad

# 5. Crear Pull Request en GitHub
# Ir a https://github.com/TU_USUARIO/paquetes-el-club-v3.1/pulls
# Crear nuevo PR: feature/nueva-funcionalidad → develop
```

### **Configuración de GitHub Actions (CI/CD)**

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r code/requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        SECRET_KEY: test-secret-key
      run: |
        cd code
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./code/coverage.xml

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to AWS Staging
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.AWS_HOST }}
        username: ${{ secrets.AWS_USERNAME }}
        key: ${{ secrets.AWS_SSH_KEY }}
        script: |
          cd /home/ubuntu/Paquetes
          git pull origin develop
          docker-compose down
          docker-compose up -d --build
          echo "✅ Staging deployment completed"

  deploy-production:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to AWS Production
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.AWS_HOST }}
        username: ${{ secrets.AWS_USERNAME }}
        key: ${{ secrets.AWS_SSH_KEY }}
        script: |
          cd /home/ubuntu/Paquetes
          git pull origin main
          docker-compose down
          docker-compose up -d --build
          echo "🚀 Production deployment completed"
```

### **Configuración de Secrets en GitHub**

```bash
# En GitHub: Settings → Secrets and variables → Actions
# Agregar los siguientes secrets:

AWS_HOST=18.214.124.14
AWS_USERNAME=ubuntu
AWS_SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----
[contenido de tu clave SSH]
-----END OPENSSH PRIVATE KEY-----

# Variables de entorno para tests
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/test_db
SECRET_KEY=test-secret-key-for-ci
```

### **Script de Sincronización con GitHub**

```bash
#!/bin/bash
# sync-github-aws.sh

echo "🔄 ========================================"
echo "🔄 SINCRONIZACIÓN GITHUB → AWS"
echo "🔄 PAQUETES EL CLUB v3.1"
echo "🔄 ========================================"

# Configuración
AWS_HOST="18.214.124.14"
AWS_PATH="/home/ubuntu/Paquetes"
SSH_KEY="~/.ssh/PAPYRUS.pem"
BRANCH=${1:-main}

echo "📋 Sincronizando rama: $BRANCH"

# Crear backup en AWS
echo "📦 Creando backup en AWS..."
ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && tar -czf backup-$(date +%Y%m%d_%H%M%S).tar.gz ."

# Sincronizar desde GitHub
echo "📥 Descargando código desde GitHub..."
ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && git fetch origin && git reset --hard origin/$BRANCH"

# Reiniciar contenedores
echo "🐳 Reiniciando contenedores..."
ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && docker-compose down && docker-compose up -d --build"

echo "✅ Sincronización completada"
```

## 🔄 **SINCRONIZACIÓN: LOCAL → AWS**

### **Método 1: SCP (Transferencia Manual)**

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

### **Método 2: Sincronización Selectiva**

```bash
# Sincronizar solo archivos específicos
scp -i ~/.ssh/PAPYRUS.pem \
    src/main.py \
    src/routers/auth.py \
    templates/login.html \
    ubuntu@18.214.124.14:/home/ubuntu/Paquetes/

# Reiniciar solo la aplicación
papyrus
docker restart paqueteria_v31_app
```

### **Método 3: Script de Sincronización Automática**

```bash
#!/bin/bash
# sync-to-aws.sh

LOCAL_PATH="/ruta/local/del/proyecto/code"
AWS_PATH="/home/ubuntu/Paquetes"
AWS_HOST="18.214.124.14"
SSH_KEY="~/.ssh/PAPYRUS.pem"

echo "🔄 Sincronizando con AWS..."

# Crear backup en AWS
ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && tar -czf backup-$(date +%Y%m%d_%H%M%S).tar.gz ."

# Transferir archivos
rsync -avz --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' \
    -e "ssh -i $SSH_KEY" \
    $LOCAL_PATH/ ubuntu@$AWS_HOST:$AWS_PATH/

# Reiniciar contenedores
ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && docker-compose down && docker-compose up -d --build"

echo "✅ Sincronización completada"
```

### **Método 4: Sincronización con GitHub (Recomendado)**

```bash
# 1. Commit y push a GitHub
git add .
git commit -m "✨ feat: nueva funcionalidad"
git push origin develop

# 2. Crear Pull Request en GitHub
# Ir a GitHub y crear PR: develop → main

# 3. Merge en main (después de review)
git checkout main
git pull origin main

# 4. Sincronizar AWS desde GitHub
./sync-github-aws.sh main
```

## 🔄 **SINCRONIZACIÓN: AWS → LOCAL**

### **Descargar Cambios desde AWS**

```bash
# Descargar todo el proyecto
scp -i ~/.ssh/PAPYRUS.pem -r ubuntu@18.214.124.14:/home/ubuntu/Paquetes/ ./aws-backup/

# Descargar archivos específicos
scp -i ~/.ssh/PAPYRUS.pem \
    ubuntu@18.214.124.14:/home/ubuntu/Paquetes/src/main.py \
    ubuntu@18.214.124.14:/home/ubuntu/Paquetes/.env \
    ./
```

### **Sincronización desde GitHub**

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/paquetes-el-club-v3.1.git
cd paquetes-el-club-v3.1

# Cambiar a rama específica
git checkout develop
git pull origin develop
```

## 🛠️ **MODIFICACIONES COMUNES Y UBICACIONES**

### **1. Cambiar Configuración de Email**
```bash
# En AWS
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

### **5. Modificar Base de Datos**
```bash
# Crear migración local
alembic revision --autogenerate -m "description"
alembic upgrade head

# Transferir migración a AWS
scp -i ~/.ssh/PAPYRUS.pem alembic/versions/xxx_migration.py ubuntu@18.214.124.14:/home/ubuntu/Paquetes/alembic/versions/
papyrus
cd /home/ubuntu/Paquetes
docker exec paqueteria_v31_app alembic upgrade head
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

### **Comandos Git Útiles**
```bash
# Ver estado del repositorio
git status

# Ver historial de commits
git log --oneline -10

# Ver diferencias
git diff

# Crear nueva rama
git checkout -b feature/nueva-funcionalidad

# Cambiar de rama
git checkout develop

# Merge de ramas
git merge feature/nueva-funcionalidad

# Rebase para mantener historial limpio
git rebase develop
```

## 📋 **CHECKLIST DE SINCRONIZACIÓN**

### **Antes de Sincronizar**
- [ ] Hacer backup del código actual en AWS
- [ ] Verificar que los cambios locales funcionan
- [ ] Actualizar versiones en requirements.txt si es necesario
- [ ] Ejecutar tests localmente
- [ ] Commit y push a GitHub

### **Durante la Sincronización**
- [ ] Transferir archivos modificados
- [ ] Verificar permisos de archivos
- [ ] Reiniciar contenedores necesarios
- [ ] Verificar que CI/CD pipeline pasa

### **Después de Sincronizar**
- [ ] Verificar que la aplicación funciona
- [ ] Revisar logs por errores
- [ ] Probar funcionalidades críticas
- [ ] Verificar que SSL sigue funcionando
- [ ] Actualizar documentación si es necesario

## 🌐 **URLS IMPORTANTES**

- **Aplicación**: https://guia.papyrus.com.co
- **Health Check**: https://guia.papyrus.com.co/health
- **Login**: https://guia.papyrus.com.co/login
- **Admin**: https://guia.papyrus.com.co/admin
- **GitHub**: https://github.com/TU_USUARIO/paquetes-el-club-v3.1

## 🎯 **FLUJO DE TRABAJO RECOMENDADO**

### **Desarrollo de Nuevas Funcionalidades**
1. **Crear rama**: `git checkout -b feature/nueva-funcionalidad`
2. **Desarrollar**: Hacer cambios en el código
3. **Testear**: Ejecutar tests localmente
4. **Commit**: `git commit -m "✨ feat: descripción"`
5. **Push**: `git push origin feature/nueva-funcionalidad`
6. **Pull Request**: Crear PR en GitHub
7. **Review**: Revisar código y tests
8. **Merge**: Merge a develop
9. **Deploy**: CI/CD despliega automáticamente

### **Hotfixes Críticos**
1. **Crear rama**: `git checkout -b hotfix/correccion-critica`
2. **Corregir**: Hacer la corrección
3. **Testear**: Verificar que funciona
4. **Commit**: `git commit -m "🐛 fix: descripción del fix"`
5. **Push**: `git push origin hotfix/correccion-critica`
6. **Merge**: Merge directo a main
7. **Deploy**: Despliegue automático a producción

---

**💡 CONSEJO**: Siempre haz un backup antes de sincronizar cambios importantes y prueba en un entorno de desarrollo antes de subir a producción.

**🚀 CON GITHUB**: Ahora tienes control de versiones profesional, CI/CD automático y un flujo de trabajo robusto para el desarrollo colaborativo.
