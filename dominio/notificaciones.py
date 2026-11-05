"""Notificaciones pendientes de una persona de la red."""
from estructuras.cola import ColaEnlazada
from estructuras.errores import NotificacionInvalidaError

NUEVO_SEGUIDOR = "NUEVO_SEGUIDOR"
COMENTARIO = "COMENTARIO"
RESPUESTA = "RESPUESTA"


class Notificacion:
    """Registro de qué pasó (tipo) y quién lo causó (origen)."""

    __slots__ = ("tipo", "origen")

    def __init__(self, tipo, origen):
        self.tipo = tipo
        self.origen = origen


class BandejaNotificaciones:
    """Guarda las notificaciones de una persona en una ColaEnlazada.

    Se leen en el orden en que llegaron. Cumple la spec 02-notificaciones v1.0.
    """

    def __init__(self):
        self._cola = ColaEnlazada()

    def agregar(self, tipo, origen):
        """Deja la notificación pendiente, como la más reciente.

        Tiempo O(1), espacio O(1).
        Lanza NotificacionInvalidaError si tipo no es uno de los tres válidos
        o si origen no es un texto no vacío.
        """
        if tipo != NUEVO_SEGUIDOR and tipo != COMENTARIO and tipo != RESPUESTA:
            raise NotificacionInvalidaError("tipo de notificación inválido")
        if not isinstance(origen, str) or origen == "":
            raise NotificacionInvalidaError("el origen debe ser un texto no vacío")
        self._cola.encolar(Notificacion(tipo, origen))

    def leer_siguiente(self):
        """Devuelve la pendiente más antigua y la quita; None si no hay.

        Tiempo O(1), espacio O(1).
        """
        if self._cola.tamanio() == 0:
            return None
        return self._cola.desencolar()

    def pendientes(self):
        """Cantidad de notificaciones sin leer. Tiempo O(1), espacio O(1)."""
        return self._cola.tamanio()