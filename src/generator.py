# =============================================================================
# RESPONSABILIDAD ÚNICA DE ESTE MODULO
# Crear el código inicial de grafico, es decir la versión 1 - V1
# =============================================================================

import pandas as pd
from . import utils
import logging

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


def generate_chart_code(
    instruction: str, model: str, out_path_v1: str, df: pd.DataFrame
) -> tuple[str, str]:
    """|
    convertir una instruccion en lenguaje natural en un script de python para crear una visualizacion, basandose en el esquema de un conjunto de datos proporcionado.

    Args:
        instruction: La instrucción del usuario.
        model: El nombre del modelo de LLM a usar.
        out_path_v1: La ruta donde se guardará el gráfico.
        df: El DataFrame con los datos para generar el esquema dinámico.

    Returns:
        Una tupla (str, str) conteniendo:
        - El string con el código Python (respuesta del LLM).
        - El string con el esquema de datos utilizado.
    """
    logger.debug("Lumina Generator: Starting code generation for V1 chart.")

    schema = utils.make_schema_text(df)
    logger.debug(f"Lumina Generator: Generated schema: {schema}")

    prompt = f"""
    You are a data visualization expert.

    Return your answer *strictly* in this format:

    <execute_python>
    # valid python code here
    </execute_python>

    Do not add explanations, only the tags and the code.

    The code should create a visualization from a DataFrame 'df'.
    This is the schema of the DataFrame (including data types):
    {schema}

    User instruction: {instruction}

    Requirements for the code:
    1. The DataFrame is already loaded and available in a variable named 'df'. **DO NOT** try to load the data again (e.g., do not use pd.read_csv).
    2. Use matplotlib for plotting.
    3. Add clear title, axis labels, and legend if needed.
    4. Save the figure as '{out_path_v1}' with dpi=300.
    5. Do not call plt.show().
    6. Close all plots with plt.close().
    7. Add all necessary import python statements

    Return ONLY the code wrapped in <execute_python> tags.
    """
    logger.debug(f"Lumina Generator: Sending prompt to LLM.")

    response = utils.get_response(model, prompt)
    logger.debug("Lumina Generator: Received response from LLM.")
    return response, schema
