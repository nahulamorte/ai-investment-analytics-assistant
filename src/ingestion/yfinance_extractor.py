import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Tuple

def extract(ticker: str, periodo: str):
    try:
        df = yf.download(ticker, period=periodo)
        if df.empty:
            raise ValueError(f"No se encontraron datos para el ticker: {ticker}")
        return df
    except Exception as e:
        print("Error de red al conectar con yfinance")
        raise


def transform(dataFrame: pd.DataFrame) -> pd.DataFrame:
    df = dataFrame.reset_index()

    columna_fecha = 'Date' if 'Date' in df.columns else 'index'

    columna_precio = 'Close' if 'Close' in df.columns else 'Adj Close'

    df = df[[columna_fecha, columna_precio]]

    df.columns = ['fecha', 'precio_cierre']

    df = df.ffill()

    return df


def obtener_historico_limpio(ticker: str, periodo: str, id_activo: int) -> List[Tuple]:
    df_crudo = extract(ticker, periodo)

    df_limpio= transform(df_crudo)


    lista_tuplas_final = []

    for _, fila in df_limpio.iterrows():
        fecha = fila['fecha'].date()
        precio = float(fila['precio_cierre'])

        tupla = (precio, fecha, id_activo)
        lista_tuplas_final.append(tupla)

        return lista_tuplas_final
