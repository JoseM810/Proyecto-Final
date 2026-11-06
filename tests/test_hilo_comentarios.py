"""Pruebas de HiloComentarios, parte T-01. Criterios de specs/04-comentarios/spec.md."""
import pytest

from dominio.hilo_comentarios import HiloComentarios
from estructuras.errores import ComentarioInvalidoError, ComentarioNoEncontradoError


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


# --- responder ---
def test_respuesta_tiene_profundidad_del_padre_mas_uno():
    """CA-01 (profundidad): una respuesta tiene la profundidad de su padre más uno."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    b = hilo.responder(a, "Luis", "buenas")
    assert hilo.obtener(a).profundidad == 0
    assert hilo.obtener(b).profundidad == 1


def test_responder_a_una_respuesta_aumenta_la_profundidad():
    """CA-01 (caso extremo): responder a una respuesta baja un nivel más."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    b = hilo.responder(a, "Luis", "buenas")
    c = hilo.responder(b, "Sara", "qué tal")
    assert hilo.obtener(c).profundidad == 2


def test_responder_aumenta_cantidad():
    """INV-01: cada respuesta sube cantidad() en uno."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    hilo.responder(a, "Luis", "buenas")
    hilo.responder(a, "Sara", "hey")
    assert hilo.cantidad() == 3


def test_responder_devuelve_un_id_unico():
    """INV-02: los ids de comentarios y respuestas no se repiten."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    b = hilo.responder(a, "Luis", "buenas")
    c = hilo.responder(b, "Sara", "hey")
    d = hilo.comentar("Eva", "otro")
    assert len({a, b, c, d}) == 4


def test_responder_inexistente():
    """CA-03: responder a un id inexistente lanza ComentarioNoEncontradoError y no cambia cantidad()."""
    hilo = HiloComentarios()
    hilo.comentar("Ana", "hola")
    for id_malo in (0, -1, 99, True, 1.5, "1", None):
        with pytest.raises(ComentarioNoEncontradoError):
            hilo.responder(id_malo, "Luis", "x")
    assert hilo.cantidad() == 1


def test_responder_invalido_se_revisa_antes_que_el_padre():
    """CA-05: si autor está vacío y el padre no existe, el error es ComentarioInvalidoError."""
    hilo = HiloComentarios()
    with pytest.raises(ComentarioInvalidoError):
        hilo.responder(99, "", "x")


def test_comentario_invalido_en_respuesta():
    """CA-05: responder con autor o texto inválido lanza ComentarioInvalidoError y no cambia cantidad()."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    casos = [("", "x"), ("Luis", ""), (None, "x"), ("Luis", None)]
    for autor, texto in casos:
        with pytest.raises(ComentarioInvalidoError):
            hilo.responder(a, autor, texto)
    assert hilo.cantidad() == 1


# --- obtener ---
def test_obtener_comentario():
    """CA-07: obtener devuelve autor y texto del comentario pedido."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    hilo.comentar("Luis", "buenas")
    assert hilo.obtener(a).autor == "Ana"
    assert hilo.obtener(a).texto == "hola"


def test_obtener_devuelve_la_respuesta_pedida():
    """CA-07: obtener de una respuesta devuelve sus datos, no los del padre."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    b = hilo.responder(a, "Luis", "buenas")
    assert hilo.obtener(b).autor == "Luis"
    assert hilo.obtener(b).texto == "buenas"


def test_obtener_id_inexistente():
    """CA-07: un id inexistente lanza ComentarioNoEncontradoError, también con el hilo vacío."""
    hilo = HiloComentarios()
    with pytest.raises(ComentarioNoEncontradoError):
        hilo.obtener(1)
    hilo.comentar("Ana", "hola")
    for id_malo in (0, -1, 99):
        with pytest.raises(ComentarioNoEncontradoError):
            hilo.obtener(id_malo)


def test_obtener_id_no_entero():
    """CA-07 (caso extremo): ids que no son enteros lanzan ComentarioNoEncontradoError."""
    hilo = HiloComentarios()
    hilo.comentar("Ana", "hola")
    for id_malo in (True, 1.5, "1", None):
        with pytest.raises(ComentarioNoEncontradoError):
            hilo.obtener(id_malo)


def test_obtener_no_modifica_el_hilo():
    """Spec: obtener no cambia la cantidad de comentarios."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "hola")
    hilo.obtener(a)
    hilo.obtener(a)
    assert hilo.cantidad() == 1


def test_cadena_profunda_de_respuestas():
    """CA-01 (caso extremo): 1 000 respuestas encadenadas llegan a profundidad 999."""
    hilo = HiloComentarios()
    ultimo = hilo.comentar("Ana", "raiz")
    for i in range(1, 1_000):
        ultimo = hilo.responder(ultimo, "Ana", f"nivel {i}")
    assert hilo.obtener(ultimo).profundidad == 999
    assert hilo.cantidad() == 1_000