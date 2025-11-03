# 📊 Guía del Notebook ETL - Análisis de Datos

*Sistema completo de análisis con pipeline ETL automatizado*

## 🎯 Introducción

Este notebook transforma archivos CSV en análisis profesionales mediante un pipeline ETL automatizado. Diseñado para ser flexible y reutilizable con cualquier dataset.

## ⚡ Configuración Rápida

### Paso 1: Preparar tu Datos

1. Coloca tu archivo CSV en la carpeta `/data/`
2. Anota el nombre exacto del archivo

### Paso 2: Configurar el Notebook

```python
# ════════════════════════════════════════
# CONFIGURACIÓN - SOLO CAMBIA ESTO
# ════════════════════════════════════════
csv_filename = 'coffee_sales.csv'  # ← CAMBIA AQUÍ tu archivo
```

### Paso 3: Ejecutar Análisis

Ejecuta las celdas en orden para obtener:
- 8 visualizaciones profesionales
- Análisis temporal automático
- Métricas ejecutivas
- Estadísticas descriptivas

## 📈 Análisis Incluidos

| Gráfico | Tipo | Información |
|---------|------|-------------|
| **Ventas por Mes** | Líneas | Tendencias temporales |
| **Top 10 Productos** | Barras | Productos más populares |
| **Métodos de Pago** | Torta | Distribución de canales |
| **Ventas por Trimestre** | Barras | Performance trimestral |
| **Distribución de Precios** | Histograma | Segmentación de precios |
| **Patrones por Hora** | Líneas | Horas de mayor actividad |
| **Heatmap Temporal** | Mapa calor | Correlación mes vs hora |
| **Resumen Ejecutivo** | KPIs | Métricas del negocio |

## 🔄 Pipeline ETL

### EXTRACT (Extraer)
- Carga datos desde CSV
- Detección automática de estructura
- Validación de formato

### TRANSFORM (Transformar)
- Enriquecimiento automático de fechas:
  - **month**: Mes extraído de fechas
  - **quarter**: Trimestre calculado
  - **year**: Año identificado
- Limpieza de datos
- Preparación para análisis

### LOAD (Cargar)
- DataFrame enriquecido
- Listo para visualización
- Optimizado para métricas

## 🚀 Uso Paso a Paso

### 1. Configuración Inicial
```python
# Celda 1: Solo cambiar csv_filename
csv_filename = 'tu_archivo.csv'
```

### 2. Carga Automática
```python
# Celda 2: Sistema detecta estructura automáticamente
# No necesitas modificar nada aquí
```

### 3. Exploración de Datos
```python
# Celda 3: Información general del dataset
# Muestra dimensiones, columnas, primeros registros
```

### 4. Análisis Detallado
```python
# Celda 4: Información técnica completa
# Tipos de datos, estadísticas, valores únicos
```

### 5. Calidad de Datos
```python
# Celda 5: Análisis de calidad
# Valores faltantes, duplicados, inconsistencias
```

### 6-13. Visualizaciones
```python
# Celdas 6-13: 8 gráficos profesionales
# Cada uno con análisis específico y métricas
```

## 📊 Tipos de Datos Soportados

### ✅ Formatos Compatibles
- CSV con encabezados
- Archivos con columna 'date' (recomendado)
- Datos numéricos y categóricos
- Fechas en formato YYYY-MM-DD

### 📅 Columnas Automáticas
Si tu dataset tiene una columna 'date', el sistema creará automáticamente:
- `month`: Mes (1-12)
- `quarter`: Trimestre (1-4)
- `year`: Año

## 🎨 Personalización

### Colores de Gráficos
Los gráficos usan una paleta de colores café profesional:
- Marrones y beiges para temas cálidos
- Colores diferenciados para categorías
- Alta legibilidad en presentaciones

### Formato de Salida
- Gráficos en alta resolución
- Formato PNG para insertar en reportes
- Títulos descriptivos en español
- Estadísticas incluidas en consola

## 📁 Estructura del Proyecto

```
notebook/
└── etl.ipynb           # Notebook principal

data/
├── coffee_sales.csv    # Dataset de ejemplo
├── retail_sales_dataset.csv  # Otro ejemplo
└── tu_archivo.csv      # ← Pon aquí tu archivo

docs/
└── notebook-etl.md     # Esta documentación
```

## 🔧 Solución de Problemas

### Archivo no encontrado
```
❌ Error: No se encontró el archivo
```
**Solución**: Verifica que el archivo esté en `/data/` y el nombre sea exacto

### Datos sin fechas
```
⚠️ Advertencia: No se encontró columna 'date'
```
**Solución**: El análisis temporal no estará disponible, pero otros gráficos sí

### Memoria insuficiente
```
MemoryError: No hay suficiente memoria
```
**Solución**: Filtra tu dataset o usa una muestra más pequeña

## 📈 Ejemplos de Uso

### Análisis de Ventas
```
csv_filename = 'ventas_mensuales.csv'
→ Gráficos de tendencias por mes
→ Análisis de productos populares
→ Patrones de pago
```

### Análisis de Marketing
```
csv_filename = 'campana_facebook.csv'
→ ROI por campaña
→ Distribución de engagement
→ Horarios óptimos
```

### Análisis Financiero
```
csv_filename = 'transacciones.csv'
→ Flujo de caja por trimestre
→ Categorización de gastos
→ Análisis de estacionalidad
```

## 🎓 Casos de Uso

### Para Analistas de Datos
- Exploración rápida de nuevos datasets
- Generación automática de reportes
- Validación de calidad de datos

### Para Equipos de Marketing
- Análisis de campañas
- ROI de productos
- Segmentación de clientes

### Para Gerentes
- Dashboards ejecutivos
- KPIs automáticos
- Métricas de performance

## 📞 Soporte

Para problemas técnicos o preguntas:
1. Verifica que el archivo CSV tenga formato correcto
2. Confirma que el nombre del archivo sea exacto
3. Revisa que todas las dependencias estén instaladas

---

*Este notebook demuestra habilidades en ETL, análisis temporal y visualización con herramientas profesionales de Python.*