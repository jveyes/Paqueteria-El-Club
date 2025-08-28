# 📧 CONFIGURACIÓN DE EMAILS - PAQUETES EL CLUB v3.1

## 🎯 **ESTADO ACTUAL**

### ✅ **Configurado:**
- **🏢 Servidor SMTP**: smtp.gmail.com
- **🔌 Puerto**: 587
- **👤 Usuario**: jveyes@gmail.com
- **🔒 TLS**: Habilitado
- **🌐 Aplicación**: https://guia.papyrus.com.co
- **🗄️ Base de datos**: AWS RDS - Funcionando
- **👥 Usuario**: jveyes (jveyes@gmail.com) - Disponible

### ⚠️ **Pendiente:**
- **🔑 Contraseña de aplicación**: Falta agregar al archivo .env

## 🔧 **PASOS PARA COMPLETAR LA CONFIGURACIÓN**

### **1. Obtener Contraseña de Aplicación de Gmail**

1. Ve a: https://myaccount.google.com/security
2. Activa la **verificación en 2 pasos** si no está activada
3. Ve a **"Contraseñas de aplicación"**
4. Selecciona **"Correo"** como aplicación
5. Genera una nueva contraseña de aplicación
6. **Copia la contraseña** (16 caracteres)

### **2. Configurar la Contraseña en el Servidor**

```bash
# Conectarse al servidor
papyrus

# Editar el archivo .env
cd /home/ubuntu/Paquetes
nano .env

# Agregar la línea:
EMAIL_PASSWORD=TU_CONTRASEÑA_DE_APLICACIÓN_AQUÍ
```

### **3. Reiniciar los Contenedores**

```bash
# Detener contenedores
docker-compose down

# Iniciar contenedores
docker-compose up -d

# Verificar estado
docker ps
```

### **4. Probar el Envío de Emails**

```bash
# Probar envío de email
python3 test_email_send.py TU_CONTRASEÑA_DE_APLICACIÓN
```

## 🧪 **PRUEBAS DISPONIBLES**

### **1. Prueba de Conexión SMTP**
```bash
python3 setup_smtp_test.py
```

### **2. Prueba de Envío de Email**
```bash
python3 test_email_send.py TU_CONTRASEÑA_DE_APLICACIÓN
```

### **3. Prueba del Sistema de Restablecimiento**
```bash
python3 test_password_reset.py
```

## 🌐 **URLS DE LA APLICACIÓN**

- **🔗 Aplicación Principal**: https://guia.papyrus.com.co
- **🔗 Login**: https://guia.papyrus.com.co/login
- **🔗 Forgot Password**: https://guia.papyrus.com.co/forgot-password
- **🔗 Health Check**: https://guia.papyrus.com.co/health

## 🔐 **CREDENCIALES DE ACCESO**

- **👤 Usuario**: jveyes
- **📧 Email**: jveyes@gmail.com
- **🔑 Contraseña**: (la misma del sistema local)

## 📧 **CONFIGURACIÓN SMTP COMPLETA**

```env
# Configuración SMTP Gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=jveyes@gmail.com
EMAIL_PASSWORD=TU_CONTRASEÑA_DE_APLICACIÓN_AQUÍ
EMAIL_USE_TLS=True
```

## 🎯 **FUNCIONALIDADES DISPONIBLES**

### **✅ Funcionando:**
- ✅ Login de usuarios
- ✅ Base de datos AWS RDS
- ✅ Aplicación web
- ✅ SSL/HTTPS
- ✅ Health checks

### **🔄 Pendiente de Configuración:**
- 🔄 Restablecimiento de contraseña por email
- 🔄 Notificaciones por email
- 🔄 Envío de reportes por email

## 🚀 **PRÓXIMOS PASOS**

1. **Obtener contraseña de aplicación** de Gmail
2. **Configurar EMAIL_PASSWORD** en el archivo .env
3. **Reiniciar contenedores**
4. **Probar envío de emails**
5. **Probar restablecimiento de contraseña**

## 📞 **SOPORTE**

Si tienes problemas con la configuración:

1. Verifica que la verificación en 2 pasos esté activada
2. Asegúrate de usar una contraseña de aplicación (no la contraseña normal)
3. Verifica que el email jveyes@gmail.com esté configurado correctamente
4. Revisa los logs de la aplicación: `docker logs paqueteria_v31_app`

---

**🎉 ¡Una vez configurado el EMAIL_PASSWORD, el sistema de emails estará completamente funcional!**
