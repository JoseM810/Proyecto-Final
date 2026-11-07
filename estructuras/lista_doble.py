"""Lista doblemente enlazada con cursor."""
from estructuras.nodo_doble import NodoDoble


class ListaDoble:
    """Lista de nodos enlazados en ambos sentidos, con una posición actual.

    Invariante de representación: _cabeza.anterior es None; para todo nodo n
    con n.siguiente distinto de None se cumple n.siguiente.anterior is n;
    _tamanio es la cantidad de nodos alcanzables desde _cabeza; _actual es
    None si y solo si _tamanio es 0.
    """

    def __init__(self):
        self._cabeza = None
        self._actual = None
        self._tamanio = 0

    def insertar_al_inicio(self, valor):
        """Pone valor antes de la cabeza y deja el cursor en él.

        Tiempo O(1), espacio O(1).
        """
        nodo = NodoDoble(valor)
        nodo.siguiente = self._cabeza
        if self._cabeza is not None:
            self._cabeza.anterior = nodo
        self._cabeza = nodo
        self._actual = nodo
        self._tamanio += 1

    def actual(self):
        """Valor en la posición actual, o None si la lista está vacía.

        Tiempo O(1), espacio O(1).
        """
        if self._actual is None:
            return None
        return self._actual.valor

    def avanzar(self):
        """Mueve el cursor al nodo siguiente (el más antiguo).

        Devuelve True si se movió, False si no hay siguiente o la lista está
        vacía; en ese caso el cursor no cambia. Tiempo O(1), espacio O(1).
        """
        if self._actual is None or self._actual.siguiente is None:
            return False
        self._actual = self._actual.siguiente
        return True

    def retroceder(self):
        """Mueve el cursor al nodo anterior (el más reciente).

        Devuelve True si se movió, False si no hay anterior o la lista está
        vacía; en ese caso el cursor no cambia. Tiempo O(1), espacio O(1).
        """
        if self._actual is None or self._actual.anterior is None:
            return False
        self._actual = self._actual.anterior
        return True

    def recorrer(self):
        """Entrega los valores de la cabeza a la cola, del más reciente al más antiguo.

        Es un generador y no mueve el cursor. Tiempo O(n) para recorrer
        todo, espacio O(1).
        """
        nodo = self._cabeza
        while nodo is not None:
            yield nodo.valor
            nodo = nodo.siguiente
            
    def tamanio(self):
        """Cantidad de elementos. Tiempo O(1), espacio O(1)."""
        return self._tamanio
        