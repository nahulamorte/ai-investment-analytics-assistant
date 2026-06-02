import psycopg2
# Importamos tus funciones analíticas desde el conector de producción
from database.db_connection import inicializar_pool, obtener_conexion


def ejecutar_test_infraestructura():
    print("==================================================")
    print("📡 INICIANDO PRUEBA DE HUMO DE PERSISTENCIA")
    print("==================================================")

    try:
        # 1. Encendemos el motor del pool (Leerá tu archivo .env local de forma segura)
        print("⏳ Paso 1: Inicializando el pool de conexiones relacional...")
        inicializar_pool()
        print("✅ Pool configurado en memoria RAM.")

        print("\n⏳ Paso 2: Solicitando socket al pool mediante Context Manager...")
        # 2. Consumimos el generador de contexto emulando el try-with-resources
        with obtener_conexion() as conn:
            print("🔑 Conexión física prestada con éxito por el Pool.")

            # En psycopg2 los cursores también implementan context manager nativo
            with conn.cursor() as cursor:
                print("📡 Enviando sentencia de control 'SELECT version();' a PostgreSQL...")

                # 3. Ejecutamos la consulta de diagnóstico del sistema
                cursor.execute("SELECT version();")

                # 4. Recuperamos el registro devuelto por el motor (fetchone)
                datos_servidor = cursor.fetchone()

                print("\n🖥️  RESPUESTA OFICIAL DEL MOTOR DOCKER:")
                print("-" * 50)
                print(datos_servidor[0])
                print("-" * 50)

                # Al ser un SELECT de control no alteramos datos, pero cerramos el bloque
                print("\n♻️ Fin del bloque de negocio. Liberando cursor...")

        # 5. Si salimos del bloque with sin excepciones, confirmamos el retorno automático
        print("\n🎉 [PASS] Contexto cerrado. La conexión fue devuelta al Pool de forma transparente.")
        print("==================================================")

    except KeyError as error_config:
        print(f"\n🚨 [FAIL] Error de Inyección Fail-Fast: Falta la variable de entorno {error_config}")
        print("Asegurate de que tu archivo .env local contenga todas las credenciales requeridas.")

    except psycopg2.OperationalError as error_red:
        print(f"\n🚨 [FAIL] Error de Red u Operaciones: {error_red}")
        print("Verificá que tu contenedor Docker de PostgreSQL esté encendido y escuchando en el puerto correcto.")

    except Exception as e:
        print(f"\n💥 Error inesperado durante el test de persistencia: {e}")


if __name__ == "__main__":
    ejecutar_test_infraestructura()