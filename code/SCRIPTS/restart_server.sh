#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Reiniciar Servidor
# ========================================

echo "🔄 REINICIANDO SERVIDOR PAQUETERÍA"
echo "=================================="

# Detener servidor actual
echo "📴 Deteniendo servidor actual..."
pkill -f "uvicorn main:app"

# Esperar un momento
sleep 2

# Verificar que se detuvo
if pgrep -f "uvicorn main:app" > /dev/null; then
    echo "⚠️  Servidor aún corriendo, forzando cierre..."
    pkill -9 -f "uvicorn main:app"
    sleep 1
fi

# Verificar que se detuvo completamente
if pgrep -f "uvicorn main:app" > /dev/null; then
    echo "❌ No se pudo detener el servidor"
    exit 1
else
    echo "✅ Servidor detenido correctamente"
fi

# Activar entorno virtual si existe
if [ -d "/opt/venv" ]; then
    echo "🐍 Activando entorno virtual..."
    source /opt/venv/bin/activate
fi

# Navegar al directorio del proyecto
cd "$(dirname "$0")"

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ No se encontró main.py en el directorio actual"
    echo "   Directorio actual: $(pwd)"
    exit 1
fi

echo "📁 Directorio del proyecto: $(pwd)"

# Verificar que el archivo main.py existe y tiene el endpoint
if grep -q "request-reset" main.py; then
    echo "✅ Endpoint request-reset encontrado en main.py"
else
    echo "⚠️  Endpoint request-reset NO encontrado en main.py"
    echo "   Verificando archivos de rutas..."
    
    if [ -f "src/routers/auth.py" ] && grep -q "request-reset" src/routers/auth.py; then
        echo "✅ Endpoint request-reset encontrado en src/routers/auth.py"
    else
        echo "❌ Endpoint request-reset NO encontrado en ningún archivo"
        echo "   Esto indica que el código no está actualizado"
        exit 1
    fi
fi

# Iniciar servidor
echo "🚀 Iniciando servidor..."
echo "   Host: 0.0.0.0"
echo "   Puerto: 8000"
echo "   Archivo: main.py"

# Iniciar en background
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

# Esperar un momento para que inicie
sleep 3

# Verificar que está corriendo
if pgrep -f "uvicorn main:app" > /dev/null; then
    echo "✅ Servidor iniciado correctamente"
    echo "📋 PID: $(pgrep -f 'uvicorn main:app')"
    
    # Verificar que responde
    echo "🔍 Verificando respuesta del servidor..."
    sleep 2
    
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Servidor responde correctamente"
        
        # Verificar endpoint de recuperación de contraseña
        echo "🔍 Verificando endpoint de recuperación de contraseña..."
        if curl -s http://localhost:8000/openapi.json | grep -q "request-reset"; then
            echo "✅ Endpoint /api/auth/request-reset disponible"
        else
            echo "❌ Endpoint /api/auth/request-reset NO disponible"
            echo "   Revisa los logs del servidor: tail -f server.log"
        fi
    else
        echo "❌ Servidor no responde"
        echo "   Revisa los logs: tail -f server.log"
    fi
else
    echo "❌ Error iniciando servidor"
    echo "   Revisa los logs: cat server.log"
    exit 1
fi

echo ""
echo "🎯 COMANDOS ÚTILES:"
echo "   Ver logs: tail -f server.log"
echo "   Detener: pkill -f 'uvicorn main:app'"
echo "   Status: curl http://localhost:8000/health"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "✅ Reinicio completado"
