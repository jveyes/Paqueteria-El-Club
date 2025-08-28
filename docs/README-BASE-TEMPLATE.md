# 📋 Plantilla Base - PAQUETES EL CLUB v3.1

## 🎯 Propósito

Esta plantilla base (`base-template.html`) proporciona una estructura consistente para todas las páginas del proyecto, incluyendo:

- ✅ **Header optimizado** con navegación responsive
- ✅ **Footer sticky** con iconos de contacto
- ✅ **Configuración completa** de Tailwind CSS, Alpine.js y HTMX
- ✅ **Paleta de colores PAPYRUS** predefinida
- ✅ **Diseño mobile-first** responsive
- ✅ **SEO optimizado** con meta tags

## 📁 Ubicación

```
code/templates/
├── components/
│   └── base-template.html          # Plantilla base principal
├── example-page.html               # Ejemplo de uso
└── README-BASE-TEMPLATE.md        # Esta documentación
```

## 🚀 Cómo Usar la Plantilla Base

### 1. Estructura Básica

```html
{% extends "components/base-template.html" %}

{% block title %}Título de la Página - PAQUETES EL CLUB v3.1{% endblock %}

{% block content %}
<!-- Tu contenido aquí -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold text-gray-900">Mi Página</h1>
    <p class="mt-4 text-gray-600">Contenido de la página...</p>
</div>
{% endblock %}
```

### 2. Bloques Disponibles

#### `{% block title %}`
Define el título de la página que aparecerá en la pestaña del navegador.

```html
{% block title %}Mi Página - PAQUETES EL CLUB v3.1{% endblock %}
```

#### `{% block content %}`
Contiene el contenido principal de la página.

```html
{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Tu contenido aquí -->
</div>
{% endblock %}
```

#### `{% block extra_head %}`
Para agregar CSS, meta tags o scripts adicionales en el `<head>`.

```html
{% block extra_head %}
<link rel="stylesheet" href="/static/css/mi-estilo.css">
<meta name="robots" content="noindex">
{% endblock %}
```

#### `{% block extra_scripts %}`
Para agregar JavaScript específico de la página al final del `<body>`.

```html
{% block extra_scripts %}
<script>
    // JavaScript específico de la página
    console.log('Página cargada');
</script>
{% endblock %}
```

## 🎨 Características Incluidas

### Header Optimizado
- **Logo y título**: "PAQUETES" con icono de paquete
- **Navegación desktop**: Dashboard, Paquetes, Clientes
- **Menú móvil**: Hamburguesa con navegación colapsable
- **Icono de login**: A la derecha (desktop) y junto al hamburguesa (móvil)

### Footer Sticky
- **Copyright**: "© 2025 PAQUETES EL CLUB - Desarrollado por JEMAVI"
- **Iconos de contacto**: Ayuda, WhatsApp, Teléfono
- **Responsive**: Iconos grandes en móvil, iconos + texto en desktop

### Configuración CSS
- **Tailwind CSS**: Configurado con paleta PAPYRUS
- **Colores disponibles**: `papyrus-blue`, `papyrus-green`, `papyrus-orange`, etc.
- **Fuente**: Inter (sistema)
- **Scrollbar personalizada**

### Frameworks JavaScript
- **Alpine.js**: Para interactividad
- **HTMX**: Para peticiones AJAX
- **Heroicons**: Iconos SVG

## 📱 Responsive Design

### Breakpoints
- **Móvil**: `< 768px`
- **Tablet**: `768px - 1024px`
- **Desktop**: `> 1024px`

### Comportamiento
- **Header**: Logo pequeño en móvil, grande en desktop
- **Navegación**: Menú hamburguesa en móvil, horizontal en desktop
- **Footer**: Iconos grandes en móvil, iconos + texto en desktop

## 🎯 Ejemplo Completo

```html
{% extends "components/base-template.html" %}

{% block title %}Mi Nueva Página - PAQUETES EL CLUB v3.1{% endblock %}

{% block extra_head %}
<meta name="description" content="Descripción específica de mi página">
<link rel="stylesheet" href="/static/css/mi-estilo.css">
{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Hero Section -->
    <div class="text-center mb-12">
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-light text-gray-900 mb-4">
            Mi Nueva Página
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            Descripción de mi nueva página usando la plantilla base.
        </p>
    </div>

    <!-- Content -->
    <div class="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <h2 class="text-xl font-medium text-gray-900 mb-4">Contenido Principal</h2>
        <p class="text-gray-600">Aquí va el contenido específico de mi página.</p>
        
        <!-- Botón con colores PAPYRUS -->
        <button class="mt-4 bg-papyrus-blue text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
            Acción Principal
        </button>
    </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
    // JavaScript específico de esta página
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Mi nueva página cargada');
    });
</script>
{% endblock %}
```

## 🔧 Personalización

### Agregar Nuevos Colores
En el bloque `<script>` de Tailwind config:

```javascript
'papyrus-nuevo': '#tu-color-hex',
```

### Modificar Header
Editar la sección del header en `base-template.html`:

```html
<!-- Logo/Nombre del proyecto -->
<div class="flex items-center space-x-2 sm:space-x-4 md:space-x-8">
    <!-- Modificar aquí -->
</div>
```

### Modificar Footer
Editar la sección del footer en `base-template.html`:

```html
<!-- Enlaces -->
<div class="flex items-center justify-center sm:justify-end space-x-3 sm:space-x-4">
    <!-- Modificar aquí -->
</div>
```

## 📋 Checklist para Nuevas Páginas

- [ ] Extender `base-template.html`
- [ ] Definir título único en `{% block title %}`
- [ ] Agregar contenido en `{% block content %}`
- [ ] Usar colores PAPYRUS (`papyrus-blue`, `papyrus-green`, etc.)
- [ ] Implementar diseño responsive
- [ ] Agregar JavaScript específico en `{% block extra_scripts %}` si es necesario
- [ ] Probar en móvil y desktop

## 🎨 Paleta de Colores PAPYRUS

```css
papyrus-blue: #1e40af
papyrus-green: #059669
papyrus-orange: #ea580c
papyrus-red: #dc2626
papyrus-yellow: #d97706
papyrus-purple: #7c3aed
papyrus-pink: #db2777
papyrus-indigo: #4f46e5
papyrus-teal: #0d9488
papyrus-cyan: #0891b2
```

## 📞 Soporte

Para dudas sobre la plantilla base, consultar:
- Este archivo README
- El archivo `example-page.html` para ejemplos
- La documentación de Tailwind CSS
- La documentación de Alpine.js

---

**Desarrollado por JEMAVI** - PAQUETES EL CLUB v3.1
