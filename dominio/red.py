"""Red de seguimiento entre usuarios: quién sigue a quién y recomendaciones."""
from estructuras.cola import ColaEnlazada
from estructuras.errores import AutoSeguimientoError, UsuarioNoExisteError
from estructuras.grafo import GrafoDirigido


class RedSeguimiento:
    """Guarda las relaciones de seguimiento en un GrafoDirigido.

    Cada usuario es un vértice identificado por un entero (0, 1, 2…).
    Cumple la spec 06-red v1.0. g es la cantidad de personas que sigue un
    usuario, V la cantidad de usuarios y E la de relaciones.
    """

    def __init__(self):
        self._grafo = GrafoDirigido()

    def agregar_usuario(self):
        """Registra un usuario sin relaciones y devuelve su identificador.

        Tiempo O(1) amortizado, espacio O(1).
        """
        return self._grafo.agregar_vertice()

    def cantidad_usuarios(self):
        """Cantidad de usuarios. Tiempo O(1), espacio O(1)."""
        return self._grafo.cantidad_vertices()

    def seguir(self, a, b):
        """a empieza a seguir a b. True si la relación era nueva, False si ya existía.

        Tiempo O(g), espacio O(1).
        Lanza UsuarioNoExisteError si a o b no existen (se revisa primero) y
        AutoSeguimientoError si a es igual a b.
        """
        self._validar(a)
        self._validar(b)
        if a == b:
            raise AutoSeguimientoError("un usuario no puede seguirse a sí mismo")
        return self._grafo.agregar_arista(a, b)

    def dejar_de_seguir(self, a, b):
        """a deja de seguir a b. True si la relación existía, False si no.

        Tiempo O(g), espacio O(1).
        Lanza UsuarioNoExisteError si a o b no existen.
        """
        self._validar(a)
        self._validar(b)
        return self._grafo.quitar_arista(a, b)

    def sigue(self, a, b):
        """True si a sigue a b. Tiempo O(g), espacio O(1).

        Lanza UsuarioNoExisteError si a o b no existen.
        """
        self._validar(a)
        self._validar(b)
        return self._grafo.existe_arista(a, b)

    def seguidos(self, a):
        """Entrega a quienes a sigue, en el orden en que empezó a seguirlos.

        Tiempo O(g), espacio O(1). Lanza UsuarioNoExisteError si a no existe.
        """
        self._validar(a)
        return self._grafo.vecinos(a)

    def recomendar(self, a):
        """Entrega personas que siguen los seguidos de a y que a no sigue ni es a.

        Búsqueda en anchura limitada a dos saltos. Sin repetidos, en el orden
        de la spec. Tiempo O(V + E), espacio O(V). No modifica la red.
        Lanza UsuarioNoExisteError si a no existe (al llamarla, no al iterar).
        """
        self._validar(a)
        return self._recomendar(a)

    def _recomendar(self, a):
        """Generador interno de recomendar, con a ya validado."""
        marcado = [False] * self._grafo.cantidad_vertices()  # soporte interno, ver plan.md
        marcado[a] = True
        frontera = ColaEnlazada()
        for amigo in self._grafo.vecinos(a):
            marcado[amigo] = True
            frontera.encolar(amigo)
        while frontera.tamanio() > 0:
            amigo = frontera.desencolar()
            for candidato in self._grafo.vecinos(amigo):
                if not marcado[candidato]:
                    marcado[candidato] = True
                    yield candidato

    def _validar(self, id_usuario):
        """Lanza UsuarioNoExisteError si id_usuario no es un entero entre 0 y cantidad - 1."""
        if (
            not isinstance(id_usuario, int)
            or isinstance(id_usuario, bool)
            or id_usuario < 0
            or id_usuario >= self._grafo.cantidad_vertices()
        ):
            raise UsuarioNoExisteError("no existe ese usuario")