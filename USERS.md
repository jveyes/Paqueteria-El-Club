# Usuarios del Sistema - PAQUETES EL CLUB v3.1

## Usuarios Administradores

### 1. Usuario Principal (jveyes)
- **Username:** jveyes
- **Email:** jveyes@gmail.com
- **Password:** il1111
- **Nombre:** JESUS VILLALOBOS
- **Rol:** ADMIN
- **Estado:** Activo

### 2. Usuario Administrador del Sistema
- **Username:** admin
- **Email:** admin@papyrus.com.co
- **Password:** admin123 (hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i)
- **Nombre:** Administrador Sistema
- **Rol:** ADMIN
- **Estado:** Activo

## Endpoints de Autenticación

### Login
```bash
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=jveyes&password=il1111
```

### Verificar Autenticación
```bash
GET /api/auth/check
Authorization: Bearer <token>
```

### Logout
```bash
POST /api/auth/logout
Authorization: Bearer <token>
```

## Páginas Web

### Login
- **URL:** http://localhost/auth/login
- **Método:** GET
- **Estado:** ✅ Funcionando

### Registro
- **URL:** http://localhost/auth/register
- **Método:** GET
- **Estado:** ✅ Funcionando

### Recuperar Contraseña
- **URL:** http://localhost/auth/forgot-password
- **Método:** GET
- **Estado:** ✅ Funcionando

## Notas

- Los usuarios se crean directamente en la base de datos PostgreSQL
- Las contraseñas se hashean con bcrypt
- Los tokens JWT tienen una duración de 30 minutos
- El sistema está configurado para desarrollo sin contraseña en Redis
