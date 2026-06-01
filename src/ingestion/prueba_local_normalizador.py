import pandas as pd
import numpy as np
# Importamos tu función desde el módulo de ingesta
from ingestion.yfinance_extractor import transform


def ejecutar_test_local():
    print("==================================================")
    print("⚙️ Generando DataFrame de juguete (Mock de Yahoo)...")
    print("==================================================")

    # 1. Creamos un rango de 4 fechas secuenciales para el índice
    fechas_prueba = pd.date_range(start="2026-06-01", periods=4)

    # 2. Armamos el diccionario replicando las columnas reales de yfinance.
    # El tercer elemento de Adj Close es un NaN a propósito para validar el ffill().
    datos_mock = {
        'Open': [100.0, 101.5, 102.0, 100.5],
        'High': [102.0, 103.0, 102.5, 101.0],
        'Low': [99.0, 100.0, 101.0, 98.5],
        'Close': [101.0, 102.0, 101.5, 99.0],
        'Adj Close': [101.0, 102.0, np.nan, 99.0],  # <-- Celda vacía de prueba
        'Volume': [1500000, 1800000, 1200000, 2000000]
    }

    # 3. Instanciamos el DataFrame simulador
    df_yahoo_mock = pd.DataFrame(data=datos_mock, index=fechas_prueba)

    print("\n📊 DataFrame crudo simulado:")
    print(df_yahoo_mock)

    print("\n--------------------------------------------------")
    print("🚀 Ejecutando tu componente normalizar_dataframe()...")
    print("--------------------------------------------------")

    try:
        # 4. Invocamos tu función pasándole el mock
        df_resultado = transform(df_yahoo_mock)

        print("\n✅ DataFrame final normalizado con éxito:")
        print(df_resultado)

        print("\n🔎 Diagnóstico técnico de tipos de datos (.dtypes):")
        print(df_resultado.dtypes)

        # 5. Validación automatizada senior usando asserts básicos
        assert 'fecha' in df_resultado.columns, "❌ Error: La columna 'fecha' no existe."
        assert 'precio_cierre' in df_resultado.columns, "❌ Error: La columna 'precio_cierre' no existe."
        assert len(df_resultado.columns) == 2, "❌ Error: El DataFrame tiene más de las 2 columnas requeridas."
        assert not df_resultado['precio_cierre'].isnull().any(), "❌ Error: El método ffill() falló, quedan valores NaN."

        # Validación del valor específico del miércoles (índice posicional 2 en base 0)
        precio_miercoles = df_resultado.loc[2, 'precio_cierre']
        assert precio_miercoles == 102.0, f"❌ Error: El precio del miércoles debería ser 102.0, pero es {precio_miercoles}"

        print("\n🎉 [PASS] ¡Control de calidad superado! El transformador funciona bajo estándar de producción.")

    except AssertionError as error_validacion:
        print(f"\n🚨 [FAIL] La validación falló: {error_validacion}")
    except Exception as e:
        print(f"\n💥 Error catastrófico durante la ejecución: {e}")


if __name__ == "__main__":
    ejecutar_test_local()