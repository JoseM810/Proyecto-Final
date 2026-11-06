"""Pruebas de HiloComentarios, parte T-01. Criterios de specs/04-comentarios/spec.md."""
import pytest

from dominio.hilo_comentarios import HiloComentarios
from estructuras.errores import ComentarioInvalidoError


# --- comentar ---
def test_comentar_devuelve_un_id_entero_positivo():
    """Spec: comentar devuelve un identificador, un entero positivo."""
    hilo = HiloComentarios()
    id_comentario = hilo.comentar("Ana", "hola")
    assert isinstance(id_comentario, int)
    assert id_comentario > 0


def test_comentar_aumenta_cantidad():
    """INV-01: cada comentario nuevo sube cantidad() en uno."""
    hilo = HiloComentarios()
    hilo.comentar("Ana", "hola")
    hilo.comentar("Luis", "buenas")
    assert hilo.cantidad() == 2


def test_los_ids_son_unicos():
    """INV-02: no hay dos comentarios con el mismo identificador."""
    hilo = HiloComentarios()
    ids = [hilo.comentar("Ana", f"comentario {i}") for i in range(10)]
    assert len(set(ids)) == 10


def test_comentar_acepta_autor_y_texto_repetidos():
    """Caso extremo: el mismo autor y texto dos veces cuentan como dos comentarios."""
    hilo = HiloComentarios()
    primero = hilo.comentar("Ana", "hola")
    segundo = hilo.comentar("Ana", "hola")
    assert primero != segundo
    assert hilo.cantidad() == 2


# --- hilo vacío ---
def test_hilo_nuevo_esta_vacio():
    """CA-06 (parte T-01): un hilo sin comentarios tiene cantidad() 0."""
    assert HiloComentarios().cantidad() == 0


# --- validación ---
def test_comentario_invalido():
    """CA-05: autor o texto vacío o nulo lanza ComentarioInvalidoError y no cambia cantidad()."""
    hilo = HiloComentarios()
    hilo.comentar("Ana", "hola")
    casos = [("", "x"), ("Ana", ""), (None, "x"), ("Ana", None), (5, "x"), ("Ana", 7)]
    for autor, texto in casos:
        with pytest.raises(ComentarioInvalidoError):
            hilo.comentar(autor, texto)
    assert hilo.cantidad() == 1


def test_comentar_despues_de_un_error_sigue_funcionando():
    """CA-05: un intento inválido no deja el hilo en mal estado."""
    hilo = HiloComentarios()
    with pytest.raises(ComentarioInvalidoError):
        hilo.comentar("", "x")
    hilo.comentar("Ana", "hola")
    assert hilo.cantidad() == 1


# --- muchos ---
def test_muchos_comentarios_de_primer_nivel():
    """Caso extremo: 5 000 comentarios, todos con identificador distinto."""
    hilo = HiloComentarios()
    ids = [hilo.comentar("Ana", f"c{i}") for i in range(5_000)]
    assert hilo.cantidad() == 5_000
    assert len(set(ids)) == 5_000