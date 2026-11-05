"""Cola enlazada: el primero en entrar es el primero en salir."""
from estructuras.nodo import Nodo
from estructuras.errores import ColaVaciaError


class ColaEnlazada:
    """Cola con referencias al frente y al final, sin usar list ni deque.

    Invariante de representación: _frente es None si y solo si _final es
    None si y solo si _tamanio es 0; _tamanio es la cantidad de nodos
    alcanzables desde _frente.
    """

    def __init__(self):
        self._frente = None
        self._final = None
        self._tamanio = 0

    def encolar(self, valor):
        """Agrega valor al final. Tiempo O(1), espacio O(1)."""
        nodo = Nodo(valor)
        if self._final is None:
            self._frente = nodo
        else:
            self._final.siguiente = nodo
        self._final = nodo
        self._tamanio += 1

    def desencolar(self):
        """Quita y devuelve el elemento del frente. Tiempo O(1), espacio O(1).

        Lanza ColaVaciaError si no hay elementos.
        """
        if self._frente is None:
            raise ColaVaciaError("la cola está vacía")
        nodo = self._frente
        self._frente = nodo.siguiente
        if self._frente is None:
            self._final = None
        self._tamanio -= 1
        return nodo.valor

    def ver_frente(self):
        """Devuelve el elemento del frente sin quitarlo. Tiempo O(1), espacio O(1).

        Lanza ColaVaciaError si no hay elementos.
        """
        if self._frente is None:
            raise ColaVaciaError("la cola está vacía")
        return self._frente.valor

    def tamanio(self):
        """Cantidad de elementos. Tiempo O(1), espacio O(1)."""
        return self._tamanio