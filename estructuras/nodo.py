"""Nodo simple, reutilizable por las estructuras enlazadas del proyecto."""


class Nodo:
    """Guarda un valor y una referencia al nodo que le sigue."""

    __slots__ = ("valor", "siguiente")

    def __init__(self, valor, siguiente=None):
        self.valor = valor
        self.siguiente = siguiente