import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import os


_conexion_pool = None

def inicializar_conexion():
    global _conexion_pool

    if _conexion_pool is None:
        try:
            _conexion_pool = pool.ThreadedConnectionPool(
                minconn= 2,
                maxconn= 10,
                user = os.environ['DB_USER'],
                password = os.environ['DB_PASSWORD'],
                host = os.environ['DB_HOST'],
                port = os.environ['DB_PORT'],
                database = os.environ['DB_NAME']
            )

        except psycopg2.OperationalError as err_infra:
            print('Fallo en la infraestructura, Proba con docker')
            raise
        except Exception as e:
            print('Algo fallo')
            raise

@contextmanager
def obtener_conexion():
    global _conexion_pool

    if _conexion_pool is None:
        raise RuntimeError("El pool de conexiones no ha sido inicializado.")

    conexion_fisica = _conexion_pool.getConn()

    try:
        yield conexion_fisica
    finally:
        _conexion_pool.putconn(conexion_fisica)



