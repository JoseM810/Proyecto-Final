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


# --- recorrer (T-03) ---
def _resumen(hilo):
    """Convierte el recorrido en pares (texto, profundidad) para compararlo."""
    return [(c.texto, c.profundidad) for c in hilo.recorrer()]


def test_hilo_en_preorden():
    """CA-02: con A, su respuesta B, la respuesta C a B y el comentario D, el orden es A(0), B(1), C(2), D(0)."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "A")
    b = hilo.responder(a, "Luis", "B")
    hilo.responder(b, "Sara", "C")
    hilo.comentar("Eva", "D")
    assert _resumen(hilo) == [("A", 0), ("B", 1), ("C", 2), ("D", 0)]


def test_respuesta_aparece_justo_despues_del_padre():
    """CA-01 (posición): una respuesta posterior aparece justo después de su padre, antes del siguiente comentario."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "A")
    hilo.comentar("Eva", "D")
    hilo.responder(a, "Luis", "B")
    assert _resumen(hilo) == [("A", 0), ("B", 1), ("D", 0)]


def test_respuestas_en_orden_de_llegada():
    """CA-04: las respuestas a un mismo comentario salen en el orden en que llegaron."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "A")
    for texto in ("R1", "R2", "R3"):
        hilo.responder(a, "Luis", texto)
    assert _resumen(hilo) == [("A", 0), ("R1", 1), ("R2", 1), ("R3", 1)]


def test_respuestas_en_orden_con_subhilos():
    """CA-04: el subhilo de una respuesta aparece antes que la respuesta siguiente del mismo padre."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "A")
    r1 = hilo.responder(a, "Luis", "R1")
    hilo.responder(a, "Sara", "R2")
    hilo.responder(r1, "Eva", "S1")
    assert _resumen(hilo) == [("A", 0), ("R1", 1), ("S1", 2), ("R2", 1)]


def test_hilo_vacio():
    """CA-06: un hilo sin comentarios tiene cantidad() 0 y recorrer() no devuelve nada ni lanza error."""
    hilo = HiloComentarios()
    assert hilo.cantidad() == 0
    assert _resumen(hilo) == []


def test_recorrer_un_solo_comentario():
    """Caso extremo: con un solo comentario, el recorrido lo devuelve a él solo."""
    hilo = HiloComentarios()
    hilo.comentar("Ana", "A")
    assert _resumen(hilo) == [("A", 0)]


def test_padre_siempre_antes_que_hijo():
    """INV-03: en recorrer(), todo comentario con padre aparece después de su padre."""
    hilo = HiloComentarios()
    padre_de = {}
    for i in range(30):
        raiz = hilo.comentar("Ana", f"raiz{i}")
        for j in range(3):
            hijo = hilo.responder(raiz, "Luis", f"hijo{i}-{j}")
            padre_de[hijo] = raiz
            for k in range(2):
                nieto = hilo.responder(hijo, "Sara", f"nieto{i}-{j}-{k}")
                padre_de[nieto] = hijo
    posicion = {}
    for lugar, comentario in enumerate(hilo.recorrer()):
        posicion[comentario.id] = lugar
    assert len(posicion) == hilo.cantidad()
    for hijo, padre in padre_de.items():
        assert posicion[padre] < posicion[hijo]


def test_recorrer_no_modifica_el_hilo():
    """Spec: recorrer no cambia el hilo; dos recorridos seguidos dan lo mismo."""
    hilo = HiloComentarios()
    a = hilo.comentar("Ana", "A")
    hilo.responder(a, "Luis", "B")
    primero = _resumen(hilo)
    segundo = _resumen(hilo)
    assert primero == segundo
    assert hilo.cantidad() == 2


def test_recorrer_cadena_muy_profunda_sin_recursion():
    """Caso extremo: 5 000 respuestas encadenadas se recorren sin desbordar la recursión."""
    hilo = HiloComentarios()
    ultimo = hilo.comentar("Ana", "raiz")
    for i in range(1, 5_000):
        ultimo = hilo.responder(ultimo, "Ana", f"nivel {i}")
    recorrido = list(hilo.recorrer())
    assert len(recorrido) == 5_000
    assert recorrido[-1].profundidad == 4_999