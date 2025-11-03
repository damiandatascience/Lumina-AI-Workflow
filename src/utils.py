# =============================================================================
# RESPONSABILIDAD ÚNICA DE ESTE MODULO
# Proporcionar herramientas esenciales para la integración con APIs, manejo de datos
# y procesacimiento de contenido, es la caja de herramientas del Pipeline
# =============================================================================

import os
import re
import json
import base64
import mimetypes

import pandas as pd
from PIL import Image  # Añadido por para integración post-launch
from openai import OpenAI

# Cargar variables de entorno y configurar el cliente de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)


def get_response(model: str, prompt: str) -> str:
    """
    Obtiene una respuesta de texto de un modelo de OpenAI.

    Args:
        model: El nombre del modelo de LLM a usar (ej. "gpt-4o-mini").
        prompt: El prompt de texto a enviar al modelo.

    Returns:
        La respuesta de texto generada por el modelo.
    """
    response = openai_client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text


def image_openai_call(model_name: str, prompt: str, media_type: str, b64: str) -> str:
    """
    Realiza una llamada a un modelo de visión de OpenAI con una imagen y un prompt.

    Args:
        model_name: El nombre del modelo de LLM con capacidad de visión.
        prompt: El prompt de texto que acompaña a la imagen.
        media_type: El tipo MIME de la imagen (ej. "image/png").
        b64: La cadena de la imagen codificada en Base64.

    Returns:
        La respuesta de texto generada por el modelo de visión.
    """
    data_url = f"data:{media_type};base64,{b64}"

    resp = openai_client.responses.create(
        model=model_name,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url},
                ],
            }  # type: ignore
        ],
    )
    content = (resp.output_text or "").strip()
    return content


def encode_image_b64(path: str) -> tuple[str, str]:
    """
    Codifica un archivo de imagen a una cadena Base64 y obtiene su tipo MIME.

    Args:
        path: La ruta al archivo de imagen.

    Returns:
        Una tupla que contiene el tipo MIME y la cadena Base64 de la imagen.
    """
    mime, _ = mimetypes.guess_type(path)
    media_type = mime or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return media_type, b64


def ensure_execute_python_tags(text: str) -> str:
    """
    Asegura que un bloque de código Python esté envuelto en etiquetas <execute_python>.

    Si el texto ya contiene las etiquetas, no hace nada. Si no, las añade.
    También elimina los bloques de código de Markdown (```).

    Args:
        text: El texto que contiene el código Python.

    Returns:
        El código Python garantizado de estar envuelto en las etiquetas correctas.
    """
    text = text.strip()
    text = re.sub(r"^```(?:python)?\s*|\s*```$", "", text).strip()
    if "<execute_python>" not in text:
        text = f"<execute_python>\n{text}\n</execute_python>"
    return text


def make_schema_text(df: pd.DataFrame) -> str:
    """
    Genera una representación de texto del esquema de un DataFrame.

    Args:
        df: El DataFrame de pandas del cual extraer el esquema.

    Returns:
        Una cadena de texto multilínea que describe las columnas y sus
        tipos de datos, legible para humanos.
    """
    return "\n".join(f"- {c}: {dt}" for c, dt in df.dtypes.items())


def parse_reflector_response(content: str) -> tuple[str, str]:
    """
    Analiza la respuesta de texto del agente reflector para extraer el feedback y el código.

    Args:
        content: El texto crudo devuelto por el LLM.

    Returns:
        Una tupla (feedback, refined_code_with_tags).
    """
    # --- Parse ONLY the first JSON line (feedback) ---
    lines = content.strip().splitlines()
    json_line = lines[0].strip() if lines else ""

    try:
        obj = json.loads(json_line)
    except Exception as e:
        # Fallback: Intenta capturar el primer {...} en todo el contenido
        m_json = re.search(r"\{.*?\}", content, flags=re.DOTALL)
        if m_json:
            try:
                obj = json.loads(m_json.group(0))
            except Exception as e2:
                obj = {"feedback": f"Failed to parse JSON: {e2}"}
        else:
            obj = {"feedback": f"Failed to find JSON: {e}"}

    # --- Extraer código refinado de <execute_python>...</execute_python> ---
    m_code = re.search(r"<execute_python>([\s\S]*?)</execute_python>", content)
    refined_code_body = m_code.group(1).strip() if m_code else ""
    refined_code = ensure_execute_python_tags(refined_code_body)

    feedback = str(obj.get("feedback", "No feedback provided.")).strip()
    return feedback, refined_code
