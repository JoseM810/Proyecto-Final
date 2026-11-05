"""Historial de navegación: permite volver a la pantalla anterior."""
from estructuras.errores import NadaAtrasError, PantallaInvalidaError
from estructuras.pila import PilaEnlazada


class Historial:
    """Recuerda las pantallas visitadas usando una PilaEnlazada.

    La pantalla actual es el tope de la pila. Cumple la spec 01-historial v1.0.
    """

    def __init__(self):
        self._pantallas = PilaEnlazada()

    def visitar(self, pantalla):
        """Registra pantalla como la actual. Tiempo O(1), espacio O(1).

        Lanza PantallaInvalidaError si pantalla es None o texto vacío.
        """
        if pantalla is None or pantalla == "":
            raise PantallaInvalidaError("la pantalla no puede ser nula ni vacía")
        self._pantallas.apilar(pantalla)

    def volver(self):
        """Vuelve a la pantalla anterior y la devuelve. Tiempo O(1), espacio O(1).

        La pantalla abandonada deja de ser alcanzable.
        Lanza NadaAtrasError si hay menos de dos pantallas.
        """
        if self._pantallas.tamanio() < 2:
            raise NadaAtrasError("no hay pantalla anterior")
        self._pantallas.desapilar()
        return self._pantallas.ver_tope()

    def actual(self):
        """Pantalla actual, o None si no se visitó ninguna. Tiempo O(1)."""
        if self._pantallas.tamanio() == 0:
            return None
        return self._pantallas.ver_tope()

    def cantidad(self):
        """Pantallas alcanzables, contando la actual. Tiempo O(1)."""
        return self._pantallas.tamanio()