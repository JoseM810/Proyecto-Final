"""Excepciones propias del proyecto."""


class PilaVaciaError(Exception):
    """Se intentó leer o quitar el tope de una pila sin elementos."""