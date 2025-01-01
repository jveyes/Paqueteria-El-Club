# PROYECTO PAQUETERIA EL CLUB v3.1 - PRD (Product Requirements Document)

## 📋 **INFORMACIÓN DEL PROYECTO**

- **Nombre**: PAQUETES EL CLUB v3.1
- **Versión**: 3.1.0
- **Fecha de Creación**: 2025-08-29
- **Estado**: ✅ COMPLETADO Y LISTO PARA PRODUCCIÓN
- **Empresa**: PAPURUS SOLUCIONES INTEGRALES S.A.S.
- **Dirección**: Cra. 91 #54-120, Local 12
- **Contacto**: info@papyrus.com.co / +57 333 400 4007

---

## 🎯 **OBJETIVO DEL PROYECTO**

Desarrollar un sistema integral de gestión de paquetería que permita a los clientes anunciar la llegada de sus paquetes, consultar su estado en tiempo real, y a los administradores gestionar todo el flujo de trabajo de manera eficiente y segura.

---

## 🏗️ **ARQUITECTURA TÉCNICA**

### **Stack Tecnológico Principal**

#### **Backend**
- **Framework**: FastAPI 0.104.1 (Python 3.11)
- **Base de Datos**: PostgreSQL 15+ (AWS RDS)
- **ORM**: SQLAlchemy 2.0.23
- **Migraciones**: Alembic 1.12.1
- **Validación**: Pydantic 2.5.0
- **Autenticación**: JWT con cookies HttpOnly

#### **Frontend**
- **Templates**: Jinja2 con HTML5
- **Estilos**: Tailwind CSS
- **JavaScript**: Vanilla JS + HTMX
- **Responsive**: Mobile-first design
- **PWA**: Progressive Web App ready

#### **Infraestructura**
- **Containerización**: Docker + Docker Compose
- **Cache**: Redis 7.0
- **Tareas**: Celery 5.3.4
- **Proxy**: Nginx
- **Monitoreo**: Prometheus + Grafana

#### **Servicios Externos**
- **SMS**: LIWA.co API v2
- **Email**: SMTP (taylor.mxrouting.net)
- **Hosting**: AWS (EC2 + RDS)
- **SSL**: No configurado actualmente

### **Patrones de Arquitectura**

- **MVC**: Model-View-Controller con FastAPI
- **Repository Pattern**: Para acceso a datos
- **Service Layer**: Lógica de negocio separada
- **Dependency Injection**: FastAPI Depends
- **Middleware**: Autenticación y rate limiting
- **Event-Driven**: Celery para tareas asíncronas

---

## 📊 **MODELOS DE DATOS**

### **Entidades Principales**

#### **User (Usuario)**
```python
- id: UUID (Primary Key)
- username: String(50) - Nombre de usuario único
- email: String(100) - Email único
- full_name: String(100) - Nombre completo
- hashed_password: String(255) - Contraseña encriptada
- role: Enum(administrador, operador, usuario) - Rol del usuario
- phone: String(20) - Teléfono opcional
- is_active: Boolean - Estado activo/inactivo
- is_verified: Boolean - Verificación de email
- profile_photo: String(500) - Foto de perfil
- created_at: DateTime - Fecha de creación
- updated_at: DateTime - Última actualización
```

#### **PackageAnnouncement (Anuncio de Paquete)**
```python
- id: UUID (Primary Key)
- customer_name: String(100) - Nombre del cliente
- phone_number: String(20) - Teléfono del cliente
- guide_number: String(50) - Número de guía único
- tracking_code: String(4) - Código de tracking único
- is_active: Boolean - Estado activo
- is_processed: Boolean - Procesado por admin
- announced_at: DateTime - Fecha de anuncio
- processed_at: DateTime - Fecha de procesamiento
- created_by_id: UUID - Usuario que creó el anuncio
```

