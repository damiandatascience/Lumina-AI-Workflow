
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import time
import logging

# Importo la logica de workflow y la configuración 
from . import main as workflow
from . import config

# --- Establezco logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# 1. Inicializo la app de fastapi
app = FastAPI(
    title="Lumina API",
    description="Una API para generar y refinar visualizaciones de datos a través de un agente de IA reflexivo.",
    version="1.0.0",
)

# 2. Montar el directorio de 'outputs/charts' como una ruta estática
# Esto permite que el frontend acceda a las imágenes generadas a través de una URL.
charts_directory = config.CHARTS_DIR
# Asegurarse de que el directorio exista
os.makedirs(charts_directory, exist_ok=True)

app.mount("/static", StaticFiles(directory=charts_directory), name="static")


# 3. Definir el modelo de datos para la solicitud
# Esto asegura que cualquier solicitud a nuestro endpoint tenga el formato correcto.
class ChartRequest(BaseModel):
    instruction: str


# 4. Definir el endpoint principal de la API
@app.post("/generate-chart/")
def generate_chart_endpoint(request: ChartRequest):
    """
    Ejecuta el workflow completo para generar y refinar un gráfico.

    Recibe una instrucción del usuario, la pasa al workflow principal y
    devuelve un diccionario con los resultados, incluyendo las URLs relativas
    a los gráficos generados para que el frontend pueda acceder a ellos.

    Args:
        request: Un objeto ChartRequest que contiene la instrucción del usuario.

    Returns:
        Un diccionario con los resultados del workflow, incluyendo el estado,
        feedback y las URLs de los gráficos V1 y V2.
    """
    start_time = time.time()

    # Log de la solicitud entrante
    logger.info(
        f"Chart generation request received - Instruction: '{request.instruction[:100]}{'...' if len(request.instruction) > 100 else ''}'"
    )

    try:
        # Llama a la función refactorizada del workflow, que ahora es más simple
        results = workflow.run_workflow(
            user_instructions=request.instruction,
            generation_model=config.GENERATION_MODEL,
            reflection_model=config.REFLECTION_MODEL,
            image_basename=config.API_IMAGE_BASENAME,
        )

        # Convierte las rutas de archivo locales en URLs públicas
        if results.get("chart_v1_path") and results.get("v1_success"):
            v1_filename = os.path.basename(results["chart_v1_path"])
            results["chart_v1_url"] = f"/static/{v1_filename}"

        if results.get("chart_v2_path") and results.get("v2_success"):
            v2_filename = os.path.basename(results["chart_v2_path"])
            results["chart_v2_url"] = f"/static/{v2_filename}"

        processing_time = time.time() - start_time
        logger.info(
            f"Chart generation completed successfully in {processing_time:.2f}s - V1: {results.get('v1_success')}, V2: {results.get('v2_success')}"
        )

        return results

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(
            f"Chart generation failed after {processing_time:.2f}s - Instruction: '{request.instruction[:100]}...' - Error: {str(e)}"
        )
        raise


# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def read_root():
    """
    Endpoint raíz para verificar el estado de la API.

    Returns:
        Un mensaje JSON simple que confirma que la API está en línea.
    """
    logger.info("Health check endpoint accessed")
    return {
        "message": "API de Lumina está en línea. Usa el endpoint /generate-chart/ para crear un gráfico."
    }
