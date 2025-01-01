// PAPYRUS - Sistema de Paquetería v3.0
// Funciones principales y utilidades

// Configuración global de Alpine.js
document.addEventListener('alpine:init', () => {
    // Store global para el estado de la aplicación
    Alpine.store('papyrus', {
        // Estado del usuario
        user: null,
        isAuthenticated: false,
        userRole: null,
        
        // Estado de la aplicación
        isLoading: false,
        notifications: [],
        currentPage: 'home',
        
        // Métodos
        setUser(userData) {
            this.user = userData;
            this.isAuthenticated = true;
            this.userRole = userData.role;
        },
        
        logout() {
            this.user = null;
            this.isAuthenticated = false;
            this.userRole = null;
            window.location.href = '/';
        },
        
        addNotification(message, type = 'info') {
            const notification = {
                id: Date.now(),
                message,
                type,
                timestamp: new Date()
            };
            this.notifications.push(notification);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                this.removeNotification(notification.id);
            }, 5000);
        },
        
        removeNotification(id) {
            this.notifications = this.notifications.filter(n => n.id !== id);
        },
        
        setLoading(loading) {
            this.isLoading = loading;
        }
    });

    // Componente para formularios
    Alpine.data('papyrusForm', (config = {}) => ({
        form: config.initialData || {},
        errors: {},
        isSubmitting: false,
        
        async submit() {
            this.isSubmitting = true;
            this.errors = {};
            
            try {
                const response = await fetch(config.endpoint, {
                    method: config.method || 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify(this.form)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    if (config.onSuccess) {
                        config.onSuccess(result);
                    }
                    Alpine.store('papyrus').addNotification('Operación exitosa', 'success');
                } else {
                    const errorData = await response.json();
                    this.errors = errorData.errors || {};
                    Alpine.store('papyrus').addNotification('Error en la operación', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                Alpine.store('papyrus').addNotification('Error de conexión', 'error');
            } finally {
                this.isSubmitting = false;
            }
        },
        
        validate() {
            this.errors = {};
            let isValid = true;
            
            if (config.validation) {
                const validationResult = config.validation(this.form);
                this.errors = validationResult.errors || {};
                isValid = validationResult.isValid;
            }
            
            return isValid;
        },
        
        reset() {
            this.form = config.initialData || {};
            this.errors = {};
        }
    }));

    // Componente para tablas de datos
    Alpine.data('papyrusTable', (config = {}) => ({
        data: [],
        filteredData: [],
        searchTerm: '',
        currentPage: 1,
        itemsPerPage: config.itemsPerPage || 10,
        sortBy: config.sortBy || null,
        sortDirection: 'asc',
        
        init() {
            this.loadData();
        },
        
        async loadData() {
            Alpine.store('papyrus').setLoading(true);
            try {
                const response = await fetch(config.endpoint);
                const result = await response.json();
                this.data = result.data || [];
                this.filteredData = [...this.data];
            } catch (error) {
                console.error('Error loading data:', error);
                Alpine.store('papyrus').addNotification('Error cargando datos', 'error');
            } finally {
                Alpine.store('papyrus').setLoading(false);
            }
        },
        
        filter() {
            if (!this.searchTerm) {
                this.filteredData = [...this.data];
            } else {
                this.filteredData = this.data.filter(item => 
                    Object.values(item).some(value => 
                        String(value).toLowerCase().includes(this.searchTerm.toLowerCase())
                    )
                );
            }
            this.currentPage = 1;
        },
        
        sort(column) {
            if (this.sortBy === column) {
                this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortBy = column;
                this.sortDirection = 'asc';
            }
            
            this.filteredData.sort((a, b) => {
                const aVal = a[column];
                const bVal = b[column];
                
                if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
                if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
                return 0;
            });
        },
        
        get paginatedData() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredData.slice(start, end);
        },
        
        get totalPages() {
            return Math.ceil(this.filteredData.length / this.itemsPerPage);
        },
        
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        }
    }));

    // Componente para notificaciones
    Alpine.data('papyrusNotifications', () => ({
        notifications: Alpine.store('papyrus').notifications,
        
        get notificationClasses() {
            return {
                'info': 'bg-blue-50 border-blue-200 text-blue-800',
                'success': 'bg-green-50 border-green-200 text-green-800',
                'warning': 'bg-yellow-50 border-yellow-200 text-yellow-800',
                'error': 'bg-red-50 border-red-200 text-red-800'
            };
        }
    }));
});

// Utilidades globales
window.PapyrusUtils = {
    // Formatear números de teléfono
    formatPhone(phone) {
        if (!phone) return '';
        const cleaned = phone.replace(/\D/g, '');
        const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
        if (match) {
            return '(' + match[1] + ') ' + match[2] + '-' + match[3];
        }
        return phone;
    },
    
    // Formatear fechas
    formatDate(date, format = 'short') {
        if (!date) return '';
        const d = new Date(date);
        
        if (format === 'short') {
            return d.toLocaleDateString('es-ES');
        } else if (format === 'long') {
            return d.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
        
        return d.toLocaleDateString('es-ES');
    },
    
    // Generar número de tracking
    generateTrackingNumber() {
        const prefix = 'PAP';
        const timestamp = Date.now().toString().slice(-6);
        const random = Math.random().toString(36).substr(2, 4).toUpperCase();
        return `${prefix}${timestamp}${random}`;
    },
    
    // Validar email
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    // Validar teléfono
    validatePhone(phone) {
        const cleaned = phone.replace(/\D/g, '');
        return cleaned.length >= 10;
    },
    
    // Copiar al portapapeles
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            Alpine.store('papyrus').addNotification('Copiado al portapapeles', 'success');
        } catch (error) {
            console.error('Error copying to clipboard:', error);
            Alpine.store('papyrus').addNotification('Error al copiar', 'error');
        }
    }
};

// Configuración de HTMX
document.body.addEventListener('htmx:configRequest', (event) => {
    // Agregar headers personalizados si es necesario
    event.detail.headers['X-Requested-With'] = 'XMLHttpRequest';
});

document.body.addEventListener('htmx:beforeRequest', (event) => {
    // Mostrar loading
    Alpine.store('papyrus').setLoading(true);
});

document.body.addEventListener('htmx:afterRequest', (event) => {
    // Ocultar loading
    Alpine.store('papyrus').setLoading(false);
    
    // Manejar respuestas de error
    if (event.detail.xhr.status >= 400) {
        Alpine.store('papyrus').addNotification('Error en la solicitud', 'error');
    }
});

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Configurar tooltips y otros elementos interactivos
    console.log('PAPYRUS Sistema de Paquetería v3.0 - Inicializado');
});