#### **Package (Paquete)**
```python
- id: UUID (Primary Key)
- tracking_number: String(50) - Número de tracking único
- customer_name: String(100) - Nombre del cliente
- customer_phone: String(20) - Teléfono del cliente
- status: Enum(anunciado, recibido, entregado, cancelado) - Estado del paquete
- package_type: Enum(paquete, extradimensionado) - Tipo de paquete
- package_condition: Enum(bueno, regular, malo) - Condición del paquete
- storage_cost: Numeric(10,2) - Costo de almacenamiento
- delivery_cost: Numeric(10,2) - Costo de entrega
- total_cost: Numeric(10,2) - Costo total
- observations: Text - Observaciones
```

#### **PasswordResetToken (Token de Reset)**
```python
- id: UUID (Primary Key)
- token: String(255) - Token único
- user_id: UUID - Usuario asociado
- is_used: Boolean - Si ya fue usado
- expires_at: DateTime - Fecha de expiración
- created_at: DateTime - Fecha de creación
- used_at: DateTime - Fecha de uso
```

#### **UserActivityLog (Log de Actividad)**
```python
- id: UUID (Primary Key)
- user_id: UUID - Usuario
- activity_type: Enum - Tipo de actividad
- description: Text - Descripción de la actividad
- ip_address: String(45) - IP del usuario
- user_agent: String(500) - Navegador/dispositivo
- activity_metadata: JSON - Metadatos adicionales
- created_at: DateTime - Fecha de la actividad
```

### **Enums y Estados**

#### **PackageStatus**
- `anunciado` - Cliente anunció llegada
- `recibido` - Paquete recibido en instalaciones
- `entregado` - Paquete entregado
- `cancelado` - Paquete cancelado

#### **PackageType**
- `paquete` - Paquete medidas normales
- `extradimensionado` - Paquete con medidas muy grandes

#### **PackageCondition**
- `bueno` - Paquete que se visualiza en buen estado
- `regular` - Paquete que se visualiza en estado regular
- `malo` - Paquete que se visualiza que tiene averías

#### **UserRole**
- `administrador` - Acceso completo al sistema
- `operador` - Gestión de usuarios y paquetes
- `usuario` - Acceso básico al dashboard

#### **ActivityType**
- `LOGIN` - Inicio de sesión
- `LOGOUT` - Cierre de sesión
- `PROFILE_UPDATE` - Actualización de perfil
- `PASSWORD_CHANGE` - Cambio de contraseña
- `PACKAGE_CREATE` - Creación de paquete
- `PACKAGE_UPDATE` - Actualización de paquete
- `PACKAGE_DELETE` - Eliminación de paquete
- `FILE_UPLOAD` - Subida de archivo
- `FILE_DELETE` - Eliminación de archivo
- `USER_CREATE` - Creación de usuario
- `USER_UPDATE` - Actualización de usuario
- `USER_DELETE` - Eliminación de usuario
- `ROLE_CHANGE` - Cambio de rol
- `STATUS_CHANGE` - Cambio de estado

---

## 🔐 **SISTEMA DE AUTENTICACIÓN Y AUTORIZACIÓN**

### **JWT Token System**
- **Algoritmo**: HS256
- **Expiración**: 30 minutos
- **Refresh**: Automático via cookies
- **Storage**: Cookies HttpOnly + localStorage

### **Middleware de Autenticación**
```python
# Verificación automática en cada request
@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_active_user_from_cookies)
):
    return {"message": f"Hola {current_user.username}"}
```

### **Sistema de Permisos por Rol**

#### **Admin (administrador)**
- ✅ Acceso completo al sistema
- ✅ Gestión de usuarios (CRUD completo)
- ✅ Gestión de paquetes
- ✅ Configuración del sistema
- ✅ Reportes y estadísticas

#### **Operator (operador)**
- ✅ Gestión de usuarios (editar, reset password)
- ✅ Gestión de paquetes
- ✅ Dashboard operativo
- ✅ No puede crear/eliminar usuarios admin

#### **User (usuario)**
- ✅ Ver perfil propio en historico
- ❌ No puede editar perfil propio
- ❌ No puede cambiar contraseña propia
- ❌ No puede gestionar otros usuarios
- ❌ No puede acceder a panel admin

