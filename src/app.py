import sys
from ingestion.yfinance_extractor import obtener_historico_limpio
from database.db_connection import obtener_conexion
from database.queries import insert_historial_precios, get_activos


def ejecutar_pipeline() -> None:
    # Logs iniciales de control en consola
    print("=" * 60)
    print("🚀 INICIALIZANDO PIPELINE TRANSACCIONAL DINÁMICO - LARA AI")
    print("=" * 60)

    try:
        print("[CORE] Solicitando conexión segura al Pool de PostgreSQL...")

        # Abrimos el bloque contextual de la conexión (Maneja Auto-commit y Auto-rollback)
        with obtener_conexion() as conn:
            print("[CORE] Conexión establecida de forma exitosa.")

            # Paso 1: Consultamos la tabla maestra 'activo_financiero' para eliminar el hardcodeo
            activos = get_activos(conn)
            print(f"[ETL] Se descubrieron {len(activos)} activos maestros en la base de datos.")
            print("-" * 50)

            # Paso 2: Iteramos el lote completo de activos recuperados de la base de datos
            for activo in activos:
                id_activo = activo[0]
                ticker = activo[1]

                print(f"👉 Procesando instrumento: {ticker} (ID Relacional: {id_activo})")

                # Paso 3: Viajamos a la API de Yahoo Finance, transformamos a tipos nativos y limpiamos nulos
                datos_ETL = obtener_historico_limpio(ticker, "1mo", id_activo)

                # Paso 4: Inyección en lote masivo (Bulk Ingestion) sobre la tabla historial_precios
                filas_afectadas = insert_historial_precios(conn, datos_ETL)
                print(f"   ↳ [SQL SUCCESS] Registros sincronizados en disco: {filas_afectadas}\n")

    except Exception as e:
        # Si falla el contenedor Docker, la red de yfinance o la sintaxis SQL, cae acá de forma segura
        print(f"\n❌ [CRITICAL ERROR] El pipeline falló catastróficamente: {e}")
        print("[CORE] Ejecutando aborto seguro del sistema.")
        sys.exit(1)

    print("=" * 60)
    print("🏁 PIPELINE CONSOLIDADO - PRUEBA DE INTEGRACIÓN COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    # Invocamos la ejecución pura del orquestador
    ejecutar_pipeline()