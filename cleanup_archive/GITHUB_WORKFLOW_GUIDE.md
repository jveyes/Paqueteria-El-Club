# 🐙 GUÍA COMPLETA: FLUJO DE TRABAJO CON GITHUB

## 🚀 **SINCRONIZACIÓN GITHUB ↔ AWS**

### **Scripts Disponibles**

1. **`github-sync-workflow.sh`** - Script principal para sincronización completa
2. **`aws-pull-from-github.sh`** - Script específico para pull desde GitHub en AWS
3. **`sync-to-aws.sh`** - Script original para sincronización manual

## 📋 **FLUJO DE TRABAJO RECOMENDADO**

### **Opción 1: Flujo Completo (Recomendado)**

```bash
# 1. Usar el script principal
./github-sync-workflow.sh

# Seleccionar opción 4: "🚀 Deploy automático (push + pull + restart en AWS)"
```

### **Opción 2: Flujo Manual**

```bash
# 1. Subir cambios a GitHub
./github-sync-workflow.sh
# Seleccionar opción 1: "📤 Subir cambios a GitHub (push)"

# 2. Bajar cambios en AWS
./aws-pull-from-github.sh
# Seleccionar opción 3: "🚀 Pull + Rebuild completo"
```

### **Opción 3: Flujo Rápido**

```bash
# 1. Push a GitHub
./github-sync-workflow.sh
# Opción 1: Push a develop

# 2. Pull en AWS
./aws-pull-from-github.sh
# Opción 2: Pull + Reiniciar contenedores
```

## 🔧 **CONFIGURACIÓN INICIAL**

### **1. Inicializar Repositorio Git**

```bash
# Ejecutar el script principal
./github-sync-workflow.sh

# Seleccionar opción 6: "🔧 Configurar repositorio remoto"
# Agregar la URL de tu repositorio GitHub
```

### **2. Crear Repositorio en GitHub**

1. Ve a https://github.com/new
2. Nombre: `paquetes-el-club-v3.1`
3. Descripción: `Sistema de gestión de paquetería para El Club`
4. Público o Privado según preferencia
5. **NO** inicializar con README (ya tienes uno)

### **3. Conectar Repositorio Local**

```bash
# En el script, seleccionar "Configurar repositorio remoto"
# Agregar: https://github.com/TU_USUARIO/paquetes-el-club-v3.1.git
```

## 📤 **SUBIR CAMBIOS A GITHUB**

### **Método 1: Script Interactivo**

```bash
./github-sync-workflow.sh
# Seleccionar opción 1: "📤 Subir cambios a GitHub (push)"
```

### **Método 2: Comandos Manuales**

```bash
# 1. Verificar cambios
git status

# 2. Agregar cambios
git add .

# 3. Crear commit
git commit -m "✨ feat: nueva funcionalidad"

# 4. Hacer push
git push origin develop
```

## 📥 **BAJAR CAMBIOS EN AWS**

### **Método 1: Script Interactivo**

```bash
./aws-pull-from-github.sh
# Seleccionar opción 3: "🚀 Pull + Rebuild completo"
```

### **Método 2: Comandos Manuales**

```bash
# Conectarse a AWS
papyrus

# Ir al directorio del proyecto
cd /home/ubuntu/Paquetes

# Hacer pull desde GitHub
git fetch origin
git reset --hard origin/develop

# Reiniciar contenedores
docker-compose down
docker-compose up -d --build
```

## 🎯 **FLUJO DE TRABAJO DIARIO**

### **Desarrollo de Nuevas Funcionalidades**

```bash
# 1. Crear nueva rama
git checkout develop
git pull origin develop
git checkout -b feature/nueva-funcionalidad

# 2. Desarrollar cambios
# ... hacer cambios en el código ...

# 3. Subir a GitHub
./github-sync-workflow.sh
# Opción 1: Push a la nueva rama

# 4. Crear Pull Request en GitHub
# Ir a GitHub y crear PR: feature/nueva-funcionalidad → develop

# 5. Después del merge, deploy en AWS
./aws-pull-from-github.sh
# Opción 3: Pull + Rebuild desde develop
```

### **Hotfixes Críticos**

```bash
# 1. Crear rama de hotfix
git checkout main
git pull origin main
git checkout -b hotfix/correccion-critica

# 2. Hacer la corrección
# ... corregir el problema ...

# 3. Deploy inmediato
./github-sync-workflow.sh
# Opción 4: Deploy automático a main
```

## 🔄 **SINCRONIZACIÓN AUTOMÁTICA**

### **Deploy Automático Completo**

```bash
./github-sync-workflow.sh
# Seleccionar opción 4: "🚀 Deploy automático"

# El script hará:
# 1. Commit de cambios locales
# 2. Push a GitHub
# 3. Pull en AWS
# 4. Rebuild de contenedores
# 5. Verificación de estado
```

### **Sincronización Completa**

```bash
./github-sync-workflow.sh
# Seleccionar opción 3: "🔄 Sincronización completa"

# El script hará:
# 1. Push a GitHub
# 2. Pull en AWS (sin reiniciar contenedores)
```

## 📊 **MONITOREO Y DEBUGGING**

### **Ver Estado del Repositorio**