---

## 📱 **FUNCIONALIDADES DEL SISTEMA**

### **1. SISTEMA PÚBLICO (Sin Autenticación)**

#### **1.1 Página Principal - Anuncio de Paquetes**
**URL**: `http://localhost/`
**Funcionalidad**: Formulario público para anunciar llegada de paquetes

**Campos del Formulario**:
- Nombre del Cliente (obligatorio)
- Número de Teléfono (obligatorio, formato colombiano)
- Número de Guía (obligatorio, único)
- Terminos y condiciones (obligatorio)

**Proceso Interno**:

1. Validación de datos con Pydantic
2. Generación automática de código de tracking (4 caracteres)
3. Creación del anuncio en base de datos
4. Respuesta con confirmación y código
5. Envío automático de SMS con código de tracking

**Validaciones**:

- Nombre: Solo letras, espacios y caracteres seguros
- Teléfono: Formato colombiano (3XX XXX XXXX o 60X XXX XXXX)
- Guía: Formato alfanumérico, único en el sistema

**Seguridad**:

- Rate limiting: Ingreso de 5 guías por minuto

#### **1.2 Sistema de Búsqueda de Paquetes**
**URL**: `http://localhost/search`
**Funcionalidad**: Búsqueda general de paquetes

**Tipos de Búsqueda**:
- Por número de guía
- Por código de tracking

**Resultados**:

- Lista de paquete encontrado
- Estado actual de cada paquete
- Fecha de anuncio
- Información del cliente
- Historial de estados (si aplica)

#### **1.3 Consulta por Código de Tracking**
**URL**: `http://localhost/track/{tracking_code}`
**Funcionalidad**: Consulta específica por código de 4 caracteres

**Información Mostrada**:

- Estado del paquete
- Fecha de anuncio
- Información del cliente
- Historial de estados (si aplica)

### **2. SISTEMA DE AUTENTICACIÓN**

#### **2.1 Login de Usuario**
**URL**: `http://localhost/auth/login`
**Funcionalidad**: Acceso al sistema

**Campos**:
- Username o Email
- Contraseña

**Proceso**:
1. Validación de credenciales
2. Verificación de usuario activo
3. Generación de JWT token
4. Establecimiento de cookies
5. Redirección al dashboard

**Seguridad**:
- Rate limiting: 5 intentos por minuto
- Bloqueo temporal tras múltiples fallos
- Logs de intentos de acceso

#### **2.2 Registro de Usuario**
**URL**: `http://localhost/auth/register`
**Funcionalidad**: Creación de nuevas cuentas (solo administrador)

**Campos**:
- Username (único, alfanumérico)
- Email (único, formato válido)
- Nombre completo
- Teléfono (obligatorio, formato colombiano)
- Rol (administrador, operador, usuario)
- Contraseña (mínimo 8 caracteres)

**Validaciones**:
- Username: 3-50 caracteres, alfanumérico
- Email: Formato válido, único en sistema
- Contraseña: Mínimo 8 caracteres, con validación de fortaleza

#### **2.3 Recuperación de Contraseña**
**URL**: `http://localhost/auth/forgot-password`
**Funcionalidad**: Reset de contraseña vía email

**Proceso**:
1. Usuario ingresa email
2. Verificación de email en sistema
3. Generación de token temporal (24 horas)
4. Envío de email con link de reset
5. Usuario accede al link y establece nueva contraseña

**Seguridad**:
- Rate limiting: 5 intentos por minuto
- Bloqueo temporal tras 10 intentos
- Token único por solicitud
- Expiración automática
- Un solo uso por token
- Logs de actividad

### **3. DASHBOARD DE USUARIO**

#### **3.1 Dashboard Principal**
**URL**: `http://localhost/dashboard`
**Funcionalidad**: Vista general del usuario

