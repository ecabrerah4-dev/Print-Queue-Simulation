import unittest 

from cola import Queue  # Clase de cola propia.
from trabajo import PrintTask  # Modelo de trabajo.
from impresora import Printer  # Modelo de impresora.
from simulacion import crear_trabajo, ejecutar_simulacion  # Motor y validaciones.


class TestQueueFIFO(unittest.TestCase):

    def test_fifo_basico(self):
        q = Queue() 
        self.assertTrue(q.is_empty()) 
        q.enqueue(10) 
        q.enqueue(20)
        self.assertEqual(q.size(), 2)
        self.assertEqual(q.dequeue(), 10) 
        self.assertEqual(q.peek(), 20) 
        self.assertEqual(q.dequeue(), 20) 
        self.assertTrue(q.is_empty()) 

    def test_dequeue_vacio(self):
        q = Queue()  
        with self.assertRaises(IndexError): 
            q.dequeue()  


class TestSimulacion(unittest.TestCase):

    def test_sin_trabajos(self):
        r = ejecutar_simulacion([], seconds_per_page=1.0)
        self.assertEqual(r["total_procesados"], 0)  
        self.assertEqual(r["max_tamano_cola"], 0)

    def test_metricas_orden_llegada(self):
        t1 = crear_trabajo(1, 1, 0.0) 
        t2 = crear_trabajo(2, 1, 0.0)  
        r = ejecutar_simulacion([t1, t2], seconds_per_page=1.0) 
        self.assertEqual(r["total_procesados"], 2)  #
        self.assertEqual(r["max_tamano_cola"], 1)  

        segundo = next(x for x in r["completados"] if x.task_id == 2) 
        self.assertAlmostEqual(segundo.wait_time, 1.0, places=5)

    def test_paginas_invalidas(self):
        with self.assertRaises(ValueError):
            crear_trabajo("x", 0, 0.0)  


class TestPrinter(unittest.TestCase):
    """Comportamiento básico de ocupación y finalización."""

    def test_busy_hasta_fin(self):
        p = Printer(seconds_per_page=2.0) 
        t = PrintTask("a", 3, 0.0)  
        p.start_printing(t, current_time=10.0)
        self.assertTrue(p.is_busy(10.0)) 
        self.assertTrue(p.is_busy(15.0))  
        self.assertFalse(p.is_busy(16.0))  
        done = p.finish_if_due(16.0)  
        self.assertIsNotNone(done) 
        self.assertEqual(done.task_id, "a") 


if __name__ == "__main__":
    unittest.main() 
