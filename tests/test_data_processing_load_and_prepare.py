import pandas as pd
import pytest
import tempfile
import os
from src.data_processing import load_and_prepare_data


class TestLoadAndPrepareData:
    """Tests para la función load_and_prepare_data."""
    
    # ---------- Tests de normalización de columnas ----------
    
    def test_normalizacion_columnas_minúsculas(self):
        """Test que las columnas se normalizan a minúsculas."""
        csv_content = "Name,Age,City\nJohn,25,NYC\nJane,30,LA"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            expected_columns = ['name', 'age', 'city']
            assert list(df.columns) == expected_columns
        finally:
            os.unlink(temp_path)
    
    def test_normalizacion_elimina_espacios(self):
        """Test que se eliminan espacios de los nombres de columnas."""
        csv_content = "  Name  ,  Age  ,  City With Spaces  \nJohn,25,NYC\nJane,30,LA"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            expected_columns = ['name', 'age', 'city with spaces']
            assert list(df.columns) == expected_columns
        finally:
            os.unlink(temp_path)
    
    def test_normalizacion_columnas_mixtas(self):
        """Test con nombres de columnas en mayúsculas, minúsculas y mixtas."""
        csv_content = "UPPERCASE,lowercase,MixedCase,ALLCAPS,alllower\n1,2,3,4,5\n6,7,8,9,10"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            expected_columns = ['uppercase', 'lowercase', 'mixedcase', 'allcaps', 'alllower']
            assert list(df.columns) == expected_columns
        finally:
            os.unlink(temp_path)
    
    # ---------- Tests de procesamiento de fechas ----------
    
    def test_procesamiento_fecha_exitoso(self):
        """Test que se procesa correctamente la columna date con fechas válidas."""
        csv_content = "date,value\n2023-11-24,100\n2023-02-27,200\n2023-01-13,300"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que la columna date es datetime
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            
            # Verificar que se extrajeron quarter, month, year
            assert 'quarter' in df.columns
            assert 'month' in df.columns
            assert 'year' in df.columns
            
            # Verificar valores específicos
            assert df['quarter'].tolist() == [4, 1, 1]
            assert df['month'].tolist() == [11, 2, 1]
            assert df['year'].tolist() == [2023, 2023, 2023]
        finally:
            os.unlink(temp_path)
    
    def test_procesamiento_fecha_formatos_multiples(self):
        """Test con diferentes formatos de fecha."""
        csv_content = """date,value
2023-11-24,100
02/27/2023,200
01/13/23,300
2023.12.25,400"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que las fechas se procesaron (aunque algunas puedan ser NaT si pandas no las reconoce)
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            assert 'quarter' in df.columns
            assert 'month' in df.columns
            assert 'year' in df.columns
            
            # Verificar que al menos algunos valores son válidos
            assert not df['year'].isna().all()
        finally:
            os.unlink(temp_path)
    
    def test_procesamiento_fecha_fechas_invalidas(self):
        """Test con fechas inválidas que deben convertirse a NaT."""
        import warnings
        
        csv_content = """date,value
