"""Excepciones propias del proyecto."""


class PilaVaciaError(Exception):
    """Se intentó leer o quitar el tope de una pila sin elementos."""


class PantallaInvalidaError(Exception):
    """La pantalla a visitar es nula o vacía."""


class NadaAtrasError(Exception):
    """No existe una pantalla anterior a la actual."""


class ColaVaciaError(Exception):
    """Se intentó leer o quitar el frente de una cola sin elementos."""


class NotificacionInvalidaError(Exception):
    """El tipo o el origen de la notificación no son válidos."""


class PublicacionInvalidaError(Exception):
    """El texto o la fecha de la publicación no son válidos."""


class FinDelFeedError(Exception):
    """No hay una publicación más antigua que la actual."""


class InicioDelFeedError(Exception):
    """No hay una publicación más reciente que la actual."""


class ComentarioInvalidoError(Exception):
    """El autor o el texto del comentario no son válidos."""


class ComentarioNoEncontradoError(Exception):
    """No existe un comentario con el identificador indicado."""