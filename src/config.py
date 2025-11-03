

# =============================================================================
# RESPONSABILIDAD ÚNICA DE ESTE MODULO
# Configuración centralizada del proyecto - y la opción de modificarlas por 
# el usuario.
# =============================================================================

from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# =============================================================================
# PARÁMETROS CONFIGURABLES POR EL USUARIO
# -----------------------------------------------------------------------------
# Esta sección contiene los parámetros principales que se pueden ajustar
# para modificar el comportamiento del workflow, como la fuente de datos
# y los modelos de IA a utilizar.
# =============================================================================

# ---- Fuente de Datos ----
# Establece en True para utilizar MongoDB; False para usar CSV local.
USE_MONGO_DB = False

# Archivo CSV a usar cuando USE_MONGO_DB = False
# Archivos disponibles en /data: "coffee_sales.csv", "retail_sales_dataset.csv"
DATA_FILENAME = "coffee_sales.csv"

# ---- Modelos de IA ----
# Modelos disponibles para las diferentes tareas
GENERATION_MODEL = "gpt-4o-mini"  # Para generar código inicial
REFLECTION_MODEL = "o4-mini-2025-04-16"  # Para reflexionar y mejorar

# ---- Instrucciones del Workflow ----
# Instrucción por defecto para el proceso de generación de gráficos
DEFAULT_WORKFLOW_INSTRUCTION = "Create a plot comparing Q1 sales in 2024 and 2025."

# ---- API (gráficos web) ----
# Nombre base para archivos generados por la API web
API_IMAGE_BASENAME = "api_chart_comparison"

# =============================================================================
# CONFIGURACIÓN AUTOMÁTICA (No tocar)
# =============================================================================

# ---- Rutas del Proyecto ----
# Se definen rutas dinámicas y absolutas para garantizar que el proyecto
# funcione en cualquier máquina, independientemente de dónde se clone o ejecute.
# Este enfoque evita problemas comunes de rutas relativas y rutas "hardcodeadas".

# 1. `PROJECT_ROOT`: Se establece como la carpeta raíz del proyecto.
#    - `Path(__file__)`: Obtiene la ruta del archivo actual (`config.py`).
#    - `.parent`: Sube un nivel al directorio `src`.
#    - `.parent`: Sube otro nivel a la raíz del proyecto (`lumina`).
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. `DATA_DIR` y `OUTPUTS_DIR`: Se construyen de forma segura a partir de la raíz.
#    El operador `/` de pathlib garantiza la compatibilidad entre sistemas
#    operativos (Windows, macOS, Linux).
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
