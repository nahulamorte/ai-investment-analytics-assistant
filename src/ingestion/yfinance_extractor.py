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

    #Filtrar y obtener las columnas necesarias
    df = df[['Date', 'Adj Close']]

    df.columns = ['fecha', 'precio_cierre']

    # Tratamiento de nulos financiero: arrastrar el último precio disponible
    df = df.ffill()

    return df



"""
TODO 
Tengo que hacer lo siguiente:
1) Extract
    Una funcion que reciba 2 parametros (ticker y periodo).
    Capturo todo en un bloque TRY - EXCEPT
    Hago uso de yfinance --> yf.download(ticker, period)
    Verificar si el dataframe esta vacio --> df.empty
        Si esta vacio: Lanzo un ValueError.

2) Transform
    Una funcion que actue como transformador de matrices
    Recibe como parametro el dataframe
    La funcion debera retornar un nuevo DataFrame a  partir del DataFrame que recibe
    Esta funcion se encarga de limpiar los nulos
    
3) Load
    Se encarga de mostrar y orquestar el dataFrame recibido.
    Esta funcion, actua como pipeline ETL de ingesta.
    Esta funcion se divide en 3

"""

