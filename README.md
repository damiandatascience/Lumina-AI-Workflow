# 💡 Lumina

<div align="center">

*De datos a claridad, al instante.*

<!-- Placeholder para el logo del proyecto. Reemplaza esta línea con tu imagen, por ejemplo: ![Project Logo](assets/logo.png) -->

**Lumina es un agente de IA que transforma instrucciones en lenguaje natural en visualizaciones de datos pulidas. Utilizando un avanzado AI Workflow basado en el patrón de "Reflexión", no solo genera gráficos, sino que los critica y refina para lograr una claridad y calidad excepcionales.**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org) [![FastAPI](https://img.shields.io/badge/FastAPI-0.119.x-green.svg)](https://fastapi.tiangolo.com) [![Gradio](https://img.shields.io/badge/Gradio-5.49+-orange.svg)](https://gradio.app) [![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4--mini-red.svg)](https://openai.com)

</div>

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
  - [Flujo del AI Workflow Detallado](#-flujo-del-ai-workflow-detallado)
- [📊 Análisis ETL y Visualización de Datos](#-análisis-etl-y-visualización-de-datos)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Principios de Diseño de Software](#-principios-de-diseño-de-software)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Logging](#-logging)
- [Uso Rápido](#-uso-rápido)
- [API Documentation](#-api-documentation)
- [Casos de Uso](#-casos-de-uso)
- [Desarrollo](#-desarrollo)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Créditos](#-créditos)
- [Soporte](#-soporte)

## ✨ Características Principales

### 🔄 Agentic Workflow

- **Generador**: Convierte instrucciones en lenguaje natural a código Python
- **Reflector**: Analiza visualizaciones y genera feedback crítico inteligente
- **Ejecutor**: Ejecuta código de forma segura y aislada

##  Contexto: AI Workflow vs Sistema de Agentes


Este proyecto implementa un **AI Workflow** (Agentic Workflow), no un sistema de agentes múltiples. La diferencia es fundamental: 

- **Sistema de Agentes**: Componentes autónomos que toman decisiones independientes
- **AI Workflow**: Pipeline estructurado donde diferentes componentes ejecutan pasos específicos en secuencia

### El Workflow en Contexto


```mermaid
graph LR
    subgraph "AI Workflow"
        direction LR
        A[Instrucción] --> B[Generator];
        B -- Código V1 --> C[Executor];
        C -- Gráfico V1 --> D[Reflector];
        D -- "Feedback +<br/>Código V2" --> E[Executor];
        E -- Gráfico V2 --> F[Salida];
    end
```


---

### 🌍 Interfaces Múltiples

- **API REST**: Integración fácil con otros sistemas
- **Interfaz Web**: Frontend intuitivo con Gradio
- **Línea de Comandos**: Para scripts y automatización

### 📊 Fuentes de Datos Flexibles

- Soporte para archivos CSV locales
- Conexión directa a MongoDB
- Procesamiento automático de fechas y enriquecimiento de datos

### 🎯 Visualizaciones Inteligentes

- Generación automática de gráficos con Matplotlib
- Refinamiento basado en análisis visual del workflow
- Feedback detallado en español
- Guardado automático en alta resolución (300 DPI)

## 📊 Análisis ETL y Visualización de Datos

El proyecto incluye un **notebook Jupyter completamente funcional** que implementa un pipeline ETL automatizado para análisis de datos. Para información detallada sobre configuración y uso, consulta [docs/notebook-etl.md](docs/notebook-etl.md).

## 📋 Diagramas de Flujo del Sistema

El proyecto cuenta con diagramas de flujo detallados para cada componente principal, lo que facilita la comprensión del funcionamiento interno del sistema:

- [Arquitectura General del Proyecto](docs/arquitectura-proyecto.md) - Visión completa de la arquitectura y relaciones entre componentes
- [Flujo del Main](docs/main-workflow.md) - Diagrama de flujo del orquestador principal
- [Flujo del API](docs/api-workflow.md) - Procesamiento de solicitudes en la API REST
- [Flujo de Data Processing](docs/data-processing-workflow.md) - Transformación y preparación de datos
- [Flujo del Generator](docs/generator-workflow.md) - Generación de código Python
- [Flujo del Executor](docs/executor-workflow.md) - Ejecución de código y generación de visualizaciones
- [Flujo del Reflector](docs/reflector-workflow.md) - Análisis y refinamiento de resultados
- [Flujo de la Interfaz](docs/interface-workflow.md) - Interacción con el usuario a través de Gradio

### Funciones de Utilidades

También se incluyen diagramas de flujo para las funciones principales del módulo `utils.py`:

- [get_response](docs/utils-get-response.md) - Comunicación con la API de OpenAI para generación de texto
- [image_openai_call](docs/utils-image-openai-call.md) - Análisis de imágenes con modelos de visión de OpenAI
- [encode_image_b64](docs/utils-encode-image-b64.md) - Codificación de imágenes a Base64
- [ensure_execute_python_tags](docs/utils-ensure-execute-python-tags.md) - Aseguramiento de etiquetas de ejecución de código
- [make_schema_text](docs/utils-make-schema-text.md) - Generación de esquemas de DataFrames
- [parse_reflector_response](docs/utils-parse-reflector-response.md) - Procesamiento de respuestas del reflector

# 🏗️ Arquitectura del Proyecto

## Diagrama de Arquitectura General

```mermaid
graph TB
    subgraph "Capa de Presentación"
        UI[Interfaz de Usuario]
    end
    
    subgraph "Capa de Control"
        MAIN[src/main.py]
        INTERFACE[src/interface.py]
    end
    
    subgraph "Capa de Procesamiento"
        GENERATOR[src/generator.py]
        EXECUTOR[src/executor.py]
        REFLECTOR[src/reflector.py]
        DATA_PROCESSING[src/data_processing.py]
    end
    
    subgraph "Capa de Servicios Externos"
        OPENAI[API de OpenAI]
        DATA[data/]
    end
    
    subgraph "Capa de Utilidades"
        UTILS[src/utils.py]
        CONFIG[src/config.py]
        API[src/api.py]
    end
    
    subgraph "Capa de Almacenamiento"
        OUTPUTS[outputs/]
        NOTEBOOK[notebook/]
    end
    
    UI --> MAIN
    MAIN --> INTERFACE
    INTERFACE --> GENERATOR
    GENERATOR --> EXECUTOR
    EXECUTOR --> REFLECTOR
    REFLECTOR --> GENERATOR
    
    GENERATOR --> UTILS
    EXECUTOR --> UTILS
    REFLECTOR --> UTILS
    
    UTILS --> OPENAI
    UTILS --> CONFIG
    UTILS --> API
    
    DATA_PROCESSING --> DATA
    GENERATOR --> DATA_PROCESSING
    
    EXECUTOR --> OUTPUTS
    OUTPUTS --> NOTEBOOK
```

## Descripción de Componentes

### Capa de Presentación
- **Interfaz de Usuario**: Punto de entrada para la interacción con el sistema.

### Capa de Control
- **main.py**: Orquestador principal del sistema, coordina el flujo de trabajo entre los diferentes componentes.
- **interface.py**: Maneja la interfaz de comunicación entre el usuario y el sistema.

### Capa de Procesamiento
- **generator.py**: Generador de código y soluciones basado en los requisitos y datos de entrada.
- **executor.py**: Ejecutor del código generado, responsable de ejecutar las operaciones y generar resultados.
- **reflector.py**: Analizador y refinador de resultados, proporciona feedback y mejora las soluciones generadas.
- **data_processing.py**: Módulo especializado en el procesamiento y transformación de datos.

### Capa de Servicios Externos
- **API de OpenAI**: Servicio externo utilizado para generación de texto y análisis de imágenes.
- **data/**: Directorio que contiene los datasets de entrada para el procesamiento.

### Capa de Utilidades
- **utils.py**: Módulo de utilidades que proporciona herramientas esenciales para la integración con APIs, manejo de datos y procesamiento de contenido.
- **config.py**: Módulo de configuración del sistema.
- **api.py**: Módulo que maneja las interacciones con APIs externas.

### Capa de Almacenamiento
- **outputs/**: Directorio que almacena los resultados generados por el sistema.
- **notebook/**: Directorio que contiene notebooks para análisis y documentación.

## Flujo de Trabajo Principal

1. **Inicio**: El usuario interactúa con el sistema a través de la interfaz de usuario.
2. **Coordinación**: El módulo `main.py` coordina el flujo de trabajo, iniciando el proceso a través de `interface.py`.
3. **Generación**: El `generator.py` utiliza los datos de entrada y las utilidades para generar soluciones iniciales.
4. **Ejecución**: El `executor.py` ejecuta el código generado, produciendo resultados.
5. **Reflexión**: El `reflector.py` analiza los resultados y proporciona feedback para mejorar las soluciones.
6. **Iteración**: El proceso se repite con el feedback del reflector para mejorar las soluciones generadas.
7. **Almacenamiento**: Los resultados finales se almacenan en el directorio `outputs/`.

## Integración con Servicios Externos

- **OpenAI API**: El sistema se integra con la API de OpenAI a través del módulo `utils.py` para:
  - Generación de texto mediante la función `get_response()`
  - Análisis de imágenes mediante la función `image_openai_call()`
  
- **Procesamiento de Datos**: El sistema procesa datasets almacenados en el directorio `data/` mediante el módulo `data_processing.py`.

## Dependencias entre Componentes

- **utils.py**: Es un módulo central utilizado por casi todos los demás componentes, proporcionando funcionalidades esenciales como:
  - Codificación/decodificación de imágenes
  - Comunicación con APIs
  - Procesamiento de texto
  - Manejo de datos

- **generator.py**, **executor.py**, **reflector.py**: Forman un ciclo iterativo de generación-ejecución-reflexión que permite mejorar continuamente las soluciones.

- **main.py**: Actúa como orquestador, coordinando la interacción entre todos los componentes.

## Patrones de Diseño Utilizados

1. **Patrón de Iteración Refinada**: El sistema sigue un ciclo de generación-ejecución-reflexión para mejorar continuamente las soluciones.
2. **Patrón de Modularidad**: Cada componente tiene una responsabilidad única y bien definida.
3. **Patrón de Inyección de Dependencias**: Los componentes utilizan utilidades y servicios externos a través de interfaces bien definidas.
4. **Patrón de Pipeline**: El flujo de trabajo sigue una estructura de pipeline donde cada etapa procesa y pasa datos a la siguiente.

## 🏆 Principios de Diseño de Software

Este proyecto no solo es un sistema de IA funcional, sino también una demostración de prácticas de ingeniería de software robustas, esenciales para entornos de producción.

### 1. Arquitectura Modular y de Responsabilidad Única
- Cada componente del AI Workflow (`generator`, `reflector`, `executor`) tiene una única y clara responsabilidad. Esto facilita el mantenimiento, las pruebas y la extensibilidad del sistema. Por ejemplo, para cambiar el modelo de reflexión, solo es necesario modificar `reflector.py`.

### 2. Configuración Centralizada
- Toda la configuración del sistema (claves de API, nombres de modelos, selección de fuente de datos) se gestiona desde `src/config.py` y un archivo `.env`. Esto permite adaptar el comportamiento de la aplicación sin modificar el código fuente principal, una práctica clave para el despliegue en diferentes entornos (desarrollo, producción).

### 3. Gestión de Rutas Agnóstica al Entorno
- **Problema:** Las rutas de archivo "hardcodeadas" (ej: `C:\Users\...`) o las rutas relativas simples (ej: `../data`) hacen que el software sea frágil y no portátil.
- **Solución:** El proyecto utiliza `pathlib` para calcular dinámicamente las rutas absolutas a directorios clave (`data`, `outputs`) basándose en la ubicación del archivo de configuración. Esto garantiza que el proyecto se ejecute sin errores en cualquier sistema operativo y en cualquier ubicación del sistema de archivos, un requisito indispensable para la colaboración y el despliegue con Docker o en la nube.

### 4. Interfaces Desacopladas (API y UI)
- La lógica principal del workflow (`main.py`) está completamente separada de las interfaces de usuario (`api.py`, `interface.py`). La comunicación se realiza a través de una API REST, lo que permite:
  - Ejecutar el workflow sin una interfaz gráfica (para pruebas o automatización).
  - Cambiar la interfaz web (de Gradio a Streamlit, por ejemplo) sin tocar la lógica del agente.
  - Integrar el agente con otros sistemas y servicios fácilmente.

### 5. Logging Estructurado
- Se utiliza el módulo `logging` de Python para proporcionar una traza clara de la ejecución del workflow. Esto es fundamental para la depuración, el monitoreo y la auditoría del comportamiento del agente en un entorno real.

### 🔄 Flujo del AI Workflow Detallado

1. **Entrada del Usuario**: Instrucción en lenguaje natural
2. **Análisis de Datos**: Carga y procesamiento del dataset
3. **Paso 1 - Generador**: Creación de código Python inicial (V1)
4. **Paso 2 - Ejecutor**: Generación de primera visualización
5. **Paso 3 - Reflector**: Análisis visual y generación de feedback + código V2
6. **Paso 4 - Ejecutor**: Generación de visualización refinada
7. **Salida**: Gráficos V1/V2 + feedback detallado

**Características del Workflow:**

- **Pipeline Secuencial**: Cada paso depende del anterior
- **Fail-Fast**: Si V1 falla, el workflow se detiene
- **Tolerante a Fallos**: Si V2 falla, se puede continuar con V1
- **Auditable**: Cada paso registra su progreso

## ️ Instalación y Configuración

### Requisitos Previos
- Python 3.12+
- uv (recomendado)
- API Key de OpenAI

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/lumina.git
cd lumina

# Instalar dependencias con uv
uv sync
```

### Configuración de Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# OpenAI Configuration
OPENAI_API_KEY=tu_api_key_aqui

# Data Source Configuration
DATA_FILENAME = your.csv

# MongoDB Configuration (optional)
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
MONGO_DB_NAME=nombre_db
MONGO_COLLECTION_NAME=nombre_coleccion

# Models Configuration (optional - defaults in config.py)
GENERATION_MODEL=gpt-4o-mini
REFLECTION_MODEL=o4-mini-2025-04-16
```

## 📝 Logging

Para detalles sobre la configuración y el uso del logging en el proyecto, consulta la [documentación de logging](docs/logging.md).


## 🚀 Uso Rápido

### Opción 1: Interfaz Web (Recomendado)

```bash
# Terminal 1: Iniciar API FastAPI en modo desarrollo (usando uv para acceder a las dependencias)

uv run -m fastapi dev src/api.py


# Terminal 2: Iniciar interfaz Gradio
uv run python src/interface.py
```

Luego abrir: http://localhost:7860

### Opción 2: Línea de Comandos (CLI)

Para ejecutar el workflow completo directamente desde la línea de comandos y ver los resultados en la consola.

```bash
# Ejecutar workflow directamente (como módulo)
uv run python -m src.main
```

### Opción 3: Uso Programático (para Desarrolladores)

Esta opción permite a los desarrolladores integrar y automatizar el AI Workflow de Lumina directamente en sus propios scripts o aplicaciones Python. Es ideal para casos de uso avanzados, como la generación de gráficos en lote o la incorporación de Lumina en un sistema de backend más grande.

```python
from src.main import run_workflow

# Ejecutar workflow con datos locales
results = run_workflow(
    user_instructions="Crea un gráfico comparando las ventas Q1 de 2024 y 2025",
    generation_model="gpt-4o-mini",
    reflection_model="o4-mini-2025-04-16",
    image_basename="comparison_chart"
)

print(f"V1 Chart: {results['chart_v1_path']}")
print(f"V2 Chart: {results['chart_v2_path']}")
print(f"Feedback: {results['feedback']}")
```

### Opción 4: API REST (para Integración)

El proyecto expone su funcionalidad principal a través de una API REST, lo que permite que cualquier otra aplicación (sin importar el lenguaje de programación) pueda integrarse con Lumina. Esta es la forma estándar de construir servicios escalables e interoperables. El siguiente ejemplo muestra cómo usar `curl` para solicitar una visualización desde la línea de comandos.

```bash
curl -X POST "http://localhost:8000/generate-chart/" \
  -H "Content-Type: application/json" \
  -d '{"instruction": "Visualiza la evolución mensual de ventas por región"}'
```

## 📡 API Documentation

La API de Lumina permite la integración programática del workflow de generación de visualizaciones.

### Endpoints Principales

#### `POST /generate-chart/`

Genera un gráfico usando el AI workflow.

**Request Body:**
```json
{
  "instruction": "string - Instrucción en lenguaje natural para la visualización."
}
```

**Response (200 OK):**
```json
{
  "status": "Completed|Error en V1|Error en V2",
  "v1_success": true,
  "chart_v1_path": "C:\\path\\to\\outputs\\charts\\chart_v1.png",
  "chart_v1_url": "/static/chart_v1.png",
  "feedback": "string",
  "v2_success": true, 
  "chart_v2_path": "C:\\path\\to\\outputs\\charts\\chart_v2.png",
  "chart_v2_url": "/static/chart_v2.png"
}
```
*   **Nota:** Las `_url` son rutas relativas. Para acceder a la imagen, concatena la URL del servidor (ej. `http://localhost:8000`) con la ruta de la URL (ej. `http://localhost:8000/static/chart_v1.png`).

#### `GET /`

Endpoint de "health check" para verificar que la API está en línea y funcionando.

**Response (200 OK):**
```json
{
  "message": "API de Lumina está en línea. Usa el endpoint /generate-chart/ para crear un gráfico."
}
```

### Ejemplos de Uso de API

#### Generar un gráfico y obtener su URL

```python
import requests

# URL base de la API
base_url = "http://localhost:8000"
endpoint = "/generate-chart/"

# Instrucción para la visualización
instruccion = "Compara las ventas del Q1 2024 vs Q1 2025 por producto"

try:
    response = requests.post(f"{base_url}{endpoint}", json={"instruction": instruccion})
    
    # Verificar si la petición fue exitosa
    if response.status_code == 200:
        data = response.json()
        print("Resultados del workflow:")
        print(f"  - Estado: {data.get('status')}")
        print(f"  - Feedback: {data.get('feedback')}")

        if data.get('v1_success'):
            # Construir la URL completa y clicable
            full_chart_url_v1 = f"{base_url}{data['chart_v1_url']}"
            print(f"  - URL del Gráfico V1: {full_chart_url_v1}")

        if data.get('v2_success'):
            full_chart_url_v2 = f"{base_url}{data['chart_v2_url']}"
            print(f"  - URL del Gráfico V2: {full_chart_url_v2}")
    else:
        print(f"Error en la petición: Código {response.status_code}")
        print(f"Respuesta: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Error de conexión con la API: {e}")
```

## 💡 Casos de Uso

### 📈 Análisis de Ventas Empresariales
```
"Analiza las tendencias de ventas por trimestre y compara el rendimiento entre años"
```

### 📊 Reportes Automáticos
```
"Genera un dashboard con los KPIs principales de la empresa para el último mes"
```

### 🔍 Exploración de Datos
```
"Crea visualizaciones que muestren la correlación entre precio y volumen de ventas"
```

### 📋 Presentaciones Ejecutivas
```
"Diseña gráficos profesionales para reporte mensual de la junta directiva"
```

### 🎯 Análisis Sectorial
```
"Compara el rendimiento de diferentes categorías de productos en el mercado"
```

## 👨‍💻 Desarrollo

### Estructura del Proyecto

```
lumina/
├── LICENSE                 # Información de licencia del proyecto
├── test_workflow.py        # Script de prueba para el workflow programático
├── src/                     # Código fuente principal
│   ├── main.py             # AI Workflow principal
│   ├── config.py           # Configuración centralizada
│   ├── api.py              # API REST FastAPI
│   ├── interface.py        # Interfaz Gradio
│   ├── generator.py        # Paso generador del workflow
│   ├── reflector.py        # Paso reflector del workflow
│   ├── executor.py         # Paso ejecutor del workflow
│   ├── data_processing.py  # Procesamiento de datos
│   └── utils.py            # Utilidades
├── data/                   # Datos CSV
├── outputs/                # Resultados generados
├── docs/                   # Documentación adicional
│   ├── logging.md          # Detalles sobre la configuración y uso del logging
│   └── notebook-etl.md     # Guía completa del notebook ETL
└── ... (otros archivos de configuración y entorno)
```

### Comandos de Desarrollo

```bash
# Linting y formateo
uv run ruff check src/
uv run ruff format src/

# Crear nueva versión del paquete
uv run python -m build
```

### Extensibilidad del AI Workflow

El sistema está diseñado para ser fácilmente extensible:

- **Nuevos Pasos del Workflow**: Agregar módulos en `src/` como pasos adicionales del pipeline
- **Fuentes de Datos**: Implementar adaptadores en `data_processing.py`
- **Modelos de IA**: Configurar diferentes LLMs en `config.py`
- **Formatos de Salida**: Extender el paso executor para nuevos tipos de visualizaciones
- **Pasos de Validación**: Añadir validaciones entre pasos del workflow
- **Estrategias de Fallback**: Implementar manejo de errores avanzados en el pipeline

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

### Guía de Contribución

- Seguir el estilo de código existente del AI Workflow
- Actualizar documentación del workflow según sea necesario
- Mantener retrocompatibilidad con la arquitectura de pipeline
- Considerar el impacto en el flujo secuencial del workflow
- Ejecutar linting antes de enviar cambios

## 📜 Licencia

Este proyecto está licenciado bajo la MIT License - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Créditos

Desarrollado con ❤️ usando:
- [OpenAI GPT-4](https://openai.com) - Modelos de lenguaje
- [FastAPI](https://fastapi.tiangolo.com) - Framework web
- [Gradio](https://gradio.app) - Interfaz de usuario
- [Pandas](https://pandas.pydata.org) - Análisis de datos
- [Matplotlib](https://matplotlib.org) - Visualizaciones

## 📞 Soporte

Para soporte y preguntas:
- Crear un [issue](https://github.com/tu-usuario/lumina/issues)
- Revisar la [documentación](docs/)
- Contactar a los desarrolladores

---

<div align="center">

**[⭐ Star este proyecto si te resulta útil! ⭐](https://github.com/tu-usuario/lumina)**

Hecho con Python • Diseñado para la comunidad • Construido para escalar

</div>
