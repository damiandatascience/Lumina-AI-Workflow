from src.main import run_workflow
import os

# La variable 'output_dir' almacena la ruta correcta a la carpeta 'outputs/charts'.
output_dir = "outputs/charts"
os.makedirs(output_dir, exist_ok=True)

print("Iniciando el workflow programático...")

# Ejecutar workflow con datos locales
results = run_workflow(
    user_instructions="Crea un gráfico comparando las ventas Q1 de 2024 y 2025",
    generation_model="gpt-4o-mini",
    reflection_model="o4-mini-2025-04-16",
    image_basename="comparison_chart"
)

print("\n--- Resultados del Workflow ---")
print(f"Estado: {results.get('status', 'N/A')}")
print(f"V1 Chart: {results.get('chart_v1_path', 'N/A')}")
print(f"V2 Chart: {results.get('chart_v2_path', 'N/A')}")
print(f"Feedback: {results.get('feedback', 'N/A')}")

print("\nWorkflow programático finalizado.")