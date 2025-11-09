# =============================================================================
# RESPONSABILIDAD ÚNICA DE ESTE MODULO
# Cargar y preparar los datos
# =============================================================================

import os
import logging
import pandas as pd
from pymongo import MongoClient
from . import config

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


def load_configured_data() -> pd.DataFrame | None:
    """
    Carga datos desde la fuente configurada (MongoDB o CSV).

    Utiliza la variable `USE_MONGO_DB` en `config.py` para decidir.

    Args:
        None: Esta función no toma argumentos directos, ya que su comportamiento
              se rige por la configuración definida en `config.py` y las variables
              de entorno para la conexión a MongoDB.

    Returns:
        pd.DataFrame | None: Un DataFrame de pandas con los datos cargados y preparados,
                             o `None` si ocurre un error durante la carga de datos
                             (por ejemplo, archivo no encontrado, credenciales de MongoDB
                             faltantes o incorrectas).
    """
    if config.USE_MONGO_DB:
        logger.debug("Lumina Data: Configuration set to use MongoDB.")
        mongo_uri = os.getenv("MONGO_URI") or ""
        db_name = os.getenv("MONGO_DB_NAME") or ""
        collection_name = os.getenv("MONGO_COLLECTION_NAME") or ""

        if not all([mongo_uri, db_name, collection_name]):
            logger.error(
                "Lumina Data Error: MongoDB configuration missing. MONGO_URI, MONGO_DB_NAME, and MONGO_COLLECTION_NAME must be defined in the .env file."
            )
            return None

        logger.debug(f"Lumina Data: Loading data from MongoDB: {db_name}.{collection_name}")
        return load_and_prepare_data_from_mongo(mongo_uri, db_name, collection_name)
    else:
        logger.debug("Lumina Data: Configuration set to use local CSV.")
        if config.DATA_FILENAME:
            csv_path = config.DATA_DIR / config.DATA_FILENAME
            if csv_path.exists():
                logger.debug(f"Lumina Data: Loading data from CSV: {csv_path}")
                return load_and_prepare_data(str(csv_path))
            else:
                logger.error(
                    f"Lumina Data Error: CSV file not found at {csv_path}."
                )
                return None
        else:
            logger.error("Lumina Data Error: DATA_FILENAME is not defined in the .env file.")
            return None


def load_and_prepare_data(csv_path: str) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV y los prepara para el análisis.
    Normaliza nombre de columnas a minusculas y elimina espacios.

    Si existe una columna 'date', la convierte a formato datetime y extrae
    automáticamente 'quarter', 'month' y 'year' en nuevas columnas para
    facilitar la creación de gráficos temporales.

    Args:
        csv_path: La ruta al archivo CSV que se va a cargar.

    Returns:
        Un DataFrame de pandas con los datos cargados y procesados.
    """
    df = pd.read_csv(csv_path)
    
    # Normalizar todas la columnas 
    df.columns = df.columns.str.lower().str.strip()

    # Procesa la columna 'date' solo si existe
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["quarter"] = df["date"].dt.quarter
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year

    return df


def load_and_prepare_data_from_mongo(
    uri: str, db_name: str, collection_name: str
) -> pd.DataFrame:
    """
    Carga datos desde una colección de MongoDB y los prepara para el análisis.

    Realiza el mismo procesamiento de fechas que `load_and_prepare_data` y
    elimina la columna `_id` de MongoDB. Maneja la conexión de forma segura.

    Args:
        uri: La cadena de conexión de MongoDB.
        db_name: El nombre de la base de datos.
        collection_name: El nombre de la colección.

    Returns:
        Un DataFrame de pandas con los datos o un DataFrame vacío si ocurre un error.
    """
    client = None  # Inicializamos client a None
    try:
        # Conexión a MongoDB
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]

        # Verificar la conexión
        db.command("ping")
        logger.info("Lumina Data: MongoDB Atlas connection successful.")

        # Leer los datos y convertirlos a un DataFrame
        documents = list(collection.find({}))
        df = pd.DataFrame(documents)

        # Procesamiento de fechas
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["quarter"] = df["date"].dt.quarter
            df["month"] = df["date"].dt.month
            df["year"] = df["date"].dt.year

        # Eliminar la columna _id de MongoDB si no se necesita
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        return df

    except Exception as e:
        logger.error(f"Lumina Data Error: Failed to connect or read from MongoDB: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    finally:
        # Asegurarse de que la conexión se cierre siempre
        if client:
            client.close()
            logger.info("Lumina Data: MongoDB connection closed.")
