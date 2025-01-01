# Configuración SendGrid para Recuperación de Contraseña

## Pasos para configurar SendGrid:

### 1. Crear cuenta en SendGrid
1. Ir a https://sendgrid.com/
2. Crear cuenta gratuita (100 emails/día gratis)
3. Verificar email y completar setup

### 2. Crear API Key
1. Settings → API Keys
2. Create API Key
3. Full Access o Restricted Access (solo Mail Send)
4. Copiar la API key

### 3. Configurar variables de entorno
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=tu-sendgrid-api-key
SMTP_FROM_NAME=PAQUETES EL CLUB
SMTP_FROM_EMAIL=noreply@papyrus.com.co
```

### 4. Reiniciar el contenedor
```bash
docker-compose restart app
```

## Ventajas de SendGrid:
- ✅ Servicio profesional de email
- ✅ Excelente reputación de entrega
- ✅ Analytics y tracking
- ✅ 100 emails/día gratis
