"""Feed de publicaciones de una persona de la red."""
from dominio.hilo_comentarios import HiloComentarios
from estructuras.errores import (
    FinDelFeedError,
    InicioDelFeedError,
    PublicacionInvalidaError,
    PublicacionNoEncontradaError,
    BusquedaInvalidaError,
)
from estructuras.lista_doble import ListaDoble


class Publicacion:
    """Registro de lo que se publicó (texto) y cuándo (fecha, día de la simulación).

    Cada publicación tiene un identificador entero asignado por el feed y su
    propio hilo de comentarios asociado.
    """

    __slots__ = ("id", "texto", "fecha", "hilo")

    def __init__(self, id_publicacion, texto, fecha):
        self.id = id_publicacion
        self.texto = texto
        self.fecha = fecha
        self.hilo = HiloComentarios()


class Feed:
    """Guarda las publicaciones en una ListaDoble, la más reciente primero.

    Cada publicación tiene un identificador entero asignado por el feed y su
    propio hilo de comentarios asociado.

    Cumple la spec 03-feed v1.0.
    """

    def __init__(self):
        self._lista = ListaDoble()
        self._siguiente_id = 1

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
        publicacion = Publicacion(self._siguiente_id, texto, fecha)
        self._siguiente_id += 1
        self._lista.insertar_al_inicio(publicacion)

    def obtener_por_id(self, id_publicacion):
        """Devuelve la publicación con el identificador dado.

        Tiempo O(n), espacio O(1), con n la cantidad de publicaciones.
        Lanza PublicacionNoEncontradaError si no existe.
        """
        if not isinstance(id_publicacion, int) or isinstance(id_publicacion, bool):
            raise PublicacionNoEncontradaError("el ID debe ser un entero")
        for p in self._lista.recorrer():
            if p.id == id_publicacion:
                return p
        raise PublicacionNoEncontradaError("no existe una publicación con ese ID")

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

    def buscar(self, palabra):
        """Entrega las publicaciones cuyo texto contiene palabra, de la más reciente a la más antigua.

        No distingue mayúsculas de minúsculas ni modifica el feed ni la posición
        actual. Tiempo O(n·m) al recorrer todo (n publicaciones, m longitud del
        texto), espacio O(1).
        Lanza BusquedaInvalidaError, al llamar y no al recorrer, si palabra no
        es un texto no vacío.
        """
        if not isinstance(palabra, str) or palabra == "":
            raise BusquedaInvalidaError("la palabra debe ser un texto no vacío")
        return self._buscar(palabra.lower())

    def _buscar(self, palabra_minuscula):
        """Generador interno de buscar, con la palabra ya validada y en minúsculas."""
        for publicacion in self._lista.recorrer():
            if palabra_minuscula in publicacion.texto.lower():
                yield publicacion

    def cantidad(self):
        """Cantidad de publicaciones. Tiempo O(1), espacio O(1)."""
        return self._lista.tamanio()

    def recorrer(self):
        """Entrega las publicaciones de la más reciente a la más antigua.

        Es un generador. Tiempo O(n), espacio O(1).
        """
        return self._lista.recorrer()