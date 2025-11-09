import pandas as pd
import pytest
from src.executor import _extract_code, _execute_code, extract_and_execute_code

# ---------- Tests para _extract_code ----------

def test_extract_code_valido():
    txt = "<execute_python>print('hola')</execute_python>"
    assert _extract_code(txt) == "print('hola')"

def test_extract_code_con_espacios():
    txt = """
    <execute_python>
        x = 1 + 1
    </execute_python>
    """
    assert _extract_code(txt) == "x = 1 + 1"

def test_extract_code_vacio_retorna_none():
    txt = "<execute_python>   \n   </execute_python>"
    assert _extract_code(txt) is None

def test_extract_code_sin_tags_retorna_none():
    assert _extract_code("print('hola')") is None

# ---------- Tests para _execute_code ----------

def test_execute_code_exito_modifica_df(df):
    code = "df['b'] = df['a'] * 2"
    ok = _execute_code(code, df)
    assert ok is True
    assert 'b' in df.columns
    assert df['b'].tolist() == [2, 4, 6]

def test_execute_code_error_retorna_false(df):
    # Falla inmediatamente (NameError) y no modifica df
    code = "dfx['b'] = 1"
    ok = _execute_code(code, df)
    assert ok is False
    assert 'b' not in df.columns

# ---------- Tests para extract_and_execute_code (integración) ----------

def test_extract_and_execute_exito(df):
    txt = """
    Texto del LLM...
    <execute_python>
    df['b'] = df['a'] + 10
    </execute_python>
    """
    ok = extract_and_execute_code(txt, df)
    assert ok is True
    assert df['b'].tolist() == [11, 12, 13]

def test_extract_and_execute_sin_tags(df):
    txt = "No hay código aquí"
    ok = extract_and_execute_code(txt, df)
    assert ok is False
    assert 'b' not in df.columns

def test_extract_and_execute_bloque_vacio(df):
    txt = "<execute_python>   </execute_python>"
    ok = extract_and_execute_code(txt, df)
    assert ok is False
    assert 'b' not in df.columns

def test_extract_and_execute_error_en_ejecucion(df):
    txt = "<execute_python>1/0</execute_python>"
    ok = extract_and_execute_code(txt, df)
    assert ok is False
    assert 'b' not in df.columns

