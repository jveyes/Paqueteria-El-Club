# Configuración de Zona Horaria - Colombia

## Resumen
Se ha configurado la zona horaria de Colombia (`America/Bogota`) en todos los contenedores locales y en AWS para el sistema de paquetería.

## Problema Solucionado
**Problema**: La aplicación mostraba fechas futuras incorrectas (ej: "jueves, 28 de agosto de 2025, 21:47" cuando eran las 4:47 PM en Colombia).

**Causa**: El código usaba `datetime.now()` sin especificar zona horaria, lo que causaba inconsistencias.

**Solución**: Se implementó un sistema de manejo de fechas con zona horaria de Colombia usando `pytz` y funciones personalizadas.

## Cambios Realizados

### 1. Nuevo Módulo de Utilidades de Fecha
- **`src/utils/datetime_utils.py`**: Módulo completo para manejo de fechas con zona horaria de Colombia
  - `get_colombia_now()`: Obtener fecha/hora actual en Colombia
  - `get_colombia_datetime()`: Convertir fechas a zona horaria de Colombia
  - `format_colombia_datetime()`: Formatear fechas en Colombia
  - Funciones auxiliares para fechas y horas

### 2. Archivos de Docker Compose
- **`docker-compose.yml`**: Agregada variable `TZ=America/Bogota` a todos los servicios
- **`docker-compose.aws.yml`**: Agregada variable `TZ=America/Bogota` a todos los servicios

### 3. Dockerfile
- Agregada variable de entorno `TZ=America/Bogota`
- Instalado paquete `tzdata` para soporte de zonas horarias
- Configurado enlace simbólico para zona horaria de Colombia

### 4. Variables de Entorno
- **`env.example`**: Agregada variable `TZ=America/Bogota`
- **`env.aws`**: Agregada variable `TZ=America/Bogota`

### 5. Código de la Aplicación
- **`package_service.py`**: Reemplazado `datetime.now()` por `get_colombia_now()`
- **`packages.py`**: Reemplazado `datetime.now()` por `get_colombia_now()`
- **`rates.py`**: Reemplazado `datetime.now()` por `get_colombia_now()`
- **`notification_service.py`**: Reemplazado `datetime.now()` por `get_colombia_now()`
- **`helpers.py`**: Reemplazado `datetime.now()` por `get_colombia_now()`

### 6. Dependencias
- **`requirements.txt`**: Agregado `pytz==2023.3` para manejo de zonas horarias

### 7. Scripts de Gestión
- **`check-timezone.sh`**: Verifica la zona horaria en todos los contenedores
- **`apply-timezone.sh`**: Aplica zona horaria a contenedores existentes
- **`aws-timezone-setup.sh`**: Configura zona horaria en servidor AWS
- **`test-timezone.py`**: Script de prueba para verificar zona horaria
- **`fix-timezone-issue.sh`**: Guía para solucionar el problema de fechas

## Servicios Configurados

### Locales
- `paqueteria_v31_postgres` - Base de datos PostgreSQL
- `paqueteria_v31_redis` - Cache Redis
- `paqueteria_v31_app` - Aplicación principal
- `paqueteria_v31_celery_worker` - Worker de tareas en segundo plano
- `paqueteria_v31_nginx` - Servidor web Nginx

### AWS
- `paqueteria_v31_nginx` - Servidor web Nginx
- `paqueteria_v31_redis` - Cache Redis
- `paqueteria_v31_app` - Aplicación principal
- `paqueteria_v31_celery_worker` - Worker de tareas en segundo plano

## Aplicación de Cambios

### Para Contenedores Locales
```bash
# Aplicar temporalmente
./scripts/apply-timezone.sh

# Aplicar permanentemente
docker-compose down
docker-compose build
docker-compose up -d

# Verificar
./scripts/check-timezone.sh

# Probar
./scripts/test-timezone.py
```

### Para AWS
```bash
# Aplicar configuración
./scripts/aws-timezone-setup.sh

# Aplicar permanentemente
ssh papyrus
cd /opt/paqueteria
docker-compose -f docker-compose.aws.yml down
docker-compose -f docker-compose.aws.yml build
docker-compose -f docker-compose.aws.yml up -d

# Verificar
ssh papyrus 'docker exec paqueteria_v31_app date'
```

## Verificación

### Verificación Local
```bash
# Verificar todos los contenedores
./scripts/check-timezone.sh

# Verificar contenedor específico
docker exec paqueteria_v31_app date
docker exec paqueteria_v31_app printenv TZ

# Probar funciones de fecha
python3 scripts/test-timezone.py
```

### Verificación AWS
```bash
# Verificar servidor
ssh papyrus 'date && timedatectl'

# Verificar contenedores
ssh papyrus 'docker exec paqueteria_v31_app date'
ssh papyrus 'docker exec paqueteria_v31_app printenv TZ'
```

## Resultado Esperado

Todos los contenedores deben mostrar:
- **Hora**: Hora de Colombia (UTC-5)
- **Variable TZ**: `America/Bogota`
- **Archivo timezone**: Contener `America/Bogota`
- **Fechas en la aplicación**: Hora correcta de Colombia (ej: 4:47 PM en lugar de 9:47 PM)

## Notas Importantes

1. **Cambios Permanentes**: Para que los cambios sean permanentes, es necesario reconstruir las imágenes Docker
2. **Base de Datos**: PostgreSQL también respetará la zona horaria configurada
3. **Logs**: Todos los logs se generarán con la hora de Colombia
4. **Aplicación**: La aplicación Python usará la zona horaria configurada para todas las operaciones de fecha/hora
5. **Tracking Numbers**: Los números de tracking ahora incluirán la fecha correcta de Colombia

## Troubleshooting

### Si la zona horaria no se aplica:
1. Verificar que el contenedor tenga el paquete `tzdata` instalado
2. Verificar que la variable `TZ` esté configurada correctamente
3. Reiniciar el contenedor después de aplicar los cambios
4. Reconstruir la imagen Docker si es necesario

### Para forzar la aplicación:
```bash
# En el contenedor
docker exec -it <container_name> bash
ln -sf /usr/share/zoneinfo/America/Bogota /etc/localtime
echo "America/Bogota" > /etc/timezone
export TZ=America/Bogota
```

### Si las fechas siguen incorrectas:
1. Verificar que se haya reconstruido la imagen Docker
2. Verificar que el código use `get_colombia_now()` en lugar de `datetime.now()`
3. Reiniciar todos los contenedores
4. Verificar con el script de prueba: `python3 scripts/test-timezone.py`