2023-13-45,100
invalid-date,200
2023-11-24,300"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            # Suprimir el warning esperado de pandas sobre formato de fecha
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    "Could not infer format.*",
                    category=UserWarning
                )
                df = load_and_prepare_data(temp_path)
            
            # Verificar que se convirtió a datetime (con errores='coerce')
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            
            # Verificar que las fechas inválidas son NaT
            assert pd.isna(df.loc[0, 'date'])
            assert pd.isna(df.loc[1, 'date'])
            
            # Verificar que quarter, month, year se crearon pero pueden tener NaN
            assert 'quarter' in df.columns
            assert 'month' in df.columns
            assert 'year' in df.columns
            
            # Verificar que hay valores NaN donde las fechas eran inválidas
            assert pd.isna(df.loc[0, 'quarter'])
            assert pd.isna(df.loc[1, 'quarter'])
            assert not pd.isna(df.loc[2, 'quarter'])
        finally:
            os.unlink(temp_path)
    
    # ---------- Tests de casos con/sin columna date ----------
    
    def test_sin_columna_date(self):
        """Test cuando no existe columna date."""
        csv_content = "name,age,city\nJohn,25,NYC\nJane,30,LA"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que no se crearon columnas de fecha
            assert 'quarter' not in df.columns
            assert 'month' not in df.columns
            assert 'year' not in df.columns
            assert 'date' not in df.columns
            
            # Verificar que los datos están presentes
            assert list(df.columns) == ['name', 'age', 'city']
            assert len(df) == 2
        finally:
            os.unlink(temp_path)
    
    def test_con_columna_date_principal(self):
        """Test con múltiples columnas incluyendo date como principal."""
        csv_content = """date,id,description,amount
2023-11-24,1,Transaction A,100.50
2023-02-27,2,Transaction B,200.75"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que todas las columnas están presentes
            expected_columns = ['date', 'id', 'description', 'amount', 'quarter', 'month', 'year']
            assert list(df.columns) == expected_columns
            
            # Verificar que date es datetime
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            
            # Verificar datos de fecha extraídos
            assert df['quarter'].tolist() == [4, 1]
            assert df['month'].tolist() == [11, 2]
            assert df['year'].tolist() == [2023, 2023]
        finally:
            os.unlink(temp_path)
    
    def test_columna_date_no_principal(self):
        """Test con date no siendo la primera columna."""
        csv_content = """id,date,amount,category
