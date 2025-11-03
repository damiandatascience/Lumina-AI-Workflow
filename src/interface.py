
import gradio as gr  # type: ignore
import requests
from PIL import Image
import io
import logging

# --- Configuración de Logging ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- Constantes de la API ---
API_BASE_URL = "http://127.0.0.1:8000"
API_ENDPOINT_URL = f"{API_BASE_URL}/generate-chart/"

# --- Tema Personalizado ---
# Un tema oscuro para darle a la aplicación un aspecto más profesional y técnico.
theme = gr.themes.Base(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.sky,
    neutral_hue=gr.themes.colors.gray,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill="*neutral_950",
    body_text_color="*neutral_200",
    background_fill_primary="*neutral_900",
    background_fill_secondary="*neutral_800",
    border_color_accent="*primary_500",
    border_color_primary="*neutral_700",
    color_accent="*primary_500",
    link_text_color="*primary_400",
    link_text_color_hover="*primary_300",
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_400",
    button_primary_text_color="white",
)


# --- Función Puente Mejorada ---
def llamar_agente_y_mostrar_resultados(instruccion):
    """
    Actúa como un puente entre Gradio y la API, ahora como una función generadora
    para proporcionar feedback en tiempo real.
    """
    # 1. Inmediatamente deshabilita el botón y muestra un estado de "procesando".
    yield {
        btn: gr.Button(interactive=False),
        feedback_output: "⏳ Procesando... El agente está generando y refinando el gráfico. Esto puede tardar hasta un minuto.",
        chart_v1: None,
        chart_v2: None,
    }

    logger.info(f"Interfaz: Enviando instrucción a la API: '{instruccion}'")
    payload = {"instruction": instruccion}

    try:
        # 2. Llama a la API para ejecutar el workflow
        response = requests.post(API_ENDPOINT_URL, json=payload)
        response.raise_for_status()
        results = response.json()
        logger.debug(f"Interfaz: Respuesta recibida de la API: {results}")

        feedback = results.get("feedback", "No se recibió feedback.")

        # 3. Descarga las imágenes
        pil_image_v1 = None
        if results.get("chart_v1_url"):
            url_v1 = f"{API_BASE_URL}{results.get('chart_v1_url')}"
            logger.info(f"Interfaz: Descargando imagen V1 desde {url_v1}")
            image_response_v1 = requests.get(url_v1)
            image_response_v1.raise_for_status()
            pil_image_v1 = Image.open(io.BytesIO(image_response_v1.content))

        pil_image_v2 = None
        if results.get("chart_v2_url"):
            url_v2 = f"{API_BASE_URL}{results.get('chart_v2_url')}"
            logger.info(f"Interfaz: Descargando imagen V2 desde {url_v2}")
            image_response_v2 = requests.get(url_v2)
            image_response_v2.raise_for_status()
            pil_image_v2 = Image.open(io.BytesIO(image_response_v2.content))

        # 4. Muestra los resultados finales y reactiva el botón.
        yield {
            btn: gr.Button(interactive=True),
            feedback_output: feedback,
            chart_v1: pil_image_v1,
            chart_v2: pil_image_v2,
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Error al llamar a la API o descargar imágenes: {e}")
        error_message = f"Error de conexión con la API en {API_ENDPOINT_URL}. ¿Está el servidor FastAPI corriendo?\n\nDetalles: {e}"
        # Muestra el error y reactiva el botón.
        yield {
            btn: gr.Button(interactive=True),
            feedback_output: error_message,
            chart_v1: None,
            chart_v2: None,
        }


# --- Construcción de la Interfaz Mejorada ---
with gr.Blocks(theme=theme) as demo:
    gr.Markdown(
        """
        # 💡 Lumina AI Workflow
        ### De Instrucción a Visualización, Refinada por IA
        Escribe una instrucción para generar un gráfico. Lumina creará una versión inicial (V1),
        la analizará de forma crítica y la refinará automáticamente en una versión mejorada (V2).
        """
    )

    # --- Sección de Entrada ---
    gr.Markdown("### ✏️ Describe tu Visualización")
    with gr.Row():
        instruccion_usuario = gr.Textbox(
            label="Instrucción para el gráfico",
            placeholder="Ej: Compara las ventas totales por categoría de producto.",
            lines=3,
            scale=4,
        )
        btn = gr.Button("✨ Generar y Refinar", variant="primary", scale=1)

    # --- Sección de Resultados ---
    gr.Markdown("### 📊 Resultados del Agente")
    with gr.Row():
        with gr.Column(scale=1, min_width=450):
            gr.Markdown("### 🔸 V1: Gráfico Inicial")
            chart_v1 = gr.Image(
                label="Primera versión del gráfico",
                show_label=True,
                show_download_button=True,
                height=400,
            )
        with gr.Column(scale=1, min_width=450):
            gr.Markdown("### 🔹 V2: Gráfico Mejorado")
            chart_v2 = gr.Image(
                label="Versión refinada del gráfico",
                show_label=True,
                show_download_button=True,
                height=400,
            )

    # --- Sección de Feedback ---
    gr.Markdown("### 💬 Análisis y Crítica del Agente")
    feedback_output = gr.Textbox(
        label="Análisis para la mejora de V1 a V2",
        lines=8,
        interactive=False,
        show_copy_button=True,
        max_lines=None,
    )

    # Conecta el botón con la función puente y los componentes
    btn.click(
        fn=llamar_agente_y_mostrar_resultados,
        inputs=instruccion_usuario,
        outputs=[btn, feedback_output, chart_v1, chart_v2],
    )

# --- Punto de Entrada para Ejecutar la Interfaz ---
if __name__ == "__main__":
    logger.info("Lanzando la interfaz de Gradio...")
    logger.info(
        "Asegúrate de que el servidor de FastAPI esté corriendo en otra terminal con:"
    )
    logger.info("uv run -m fastapi dev src/api.py")
    demo.launch()
