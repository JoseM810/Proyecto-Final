"""Árbol binario de búsqueda, escrito con ciclos y sin recursión."""
from estructuras.pila import PilaEnlazada


class NodoArbol:
    """Guarda una clave, su valor y los dos hijos."""

    __slots__ = ("clave", "valor", "izquierdo", "derecho")

    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


class ArbolBST:
    """Árbol de búsqueda: a la izquierda las claves menores, a la derecha las mayores.

    Invariante de representación: para todo nodo, las claves de su subárbol
    izquierdo son menores que la suya y las de su subárbol derecho son
    mayores; _tamanio es la cantidad de nodos alcanzables desde _raiz.
    """

    def __init__(self):
        self._raiz = None
        self._tamanio = 0

    def insertar(self, clave, valor):
        """Agrega la clave con su valor. Devuelve True si la agregó y False si ya existía.

        Si ya existía, el árbol no cambia. Tiempo O(h), espacio O(1), con h la
        altura: O(log n) en promedio y O(n) si las claves llegan ya ordenadas.
        """
        nuevo = NodoArbol(clave, valor)
        if self._raiz is None:
            self._raiz = nuevo
            self._tamanio = 1
            return True
        actual = self._raiz
        while True:
            if clave == actual.clave:
                return False
            if clave < actual.clave:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    break
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    break
                actual = actual.derecho
        self._tamanio += 1
        return True

    def buscar(self, clave):
        """Devuelve el valor de la clave, o None si no existe.

        Tiempo O(h), espacio O(1).
        """
        actual = self._raiz
        while actual is not None:
            if clave == actual.clave:
                return actual.valor
            if clave < actual.clave:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

    def recorrer_en_orden(self):
        """Entrega las claves de menor a mayor, una a una (generador).

        Usa una PilaEnlazada para recordar los nodos pendientes. Tiempo O(n)
        para recorrer todo, espacio O(h). No modifica el árbol.
        """
        pila = PilaEnlazada()
        actual = self._raiz
        while actual is not None or pila.tamanio() > 0:
            while actual is not None:
                pila.apilar(actual)
                actual = actual.izquierdo
            actual = pila.desapilar()
            yield actual.clave
            actual = actual.derecho

    def tamanio(self):
        """Cantidad de claves. Tiempo O(1), espacio O(1)."""
        return self._tamanio