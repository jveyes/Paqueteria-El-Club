# PRD - Sistema de Diseño PAPYRUS v3.0
## Guía de Estilos y Componentes Base

---

## 📋 Índice
1. [Visión General](#visión-general)
2. [Principios de Diseño](#principios-de-diseño)
3. [Paleta de Colores](#paleta-de-colores)
4. [Tipografía](#tipografía)
5. [Espaciado y Layout](#espaciado-y-layout)
6. [Componentes Base](#componentes-base)
7. [Formularios](#formularios)
8. [Iconografía](#iconografía)
9. [Estados y Interacciones](#estados-y-interacciones)
10. [Responsive Design](#responsive-design)
11. [Implementación Técnica](#implementación-técnica)
12. [Checklist de Componentes](#checklist-de-componentes)

---

## 🎯 Visión General

### Objetivo
Establecer un sistema de diseño consistente y escalable para PAQUETES EL CLUB que garantice una experiencia de usuario coherente, profesional y accesible en todos los componentes del sistema.

### Alcance
- Todos los componentes de la interfaz de usuario
- Formularios y elementos de entrada
- Navegación y estructura de páginas
- Dashboard y vistas administrativas
- Componentes de ayuda y soporte

---

## 🎨 Principios de Diseño

### 1. Minimalismo Corporativo
- **Limpieza visual**: Espacios en blanco estratégicos
- **Jerarquía clara**: Información organizada por importancia
- **Simplicidad**: Eliminar elementos innecesarios

### 2. Consistencia
- **Patrones uniformes**: Mismos comportamientos en situaciones similares
- **Lenguaje visual coherente**: Colores, tipografía y espaciado consistentes
- **Interacciones predecibles**: Feedback visual claro

### 3. Accesibilidad
- **Contraste adecuado**: Texto legible en todos los fondos
- **Navegación por teclado**: Todos los elementos interactivos accesibles
- **Etiquetas descriptivas**: Textos alternativos para iconos

---

## 🎨 Paleta de Colores

### Colores Principales
```css
/* PAPYRUS Corporate Colors */
--papyrus-red: #DC2626;      /* Acciones principales, alertas */
--papyrus-orange: #F97316;   /* Acentos, hover states */
--papyrus-yellow: #F59E0B;   /* Advertencias, destacados */
--papyrus-green: #10B981;    /* Éxito, confirmaciones */
--papyrus-blue: #3B82F6;     /* Enlaces, información */
--papyrus-dark: #1F2937;     /* Texto principal */
--papyrus-light: #F9FAFB;    /* Fondos claros */
```

### Colores de Interfaz
```css
/* Estados y Feedback */
--success: #10B981;          /* Verde para éxito */
--warning: #F59E0B;          /* Amarillo para advertencias */
--error: #DC2626;            /* Rojo para errores */
--info: #3B82F6;             /* Azul para información */

/* Neutros */
--gray-50: #F9FAFB;          /* Fondos muy claros */
--gray-100: #F3F4F6;         /* Fondos claros */
--gray-200: #E5E7EB;         /* Bordes, separadores */
--gray-300: #D1D5DB;         /* Bordes de inputs */
--gray-500: #6B7280;         /* Texto secundario */
--gray-700: #374151;         /* Texto principal */
--gray-900: #111827;         /* Texto importante */
```

---

## 📝 Tipografía

### Jerarquía de Textos
```css
/* Títulos */
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }  /* H1 Principal */
.text-2xl { font-size: 1.5rem; line-height: 2rem; }       /* H2 Secciones */
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }    /* H3 Subsections */
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }   /* H4 */

/* Cuerpo de texto */
.text-base { font-size: 1rem; line-height: 1.5rem; }      /* Texto normal */
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }   /* Texto pequeño */
.text-xs { font-size: 0.75rem; line-height: 1rem; }       /* Texto muy pequeño */

/* Pesos */
.font-light { font-weight: 300; }    /* Títulos elegantes */
.font-normal { font-weight: 400; }   /* Texto normal */
.font-medium { font-weight: 500; }   /* Texto importante */
.font-semibold { font-weight: 600; } /* Subtítulos */
.font-bold { font-weight: 700; }     /* Títulos principales */
```

### Familia de Fuentes
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

---

## 📐 Espaciado y Layout

### Layout Principal (Sticky Footer)
```html
<!-- Estructura base para páginas con sticky footer -->
<body class="bg-gray-50 min-h-screen flex flex-col">
    <!-- Header fijo -->
    <header class="bg-white shadow-sm border-b flex-shrink-0">
        <!-- Contenido del header -->
    </header>
    
    <!-- Contenido principal que se expande -->
    <main class="flex-1 flex-grow">
        <!-- Contenido de la página -->
    </main>
    
    <!-- Footer pegado al fondo -->
    <footer class="bg-white shadow-sm border-t flex-shrink-0">
        <!-- Contenido del footer -->
    </footer>
</body>
```

### Sistema de Espaciado
```css
/* Espaciado base (múltiplos de 4px) */
space-1: 0.25rem;   /* 4px */
space-2: 0.5rem;    /* 8px */
space-3: 0.75rem;   /* 12px */
space-4: 1rem;      /* 16px */
space-6: 1.5rem;    /* 24px */
space-8: 2rem;      /* 32px */
space-12: 3rem;     /* 48px */
space-16: 4rem;     /* 64px */
```

### Contenedores
```css
/* Máximo ancho de contenido */
.max-w-4xl { max-width: 56rem; }    /* Formularios */
.max-w-7xl { max-width: 80rem; }    /* Páginas principales */
```

### Grid System
```css
/* Grid responsivo */
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.md:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.md:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.md:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
```

---

## 🧩 Componentes Base

### 1. Header Component
```html
<!-- Estructura base del header con menú móvil -->
<header class="bg-white shadow-sm border-b flex-shrink-0" x-data="{ mobileMenuOpen: false }">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
            <!-- Logo/Nombre del proyecto -->
            <div class="flex items-center space-x-4 md:space-x-8">
                <div class="flex items-center space-x-2 md:space-x-3">
                    <svg class="w-6 h-6 md:w-8 md:h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <!-- Icono SVG -->
                    </svg>
                    <h1 class="text-lg md:text-xl font-light text-gray-900">PAQUETES EL CLUB</h1>
                </div>

                <!-- Navegación Desktop -->
                <nav class="hidden md:flex items-center space-x-6">
                    <a href="#" class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors font-medium">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <!-- Icono SVG -->
                        </svg>
                        <span>Anunciar</span>
                    </a>
                    <a href="#" class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors font-medium">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <!-- Icono SVG -->
                        </svg>
                        <span>Consulta</span>
                    </a>
                </nav>
            </div>

            <!-- Acciones -->
            <div class="flex items-center">
                <a href="#" class="bg-gray-900 text-white px-3 py-2 md:px-4 md:py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors text-sm md:text-base">
                    Iniciar Sesión
                </a>
            </div>

            <!-- Botón de menú móvil -->
            <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 text-gray-700 hover:text-blue-600 transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path x-show="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    <path x-show="mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        </div>

        <!-- Menú móvil -->
        <div x-show="mobileMenuOpen" 
             x-transition:enter="transition ease-out duration-200"
             x-transition:enter-start="opacity-0 -translate-y-2"
             x-transition:enter-end="opacity-100 translate-y-0"
             x-transition:leave="transition ease-in duration-150"
             x-transition:leave-start="opacity-100 translate-y-0"
             x-transition:leave-end="opacity-0 -translate-y-2"
             class="md:hidden border-t border-gray-200 pt-4 pb-4">
            
            <nav class="flex flex-col space-y-3">
                <a href="#" class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors font-medium py-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <!-- Icono SVG -->
                    </svg>
                    <span>Anunciar</span>
                </a>
                <a href="#" class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors font-medium py-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <!-- Icono SVG -->
                    </svg>
                    <span>Consulta</span>
                </a>
            </nav>
        </div>
    </div>
</header>
```

### 2. Footer Component (Sticky Footer)
```html
<!-- Estructura base del footer responsivo con sticky footer -->
<footer class="bg-white shadow-sm border-t flex-shrink-0">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center py-4 space-y-2 sm:space-y-0">
            <!-- Copyright -->
            <div class="text-sm text-gray-500 text-center sm:text-left">
                &copy; 2024 PAQUETES EL CLUB. Todos los derechos reservados.
            </div>
            
            <!-- Enlaces -->
            <div class="flex items-center justify-center sm:justify-end space-x-4">
                <a href="#" class="text-gray-500 hover:text-gray-900 transition-colors text-sm flex items-center space-x-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <!-- Icono SVG -->
                    </svg>
                    <span>Ayuda</span>
                </a>
                <a href="#" class="text-gray-500 hover:text-gray-900 transition-colors text-sm flex items-center space-x-1">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                        <!-- Icono WhatsApp -->
                    </svg>
                    <span>WhatsApp</span>
                </a>
                <a href="#" class="text-gray-500 hover:text-gray-900 transition-colors text-sm flex items-center space-x-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <!-- Icono Teléfono -->
                    </svg>
                    <span>Teléfono</span>
                </a>
            </div>
        </div>
    </div>
</footer>
```

### 3. Card Component
```html
<!-- Estructura base de tarjetas responsivas -->
<div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-all duration-200">
    <div class="flex items-center space-x-3">
        <div class="bg-gray-100 rounded-lg p-2">
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <!-- Icono SVG -->
            </svg>
        </div>
        <div>
            <h3 class="text-sm font-medium text-gray-600 uppercase tracking-wide">Título</h3>
            <p class="text-2xl font-bold text-gray-900">Valor</p>
        </div>
    </div>
</div>
```

### 4. Navigation Menu Component
```html
<!-- Menú de navegación responsivo -->
<nav class="bg-white shadow-sm border-b sticky top-0 z-50" x-data="{ mobileMenuOpen: false }">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center py-4">
            <h1 class="text-lg sm:text-xl md:text-2xl font-bold text-gray-900">🎨 Demo - PAQUETES EL CLUB</h1>
            
            <!-- Navegación Desktop -->
            <div class="hidden md:flex space-x-2">
                <button @click="currentSection = 'header'" class="px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">Header</button>
                <button @click="currentSection = 'forms'" class="px-3 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 text-sm">Formularios</button>
                <button @click="currentSection = 'dashboard'" class="px-3 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 text-sm">Dashboard</button>
                <button @click="currentSection = 'helpdesk'" class="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm">Helpdesk</button>
                <button @click="currentSection = 'footer'" class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">Footer</button>
            </div>
            
            <!-- Botón de menú móvil -->
            <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 text-gray-700 hover:text-gray-900">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path x-show="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    <path x-show="mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        </div>
        
        <!-- Menú móvil -->
        <div x-show="mobileMenuOpen" 
             x-transition:enter="transition ease-out duration-200"
             x-transition:enter-start="opacity-0 -translate-y-2"
             x-transition:enter-end="opacity-100 translate-y-0"
             x-transition:leave="transition ease-in duration-150"
             x-transition:leave-start="opacity-100 translate-y-0"
             x-transition:leave-end="opacity-0 -translate-y-2"
             class="md:hidden border-t border-gray-200 pt-4 pb-4">
            <div class="grid grid-cols-2 gap-2">
                <button @click="currentSection = 'header'; mobileMenuOpen = false" class="px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">Header</button>
                <button @click="currentSection = 'forms'; mobileMenuOpen = false" class="px-3 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 text-sm">Formularios</button>
                <button @click="currentSection = 'dashboard'; mobileMenuOpen = false" class="px-3 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 text-sm">Dashboard</button>
                <button @click="currentSection = 'helpdesk'; mobileMenuOpen = false" class="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm">Helpdesk</button>
                <button @click="currentSection = 'footer'; mobileMenuOpen = false" class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">Footer</button>
            </div>
        </div>
    </div>
</nav>
```

---

## 📝 Formularios

### 1. Input con Icono
```html
<!-- Estructura base para inputs con icono -->
<div class="input-with-icon">
    <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <!-- Icono SVG -->
    </svg>
    <input type="text" class="w-full px-0 py-3 border-0 border-b-2 border-gray-200 focus:border-blue-600 focus:ring-0 bg-transparent transition-colors" placeholder="Placeholder">
</div>
```

### 2. Select con Icono
```html
<!-- Estructura base para selects con icono -->
<div class="select-with-icon">
    <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <!-- Icono SVG -->
    </svg>
    <select class="w-full px-0 py-3 border-0 border-b-2 border-gray-200 focus:border-blue-600 focus:ring-0 bg-transparent transition-colors">
        <option>Opción 1</option>
        <option>Opción 2</option>
    </select>
</div>
```

### 3. Select Múltiple
```html
<!-- Estructura base para selects múltiples -->
<div class="relative">
    <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
        <svg class="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <!-- Icono SVG -->
        </svg>
        Título del Campo
    </label>
    <select multiple class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-1 focus:ring-blue-500 bg-white transition-colors">
        <option>Opción 1</option>
        <option>Opción 2</option>
    </select>
</div>
```

### 4. Formulario Responsivo
```html
<!-- Estructura base para formularios responsivos -->
<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
    <div class="bg-white rounded-xl shadow-lg border border-gray-100">
        <!-- Header del formulario -->
        <div class="border-b border-gray-100 px-4 sm:px-8 py-4 sm:py-6">
            <div class="text-center">
                <img src="assets/images/papyrus-logo.png" alt="PAPYRUS Logo" class="h-12 sm:h-16 mx-auto mb-4">
                <h2 class="text-xl sm:text-2xl font-light text-gray-900">Título del Formulario</h2>
                <p class="text-sm text-gray-500 mt-1">Descripción del formulario</p>
            </div>
        </div>
        
        <!-- Contenido del formulario -->
        <div class="p-4 sm:p-8">
            <form class="space-y-6">
                <!-- Grid responsivo para campos -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Campos de formulario -->
                </div>
                
                <!-- Grid responsivo para campos de 3 columnas -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
                    <!-- Campos de formulario -->
                </div>
            </form>
        </div>
    </div>
</div>
```

### 2. Select con Icono
```html
<!-- Estructura base para selects con icono -->
<div class="select-with-icon">
    <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <!-- Icono SVG -->
    </svg>
    <select class="w-full px-0 py-3 border-0 border-b-2 border-gray-200 focus:border-blue-600 focus:ring-0 bg-transparent transition-colors">
        <option>Opción 1</option>
        <option>Opción 2</option>
    </select>
</div>
```

### 3. Select Múltiple
```html
<!-- Estructura base para selects múltiples -->
<div class="relative">
    <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
        <svg class="w-4 h-4 mr-2 text-gray-500">...</svg>
        Título del Campo
    </label>
    <select multiple class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-1 focus:ring-blue-500 bg-white transition-colors">
        <option>Opción 1</option>
        <option>Opción 2</option>
    </select>
</div>
```

### CSS para Formularios
```css
/* Input con icono */
.input-with-icon {
    position: relative;
}

.input-with-icon input,
.input-with-icon textarea {
    padding-left: 40px;
}

.input-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #6B7280;
    width: 20px;
    height: 20px;
    z-index: 10;
}

/* Select con icono */
.select-with-icon {
    position: relative;
}

.select-with-icon select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
    background-position: right 8px center;
    background-repeat: no-repeat;
    background-size: 16px;
    padding-left: 40px;
    padding-right: 40px;
}
```

---

## 🎯 Iconografía

### Tamaños de Iconos
```css
/* Tamaños estándar */
.w-4 h-4 { width: 1rem; height: 1rem; }    /* 16px - Iconos pequeños */
.w-5 h-5 { width: 1.25rem; height: 1.25rem; } /* 20px - Iconos de navegación */
.w-6 h-6 { width: 1.5rem; height: 1.5rem; }   /* 24px - Iconos de tarjetas */
.w-8 h-8 { width: 2rem; height: 2rem; }       /* 32px - Iconos principales */
```

### Colores de Iconos
```css
/* Estados de color */
.text-gray-500 { color: #6B7280; }    /* Iconos secundarios */
.text-gray-600 { color: #4B5563; }    /* Iconos principales */
.text-blue-600 { color: #2563EB; }    /* Iconos de acción */
.text-red-600 { color: #DC2626; }     /* Iconos de alerta */
```

### Biblioteca de Iconos
- **Heroicons**: Biblioteca principal (SVG outline)
- **Consistencia**: Todos los iconos deben ser outline style
- **Accesibilidad**: Incluir `fill="none" stroke="currentColor"`

---

## 🔄 Estados y Interacciones

### Estados de Hover
```css
/* Enlaces y botones */
.hover:text-blue-600 { color: #2563EB; }
.hover:bg-gray-50 { background-color: #F9FAFB; }
.hover:shadow-md { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }

/* Transiciones */
.transition-colors { transition: color 0.15s ease-in-out; }
.transition-all { transition: all 0.15s ease-in-out; }
.duration-200 { transition-duration: 200ms; }
```

### Estados de Focus
```css
/* Inputs y selects */
.focus:border-blue-600 { border-color: #2563EB; }
.focus:ring-1 { box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.1); }
.focus:ring-blue-500 { box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.5); }
.focus:outline-none { outline: none; }
```

### Estados de Loading
```css
/* Estado de carga */
.loading {
    opacity: 0.6;
    pointer-events: none;
}

.loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #DC2626;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

---

## 📱 Responsive Design

### Breakpoints
```css
/* Breakpoints estándar */
sm: 640px   /* Tablets pequeñas */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Pantallas grandes */
```

### Patrones Responsive
```html
<!-- Grid responsivo -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- Contenido -->
</div>

<!-- Navegación responsiva -->
<nav class="hidden md:flex items-center space-x-6">
    <!-- Navegación desktop -->
</nav>
<button class="md:hidden">
    <!-- Menú móvil -->
</button>

<!-- Contenedores responsivos -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
    <!-- Contenido principal -->
</div>

<!-- Padding responsivo -->
<div class="p-4 sm:p-8">
    <!-- Contenido con padding adaptativo -->
</div>

<!-- Texto responsivo -->
<h1 class="text-lg sm:text-xl md:text-2xl font-bold">Título Adaptativo</h1>

<!-- Iconos responsivos -->
<svg class="w-6 h-6 md:w-8 md:h-8">...</svg>

<!-- Botones responsivos -->
<button class="px-3 py-2 md:px-4 md:py-2 text-sm md:text-base">Botón</button>
```

### Componentes Responsivos Específicos

#### Dashboard Cards
```html
<!-- Grid de métricas responsivo -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 sm:mb-8">
    <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-all duration-200">
        <div class="flex items-center space-x-3">
            <div class="bg-gray-100 rounded-lg p-2">
                <svg class="w-6 h-6 text-gray-600">...</svg>
            </div>
            <div>
                <h3 class="text-sm font-medium text-gray-600 uppercase tracking-wide">Título</h3>
                <p class="text-2xl font-bold text-gray-900">Valor</p>
            </div>
        </div>
    </div>
</div>
```

#### Tabla Responsiva
```html
<!-- Tabla con columnas que se ocultan en móvil -->
<div class="overflow-x-auto">
    <table class="w-full">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tracking</th>
                <th class="hidden sm:table-cell px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                <th class="hidden md:table-cell px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Tracking</td>
                <td class="hidden sm:table-cell px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-500">Cliente</td>
                <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
                    <span class="px-2 py-1 text-xs font-medium rounded-full">Estado</span>
                </td>
                <td class="hidden md:table-cell px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-500">Fecha</td>
                <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div class="flex items-center space-x-1 sm:space-x-2">
                        <!-- Botones de acción -->
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

#### Filtros Responsivos
```html
<!-- Filtros que se apilan en móvil -->
<div class="flex flex-col sm:flex-row sm:flex-wrap sm:justify-between sm:items-center gap-4 mb-6">
    <div class="flex flex-wrap gap-2">
        <button class="px-3 py-2 text-sm rounded transition-colors">Filtro 1</button>
        <button class="px-3 py-2 text-sm rounded transition-colors">Filtro 2</button>
    </div>
    <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
        <button class="w-full sm:w-auto px-3 py-2 text-sm rounded transition-colors">Acción 1</button>
        <button class="w-full sm:w-auto px-3 py-2 text-sm rounded transition-colors">Acción 2</button>
    </div>
</div>
```

### Mobile-First Approach
- **Base**: Estilos para móvil (sin prefijos)
- **Progresivo**: Mejoras para pantallas más grandes
- **Touch-friendly**: Tamaños mínimos de 44px para elementos táctiles
- **Menús móviles**: Implementación con Alpine.js y transiciones suaves
- **Grid adaptativo**: Columnas que se ajustan según el dispositivo
- **Contenido prioritario**: Información más importante visible en móvil

---

## ⚙️ Implementación Técnica

### Stack Tecnológico
```html
<!-- Dependencias base -->
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
<script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
```

### Configuración de Tailwind
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'papyrus-red': '#DC2626',
                'papyrus-orange': '#F97316',
                'papyrus-yellow': '#F59E0B',
                'papyrus-green': '#10B981',
                'papyrus-blue': '#3B82F6',
                primary: '#3B82F6',
                secondary: '#10B981',
                accent: '#F59E0B',
            }
        }
    }
}
```

### Estructura de Archivos
```
CODE/design-system/
├── assets/
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       └── papyrus-logo.png
├── components/
│   ├── header.html
│   └── footer.html
├── forms/
│   └── client/
│       ├── announce-package.html
│       └── track-package.html
├── admin/
│   └── dashboard.html
├── helpdesk/
│   └── ticket-list.html
├── demo-simple.html
└── PRD-Sistema-Diseno-PAPYRUS-v3.0.md
```

### Características Responsive Implementadas

#### Layout Principal
- **Sticky Footer**: Implementado con flexbox para mantener el footer siempre al fondo
- **Body flexbox**: `flex flex-col` para layout vertical flexible
- **Header fijo**: `flex-shrink-0` para mantener tamaño constante
- **Contenido expandible**: `flex-grow` para ocupar espacio disponible
- **Footer pegado**: `flex-shrink-0` para mantener posición al fondo

#### Navegación
- **Menú hamburguesa**: Funcional con Alpine.js
- **Transiciones suaves**: Animaciones para abrir/cerrar
- **Grid responsivo**: Botones organizados en móvil
- **Título adaptativo**: Tamaño que se ajusta al dispositivo

#### Header
- **Menú móvil integrado**: Navegación colapsable
- **Iconos adaptativos**: Tamaños responsivos
- **Espaciado responsivo**: Diferentes espaciados por dispositivo
- **Botón de login**: Tamaño y padding adaptativos

#### Formularios
- **Padding responsivo**: `p-4 sm:p-8`
- **Grid adaptativo**: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`
- **Logo adaptativo**: `h-12 sm:h-16`
- **Títulos responsivos**: `text-xl sm:text-2xl`

#### Dashboard
- **Métricas responsivas**: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`
- **Tabla adaptativa**: Columnas que se ocultan en móvil
- **Filtros apilados**: Layout vertical en móvil
- **Botones adaptativos**: Tamaños y espaciado responsivos

#### Helpdesk
- **Filtros responsivos**: Layout vertical en móvil
- **Tarjetas adaptativas**: Información reorganizada
- **Botones de acción**: Mejor espaciado y hover states
- **Prioridades**: Badges que se ajustan al contenido

#### Footer
- **Layout vertical en móvil**: Copyright y enlaces apilados
- **Centrado en móvil**: Mejor alineación para pantallas pequeñas
- **Espaciado adaptativo**: Diferentes márgenes según dispositivo
- **Sticky footer**: Siempre pegado al fondo de la pantalla
- **Flexbox layout**: `flex-shrink-0` para mantener posición fija
- **Responsive**: Se adapta al contenido sin afectar el layout principal

---

## ✅ Checklist de Componentes

### Antes de Crear un Nuevo Componente

#### ✅ Estructura Base
- [ ] Usar contenedor `max-w-7xl` para páginas principales
- [ ] Usar contenedor `max-w-4xl` para formularios
- [ ] Implementar padding consistente `px-4 sm:px-6 lg:px-8`
- [ ] Usar grid responsivo cuando sea apropiado

#### ✅ Estilos Visuales
- [ ] Aplicar `bg-white` para fondos de componentes
- [ ] Usar `shadow-sm` para sombras sutiles
- [ ] Implementar `border border-gray-200` para bordes
- [ ] Aplicar `rounded-lg` para esquinas redondeadas

#### ✅ Tipografía
- [ ] Usar `font-light` para títulos principales
- [ ] Implementar `text-gray-900` para texto principal
- [ ] Usar `text-gray-500` para texto secundario
- [ ] Aplicar jerarquía de tamaños consistente

#### ✅ Interacciones
- [ ] Implementar `hover:` states para elementos interactivos
- [ ] Usar `transition-colors` para transiciones suaves
- [ ] Aplicar `focus:` states para accesibilidad
- [ ] Incluir `cursor: pointer` para elementos clickeables

#### ✅ Iconografía
- [ ] Usar Heroicons outline style
- [ ] Implementar tamaños estándar (w-4, w-5, w-6, w-8)
- [ ] Aplicar colores consistentes
- [ ] Incluir `fill="none" stroke="currentColor"`

#### ✅ Responsive
- [ ] Implementar mobile-first approach
- [ ] Usar breakpoints apropiados (sm:, md:, lg:)
- [ ] Ocultar/mostrar elementos según el dispositivo
- [ ] Ajustar espaciado para móviles
- [ ] Implementar menús móviles con Alpine.js
- [ ] Usar padding responsivo (p-4 sm:p-8)
- [ ] Aplicar texto responsivo (text-lg sm:text-xl md:text-2xl)
- [ ] Implementar iconos adaptativos (w-6 h-6 md:w-8 md:h-8)
- [ ] Usar botones responsivos (px-3 py-2 md:px-4 md:py-2)
- [ ] Implementar tablas con columnas ocultas en móvil
- [ ] Usar filtros que se apilan en dispositivos pequeños
- [ ] Implementar sticky footer con flexbox (flex flex-col en body)
- [ ] Usar flex-shrink-0 para header y footer
- [ ] Aplicar flex-grow al contenido principal

#### ✅ Accesibilidad
- [ ] Incluir `alt` text para imágenes
- [ ] Usar `aria-label` para iconos sin texto
- [ ] Implementar navegación por teclado
- [ ] Mantener contraste de color adecuado

---

## 📋 Criterios de Aceptación

### Para Cada Componente Nuevo

1. **Consistencia Visual**
   - [ ] Sigue la paleta de colores establecida
   - [ ] Usa la tipografía definida
   - [ ] Mantiene el espaciado consistente

2. **Funcionalidad**
   - [ ] Funciona correctamente en todos los dispositivos
   - [ ] Implementa estados de hover y focus
   - [ ] Maneja errores y estados de carga

3. **Accesibilidad**
   - [ ] Es navegable por teclado
   - [ ] Tiene contraste de color adecuado
   - [ ] Incluye textos alternativos

4. **Performance**
   - [ ] Carga rápidamente
   - [ ] No causa reflows innecesarios
   - [ ] Optimizado para móviles

---

## 🔄 Proceso de Desarrollo

### 1. Planificación
- Revisar este PRD antes de crear componentes
- Identificar patrones existentes aplicables
- Definir estructura y funcionalidad

### 2. Implementación
- Seguir las estructuras base definidas
- Usar las clases CSS establecidas
- Implementar responsive design

### 3. Revisión
- Verificar checklist de componentes
- Probar en diferentes dispositivos
- Validar accesibilidad

### 4. Documentación
- Actualizar este PRD si es necesario
- Documentar nuevos patrones
- Mantener ejemplos actualizados

---

## 📞 Soporte y Mantenimiento

### Contacto
- **Equipo de Diseño**: Para consultas sobre estilos
- **Equipo de Desarrollo**: Para implementación técnica
- **QA**: Para validación de componentes

### Actualizaciones
- Este documento se actualiza con cada nueva versión
- Los cambios se comunican al equipo completo
- Se mantiene versionado junto con el código

---

**Versión**: 3.2  
**Fecha**: Enero 2024  
**Autor**: Equipo PAPYRUS  
**Estado**: Aprobado para implementación  
**Última actualización**: Sticky Footer implementado con flexbox layout

