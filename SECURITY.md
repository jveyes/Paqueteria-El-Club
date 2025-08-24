# 🔒 Política de Seguridad

## 🛡️ Reportar una Vulnerabilidad

Si descubres una vulnerabilidad de seguridad, por favor **NO** abras un issue público.
En su lugar, envía un email a **soporte@papyrus.com.co** con los detalles.

### 📧 Información a Incluir

- **Descripción** de la vulnerabilidad
- **Pasos** para reproducir
- **Impacto** potencial
- **Sugerencias** de mitigación (si las tienes)

### ⏱️ Respuesta

- **Confirmación** de recepción: 24-48 horas
- **Evaluación inicial**: 3-5 días hábiles
- **Actualizaciones**: Semanales hasta resolución

## 🔐 Medidas de Seguridad

### Autenticación
- JWT tokens con expiración
- Passwords hasheados con bcrypt
- Rate limiting en endpoints sensibles

### Autorización
- Roles de usuario (Admin, User)
- Validación de permisos por endpoint
- Sanitización de inputs

### Datos
- Conexiones HTTPS/TLS
- Validación de datos con Pydantic
- Escape de caracteres especiales

### Infraestructura
- Contenedores Docker aislados
- Variables de entorno para secretos
- Logs de auditoría

## 🚨 Vulnerabilidades Conocidas

Actualmente no hay vulnerabilidades de seguridad conocidas.

## 📞 Contacto

- **Email de seguridad:** soporte@papyrus.com.co
- **Respuesta:** 24-48 horas
- **Horario:** Lunes a Viernes, 9:00 AM - 6:00 PM (GMT-5)

---

**Gracias por ayudar a mantener seguro el Sistema de Paquetería v3.0** 🛡️
