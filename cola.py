
class Queue:

    def __init__(self):
        self._items = []

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("No se puede hacer dequeue: la cola está vacía.")
        return self._items.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("No se puede hacer peek: la cola está vacía.")
        return self._items[0]