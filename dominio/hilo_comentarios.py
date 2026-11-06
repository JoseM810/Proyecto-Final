"""Hilo de comentarios de una publicación."""
from estructuras.errores import ComentarioInvalidoError


class NodoComentario:
    """Un comentario dentro del árbol, en la forma primer-hijo / siguiente-hermano."""

    __slots__ = (
        "id",
        "autor",
        "texto",
        "profundidad",
        "primer_hijo",
        "ultimo_hijo",
        "siguiente_hermano",
    )

    def __init__(self, id_comentario, autor, texto, profundidad):
        self.id = id_comentario
        self.autor = autor
        self.texto = texto
        self.profundidad = profundidad
        self.primer_hijo = None
        self.ultimo_hijo = None
        self.siguiente_hermano = None


class HiloComentarios:
    """Árbol general de comentarios con una raíz virtual.

    La raíz virtual (id 0, profundidad -1) no es un comentario: sus hijos son
    los comentarios de primer nivel. _nodos es un arreglo de apoyo donde el
    nodo con id i está en la posición i. Cumple la spec 04-comentarios v1.0.

    Invariante de representación: _nodos[i].id == i; _cantidad es la cantidad
    de nodos sin contar la raíz virtual; el hijo tiene profundidad igual a la
    del padre más uno.
    """

    def __init__(self):
        self._raiz = NodoComentario(0, None, None, -1)
        self._nodos = [self._raiz]  # soporte interno, ver plan.md
        self._cantidad = 0

    def comentar(self, autor, texto):
        """Crea un comentario de primer nivel y devuelve su identificador.

        Tiempo O(1) amortizado, espacio O(1).
        Lanza ComentarioInvalidoError si autor o texto no son textos no vacíos.
        """
        self._validar(autor, texto)
        return self._agregar_hijo(self._raiz, autor, texto)

    def cantidad(self):
        """Cantidad de comentarios, respuestas incluidas. Tiempo O(1)."""
        return self._cantidad

    @staticmethod
    def _validar(autor, texto):
        """Lanza ComentarioInvalidoError si autor o texto no son textos no vacíos."""
        if not isinstance(autor, str) or autor == "":
            raise ComentarioInvalidoError("el autor debe ser un texto no vacío")
        if not isinstance(texto, str) or texto == "":
            raise ComentarioInvalidoError("el texto debe ser un texto no vacío")

    def _agregar_hijo(self, padre, autor, texto):
        """Enlaza un comentario nuevo al final de los hijos de padre.

        Tiempo O(1) amortizado: el enlace es O(1) y el arreglo de apoyo crece
        por append. Devuelve el identificador del comentario nuevo.
        """
        nodo = NodoComentario(self._cantidad + 1, autor, texto, padre.profundidad + 1)
        if padre.ultimo_hijo is None:
            padre.primer_hijo = nodo
        else:
            padre.ultimo_hijo.siguiente_hermano = nodo
        padre.ultimo_hijo = nodo
        self._nodos.append(nodo)
        self._cantidad += 1
        return nodo.id
        