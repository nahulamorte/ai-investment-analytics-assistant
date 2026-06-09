#Patron DAO
#imports
from typing import List, Tuple
from psycopg2 import extensions

def insert_historial_precios(connection: extensions.connection, datos_precios: List[Tuple]) -> int:
    insert_query = """
            INSERT INTO historial_precios (precio_cierre, fecha, id_activo) 
            VALUES (%s, %s, %s)
            ON CONFLICT (fecha, id_activo)
            DO UPDATE SET 
                precio_cierre = EXCLUDED.precio_cierre;
        """

    registros_insertados = 0
    with connection.cursor() as cursor:
        try:
            cursor.executemany(insert_query, datos_precios)
            registros_insertados = cursor.rowcount
        except Exception as e:
            print(f"Error al insertar datos en historial_precios: {e}")
            raise e

    return registros_insertados


def get_activos(connection: extensions.connection)-> List[Tuple[int, str]]:
    query = "SELECT id_activo, ticker FROM activo_financiero"

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener activos financieros: {e}")
            raise e


