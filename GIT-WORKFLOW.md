# 🌿 Git Workflow - Sistema de Paquetería EL CLUB

## 📋 **Estrategia de Ramas Simplificada**

### **Ramas Principales:**

#### 🌟 **main** (Producción)
- **Propósito:** Código estable y listo para producción
- **Origen:** Merge desde `develop` cuando esté probado
- **Protección:** No commits directos, solo merges aprobados
- **Releases:** Tags de versiones estables

#### 🔄 **develop** (Desarrollo)
- **Propósito:** Desarrollo activo y testing
- **Origen:** Rama principal de desarrollo
- **Protección:** Commits directos permitidos
- **Testing:** Ambiente de pruebas integrado

## 🔄 **Flujo de Trabajo Simplificado**

### **1. Desarrollo Diario**

```bash
# 1. Asegurarse de estar en develop
git checkout develop
git pull origin develop

# 2. Desarrollar y hacer commits directamente en develop
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 3. Subir cambios a develop
git push origin develop
```

### **2. Release a Producción**

```bash
# 1. Cuando develop esté estable y probado
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

### **3. Sincronización de Ramas**

```bash
# Después de un release, actualizar develop con main
git checkout develop
git pull origin main
git push origin develop
```

## 📝 **Convenciones de Commits**

### **Formato:**
```
tipo(alcance): descripción

[body opcional]
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
- ✅ Requiere Pull Request desde develop
- ✅ Requiere aprobación de review
- ✅ Requiere que los tests pasen
- ✅ No permite commits directos

### **develop:**
- ✅ Permite commits directos para desarrollo
- ✅ Requiere que los tests pasen
- ✅ Debe estar siempre actualizada

## 🔧 **Comandos Útiles**

### **Gestión de Ramas:**
```bash
# Ver todas las ramas
git branch -a

# Ver ramas locales
git branch

# Cambiar de rama
git checkout nombre-rama

# Ver estado actual
git status
```

### **Sincronización:**
```bash
# Actualizar develop
git checkout develop
git pull origin develop

# Actualizar main
git checkout main
git pull origin main

# Subir cambios
git push origin develop
git push origin main
```

### **Logs y Diferencias:**
```bash
# Ver historial de commits
git log --oneline

# Ver historial gráfico
git log --oneline --graph --all

# Ver diferencias entre ramas
git diff main..develop
```

## 🚨 **Buenas Prácticas**

### **✅ Hacer:**
- Desarrollar siempre en `develop`
- Hacer commits pequeños y descriptivos
- Probar antes de hacer merge a main
- Mantener main siempre estable
- Crear tags para releases

### **❌ Evitar:**
- Commits directos a main
- Commits grandes sin descripción
- Merge a main sin testing
- Ignorar los tests
- Dejar develop sin sincronizar

## 📊 **Workflow Visual Simplificado**

```
main     ●────────●────────●────────●
         │        │        │        │
develop  ●────────●────────●────────●
         │        │        │        │
         │        │        │        │
         │        │        │        │
         │        │        │        │
```

## 🎯 **Proceso de Release**

### **1. Preparación:**
```bash
# Asegurarse de que develop esté estable
git checkout develop
git pull origin develop
# Ejecutar tests y verificar funcionalidad
```

### **2. Release:**
```bash
# Merge a main
git checkout main
git pull origin main
git merge develop

# Crear tag
git tag -a v3.1.1 -m "Release v3.1.1"
git push origin v3.1.1
git push origin main
```

### **3. Post-Release:**
```bash
# Actualizar develop con main
git checkout develop
git pull origin main
git push origin develop
```

## 🔄 **Ciclo de Desarrollo**

1. **Desarrollo:** Trabajar en `develop`
2. **Testing:** Probar en `develop`
3. **Release:** Merge `develop` → `main`
4. **Tag:** Crear tag de versión
5. **Sync:** Actualizar `develop` con `main`

## 🎯 **Ventajas de este Flujo**

- ✅ **Simplicidad:** Solo 2 ramas principales
- ✅ **Velocidad:** Menos overhead de gestión
- ✅ **Claridad:** Flujo directo y fácil de entender
- ✅ **Eficiencia:** Ideal para equipos pequeños
- ✅ **Mantenimiento:** Fácil de mantener

---

**Última actualización:** Enero 2025  
**Versión:** 2.0 - Simplificado  
**Mantenido por:** Equipo de Desarrollo EL CLUB
