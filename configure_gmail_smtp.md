# Configuración Gmail SMTP para Recuperación de Contraseña

## Pasos para configurar Gmail SMTP:

### 1. Crear una App Password en Gmail
1. Ir a https://myaccount.google.com/
2. Seguridad → Verificación en 2 pasos (debe estar activada)
3. Contraseñas de aplicaciones → Generar contraseña
4. Seleccionar "Correo" y "Otro (nombre personalizado)"
5. Escribir "PAQUETES EL CLUB"
6. Copiar la contraseña generada (16 caracteres)

### 2. Configurar variables de entorno
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password-de-16-caracteres
SMTP_FROM_NAME=PAQUETES EL CLUB
SMTP_FROM_EMAIL=tu-email@gmail.com
```

### 3. Reiniciar el contenedor
```bash
docker-compose restart app
```

## Ventajas de Gmail SMTP:
- ✅ Confiable y no marca emails como spam
- ✅ Fácil de configurar
- ✅ Gratuito
- ✅ Buena reputación de entrega
