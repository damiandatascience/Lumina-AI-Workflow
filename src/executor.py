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

# =============================================================================
# FUNCIONES INTERNAS ( Refactorizadas)
# Estas funciones hacen el trabajo pesado y seróan probadas individualmente
# El guión bajo (_) al inicio indica que son para uso interno del módulo.
# =============================================================================

def _extract_code(llm_response_text: str) -> str | None:
    """
    Responsabilidad 1: Extracción
    Busca y extrae un bloque de código Python de un texto.
    Devuelve el código como un string, o None si no se encuentra o está vacio.
    """
    # Busca el bloque de código entre las etiquetas <execute_python>
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", llm_response_text)

    if not match:
        logger.error("Lumina _extract_code error: No executable code found between <execute_python> tags.")
        return None
    
    # Extrae el código y elimina espacios en blanco al inicio/final
    code_to_execute = match.group(1).strip()

    if not code_to_execute:
        logger.error("Lumina _extract_code error: The executable code block is empty.")
        return None
    
    return code_to_execute

def _execute_code(code_to_execute: str, df: pd.DataFrame) -> bool:
    """
    Responsabilidad 2: Ejecución
    Ejecuta un string de código python en un entorno controlado
    Devuelve True si tiene éxito, False si falla.
    """
    try:
        # Define el entorno de ejecución. Solo el DataFrame 'df' estará disponible.
        exec_globals = {"df": df}
        exec(code_to_execute, exec_globals)
        logger.debug(">>> Code executed successfully.")
        return True
    except Exception as e:
        logger.error(f"Lumina _execute_code Error: Error during code execution: {e}")
        return False

# =============================================================================
# FUNCIÓN PÚBLICA (farcade)
# Esta es la única función que otros módulos deben llamar
# Su firma no cambia, por lo que no afecta a src/main
# =============================================================================

def extract_and_execute_code(llm_response_text: str, df: pd.DataFrame) -> bool:
    """ 
    Extrae y ejecuta código Python desde la respuesta de un LLM.
    Esta función actuá como un farcade, orquestando las llamadas a las 
    funciones internas _extract_code y _execute_code.
    """
    # Paso 1: Llama a la función de extracción.
    code_to_execute = _extract_code(llm_response_text)

    # Si la extracción falla, _extract_code ya ha registrado el error.
    # Simplemente retornamos False, manteniendo el comportamiento original
    if code_to_execute is None:
        return False

    # Paso 2: Si la extracción tiene éxito, llama a la función de ejecución 
    return _execute_code(code_to_execute, df)




    