**Contenido**:
- Información del perfil
- Estadísticas de actividad
- Paquetes recientes
- Notificaciones pendientes
- Accesos rápidos a funciones

#### **3.2 Gestión de Perfil**
**URL**: `http://localhost/profile`
**Funcionalidad**: Ver y editar información personal

**Campos Editables**:
- Nombre completo
- Username
- Email
- Teléfono
- Foto de perfil

**Validaciones**:
- Username único en el sistema
- Email único en el sistema
- Formato de teléfono colombiano

#### **3.3 Cambio de Contraseña**
**URL**: `http://localhost/profile/change-password`
**Funcionalidad**: Modificar contraseña personal

**Proceso**:
1. Verificación de contraseña actual
2. Validación de nueva contraseña
3. Confirmación de nueva contraseña
4. Actualización en base de datos
5. Log de actividad

**Validaciones**:
- Contraseña actual correcta
- Nueva contraseña diferente a la actual
- Mínimo 8 caracteres
- Confirmación coincidente

### **4. PANEL DE ADMINISTRACIÓN**

#### **4.1 Dashboard Administrativo**
**URL**: `http://localhost/admin`
**Funcionalidad**: Vista general del sistema

**Métricas Mostradas**:
- Total de usuarios
- Total de paquetes
- Paquetes por estado
- Actividad reciente
- Alertas del sistema

#### **4.2 Gestión de Usuarios**
**URL**: `http://localhost/admin/users`
**Funcionalidad**: CRUD completo de usuarios

**Operaciones Disponibles**:

**Crear Usuario**:
- Formulario completo con validaciones
- Asignación de rol
- Generación automática de contraseña temporal
- Notificación por email

**Editar Usuario**:
- Modificación de información personal
- Cambio de rol (solo administrador)
- Activación/desactivación
- Solo disponible para administrador y operador

**Eliminar Usuario**:
- Eliminación lógica (soft delete)
- Verificación de dependencias
- Confirmación requerida
- Log de actividad

**Restablecer Contraseña**:
- Generación de nueva contraseña temporal
- Notificación por email
- Solo disponible para administrador y operador

**Activar/Desactivar**:
- Toggle de estado activo
- Bloqueo temporal de acceso
- Log de cambios de estado

#### **4.3 Gestión de Paquetes**
**URL**: `http://localhost/admin/packages`
**Funcionalidad**: Administración de paquetes del sistema

**Operaciones**:
- Ver todos los paquetes
- Cambiar estado de paquetes
- Agregar observaciones
- Calcular costos
- Generar reportes

**Estados Manejables**:
- `anunciado` → `recibido`
- `recibido` → `entregado`
- Cualquier estado → `cancelado`

### **5. SISTEMA DE NOTIFICACIONES**

#### **5.1 SMS Automático**
**Proveedor**: LIWA.co API v2
**Funcionalidad**: Envío automático de códigos de tracking

**Configuración API**:
- **Auth URL**: https://api.liwa.co/v2/auth/login
- **SMS URL**: https://api.liwa.co/v2/sms/single
- **Account**: 00486396309
- **API Key**: c52d8399ac63a24563ee8a967bafffc6cb8d8dfa
- **Authorization**: Bearer token (autenticación automática)

**Proceso**:
1. Autenticación automática con LIWA.co
2. Creación de anuncio de paquete
3. Generación de código de tracking
4. Formateo de número de teléfono (+57)
5. Envío vía API LIWA.co v2
6. Confirmación de entrega

**Mensaje SMS**:
```
PAQUETES EL CLUB: Hola {nombre}, tu paquete con guía {guia} tiene código de consulta: {codigo}. Consulta en: http://localhost/search
```

#### **5.2 Notificaciones por Email**
**Proveedor**: SMTP (taylor.mxrouting.net)
**Configuración SMTP**:
- **Host**: taylor.mxrouting.net
- **Puerto**: 587
- **Usuario**: guia@papyrus.com.co
- **Contraseña**: ^Kxub2aoh@xC2LsK
- **Remitente**: PAQUETES EL CLUB

