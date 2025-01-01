# 📦 Códigos de Prueba con Estados Cronológicos - PAQUETES EL CLUB v3.1

## 🎯 **Códigos Disponibles para Probar Diferentes Historiales**

### **✅ Flujos Completos (Anunciado → Recibido → Entregado)**

#### **1. YJWX - MARIA GONZALEZ**
- **Guía**: GUIA000
- **Teléfono**: 3001234567
- **Estados**: ANUNCIADO → RECIBIDO → ENTREGADO
- **Estado Final**: ENTREGADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `YJWX`

#### **2. KYPU - LUISA FERNANDEZ**
- **Guía**: GUIA004
- **Teléfono**: 3005678901
- **Estados**: ANUNCIADO → RECIBIDO → ENTREGADO
- **Estado Final**: ENTREGADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `KYPU`

#### **3. VBU9 - ROBERTO SANCHEZ**
- **Guía**: GUIA007
- **Teléfono**: 3007890123
- **Estados**: ANUNCIADO → RECIBIDO → ENTREGADO
- **Estado Final**: ENTREGADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `VBU9`

#### **4. I961 - MIGUEL TORRES**
- **Guía**: GUIA009
- **Teléfono**: 3009012345
- **Estados**: ANUNCIADO → RECIBIDO → ENTREGADO
- **Estado Final**: ENTREGADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `I961`

#### **5. YDBS - TERESA RAMOS**
- **Guía**: GUIA018
- **Teléfono**: 3000000000
- **Estados**: ANUNCIADO → RECIBIDO → ENTREGADO
- **Estado Final**: ENTREGADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `YDBS`

---

### **📥 Solo Recibidos (Anunciado → Recibido)**

#### **6. Z7UH - CARLOS RODRIGUEZ**
- **Guía**: GUIA001
- **Teléfono**: 3002345678
- **Estados**: ANUNCIADO → RECIBIDO
- **Estado Final**: RECIBIDO
- **URL de Prueba**: `http://localhost/search` → Buscar: `Z7UH`

#### **7. 1TMJ - JUAN PEREZ**
- **Guía**: GUIA005
- **Teléfono**: 3006789012
- **Estados**: ANUNCIADO → RECIBIDO
- **Estado Final**: RECIBIDO
- **URL de Prueba**: `http://localhost/search` → Buscar: `1TMJ`

#### **8. AVQQ - ELENA MORALES**
- **Guía**: GUIA010
- **Teléfono**: 3001111111
- **Estados**: ANUNCIADO → RECIBIDO
- **Estado Final**: RECIBIDO
- **URL de Prueba**: `http://localhost/search` → Buscar: `AVQQ`

---

### **❌ Cancelaciones Tempranas (Anunciado → Cancelado)**

#### **9. J1NK - ANA MARTINEZ**
- **Guía**: GUIA002
- **Teléfono**: 3003456789
- **Estados**: ANUNCIADO → CANCELADO
- **Estado Final**: CANCELADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `J1NK`

#### **10. LSXI - ISABEL GARCIA**
- **Guía**: GUIA006
- **Teléfono**: 3007777777
- **Estados**: ANUNCIADO → CANCELADO
- **Estado Final**: CANCELADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `LSXI`

#### **11. MB9D - FRANCISCO JIMENEZ**
- **Guía**: GUIA011
- **Teléfono**: 3002222222
- **Estados**: ANUNCIADO → CANCELADO
- **Estado Final**: CANCELADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `MB9D`

---

### **⚠️ Cancelaciones Tardías (Anunciado → Recibido → Cancelado)**

#### **12. D3F4 - PEDRO LOPEZ**
- **Guía**: GUIA003
- **Teléfono**: 3004567890
- **Estados**: ANUNCIADO → RECIBIDO → CANCELADO
- **Estado Final**: CANCELADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `D3F4`

#### **13. EX8Z - CARMEN DIAZ**
- **Guía**: GUIA008
- **Teléfono**: 3008888888
- **Estados**: ANUNCIADO → RECIBIDO → CANCELADO
- **Estado Final**: CANCELADO
- **URL de Prueba**: `http://localhost/search` → Buscar: `EX8Z`

---

## 📊 **Resumen de Estados**

| Estado Final | Cantidad | Códigos |
|--------------|----------|---------|
| **ENTREGADO** | 5 | YJWX, KYPU, VBU9, I961, YDBS |
| **RECIBIDO** | 3 | Z7UH, 1TMJ, AVQQ |
| **CANCELADO** | 5 | J1NK, LSXI, MB9D, D3F4, EX8Z |

## 🎯 **Cómo Probar**

1. **Ir a la página de búsqueda**: `http://localhost/search`
2. **Ingresar cualquiera de los códigos** de la lista anterior
3. **Ver el historial completo** con fechas realistas
4. **Observar la línea de tiempo** con diferentes estados

## 📅 **Fechas Generadas**

- **Anunciado**: Fecha original del anuncio
- **Recibido**: 1-5 días después del anuncio
- **Entregado**: 1-3 días después de recibido
- **Cancelado**: 1-5 días después del estado anterior

## 🎨 **Estados Visuales**

- **🟢 ANUNCIADO**: Verde - Paquete anunciado por el cliente
- **🔵 RECIBIDO**: Azul - Paquete recibido en instalaciones
- **✅ ENTREGADO**: Verde con check - Paquete entregado al cliente
- **❌ CANCELADO**: Rojo - Paquete cancelado

---

**Desarrollado por JEMAVI para PAPYRUS**
**PAQUETES EL CLUB v3.1**
**Fecha**: 2025-01-24
