# =============================================================================
# RESPONSABILIDAD ÚNICA DE ESTE MODULO
# Tomar un bloque de texto, extraer el código python de él y ejecutarlo
# NOTA IMPORTANTE:
# Configure el backend de Matplotlib a uno no interactivo para evitar errores en hilos
# =============================================================================


import matplotlib

matplotlib.use("Agg")

import re
import pandas as pd
import logging

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


def extract_and_execute_code(llm_response_text: str, df: pd.DataFrame) -> bool:
    """
    Extrae y ejecuta código Python desde la respuesta de un LLM.

    Args:
        llm_response_text: El texto completo devuelto por el LLM, que se espera
                           que contenga etiquetas <execute_python>.
        df: El DataFrame de pandas que debe estar disponible para el código ejecutado.

    Returns:
        bool: True si el código se extrajo y ejecutó, False en caso contrario.
    """
    # Busca el bloque de código entre las etiquetas <execute_python>
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", llm_response_text)

    if not match:
        logger.error("Lumina Executor Error: No executable code found between <execute_python> tags.")
        return False

    # Extrae el código y elimina espacios en blanco al inicio/final
    code_to_execute = match.group(1).strip()

    if not code_to_execute:
        logger.error("Lumina Executor Error: The executable code block is empty.")
        return False

    logger.debug("--- Code to be executed ---")
    logger.debug(code_to_execute)
    logger.debug("------------------------")

    try:
        # Define el entorno de ejecución. Solo el DataFrame 'df' estará disponible.
        exec_globals = {"df": df}
        exec(code_to_execute, exec_globals)
        logger.debug(">>> Code executed successfully.")
        return True
    except Exception as e:
        logger.error(f"Lumina Executor Error: Error during code execution: {e}")
        return False