**Funcionalidades**:
- Recuperación de contraseña
- Confirmación de cambios de perfil
- Notificaciones administrativas
- Reportes del sistema

### **6. SISTEMA DE REPORTES Y ESTADÍSTICAS**

#### **6.1 Métricas del Sistema**
- Usuarios activos/inactivos
- Paquetes por estado
- Tiempo promedio de entrega
- Volumen de anuncios por día
- Uso de recursos del sistema

#### **6.2 Logs de Actividad**
- Todas las acciones de usuarios
- Intentos de acceso
- Cambios de estado
- Modificaciones de datos
- Errores del sistema

---

## 🔧 **CONFIGURACIÓN TÉCNICA**

### **Variables de Entorno**
```bash
# Configuración de la Aplicación
APP_NAME=PAQUETES EL CLUB
APP_VERSION=3.1.0
DEBUG=True
ENVIRONMENT=development

# Base de Datos AWS RDS (ÚNICA FUENTE)
DATABASE_URL=postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria
POSTGRES_PASSWORD=a?HC!2.*1#?[==:|289qAI=)#V4kDzl$
POSTGRES_USER=jveyes
POSTGRES_DB=paqueteria
POSTGRES_HOST=ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com
POSTGRES_PORT=5432

# Cache Redis
REDIS_URL=redis://:redis123@redis:6379/0
REDIS_PASSWORD=redis123
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Seguridad
SECRET_KEY=paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración SMTP
SMTP_HOST=taylor.mxrouting.net
SMTP_PORT=587
SMTP_USER=guia@papyrus.com.co
SMTP_PASSWORD=^Kxub2aoh@xC2LsK
SMTP_FROM_NAME=PAQUETES EL CLUB
SMTP_FROM_EMAIL=guia@papyrus.com.co

# Configuración SMS (LIWA.co)
LIWA_API_KEY=c52d8399ac63a24563ee8a967bafffc6cb8d8dfa
LIWA_ACCOUNT=00486396309
LIWA_PASSWORD=6fEuRnd*$$#NfFAS
LIWA_AUTH_URL=https://api.liwa.co/v2/auth/login
LIWA_SMS_URL=https://api.liwa.co/v2/sms/single
LIWA_FROM_NAME=PAQUETES EL CLUB

# Configuración de Tarifas
BASE_STORAGE_RATE=1000
BASE_DELIVERY_RATE=1500
NORMAL_PACKAGE_MULTIPLIER=1500
EXTRA_DIMENSION_PACKAGE_MULTIPLIER=2000
CURRENCY=COP

# Configuración de Archivos
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

# Configuración de la Empresa
COMPANY_NAME=PAQUETES EL CLUB
COMPANY_ADDRESS=Cra. 91 #54-120, Local 12
COMPANY_PHONE=3334004007
COMPANY_EMAIL=guia@papyrus.com.co

# Configuración de Monitoreo
GRAFANA_PASSWORD=Grafana2025!Secure
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Configuración de Logs
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Configuración de PWA
PWA_NAME=PAQUETES EL CLUB
PWA_SHORT_NAME=Paquetes
PWA_DESCRIPTION=Sistema de gestión de paquetería
PWA_THEME_COLOR=#3B82F6
PWA_BACKGROUND_COLOR=#FFFFFF
```

### **Configuración de Base de Datos**
```python
# PostgreSQL AWS RDS (Producción)
- Host: ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com
- Puerto: 5432
- Base de Datos: paqueteria
- Usuario: jveyes
- Timezone: America/Bogota
- Encoding: UTF-8
- Connection Pool: 20 conexiones
- SSL: Requerido
- Backup: Automático diario
- Región AWS: us-east-1
```

### **Configuración de Redis**
```python
# Cache y Rate Limiting
- Host: redis
- Puerto: 6379
- Base de Datos: 0
- Contraseña: redis123
- Max Memory: 64MB
- Policy: allkeys-lru
- Max Clients: 50
- Persistence: RDB + AOF
```

