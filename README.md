simuladorvimpresion
 main.py # Interfaz gráfica
 simulacion.py # Lógica de simulación
 cola.py # Implementación de cola FIFO
 impresora.py # Modelo de impresora
 trabajo.py # Modelo de tarea de impresión
 test_simulacion.py # Pruebas unitarias
 
 Instalación y Ejecución

Pasos
 **Descargar** todos los archivos en la misma carpeta
 Cómo Usar

Agregar trabajos
Páginas: Número entero ≥ 1

Llegada (segundos): Tiempo de llegada a la cola

Presionar "Agregar"

Gestionar
Vaciar cola: Elimina todos los trabajos

Ejecutar simulación: Procesa los trabajos

Ver resultados
Pestaña "Cola": Trabajos pendientes

Pestaña "Resumen": Métricas y detalles

 Ejemplo
Segundos por página = 2.0

Agregar: Páginas = 5, Llegada = 0.0

Agregar: Páginas = 3, Llegada = 2.0

Presionar "Ejecutar simulación"

 Pruebas Unitarias
bash
pyhon -m unittest test_simulacion.py -v
Verifica:

Comportamiento FIFO

Cola vacía

Simulación sin trabajos

Cálculo de tiempos

Validación de datos

 Componentes
Queue (cola.py)
Cola FIFO con: enqueue(), dequeue(), peek(), is_empty(), size()

Printer (impresora.py)
Modela impresora con: is_busy(), start_printing(), finish_if_due()

PrintTask (trabajo.py)
Tarea con: ID, páginas, tiempo de llegada, inicio y espera

ejecutar_simulacion() (simulacion.py)
Motor principal de simulación basado en eventos

 Lógica de Simulación
Ordenar trabajos por tiempo de llegada

Avanzar al siguiente evento (llegada o finalización)

Encolar trabajos que llegan

Imprimir si la impresora está libre

Calcular métricas al finalizar

Errores Comunes
"Segundos por página debe ser mayor que 0" → Verificar valor

"Páginas debe ser entero ≥ 1" → Usar número positivo

"Tiempo de llegada debe ser ≥ 0" → Usar valor no negativo

"Cola vacía" → Agregar trabajos antes de simular
y eso seria todo gracias....😎😎
