import sys
from ingestion.yfinance_extractor import obtener_historico_limpio
from database.db_connection import obtener_conexion
from database.queries import insert_historial_precios, get_activos


def ejecutar_pipeline() -> None:
    try:
        with obtener_conexion() as conn:
            activos = get_activos(conn)
            for activo in activos:
                id_activo = activo[0]
                ticker = activo[1]

                datos_ETL = obtener_historico_limpio(ticker, "1mo", id_activo)
                insert_historial_precios(conn, datos_ETL)

    except Exception as e:
        print(f"Error durante la ejecución del pipeline: {e}")
        sys.exit(1)