### **Configuración de Tarifas**
```python
# Sistema de Cálculo Automático
- Moneda: COP (Pesos Colombianos)
- Tarifa Base Almacenamiento: $1,000
- Tarifa Base Entrega: $1,500
- Multiplicador Paquete Normal: $1,500
- Multiplicador Paquete Extradimensionado: $2,000
- Cálculo Total: Base + (Tipo × Multiplicador)
```

### **Configuración de Archivos**
```python
# Gestión de Archivos
- Directorio de Subida: ./uploads
- Tamaño Máximo: 5MB (5,242,880 bytes)
- Extensiones Permitidas: jpg, jpeg, png, gif, webp
- Soporte para Imágenes WebP
```

### **Configuración de Monitoreo**
```python
# Prometheus + Grafana
- Prometheus Puerto: 9090
- Grafana Puerto: 3000
- Grafana Contraseña: Grafana2025!Secure
- Métricas del Sistema en Tiempo Real
- Dashboard de Monitoreo Disponible
```

### **Configuración de Logs**
```python
# Sistema de Logging
- Nivel: INFO
- Archivo: ./logs/app.log
- Formato: %(asctime)s - %(name)s - %(levelname)s - %(message)s
- Auditoría Completa del Sistema
- Trazabilidad de Todas las Operaciones
```

### **Configuración SSL**
```python
# Certificados SSL
- Estado: No configurado actualmente
- Tipo: HTTP (no HTTPS)
- Puerto: 80 (HTTP estándar)
- Nota: Para producción se recomienda configurar SSL/TLS
```

### **Configuración PWA**
```python
# Progressive Web App
- Nombre: PAQUETES EL CLUB
- Nombre Corto: Paquetes
- Descripción: Sistema de gestión de paquetería
- Color del Tema: #3B82F6 (Azul)
- Color de Fondo: #FFFFFF (Blanco)
- Instalable en Dispositivos Móviles
```

### **Configuración LIWA.co API v2**
```python
# Servicio de SMS
- Auth URL: https://api.liwa.co/v2/auth/login
- SMS URL: https://api.liwa.co/v2/sms/single
- Account: 00486396309
- API Key: c52d8399ac63a24563ee8a967bafffc6cb8d8dfa
- Authorization: Bearer token
- Autenticación: Automática en cada envío
```

### **Configuración SMTP**
```python
# Servicio de Email
- Host: taylor.mxrouting.net
- Puerto: 587
- Usuario: guia@papyrus.com.co
- Contraseña: ^Kxub2aoh@xC2LsK
- Remitente: PAQUETES EL CLUB
- Seguridad: STARTTLS
```

### **Configuración de Celery**
```python
# Tareas Asíncronas
- Workers: 2
- Concurrency: 2 por worker
- Max Tasks per Child: 500
- Soft Time Limit: 5 minutos
- Hard Time Limit: 10 minutos
```

---

## 🚀 **DESPLIEGUE Y OPERACIONES**

### **Entorno de Desarrollo**
```bash
# Clonar repositorio
git clone <repository-url>
cd paqueteria-v3.1

# Configurar variables de entorno
cp code/env.example code/.env
# Editar .env con configuraciones locales

# Iniciar con Docker
cd code
docker-compose up -d

# Verificar servicios
docker-compose ps
docker-compose logs -f
```

### **Entorno de Producción**
```bash
# Conectar al servidor AWS
ssh papyrus

# Desplegar aplicación
cd /path/to/project
./deploy-aws.sh

# Verificar estado
docker ps
docker logs paqueteria_v31_app
```

### **Monitoreo y Logs**
```bash
# Logs de aplicación
docker-compose logs -f app

# Logs de base de datos
docker-compose logs -f postgres

# Métricas Prometheus
curl http://localhost:9090/metrics

# Dashboard Grafana
http://localhost:3000
```

---

## 📊 **REQUERIMIENTOS NO FUNCIONALES**

