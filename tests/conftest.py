import pytest
import pandas as pd

@pytest.fixture
def df():
    return pd.DataFrame({"a": [1, 2, 3]})