from cola import Queue
from trabajo import PrintTask
from impresora import Printer


def _validar_trabajo(task_id, pages, arrival):
    if not isinstance(task_id, (int, str)):
        raise ValueError("El identificador del trabajo debe ser int o str.")
    if not isinstance(pages, int) or pages < 1:
        raise ValueError("Las páginas deben ser un entero >= 1.")
    if not isinstance(arrival, (int, float)) or arrival < 0:
        raise ValueError("El tiempo de llegada debe ser un número >= 0.")


def crear_trabajo(task_id, pages, arrival):
    _validar_trabajo(task_id, pages, arrival)
    return PrintTask(task_id, pages, arrival)


def ejecutar_simulacion(
    trabajos,
    seconds_per_page,
    tiempo_fin_simulacion=None,
):

    cola = Queue()
    impresora = Printer(seconds_per_page)

    if not isinstance(seconds_per_page, (int, float)) or seconds_per_page <= 0:
        raise ValueError("seconds_per_page debe ser un número positivo.")
    pendientes = sorted(trabajos, key=lambda t: t.arrival_time)
   
    idx_llegada = 0
    tiempo = 0.0
    max_cola = 0
    completados = []

    if not pendientes:
        return {
            "completados": [],
            "total_procesados": 0,
            "promedio_espera": 0.0,
            "max_espera": 0.0,
            "tarea_max_espera": None,
            "max_tamano_cola": 0,
            "tiempo_final": 0.0,
        }

    if tiempo_fin_simulacion is None:
        ultima_llegada = max(t.arrival_time for t in pendientes)
        tiempo_fin_simulacion = ultima_llegada + sum(t.pages for t in pendientes) * seconds_per_page + 1.0

    while tiempo <= tiempo_fin_simulacion:
        while idx_llegada < len(pendientes) and pendientes[idx_llegada].arrival_time <= tiempo:
            cola.enqueue(pendientes[idx_llegada])
            idx_llegada += 1
        max_cola = max(max_cola, cola.size())
        if not impresora.is_busy(tiempo) and not cola.is_empty():
            siguiente = cola.dequeue()
            impresora.start_printing(siguiente, tiempo)
        candidatos = []

        if idx_llegada < len(pendientes):
            candidatos.append(pendientes[idx_llegada].arrival_time)

        bu = impresora.get_busy_until()
        if bu is not None:
            candidatos.append(bu)

        if not candidatos:
            if cola.is_empty() and not impresora.is_busy(tiempo) and idx_llegada >= len(pendientes):
                break
            tiempo += 0.001
            continue

        futuros = [c for c in candidatos if c > tiempo]
        if not futuros:
            if cola.is_empty() and not impresora.is_busy(tiempo) and idx_llegada >= len(pendientes):
                break
            tiempo += 0.001
            continue
        siguiente_tiempo = min(futuros)
        tiempo = siguiente_tiempo

        terminado = impresora.finish_if_due(tiempo)
        if terminado is not None:
            terminado.wait_time = terminado.start_time - terminado.arrival_time
            completados.append(terminado)
        if idx_llegada >= len(pendientes) and cola.is_empty() and not impresora.is_busy(tiempo):
            break

    total = len(completados)
    if total == 0:
        promedio = 0.0
        max_espera = 0.0
        tarea_max = None
    else:
        suma_espera = sum(t.wait_time for t in completados)
        promedio = suma_espera / total
        tarea_max = max(completados, key=lambda t: t.wait_time)
        max_espera = tarea_max.wait_time

    return {
        "completados": completados,
        "total_procesados": total,
        "promedio_espera": promedio,
        "max_espera": max_espera,
        "tarea_max_espera": tarea_max,
        "max_tamano_cola": max_cola,
        "tiempo_final": tiempo,
    }
