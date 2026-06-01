import yfinance as yf
import pandas as pd
import numpy as np


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
    #Liberar la fecha del indice
    df = dataFrame.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill="")

    df = df[['index', 'Adj Close']]

    df.columns = ['fecha', 'precio_cierre']

    # Tratamiento de nulos financiero: arrastrar el último precio disponible
    df = df.ffill()

    return df




