# Scripts de Consulta de Tracking - PAQUETES EL CLUB v3.1

Este directorio contiene scripts para consultar información de paquetes en la base de datos.

## 📋 Scripts Disponibles

### 1. `consultar_telefono_tracking.py` - Consulta Detallada
**Propósito**: Consulta completa de información de un paquete por código de tracking.

**Uso**:
```bash
python3 consultar_telefono_tracking.py <CODIGO_TRACKING>
```

**Ejemplo**:
```bash
python3 consultar_telefono_tracking.py PAP2025010112345678
```

**Salida**: Información completa del paquete incluyendo nombre del cliente, teléfono, estado, fechas, etc.

---

### 2. `consulta_rapida_tracking.py` - Consulta Rápida
**Propósito**: Consulta rápida que solo muestra el teléfono asociado a un código de tracking.

**Uso**:
```bash
python3 consulta_rapida_tracking.py <CODIGO_TRACKING>
```

**Ejemplo**:
```bash
python3 consulta_rapida_tracking.py PAP2025010112345678
```

**Salida**: Solo el número de teléfono (formato: 📱 3001234567)

---

### 3. `busqueda_avanzada_tracking.py` - Búsqueda Multidimensional
**Propósito**: Búsqueda por diferentes criterios: tracking, teléfono o nombre del cliente.

**Uso**:
```bash
# Por código de tracking
python3 busqueda_avanzada_tracking.py tracking <CODIGO_TRACKING>

# Por número de teléfono
python3 busqueda_avanzada_tracking.py telefono <NUMERO_TELEFONO>

# Por nombre del cliente
python3 busqueda_avanzada_tracking.py nombre <NOMBRE_CLIENTE>
```

**Ejemplos**:
```bash
# Buscar por código de tracking
python3 busqueda_avanzada_tracking.py tracking PAP2025010112345678

# Buscar por teléfono
python3 busqueda_avanzada_tracking.py telefono 3001234567

# Buscar por nombre
python3 busqueda_avanzada_tracking.py nombre "Juan Pérez"
```

**Salida**: Lista completa de resultados con toda la información disponible.

---

## 🔍 Casos de Uso

### Caso 1: Saber a qué teléfono se envió un código de consulta
```bash
python3 consultar_telefono_tracking.py PAP2025010112345678
```

### Caso 2: Consulta rápida solo del teléfono
```bash
python3 consulta_rapida_tracking.py PAP2025010112345678
```

### Caso 3: Buscar todos los paquetes de un cliente por teléfono
```bash
python3 busqueda_avanzada_tracking.py telefono 3001234567
```

### Caso 4: Buscar todos los paquetes de un cliente por nombre
```bash
python3 busqueda_avanzada_tracking.py nombre "María González"
```

---

## 📊 Información que se Consulta

Los scripts extraen la siguiente información de la base de datos:

- **Código de Tracking**: Número único del paquete
- **Nombre del Cliente**: Nombre completo del destinatario
- **Teléfono**: Número de contacto del cliente
- **Estado del Paquete**: ANUNCIADO, RECIBIDO, EN_TRANSITO, ENTREGADO, CANCELADO
- **Fecha de Creación**: Cuando se creó el registro
- **Fecha de Anuncio**: Cuando se anunció el paquete

---

## ⚠️ Notas Importantes

1. **Formato de Teléfono**: Los teléfonos se almacenan en formato colombiano (ej: 3001234567)
2. **Códigos de Tracking**: Se generan automáticamente con formato PAP + timestamp + random
3. **Base de Datos**: Los scripts se conectan a la base de datos PostgreSQL de AWS RDS
4. **Permisos**: Asegúrate de que los scripts tengan permisos de ejecución (`chmod +x`)

---

## 🚀 Instalación y Configuración

1. **Hacer ejecutables los scripts**:
```bash
chmod +x *.py
```

2. **Verificar dependencias**:
```bash
pip3 install sqlalchemy psycopg2-binary
```

3. **Configuración de base de datos**: Los scripts usan la configuración de `code/src/config.py`

---

## 🔧 Solución de Problemas

### Error de conexión a la base de datos
- Verificar que la base de datos esté accesible
- Revisar la configuración en `config.py`
- Verificar credenciales de AWS RDS

### Error de módulos no encontrados
- Asegurarse de ejecutar desde el directorio `code/scripts/`
- Verificar que el directorio `src` esté en el path

### No se encuentran resultados
- Verificar que el código de tracking exista
- Revisar que no haya espacios extra en el código
- Confirmar que el paquete esté registrado en el sistema

---

## 📞 Soporte

Para problemas técnicos o consultas adicionales, contactar al administrador del sistema.
