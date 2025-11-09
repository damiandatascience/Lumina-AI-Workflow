import pytest
import pandas as pd

@pytest.fixture
def df():
    """
    DataFrame con la estructura real después de load_and_prepare_data().
    Refleja el retail_sales_dataset con columnas normalizadas.
    """
    return pd.DataFrame({
        # Columnas normalizadas (después de load_and_prepare_data)
        "transaction_id": [1, 2, 3],
        "date": ["2023-11-24", "2023-02-27", "2023-01-13"],  # Como string, se convertirá a datetime
        "customer_id": ["CUST001", "CUST002", "CUST003"],
        "gender": ["Male", "Female", "Male"],
        "age": [34, 26, 50],
        "product_category": ["Beauty", "Clothing", "Electronics"],
        "quantity": [3, 2, 1],
        "price_per_unit": [50, 500, 30],
        "total_amount": [150, 1000, 30],
        # Columnas añadidas por load_and_prepare_data
        "quarter": [4, 1, 1],
        "month": [11, 2, 1],
        "year": [2023, 2023, 2023]
    })
