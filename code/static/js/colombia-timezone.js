/**
 * Utilidades de Zona Horaria de Colombia - PAQUETES EL CLUB v3.1
 * =============================================================
 * 
 * Funciones para formatear fechas y horas en zona horaria de Colombia (America/Bogota)
 */

// Configuración de zona horaria de Colombia
const COLOMBIA_TIMEZONE = 'America/Bogota';
const COLOMBIA_LOCALE = 'es-CO';

/**
 * Convierte una fecha UTC a zona horaria de Colombia
 * @param {string|Date} utcDate - Fecha UTC
 * @returns {Date} Fecha en zona horaria de Colombia
 */
function convertUTCToColombia(utcDate) {
    const date = new Date(utcDate);
    
    // Colombia está en UTC-5 (sin horario de verano)
    const colombiaOffset = -5 * 60; // -5 horas en minutos
    const utcOffset = date.getTimezoneOffset(); // Offset local en minutos
    
    // Calcular la diferencia total
    const totalOffset = colombiaOffset + utcOffset;
    
    // Crear nueva fecha con el offset aplicado
    const colombiaDate = new Date(date.getTime() + (totalOffset * 60 * 1000));
    
    return colombiaDate;
}

/**
 * Formatea una fecha en zona horaria de Colombia
 * @param {string|Date} date - Fecha a formatear
 * @param {Object} options - Opciones de formateo
 * @returns {string} Fecha formateada
 */
function formatColombiaDate(date, options = {}) {
    try {
        // Primero convertir a zona horaria de Colombia
        const colombiaDate = convertUTCToColombia(date);
        
        const defaultOptions = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        return colombiaDate.toLocaleString(COLOMBIA_LOCALE, finalOptions);
    } catch (error) {
        console.error('Error formateando fecha de Colombia:', error);
        // Fallback: mostrar la fecha original
        return new Date(date).toLocaleString(COLOMBIA_LOCALE);
    }
}

/**
 * Formatea solo la fecha (sin hora) en zona horaria de Colombia
 * @param {string|Date} date - Fecha a formatear
 * @returns {string} Fecha formateada
 */
function formatColombiaDateOnly(date) {
    return formatColombiaDate(date, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Formatea solo la hora en zona horaria de Colombia
 * @param {string|Date} date - Fecha a formatear
 * @returns {string} Hora formateada
 */
function formatColombiaTimeOnly(date) {
    return formatColombiaDate(date, {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

/**
 * Formatea fecha y hora completa en zona horaria de Colombia
 * @param {string|Date} date - Fecha a formatear
 * @returns {string} Fecha y hora formateada
 */
function formatColombiaDateTime(date) {
    return formatColombiaDate(date, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

/**
 * Obtiene la fecha actual en zona horaria de Colombia
 * @returns {Date} Fecha actual en Colombia
 */
function getColombiaNow() {
    const now = new Date();
    return convertUTCToColombia(now);
}

/**
 * Verifica si una fecha está en zona horaria de Colombia
 * @param {string|Date} date - Fecha a verificar
 * @returns {boolean} True si está en zona horaria de Colombia
 */
function isColombiaTimezone(date) {
    try {
        const colombiaDate = convertUTCToColombia(date);
        const originalDate = new Date(date);
        return colombiaDate.getTime() !== originalDate.getTime();
    } catch (error) {
        return false;
    }
}

/**
 * Función de debug para mostrar información de zona horaria
 * @param {string|Date} date - Fecha a debuggear
 */
function debugTimezone(date) {
    const originalDate = new Date(date);
    const colombiaDate = convertUTCToColombia(date);
    
    console.log('🌍 Debug de Zona Horaria:');
    console.log('Fecha original:', originalDate.toISOString());
    console.log('Fecha UTC:', originalDate.toUTCString());
    console.log('Fecha local:', originalDate.toLocaleString());
    console.log('Fecha Colombia:', colombiaDate.toLocaleString(COLOMBIA_LOCALE));
    console.log('Offset local:', originalDate.getTimezoneOffset(), 'minutos');
    console.log('Offset Colombia:', -5 * 60, 'minutos');
}

// Exportar funciones para uso global
window.ColombiaTimezone = {
    formatDate: formatColombiaDate,
    formatDateOnly: formatColombiaDateOnly,
    formatTimeOnly: formatColombiaTimeOnly,
    formatDateTime: formatColombiaDateTime,
    getNow: getColombiaNow,
    convertUTC: convertUTCToColombia,
    isColombiaTimezone: isColombiaTimezone,
    debugTimezone: debugTimezone,
    TIMEZONE: COLOMBIA_TIMEZONE,
    LOCALE: COLOMBIA_LOCALE
};

// Log de inicialización
console.log('🌍 Utilidades de zona horaria de Colombia cargadas');
console.log(`📍 Zona horaria: ${COLOMBIA_TIMEZONE}`);
console.log(`🌐 Locale: ${COLOMBIA_LOCALE}`);
console.log('🕐 Offset Colombia: UTC-5 (sin horario de verano)');