```bash
# Local
./github-sync-workflow.sh
# Opción 5: "📋 Ver estado del repositorio"

# En AWS
./aws-pull-from-github.sh
# Opción 4: "📋 Ver estado del repositorio en AWS"
```

### **Ver Logs de Contenedores**

```bash
./aws-pull-from-github.sh
# Opción 5: "🔍 Ver logs de los contenedores"

# Opciones disponibles:
# - Aplicación (app)
# - Nginx
# - Redis
# - Celery Worker
# - Todos los contenedores
```

### **Limpieza Completa**

```bash
./aws-pull-from-github.sh
# Opción 6: "🧹 Limpiar y resetear completamente"

# ⚠️ ATENCIÓN: Esta operación es destructiva
# Elimina contenedores, imágenes y código actual
```

## 🌿 **ESTRUCTURA DE RAMAS**

### **Ramas Principales**

- **`main`** - Código de producción
- **`develop`** - Código en desarrollo

### **Ramas de Características**

- **`feature/nueva-funcionalidad`** - Nuevas funcionalidades
- **`feature/mejora-email`** - Mejoras en sistema de emails
- **`feature/optimizacion-db`** - Optimizaciones de base de datos

### **Ramas de Hotfix**

- **`hotfix/correccion-critica`** - Correcciones urgentes
- **`hotfix/seguridad`** - Parches de seguridad

### **Ramas de Release**

- **`release/v3.1.1`** - Preparación de releases
- **`release/v3.2.0`** - Nuevas versiones

## 📝 **CONVENCIONES DE COMMITS**

### **Tipos de Commits**

- **`feat`** - Nueva funcionalidad
- **`fix`** - Corrección de bug
- **`docs`** - Documentación
- **`style`** - Mejora de código
- **`refactor`** - Refactorización
- **`perf`** - Mejora de rendimiento
- **`test`** - Tests
- **`chore`** - Configuración

### **Ejemplos de Commits**

```bash
git commit -m "✨ feat: agregar sistema de reportes"
git commit -m "🐛 fix: corregir error en login"
git commit -m "📝 docs: actualizar README"
git commit -m "🎨 style: mejorar formato de código"
git commit -m "♻️ refactor: reorganizar estructura de archivos"
git commit -m "⚡ perf: optimizar consultas de base de datos"
git commit -m "🧪 test: agregar tests para autenticación"
git commit -m "🔧 chore: actualizar dependencias"
```

## 🔧 **CONFIGURACIÓN AVANZADA**

### **Git Hooks (Opcional)**

```bash
# Crear pre-commit hook para tests
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🧪 Ejecutando tests antes del commit..."
cd code
python -m pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "❌ Tests fallaron. Commit cancelado."
    exit 1
fi
echo "✅ Tests pasaron. Commit permitido."
EOF

chmod +x .git/hooks/pre-commit
```

### **Aliases de Git (Opcional)**

```bash
# Agregar aliases útiles
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Error: "No se puede conectar al servidor AWS"**

```bash
# Verificar conexión SSH
ssh -i ~/.ssh/PAPYRUS.pem ubuntu@18.214.124.14 "echo 'test'"

# Verificar clave SSH
ls -la ~/.ssh/PAPYRUS.pem

# Verificar permisos
chmod 600 ~/.ssh/PAPYRUS.pem
```

### **Error: "No se puede hacer push a GitHub"**

```bash
# Verificar remoto configurado
git remote -v

# Configurar remoto si no existe
git remote add origin https://github.com/TU_USUARIO/paquetes-el-club-v3.1.git

# Configurar credenciales si es necesario
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### **Error: "Conflictos en merge"**

```bash
# Ver conflictos
git status

# Resolver conflictos manualmente
# Editar archivos con conflictos

# Agregar archivos resueltos
git add .

# Continuar merge
git commit
```

### **Error: "Contenedores no inician"**

```bash
# Ver logs de contenedores
./aws-pull-from-github.sh
# Opción 5: Ver logs

# Verificar configuración
docker-compose config

# Rebuild completo
docker-compose down
docker-compose up -d --build
```

## 📋 **CHECKLIST DE DEPLOY**

### **Antes del Deploy**

- [ ] Tests pasan localmente
- [ ] Código revisado
- [ ] Commit con mensaje descriptivo
- [ ] Push a rama correcta

### **Durante el Deploy**

- [ ] Push exitoso a GitHub
- [ ] Pull exitoso en AWS
- [ ] Contenedores se reinician correctamente
- [ ] No hay errores en logs

### **Después del Deploy**

- [ ] Aplicación responde correctamente
- [ ] Funcionalidades críticas funcionan
- [ ] SSL/HTTPS funciona
- [ ] Base de datos conecta correctamente

## 🌐 **URLS ÚTILES**

- **🔗 Aplicación**: https://guia.papyrus.com.co
- **🔗 Health Check**: https://guia.papyrus.com.co/health
- **🔗 Login**: https://guia.papyrus.com.co/login
- **🔗 GitHub**: https://github.com/TU_USUARIO/paquetes-el-club-v3.1

---

**💡 CONSEJO**: Usa siempre el script `github-sync-workflow.sh` para operaciones normales y `aws-pull-from-github.sh` solo cuando necesites control específico sobre AWS.

**🚀 ¡Con estos scripts tienes un flujo de trabajo profesional y automatizado!**
