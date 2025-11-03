

# =============================================================================
# RESPONSABILIDAD ÚNICA DE ESTE MODULO
# Script principal que orquesta todo el workflow
# Ejecuta el proceso de generación, ejecución, reflexión y refinamiento
# =============================================================================

import logging
import pandas as pd
from . import config
from . import data_processing
from . import generator
from . import reflector
from . import executor

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


def run_workflow(
    user_instructions: str,
    generation_model: str,
    reflection_model: str,
    image_basename: str = "chart",
) -> dict:
    """
    Ejecuta el pipeline completo de generación y refinamiento de gráficos.
    Utiliza un interruptor en config.py para decidir si cargar
    datos desde MongoDB o un CSV local.

    Args:
        user_instructions: Instrucciones para generar el gráfico
        generation_model: Modelo para generar código inicial
        reflection_model: Modelo para reflexionar y mejorar
        image_basename: Nombre base para los archivos de salida

    Returns:
        Diccionario con resultados del pipeline
    """
    logger.info("Iniciando Lumina AI Workflow...")

    # 1. Configurar rutas para guardar los gráficos
    logger.debug("Setting up output paths...")
    out_path_v1 = str(config.CHARTS_DIR / f"{image_basename}_v1.png")
    out_path_v2 = str(config.CHARTS_DIR / f"{image_basename}_v2.png")

    # 2. Cargar datos según la configuración
    logger.debug("Deciding data source based on configuration...")
    df = data_processing.load_configured_data()

    if df is None or df.empty:
        logger.error("Lumina Workflow Error: No data loaded. Please check data source configuration in .env or config.py.")
        return {"status": "Error", "message": "No se pudieron cargar los datos."}

    logger.debug("Data loaded successfully.")

    # 3. Ejecutar pipeline de generación de gráficos V1→V2
    logger.debug(f"Lumina Workflow - Step 1 (Generate): Using {generation_model} to generate initial code.")
    code_v1_response, schema = generator.generate_chart_code(
        instruction=user_instructions,
        model=generation_model,
        out_path_v1=out_path_v1,
        df=df,
    )

    # 3.1. Ejecutar V1 (con verificación)
    logger.debug("Lumina Workflow - Step 2 (Execute V1): Executing initial code.")
    v1_success = executor.extract_and_execute_code(code_v1_response, df)
    if not v1_success:
        logger.error("Lumina Workflow Error: Stopping workflow due to a critical error in V1 code execution.")
        return {
            "status": "Error en V1",
            "v1_success": False,
            "chart_v1_path": None,
            "feedback": None,
            "v2_success": False,
            "chart_v2_path": None,
        }

    logger.info(f"Grafico V1 guardado en: {out_path_v1}")

    # 4. Reflexionar sobre V1 para obtener feedback y código V2
    logger.debug(f"Lumina Workflow - Step 3 (Reflect): Using {reflection_model} to analyze V1 chart.")
    feedback, code_v2_response = reflector.reflect_on_image_and_regenerate(
        chart_path=out_path_v1,
        instruction=user_instructions,
        model_name=reflection_model,
        out_path_v2=out_path_v2,
        code_v1=code_v1_response,
        schema=schema,
    )
    logger.debug("Feedback received from reflector:")
    # Reemplaza caracteres no soportados para evitar errores en la consola de Windows
    safe_feedback = feedback.encode("cp1252", errors="replace").decode("cp1252")
    logger.debug(safe_feedback)

    # 5. Ejecutar V2 (con verificación)
    logger.debug("Lumina Workflow - Step 4 (Execute V2): Executing refined code.")
    v2_success = executor.extract_and_execute_code(code_v2_response, df)
    if not v2_success:
        logger.error("Lumina Workflow Warning: Could not generate V2 chart due to an error in refined code execution. V1 chart is still available.")
        return {
            "status": "Error en V2",
            "v1_success": True,
            "chart_v1_path": out_path_v1,
            "feedback": feedback,
            "v2_success": False,
            "chart_v2_path": None,
        }

    logger.info(f"Grafico V2 mejorado y guardado en: {out_path_v2}")
    logger.info("Lumina AI Workflow completado exitosamente.")

    # 6. Devolver el diccionario de resultados
    return {
        "status": "Completed",
        "v1_success": True,
        "chart_v1_path": out_path_v1,
        "feedback": feedback,
        "v2_success": True,
        "chart_v2_path": out_path_v2,
    }


if __name__ == "__main__":
    # Configurar logging básico para la ejecución directa del script,
    # para que los mensajes INFO se muestren en la consola.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Silenciar loggers de librerías de terceros para mantener la salida limpia
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)

    # Las instrucciones desde configuración centralizada
    instructions = config.DEFAULT_WORKFLOW_INSTRUCTION

    # Simplemente ejecuta el workflow. La configuración en config.py y .env
    # decidirá de dónde se cargan los datos.
    results = run_workflow(
        user_instructions=instructions,
        generation_model=config.GENERATION_MODEL,
        reflection_model=config.REFLECTION_MODEL,
        image_basename="sales_comparison_final",
    )

    logger.info("\n--- LUMINA AI WORKFLOW RESULTADOS ---")
    logger.info(f"Status: {results.get('status')}")
    if results.get("v1_success"):
        logger.info(f"Grafico V1 almacenado en: {results.get('chart_v1_path')}")
    if results.get("v2_success"):
        logger.info(f"Grafico V2 almacenado en: {results.get('chart_v2_path')}")
    if results.get("feedback"):
        # Imprime el feedback de forma segura para la consola
        safe_feedback = (
            results.get("feedback", "")
            .encode("cp1252", errors="replace")
            .decode("cp1252")
        )
        logger.info(f"Feedback: {safe_feedback}")
    logger.info("------------------------------------")
