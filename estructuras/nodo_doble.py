"""Nodo con enlace a sus dos vecinos."""


class NodoDoble:
    """Guarda un valor y referencias al nodo anterior y al siguiente."""

    __slots__ = ("valor", "anterior", "siguiente")

    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.siguiente = None