1,2023-11-24,100.50,A
2,2023-02-27,200.75,B"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que todas las columnas están presentes
            expected_columns = ['id', 'date', 'amount', 'category', 'quarter', 'month', 'year']
            assert list(df.columns) == expected_columns
            
            # Verificar que date es datetime
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            
            # Verificar datos de fecha extraídos
            assert df['quarter'].tolist() == [4, 1]
            assert df['month'].tolist() == [11, 2]
            assert df['year'].tolist() == [2023, 2023]
        finally:
            os.unlink(temp_path)
    
    # ---------- Tests de errores y casos edge ----------
    
    def test_archivo_vacio(self):
        """Test con archivo CSV vacío."""
        csv_content = ""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            # pd.read_csv() debería lanzar una excepción para archivo vacío
            with pytest.raises(pd.errors.EmptyDataError):
                load_and_prepare_data(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_solo_encabezados(self):
        """Test con archivo que solo tiene encabezados."""
        csv_content = "name,age,city"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que se crearon las columnas normalizadas
            assert list(df.columns) == ['name', 'age', 'city']
            
            # Verificar que no hay datos (DataFrame vacío)
            assert len(df) == 0
            
            # Verificar que no se crearon columnas de fecha
            assert 'quarter' not in df.columns
            assert 'month' not in df.columns
            assert 'year' not in df.columns
        finally:
            os.unlink(temp_path)
    
    def test_archivo_no_existe(self):
        """Test cuando el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            load_and_prepare_data("archivo_inexistente.csv")
    
    def test_datos_mixtos_fechas(self):
        """Test con mezcla de fechas válidas e inválidas."""
        csv_content = """date,value
2023-11-24,100
invalid,200
2023-13-45,300
2023-02-27,400"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar estructura
            assert list(df.columns) == ['date', 'value', 'quarter', 'month', 'year']
            
            # Verificar que date es datetime
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            
            # Verificar que las fechas válidas tienen quarter, month, year correctos
            valid_rows = df[df['date'].notna()]
            for _, row in valid_rows.iterrows():
                assert not pd.isna(row['quarter'])
                assert not pd.isna(row['month'])
                assert not pd.isna(row['year'])
            
            # Verificar que las fechas inválidas tienen valores NaN en los campos de fecha
            invalid_rows = df[df['date'].isna()]
            for _, row in invalid_rows.iterrows():
                assert pd.isna(row['quarter'])
                assert pd.isna(row['month'])
                assert pd.isna(row['year'])
        finally:
            os.unlink(temp_path)
    
    def test_muchos_registros_año_bisiesto(self):
        """Test con fechas de año bisiesto."""
        csv_content = """date,value
2020-02-29,100
2021-02-28,200
2024-02-29,300"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que se procesaron correctamente las fechas
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            assert 'quarter' in df.columns
            assert 'month' in df.columns
            assert 'year' in df.columns
            
            # Verificar años específicos
            assert df['year'].tolist() == [2020, 2021, 2024]
            assert df['month'].tolist() == [2, 2, 2]
            assert df['quarter'].tolist() == [1, 1, 1]
        finally:
            os.unlink(temp_path)
    
    # ---------- Test de integración completa ----------
    
    def test_integracion_completa(self):
        """Test de integración que simula el flujo completo de procesamiento."""
        # Simular un CSV similar al retail_sales_dataset pero con nombres de columnas en mayúsculas
        csv_content = """Transaction_ID,Date,Customer_ID,Gender,Age,Product_Category,Quantity,Price_Per_Unit,Total_Amount
1,2023-11-24,CUST001,Male,34,Beauty,3,50,150
2,2023-02-27,CUST002,Female,26,Clothing,2,500,1000
3,2023-01-13,CUST003,Male,50,Electronics,1,30,30"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = load_and_prepare_data(temp_path)
            
            # Verificar que todas las columnas se normalizaron correctamente
            expected_columns = [
                'transaction_id', 'date', 'customer_id', 'gender', 'age', 
                'product_category', 'quantity', 'price_per_unit', 'total_amount',
                'quarter', 'month', 'year'
            ]
            assert list(df.columns) == expected_columns
            
            # Verificar que date es datetime
            assert pd.api.types.is_datetime64_any_dtype(df['date'])
            
            # Verificar valores de fecha extraídos
            assert df['quarter'].tolist() == [4, 1, 1]
            assert df['month'].tolist() == [11, 2, 1]
            assert df['year'].tolist() == [2023, 2023, 2023]
            
            # Verificar que los datos originales se mantuvieron
            assert df['transaction_id'].tolist() == [1, 2, 3]
            assert df['customer_id'].tolist() == ['CUST001', 'CUST002', 'CUST003']
            assert df['total_amount'].tolist() == [150, 1000, 30]
            
            # Verificar que no hay valores nulos en los datos originales
            assert not df['transaction_id'].isna().any()
            assert not df['customer_id'].isna().any()
            assert not df['total_amount'].isna().any()
        finally:
            os.unlink(temp_path)


class TestLoadAndPrepareDataFixtures:
    """Tests usando el fixture de conftest.py para verificar comportamiento."""
    
    def test_comportamiento_esperado_con_fixture(self, df):
        """Test que verifica el comportamiento esperado con el fixture de conftest."""
        # El fixture df refleja el estado DESPUÉS de load_and_prepare_data
        # (simulando el resultado con columnas normalizadas y datos de fecha extraídos)
        
        # Verificar que tiene las columnas de fecha
        assert 'quarter' in df.columns
        assert 'month' in df.columns
        assert 'year' in df.columns
        
        # Verificar que tiene la columna date (como string, simula el resultado final)
        assert 'date' in df.columns
        
        # Verificar valores específicos de fecha extraída
        assert df['quarter'].tolist() == [4, 1, 1]
        assert df['month'].tolist() == [11, 2, 1]
        assert df['year'].tolist() == [2023, 2023, 2023]
        
        # Verificar datos de retail_sales
        assert df['transaction_id'].tolist() == [1, 2, 3]
        assert df['customer_id'].tolist() == ['CUST001', 'CUST002', 'CUST003']
        assert df['product_category'].tolist() == ['Beauty', 'Clothing', 'Electronics']
        
        # Verificar que todas las columnas esperadas están presentes
        expected_columns = [
            'transaction_id', 'date', 'customer_id', 'gender', 'age',
            'product_category', 'quantity', 'price_per_unit', 'total_amount',
            'quarter', 'month', 'year'
        ]
        assert list(df.columns) == expected_columns