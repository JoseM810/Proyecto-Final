"""Índice de los usuarios de la red, buscables por nombre."""
from estructuras.arbol_bst import ArbolBST
from estructuras.errores import EntradaInvalidaError, NombreDuplicadoError


class IndiceUsuarios:
    """Guarda los usuarios en un ArbolBST ordenado por nombre.

    Cumple la spec 05-indice-usuarios v1.0.
    """

    def __init__(self):
        self._arbol = ArbolBST()

    def agregar(self, nombre, usuario):
        """Registra el usuario con ese nombre. Tiempo O(h), espacio O(1).

        Lanza EntradaInvalidaError si nombre no es un texto no vacío o usuario
        es None (se revisa primero), y NombreDuplicadoError si el nombre ya existe.
        """
        if not isinstance(nombre, str) or nombre == "":
            raise EntradaInvalidaError("el nombre debe ser un texto no vacío")
        if usuario is None:
            raise EntradaInvalidaError("el usuario no puede ser nulo")
        if not self._arbol.insertar(nombre, usuario):
            raise NombreDuplicadoError("ya existe un usuario con ese nombre")

    def buscar(self, nombre):
        """Devuelve el usuario con ese nombre exacto, o None si no existe.

        Un nombre que no es texto devuelve None. Tiempo O(h), espacio O(1).
        """
        if not isinstance(nombre, str):
            return None
        return self._arbol.buscar(nombre)

    def listar(self):
        """Entrega los nombres en orden alfabético, uno a uno.

        Tiempo O(n), espacio O(h).
        """
        return self._arbol.recorrer_en_orden()

    def cantidad(self):
        """Cantidad de usuarios registrados. Tiempo O(1), espacio O(1)."""
        return self._arbol.tamanio()