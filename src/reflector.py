# =============================================================================
# RESPONSABILIDAD ÚNICA DE ESTE MÓDULO
# Su trabajo es analizar un gráfico existente V1 y el código que lo generó,
# para luego proporcionar retroalimentación y un nuevo bloque de código mejorado.
# =============================================================================

from . import utils


def reflect_on_image_and_regenerate(
    chart_path: str,
    instruction: str,
    model_name: str,
    out_path_v2: str,
    code_v1: str,
    schema: str,  # Parámetro añadido para el esquema dinámico
) -> tuple[str, str]:
    """
    Critica la IMAGEN del gráfico y el código original, y luego devuelve
    código matplotlib refinado.

    Args:
        chart_path: Ruta a la imagen del gráfico v1.
        instruction: La instrucción original del usuario.
        model_name: El nombre del modelo de LLM (con visión) a usar.
        out_path_v2: La ruta donde se guardará el nuevo gráfico v2.
        code_v1: El código original que generó el gráfico v1 (para contexto).
        schema: El esquema de texto del DataFrame.

    Returns:
        Una tupla conteniendo (feedback, refined_code_with_tags).
    """
    # 1. Codifica la imagen a formato Base64 para poder enviarla a la API.
    media_type, b64_image = utils.encode_image_b64(chart_path)

    # 2. Construye el prompt detallado para el modelo de visión.
    prompt = f"""
    You are a data visualization expert.
    Your task is to critique the attached chart and then provide refined matplotlib code.
    The critique (the "feedback" field) MUST be in Spanish.

    You MUST return your response in this exact two-part format, with no extra text:

    PART 1: A single-line, valid JSON object with a single key "feedback".
    PART 2: After a newline, the Python code wrapped in <execute_python> tags.

    EXAMPLE of a perfect response:
    {{"feedback": "Este es un ejemplo de crítica en español."}}
    <execute_python>
    import matplotlib.pyplot as plt
    import pandas as pd
    # Your code here
    plt.style.use('ggplot') # Use a safe, common style
    # ... more code ...
    plt.savefig('{out_path_v2}', dpi=300)
    plt.close()
    </execute_python>

    Original code (for context):
    {code_v1}

    HARD CONSTRAINTS for the generated code:
    - Use a common, built-in matplotlib style like 'ggplot' or 'fivethirtyeight'. Do NOT use seaborn styles.
    - Use pandas/matplotlib only (no seaborn).
    - Assume the DataFrame 'df' already exists; do not read from files.
    - Save the new chart to '{out_path_v2}' with dpi=300.
    - Always call plt.close() at the end. Do not call plt.show().
    - Include all necessary import statements.

    Schema (columns available in df):
    {schema}

    Instruction:
    {instruction}
    """

    # 3. Llama al modelo de visión para obtener la respuesta cruda.
    content = utils.image_openai_call(model_name, prompt, media_type, b64_image)

    # 4. Delega el parsing complejo a la nueva función de utilidad.
    feedback, refined_code = utils.parse_reflector_response(content)

    return feedback, refined_code
