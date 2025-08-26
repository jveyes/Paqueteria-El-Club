# 🌿 Git Workflow - Sistema de Paquetería EL CLUB

## 📋 **Estrategia de Ramas**

### **Ramas Principales:**

#### 🌟 **main** (Producción)
- **Propósito:** Código estable y listo para producción
- **Origen:** Merge desde `develop` cuando esté probado
- **Protección:** No commits directos, solo merges aprobados
- **Releases:** Tags de versiones estables

#### 🔄 **develop** (Desarrollo)
- **Propósito:** Integración de features y testing
- **Origen:** Rama principal de desarrollo
- **Protección:** Commits directos permitidos para desarrollo
- **Testing:** Ambiente de pruebas integrado

### **Ramas de Features:**

#### 🚀 **feature/nombre-feature**
- **Propósito:** Desarrollo de funcionalidades específicas
- **Origen:** Desde `develop`
- **Destino:** Merge a `develop` cuando esté completo
- **Ejemplos:**
  - `feature/user-authentication`
  - `feature/package-tracking`
  - `feature/payment-integration`

#### 🐛 **hotfix/nombre-fix**
- **Propósito:** Correcciones urgentes en producción
- **Origen:** Desde `main`
- **Destino:** Merge a `main` y `develop`
- **Ejemplos:**
  - `hotfix/security-patch`
  - `hotfix/critical-bug`

## 🔄 **Flujo de Trabajo**

### **1. Desarrollo de Features**

```bash
# 1. Asegurarse de estar en develop
git checkout develop
git pull origin develop

# 2. Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# 3. Desarrollar y hacer commits
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 4. Subir rama de feature
git push -u origin feature/nueva-funcionalidad

# 5. Crear Pull Request en GitHub
# 6. Code review y merge a develop
```

### **2. Integración a Develop**

```bash
# 1. Cambiar a develop
git checkout develop
git pull origin develop

# 2. Merge de feature
git merge feature/nueva-funcionalidad

# 3. Subir cambios
git push origin develop

# 4. Eliminar rama de feature (opcional)
git branch -d feature/nueva-funcionalidad
git push origin --delete feature/nueva-funcionalidad
```

### **3. Release a Producción**

```bash
# 1. Cuando develop esté estable
git checkout main
git pull origin main

# 2. Merge desde develop
git merge develop

# 3. Crear tag de versión
git tag -a v3.1.1 -m "Release v3.1.1 - Nueva funcionalidad"
git push origin v3.1.1

# 4. Subir a main
git push origin main
```

## 📝 **Convenciones de Commits**

### **Formato:**
```
tipo(alcance): descripción

[body opcional]

[footer opcional]
```

### **Tipos:**
- **feat:** Nueva funcionalidad
- **fix:** Corrección de bug
- **docs:** Documentación
- **style:** Formato de código
- **refactor:** Refactorización
- **test:** Tests
- **chore:** Tareas de mantenimiento

### **Ejemplos:**
```bash
git commit -m "feat(auth): implementar autenticación JWT"
git commit -m "fix(api): corregir endpoint de paquetes"
git commit -m "docs(readme): actualizar instrucciones de instalación"
git commit -m "refactor(database): optimizar consultas SQL"
```

## 🛡️ **Protección de Ramas**

### **main:**
- ✅ Requiere Pull Request
- ✅ Requiere aprobación de review
- ✅ Requiere que los tests pasen
- ✅ No permite commits directos

### **develop:**
- ✅ Requiere Pull Request para features
- ✅ Permite commits directos para desarrollo
- ✅ Requiere que los tests pasen

## 🔧 **Comandos Útiles**

### **Gestión de Ramas:**
```bash
# Ver todas las ramas
git branch -a

# Ver ramas locales
git branch

# Ver ramas remotas
git branch -r

# Cambiar de rama
git checkout nombre-rama

# Crear y cambiar a nueva rama
git checkout -b nueva-rama

# Eliminar rama local
git branch -d nombre-rama

# Eliminar rama remota
git push origin --delete nombre-rama
```

### **Estado y Logs:**
```bash
# Ver estado actual
git status

# Ver historial de commits
git log --oneline

# Ver historial gráfico
git log --oneline --graph --all

# Ver diferencias
git diff

# Ver diferencias entre ramas
git diff main..develop
```

### **Sincronización:**
```bash
# Actualizar rama local
git pull origin nombre-rama

# Subir cambios
git push origin nombre-rama

# Forzar push (usar con cuidado)
git push --force-with-lease origin nombre-rama
```

## 🚨 **Buenas Prácticas**

### **✅ Hacer:**
- Crear ramas de feature para cada funcionalidad
- Hacer commits pequeños y descriptivos
- Actualizar develop regularmente
- Hacer code review antes de merge
- Mantener main siempre estable

### **❌ Evitar:**
- Commits directos a main
- Commits grandes sin descripción
- Dejar ramas de feature sin merge
- Ignorar los tests
- Hacer merge sin revisar

## 📊 **Workflow Visual**

```
main     ●────────●────────●────────●
         │        │        │        │
develop  ●────────●────────●────────●
         │    │   │    │   │    │   │
feature1 ●────●   │    │   │    │   │
         │    │   │    │   │    │   │
feature2 ●────●───●    │   │    │   │
         │    │   │    │   │    │   │
feature3 ●────●───●────●   │    │   │
         │    │   │    │   │    │   │
hotfix   ●────●───●────●───●    │   │
```

## 🎯 **Próximos Pasos**

1. **Configurar protección de ramas** en GitHub
2. **Crear templates** para Pull Requests
3. **Configurar GitHub Actions** para CI/CD
4. **Establecer code review** guidelines
5. **Documentar** procesos específicos del equipo

---

**Última actualización:** Enero 2025  
**Versión:** 1.0  
**Mantenido por:** Equipo de Desarrollo EL CLUB
