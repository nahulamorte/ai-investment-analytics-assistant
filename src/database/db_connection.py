import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import os



_conexion_pool = None

def inicializar_pool():
    global _conexion_pool

    if _conexion_pool is None:
        try:
            _conexion_pool = pool.ThreadedConnectionPool(
                minconn=2,
                maxconn=10,
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', 'WarrenMinds2026'),
                host=os.environ.get('DB_HOST', 'localhost'),
                port=os.environ.get('DB_PORT', '5432'),
                database=os.environ.get('DB_NAME', 'buffettminds_db')
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
        inicializar_pool()

    conexion_fisica = _conexion_pool.getconn()

    try:
        yield conexion_fisica
        conexion_fisica.commit()
    except Exception as e:
        print(f"Error durante la operación con la base de datos: {e}")
        conexion_fisica.rollback()
        raise e
    finally:
        _conexion_pool.putconn(conexion_fisica)