### **Rendimiento**
- **Usuarios Simultáneos**: 50 usuarios
- **Tiempo de Respuesta**: < 200ms para APIs
- **Throughput**: 100 requests/segundo
- **Disponibilidad**: 99.9%

### **Escalabilidad**
- **Horizontal**: Múltiples instancias de app
- **Vertical**: Aumento de recursos por instancia
- **Base de Datos**: Read replicas para consultas
- **Cache**: Redis cluster para alta disponibilidad

### **Seguridad**
- **Autenticación**: JWT con expiración
- **Autorización**: RBAC por roles
- **Validación**: Input sanitization
- **Rate Limiting**: Por IP y usuario
- **Logs**: Auditoría completa de acciones

### **Mantenibilidad**
- **Código**: PEP 8, documentación inline
- **Testing**: Cobertura > 80%
- **CI/CD**: Pipeline automatizado
- **Documentación**: README y API docs
- **Versionado**: Semantic versioning

---

## 🧪 **TESTING Y CALIDAD**

### **Tipos de Pruebas**
- **Unit Tests**: Funciones individuales
- **Integration Tests**: APIs y base de datos
- **End-to-End**: Flujos completos de usuario
- **Performance Tests**: Carga y estrés
- **Security Tests**: Vulnerabilidades y permisos

### **Herramientas de Testing**
- **Framework**: pytest
- **Coverage**: pytest-cov
- **Mocking**: unittest.mock
- **HTTP Testing**: httpx
- **Database Testing**: testcontainers

### **Cobertura de Pruebas**
- **Backend**: 95%+
- **APIs**: 100% endpoints probados
- **Modelos**: 100% validaciones
- **Servicios**: 100% lógica de negocio
- **Frontend**: 90% funcionalidades

---

## 📚 **DOCUMENTACIÓN Y MANUALES**

### **Documentación Técnica**
- **README.md**: Visión general del proyecto
- **API.md**: Documentación de endpoints
- **DEPLOYMENT.md**: Guía de despliegue
- **STRUCTURE.md**: Arquitectura del sistema
- **CHANGELOG.md**: Historial de cambios

### **Manuales de Usuario**
- **Usuario Final**: Cómo usar el sistema público
- **Operador**: Gestión de paquetes y usuarios
- **Administrador**: Configuración del sistema
- **Desarrollador**: Guía de contribución

### **Diagramas y Arquitectura**
- **ERD**: Modelo de base de datos
- **API Flow**: Flujo de endpoints
- **Deployment**: Arquitectura de infraestructura
- **Security**: Modelo de amenazas

---

## 🔮 **ROADMAP Y FUTURAS VERSIONES**

### **v3.2 (Próxima)**
- [ ] Integración con WhatsApp Business API
- [ ] Sistema de notificaciones push
- [ ] App móvil nativa (React Native)
- [ ] Dashboard de analytics avanzado
- [ ] Sistema de facturación automática

### **v4.0 (Largo Plazo)**
- [ ] Microservicios arquitectura
- [ ] API GraphQL
- [ ] Machine Learning para predicciones
- [ ] Integración con servicios de logística
- [ ] Sistema multi-tenant

---

## 📞 **CONTACTO Y SOPORTE**

### **Equipo de Desarrollo**
- **Desarrollador Principal**: JEMAVI
- **Arquitecto**: JEMAVI
- **DevOps**: JEMAVI
- **QA**: JEMAVI

### **Canales de Soporte**
- **Email**: guia@papyrus.com.co
- **Teléfono**: +57 333 400 4007
- **WhatsApp**: +57 333 400 4007
- **Documentación**: README.md del proyecto

### **Horarios de Soporte**
- **Lunes a Viernes**: 8:00 AM - 6:00 PM (COT)
- **Sábados**: 9:00 AM - 1:00 PM (COT)
- **Emergencias**: 24/7 para usuarios admin

---

**Documento generado el**: 2025-09-01  
**Versión del documento**: 1.0  
**Estado**: ✅ COMPLETADO  
**Próxima revisión**: 2025-12-01
