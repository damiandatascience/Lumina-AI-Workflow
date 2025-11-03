## 📝 Logging

El proyecto utiliza el módulo `logging` de Python para registrar eventos, errores y el progreso del AI Workflow.

### Configuración Actual

- **Nivel:** INFO (muestra información y errores)
- **Formato:** `timestamp - módulo - nivel - mensaje`
- **Ubicación:** Consola (salida estándar)

### Ejemplo de Salida

Cuando ejecutas el workflow, verás logs detallados como:

```
2025-11-02 03:34:54 - src.main - INFO - Initializing agentic visualization workflow...
2025-11-02 03:34:55 - src.main - INFO - Deciding data source based on configuration...
2025-11-02 03:34:55 - src.main - INFO - Configuration set to use local CSV.
2025-11-02 03:34:56 - src.main - INFO - Loading data from: data/coffee_sales.csv
2025-11-02 03:34:57 - src.main - INFO - Data loaded successfully.
2025-11-02 03:34:58 - src.main - INFO - Using gpt-4o-mini to generate V1 chart code...
2025-11-02 03:34:59 - src.main - INFO - Executing code for V1 chart...
2025-11-02 03:35:00 - src.main - INFO - V1 Chart saved to: outputs/charts/comparison_chart_v1.png
2025-11-02 03:35:01 - src.main - INFO - Using o4-mini-2025-04-16 to reflect on V1 chart...
2025-11-02 03:35:02 - src.main - INFO - Feedback received from reflector:
2025-11-02 03:35:03 - src.main - INFO - Executing refined code for V2 chart...
2025-11-02 03:35:04 - src.main - INFO - V2 Chart (improved) saved to: outputs/charts/comparison_chart_v2.png
2025-11-02 03:35:05 - src.main - INFO - Workflow completed successfully.
```

### Niveles de Logging

- **DEBUG**: Información detallada para desarrollo y debugging.
- **INFO**: Información general del flujo del workflow.
- **WARNING**: Advertencias que no detienen la ejecución.
- **ERROR**: Errores que afectan el resultado pero permiten continuar.
- **CRITICAL**: Errores críticos que requieren atención inmediata.

### Estrategia y Uso de Niveles

El sistema de logging está diseñado con dos modos principales de operación para separar la información de alto nivel de los detalles de depuración.

#### Modo Estándar (`level=logging.INFO`)

Este es el modo por defecto. Está configurado para mostrar solo los hitos importantes del flujo de trabajo, como la creación de artefactos (gráficos) y la finalización del proceso. Proporciona una salida limpia y concisa, ideal para la ejecución normal y la demostración del proyecto.

#### Modo de Depuración (`level=logging.DEBUG`)

Este modo está destinado al desarrollo y la solución de problemas. Al activarlo, se muestran todos los mensajes de log, incluyendo los pasos internos detallados, el contenido de los prompts y las respuestas de la API.

Para activar el modo de depuración, es necesario modificar el punto de entrada de la aplicación en `src/main.py`. Localice el bloque `logging.basicConfig` y cambie el nivel:

```python
# En src/main.py, dentro de if __name__ == "__main__":

logging.basicConfig(
    level=logging.DEBUG, # Cambiar a DEBUG para habilitar logs detallados
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Guardar Logs en Archivo (Opcional)

Si se desea guardar los logs en un archivo `app.log` para referencia futura, se puede modificar la configuración en `src/config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Guarda en archivo
        logging.StreamHandler()           # También muestra en consola
    ]
)
```

**Importante:** Si se guardan logs en archivo, es una buena práctica agregar el nombre del archivo o la carpeta de logs al `.gitignore`:

```
*.log
logs/
```

### Usar Logging en Nuevos Módulos

Para agregar logging a nuevos módulos, siga el patrón estándar:

```python
import logging

logger = logging.getLogger(__name__)

def mi_funcion():
    logger.info("Procesando datos...")
    logger.debug("Variable x = %s", x)
    logger.warning("Valor bajo detectado")
    logger.error("Error en la conexión")
```

### Beneficios del Logging

- **Timestamps automáticos**: Permite saber exactamente cuándo ocurrió cada evento.
- **Trazabilidad**: Cada log indica el módulo de origen.
- **Niveles de severidad**: Permite distinguir entre información general, advertencias y errores.
- **Debugging eficiente**: Facilita encontrar problemas rápidamente.
- **Auditoría**: Mantiene un registro del comportamiento del sistema.