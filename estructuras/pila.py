"""Pila enlazada: el último en entrar es el primero en salir."""
from estructuras.nodo import Nodo
from estructuras.errores import PilaVaciaError


class PilaEnlazada:
    """Pila implementada con nodos enlazados, sin usar list ni deque.

    Invariante de representación: _tamanio es la cantidad de nodos
    alcanzables desde _tope, y _tope es None si y solo si _tamanio es 0.
    """

    def __init__(self):
        self._tope = None
        self._tamanio = 0

    def apilar(self, valor):
        """Pone valor en el tope. Tiempo O(1), espacio O(1)."""
        self._tope = Nodo(valor, self._tope)
        self._tamanio += 1

    def desapilar(self):
        """Quita y devuelve el tope. Tiempo O(1), espacio O(1).

        Lanza PilaVaciaError si no hay elementos.
        """
        if self._tope is None:
            raise PilaVaciaError("la pila está vacía")
        nodo = self._tope
        self._tope = nodo.siguiente
        self._tamanio -= 1
        return nodo.valor

    def ver_tope(self):
        """Devuelve el tope sin quitarlo. Tiempo O(1), espacio O(1).

        Lanza PilaVaciaError si no hay elementos.
        """
        if self._tope is None:
            raise PilaVaciaError("la pila está vacía")
        return self._tope.valor

    def tamanio(self):
        """Cantidad de elementos. Tiempo O(1), espacio O(1)."""
        return self._tamanio