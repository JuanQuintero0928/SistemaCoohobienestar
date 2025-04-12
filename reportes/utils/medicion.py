import time
import psutil
import os
import logging
from functools import wraps
from datetime import datetime
from django.db import connection

logger = logging.getLogger(__name__)

def medir_rendimiento(nombre_test="test"):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            proceso = psutil.Process(os.getpid())
            mem_inicio = proceso.memory_info().rss / (1024 * 1024)
            tiempo_inicio = time.time()

            # Limpiar queries previas
            connection.queries_log.clear()

            resultado = func(*args, **kwargs)

            tiempo_fin = time.time()
            mem_fin = proceso.memory_info().rss / (1024 * 1024)

            tiempo_total = tiempo_fin - tiempo_inicio
            memoria_usada = mem_fin - mem_inicio
            num_consultas = len(connection.queries)

            queries_sql = "\n".join(
                f"{i+1}. ({q['time']}s) {q['sql']}" for i, q in enumerate(connection.queries)
            )

            resumen = (
                f"[{nombre_test}] Tiempo total: {tiempo_total:.2f} segundos\n"
                f"[{nombre_test}] Memoria usada: {memoria_usada:.2f} MB\n"
                f"[{nombre_test}] Consultas a la base de datos: {num_consultas}\n"
                # f"[{nombre_test}] Detalle de queries:\n{queries_sql}\n"
            )

            # Imprimir en consola
            print(resumen)

            # Guardar en log si está configurado
            logger.info(resumen)

            # Guardar en archivo de texto
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            ruta_archivo = os.path.join("logs_rendimiento", f"{nombre_test}_{timestamp}.txt")

            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

            with open(ruta_archivo, "w") as f:
                f.write(resumen)

            return resultado
        return wrapper
    return decorador
