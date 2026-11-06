"""Hilo de comentarios de una publicación."""
from estructuras.errores import ComentarioInvalidoError, ComentarioNoEncontradoError
from estructuras.pila import PilaEnlazada


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

    def responder(self, id_padre, autor, texto):
        """Crea una respuesta al comentario id_padre y devuelve su identificador.

        Tiempo O(1) amortizado, espacio O(1).
        Lanza ComentarioInvalidoError si autor o texto no son válidos (se revisa
        primero) y ComentarioNoEncontradoError si id_padre no existe.
        """
        self._validar(autor, texto)
        padre = self._buscar(id_padre)
        return self._agregar_hijo(padre, autor, texto)

    def obtener(self, id_comentario):
        """Devuelve el comentario con ese identificador. Tiempo O(1), espacio O(1).

        Lanza ComentarioNoEncontradoError si no existe.
        """
        return self._buscar(id_comentario)

    def recorrer(self):
        """Entrega los comentarios en preorden, cada uno después de su padre.

        Es un generador: devuelve los nodos uno a uno (cada uno con su
        profundidad), sin construir una lista y sin recursión. Usa una
        PilaEnlazada para recordar el hermano pendiente de cada nivel.
        Tiempo O(n) para recorrer todo, espacio O(h), con h la profundidad
        máxima. No modifica el hilo.
        """
        pila = PilaEnlazada()
        actual = self._raiz.primer_hijo
        while actual is not None or pila.tamanio() > 0:
            if actual is None:
                actual = pila.desapilar()
            yield actual
            if actual.siguiente_hermano is not None:
                pila.apilar(actual.siguiente_hermano)
            actual = actual.primer_hijo

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

    def _buscar(self, id_comentario):
        """Devuelve el nodo con ese id leyendo el arreglo de apoyo. Tiempo O(1).

        Un id válido es un entero (no booleano) entre 1 y cantidad(); el 0 es
        la raíz virtual y no cuenta como comentario.
        """
        if (
            not isinstance(id_comentario, int)
            or isinstance(id_comentario, bool)
            or id_comentario < 1
            or id_comentario > self._cantidad
        ):
            raise ComentarioNoEncontradoError("no existe ese comentario")
        return self._nodos[id_comentario]
        