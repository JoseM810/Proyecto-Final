"""Feed de publicaciones de una persona de la red."""
from estructuras.errores import (
    FinDelFeedError,
    InicioDelFeedError,
    PublicacionInvalidaError,
)
from estructuras.lista_doble import ListaDoble


class Publicacion:
    """Registro de lo que se publicó (texto) y cuándo (fecha, día de la simulación)."""

    __slots__ = ("texto", "fecha")

    def __init__(self, texto, fecha):
        self.texto = texto
        self.fecha = fecha


class Feed:
    """Guarda las publicaciones en una ListaDoble, la más reciente primero.

    Cumple la spec 03-feed v1.0.
    """

    def __init__(self):
        self._lista = ListaDoble()

    def publicar(self, texto, fecha):
        """Agrega la publicación como la más reciente y la deja como actual.

        Tiempo O(1), espacio O(1).
        Lanza PublicacionInvalidaError si texto no es un texto no vacío o si
        fecha no es un entero mayor o igual que 0.
        """
        if not isinstance(texto, str) or texto == "":
            raise PublicacionInvalidaError("el texto debe ser no vacío")
        if not isinstance(fecha, int) or isinstance(fecha, bool) or fecha < 0:
            raise PublicacionInvalidaError("la fecha debe ser un entero >= 0")
        self._lista.insertar_al_inicio(Publicacion(texto, fecha))

    def actual(self):
        """Publicación en la posición actual, o None si el feed está vacío.

        Tiempo O(1), espacio O(1).
        """
        return self._lista.actual()

    def avanzar(self):
        """Pasa a la siguiente publicación más antigua y la devuelve.

        Tiempo O(1), espacio O(1).
        Lanza FinDelFeedError si no hay una más antigua o el feed está vacío.
        """
        if not self._lista.avanzar():
            raise FinDelFeedError("no hay publicaciones más antiguas")
        return self._lista.actual()

    def retroceder(self):
        """Pasa a la siguiente publicación más reciente y la devuelve.

        Tiempo O(1), espacio O(1).
        Lanza InicioDelFeedError si no hay una más reciente o el feed está vacío.
        """
        if not self._lista.retroceder():
            raise InicioDelFeedError("no hay publicaciones más recientes")
        return self._lista.actual()

    def cantidad(self):
        """Cantidad de publicaciones. Tiempo O(1), espacio O(1)."""
        return self._lista.tamanio()