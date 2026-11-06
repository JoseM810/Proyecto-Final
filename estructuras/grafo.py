"""Grafo dirigido con listas de adyacencia enlazadas."""
from estructuras.nodo import Nodo


class ListaAdyacencia:
    """Lista enlazada de identificadores de vecinos, con primero y último.

    Invariante de representación: no hay identificadores repetidos;
    _tamanio es la cantidad de nodos alcanzables desde _primero; _ultimo es
    el último nodo de la cadena, o None si la lista está vacía.
    """

    def __init__(self):
        self._primero = None
        self._ultimo = None
        self._tamanio = 0

    def agregar_si_no_existe(self, id_vecino):
        """Agrega id_vecino al final. Devuelve True si lo agregó y False si ya estaba.

        Tiempo O(g), con g el tamaño de la lista: hay que recorrerla para
        comprobar que no esté. Espacio O(1).
        """
        actual = self._primero
        while actual is not None:
            if actual.valor == id_vecino:
                return False
            actual = actual.siguiente
        nodo = Nodo(id_vecino)
        if self._ultimo is None:
            self._primero = nodo
        else:
            self._ultimo.siguiente = nodo
        self._ultimo = nodo
        self._tamanio += 1
        return True

    def quitar(self, id_vecino):
        """Quita id_vecino. Devuelve True si estaba y False si no.

        Tiempo O(g), espacio O(1).
        """
        anterior = None
        actual = self._primero
        while actual is not None:
            if actual.valor == id_vecino:
                if anterior is None:
                    self._primero = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                if actual is self._ultimo:
                    self._ultimo = anterior
                self._tamanio -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def contiene(self, id_vecino):
        """True si id_vecino está en la lista. Tiempo O(g), espacio O(1)."""
        actual = self._primero
        while actual is not None:
            if actual.valor == id_vecino:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        """Entrega los identificadores en el orden en que se agregaron (generador).

        Tiempo O(g) para recorrer todo, espacio O(1).
        """
        actual = self._primero
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def tamanio(self):
        """Cantidad de vecinos. Tiempo O(1), espacio O(1)."""
        return self._tamanio


class GrafoDirigido:
    """Grafo dirigido: una ListaAdyacencia por vértice.

    Los vértices se numeran 0, 1, 2… El arreglo _listas es soporte interno
    (ver plan.md): da acceso al vértice por su número en O(1). Esta clase
    supone identificadores válidos; los valida RedSeguimiento.
    """

    def __init__(self):
        self._listas = []

    def agregar_vertice(self):
        """Agrega un vértice sin aristas y devuelve su número. Tiempo O(1) amortizado."""
        self._listas.append(ListaAdyacencia())
        return len(self._listas) - 1

    def cantidad_vertices(self):
        """Cantidad de vértices. Tiempo O(1), espacio O(1)."""
        return len(self._listas)

    def agregar_arista(self, origen, destino):
        """Agrega la arista origen -> destino. True si era nueva, False si ya existía.

        Tiempo O(g), espacio O(1).
        """
        return self._listas[origen].agregar_si_no_existe(destino)

    def quitar_arista(self, origen, destino):
        """Quita la arista origen -> destino. True si existía, False si no.

        Tiempo O(g), espacio O(1).
        """
        return self._listas[origen].quitar(destino)

    def existe_arista(self, origen, destino):
        """True si existe la arista origen -> destino. Tiempo O(g), espacio O(1)."""
        return self._listas[origen].contiene(destino)

    def vecinos(self, origen):
        """Entrega los destinos de las aristas que salen de origen, en orden de inserción.

        Tiempo O(g), espacio O(1).
        """
        return self._listas[origen].recorrer()